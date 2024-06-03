import sublime, sublime_plugin, json, re

class ReplaceInSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, replaceStr, withStr):
        for region in self.view.sel():
            if not region.empty():
                text = self.view.substr(region)
                self.view.replace(edit, region, text.replace(replaceStr, withStr))

class ReplaceInSelectionExecPromptCommand(sublime_plugin.TextCommand):
    def run(self, edit, command = "", args = []):
        self.view.window().show_input_panel('Run command:', command, self.on_done, None, None)
        # self.view.window().show_input_panel('Run command:', command, self.on_done, None, None)

    def on_done(self, text):
        self.view.window().run_command('replace_in_selection', { 'replaceStr': text, 'withStr': text })
