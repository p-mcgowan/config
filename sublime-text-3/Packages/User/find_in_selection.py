import sublime_plugin, json, re

class FindInSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        in_selection = False

        for region in self.view.sel():
            if not region.empty():
                in_selection = True

        window = self.view.window()
        window.run_command("show_panel", { "panel": "find", "reverse": False, "in_selection": in_selection })

