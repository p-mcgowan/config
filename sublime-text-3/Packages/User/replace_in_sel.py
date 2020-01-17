import sublime, sublime_plugin, json, re

class ReplaceInSelCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                in_selection=True
            else:
                in_selection=False
            self.view.window().run_command("show_panel", { "panel": "replace", "in_selection": in_selection })
