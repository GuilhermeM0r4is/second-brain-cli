from prompt_toolkit.completion import Completer, Completion

from ui.helper import COMMAND_TREE


class TreeCompleter(Completer):
    ''' walks COMMAND_TREE to any depth, offering next-word completions
        or a usage hint once a leaf command is reached '''

    def get_completions(self, document, complete_event):

        text = document.text_before_cursor
        if not text.startswith("/"): return

        command_text = text[1:]

        # a trailing space means the last word was already finished;
        ends_with_space = command_text == "" or command_text.endswith(" ")
        parts = command_text.split()

        matched_parts = parts if ends_with_space else parts[:-1]
        partial = "" if ends_with_space else parts[-1]

        node = self._walk(matched_parts)
        if node is None: return   # typed a word that doesn't exist anywhere in the tree

        subcommands = node.get("subcommands", {})

        if subcommands: yield from self._complete_next_word(subcommands, partial)
        else: yield from self._complete_usage_hint(node, matched_parts)


    def _walk(self, parts: list[str]) -> dict | None:
        ''' follows a list of already-typed words down COMMAND_TREE,
            returning the node reached or None if the path doesn't exist '''

        node = {"subcommands": COMMAND_TREE}

        for part in parts:
            subcommands = node.get("subcommands", {})

            if part not in subcommands: return None
            node = subcommands[part]

        return node


    def _complete_next_word(self, subcommands: dict, partial: str):
        ''' yields every subcommand name that starts with what's being typed '''

        for name, data in subcommands.items():
            if name.startswith(partial):

                yield Completion(name, start_position = -len(partial),
                                display = name, display_meta = data.get("description", ""))


    def _complete_usage_hint(self, node: dict, matched_parts: list[str]):
        ''' reached a leaf command — show its usage as a hint instead of
            a real insertable completion, since there's nothing left to type '''

        usage = node.get("usage", "")
        if not usage: return

        path = " ".join(matched_parts)
        yield Completion("", start_position = 0, display = f"Usage: /{path} {usage}",
                         display_meta = node.get("description", ""))