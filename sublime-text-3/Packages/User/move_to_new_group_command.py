import sublime, sublime_plugin

# https://forum.sublimetext.com/t/set-layout-reference/5713
class MoveToNewGroupCommand(sublime_plugin.WindowCommand):
    def run(self, group = 1):
        print("group {}".format(group))
        if (len(self.window.get_layout()["cells"]) <= group):
            self.window.set_layout({"cells": [[0, 0, 1, 1], [1, 0, 2, 1]], "cols": [0.0, 0.5, 1.0], "rows": [0.0, 1.0]})
        self.window.run_command("move_to_group", {"group": group, "focus": True})
        self.window.focus_group(group)
