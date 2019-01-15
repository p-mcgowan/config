import sublime
import sublime_plugin

# Keybinds
# { "keys": ["ctrl+alt+shift+r"], "command": "close_to_right" }
# { "keys": ["ctrl+alt+shift+o"], "command": "close_others" }
# Pallete:
# { "command": "close_to_right", "caption": "Close Tabs to the Right" },
# { "command": "close_others", "caption": "Close Other Tabs" }


class CloseOthersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window = self.view.window()
        group_index, view_index = window.get_view_index(self.view)
        window.run_command("close_others_by_index", { "group": group_index, "index": view_index})

class CloseToRightCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window = self.view.window()
        group_index, view_index = window.get_view_index(self.view)
        window.run_command("close_to_right_by_index", { "group": group_index, "index": view_index})
