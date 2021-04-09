import sublime
import sublime_plugin
import re

class FindReplaceCommand(sublime_plugin.TextCommand):
    """The implementation of 'find_replace' text command.

    Example:

        view.run_command(
            "find_replace", {
                "pattern": "the",
                "replace_by": "THE",
                "start_pt": 100,
                "flags": ["LITERAL"]
            }
        )
    """

    FLAGS = {
        "LITERAL": sublime.LITERAL,
        "IGNORECASE": sublime.IGNORECASE
    }

    def run(self, edit, pattern, replace_by, start_pt=0, flags=["LITERAL"]):
        print(pattern)
        print('replace_by')
        print(replace_by)
        replace_by = r'{}'.format(replace_by)
        print(replace_by)
        # re.compile(replace_by.encode('unicode-escape'))

        # print('replace_by.replace("$", r\'\\\')')
        # print(replace_by.replace("$", r'\\'))
        # print(re.compile(replace_by.replace("$", r'\\')))
        """Find and replace all patterns.

        Arguments:
            edit (sublime.Edit):
                The edit token used to undo this command.
            pattern (string):
                The regex pattern to use for finding.
            replace_by (string):
                The text to replace all found words by.
            start_pt (int):
                The text position where to start.
            flags (list):
                The flags to pass to view.find()
                ["LITERAL", "IGNORECASE"]
        """
        while True:
            found = self.view.find(pattern, self._flags(flags), start_pt)
            if not found:
                return
            self.view.replace(edit, found, replace_by)
            start_pt = found.begin()

    def _flags(self, flags):
        """Translate list of flags."""
        result = 0
        for flag in flags:
            result |= self.FLAGS.get(flag, 0)
        return result
