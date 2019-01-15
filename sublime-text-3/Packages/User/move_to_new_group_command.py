import sublime, sublime_plugin

class MoveToNewGroupCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command("set_layout", {"cells": [[0, 0, 1, 1], [1, 0, 2, 1]], "cols": [0.0, 0.5, 1.0], "rows": [0.0, 1.0]})
        self.window.run_command("focus_group", {"group": 0})
        self.window.run_command("move_to_group", {"group": 1})
