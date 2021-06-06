import sublime_plugin

class LspImportCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.view.run_command("move", { "by": "word_ends", "forward": "true" })
        self.view.run_command("auto_complete")
