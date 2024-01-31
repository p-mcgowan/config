import sublime
import sublime_plugin
import re
import os

# sublime.log_commands(True)
# set syntax - copy paste

syntax_tests = [
    [re.compile(r"^[dD]ockerfile.*"), "Packages/Dockerfile Syntax Highlighting/Syntaxes/Dockerfile.sublime-syntax"],
    [re.compile(r"^.*\.scss$"), "Packages/Sass/Syntaxes/SCSS.sublime-syntax"],
    [re.compile(r"^\.env.*"), "Packages/ShellScript/Bash.sublime-syntax"]
]


class SyntaxByFileNameCommand(sublime_plugin.EventListener):
    def on_load(self, view):
        self.detect_syntax(view)

    def detect_syntax(self, view):
        if view.is_scratch() or not view.file_name():
            return
        filename = os.path.basename(view.file_name())

        for syntax_test, syntax in syntax_tests:
            if syntax_test.match(filename):
                return view.assign_syntax(syntax)
