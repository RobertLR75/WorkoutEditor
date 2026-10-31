import json
import shlex
import sys


def dangerous_git(arguments):
    # Git's global options precede the subcommand; these consume a separate value.
    value_options = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--config-env"}
    index = 0
    while index < len(arguments) and arguments[index].startswith("-"):
        index += 2 if arguments[index] in value_options else 1
    if index >= len(arguments):
        return False

    subcommand, *arguments = arguments[index:]
    if subcommand == "push":
        return True
    if subcommand in {"checkout", "restore"}:
        return "." in arguments

    if subcommand == "clean":
        options = iter(arguments)
        for option in options:
            if option == "--":
                break
            if option == "--force":
                return True
            if option == "--exclude":
                next(options, None)
            elif option.startswith("-") and not option.startswith("--"):
                flags, exclude, pattern = option[1:].partition("e")
                if "f" in flags:
                    return True
                if exclude and not pattern:
                    next(options, None)
        return False

    # A path after -- is not an option, even when its name starts with a dash.
    options = arguments[:arguments.index("--")] if "--" in arguments else arguments
    if subcommand == "reset":
        return "--hard" in options
    short_flags = {
        flag
        for option in options
        if option.startswith("-") and not option.startswith("--")
        for flag in option[1:]
    }
    if subcommand == "branch":
        delete = "d" in short_flags or "--delete" in options
        force = "f" in short_flags or "--force" in options
        return "D" in short_flags or (delete and force)
    return False


def normalize_substitutions(command, start=0, closing=None):
    # Inspect substitution bodies, then replace their complete source spans before
    # tokenization. This preserves quotes and adjoining path prefixes/suffixes.
    parts = []
    quote = None
    word_start = True
    depth = 0
    index = start
    while index < len(command):
        char = command[index]
        if char == "\\" and quote != "'":
            escaped = command[index:index + 2]
            if closing == "`" and escaped == "\\`":
                raise ValueError("unsupported escaped backtick substitution")
            if escaped != "\\\n":
                parts.append(escaped)
                word_start = False
            index += 2
            continue
        if quote == "'":
            if char == "'":
                quote = None
        elif char == '"':
            quote = None if quote == '"' else '"'
        elif char == "'" and quote is None:
            quote = "'"
        elif char == "`" and closing == "`":
            return "".join(parts), index + 1
        elif command.startswith("$(", index) or char == "`":
            end = ")" if char == "$" else "`"
            body, index = normalize_substitutions(command, index + (2 if char == "$" else 1), end)
            if dangerous_command(body):
                raise ValueError("dangerous command substitution")
            parts.append("__command_substitution__")
            word_start = False
            continue
        elif quote is None:
            if char == "#" and word_start:
                newline = command.find("\n", index)
                index = newline if newline >= 0 else len(command)
                continue
            if closing == ")":
                if char == "(":
                    depth += 1
                elif char == ")":
                    if depth == 0:
                        return "".join(parts), index + 1
                    depth -= 1
        parts.append(char)
        word_start = quote is None and char in " \t\r\n;&|()"
        index += 1
    if closing is not None:
        raise ValueError("unterminated command substitution")
    return "".join(parts), index


def dangerous_command(command):
    command, _ = normalize_substitutions(command)
    separators = ";&|()\n"
    lexer = shlex.shlex(command, posix=True, punctuation_chars=separators)
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    commands = [[]]
    for token in lexer:
        if token and all(character in separators for character in token):
            commands.append([])
        else:
            commands[-1].append(token)
    for words in commands:
        for index, word in enumerate(words):
            program = word.rsplit("/", 1)[-1]
            arguments = words[index + 1:]
            if program == "git" and dangerous_git(arguments):
                return True
            if program in {"sh", "bash", "zsh"}:
                for option_index, option in enumerate(arguments[:-1]):
                    if option.startswith("-") and not option.startswith("--") and "c" in option:
                        if dangerous_command(arguments[option_index + 1]):
                            return True
                        break
    return False


def main():
    try:
        command = json.load(sys.stdin)["tool_input"]["command"]
        if not isinstance(command, str) or not command.strip() or "\0" in command:
            raise ValueError("expected a nonempty command string")
        return 2 if dangerous_command(command) else 0
    except (ValueError, KeyError, TypeError):
        print("BLOCKED: Git guardrails could not accept the command input.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
