import sublime_plugin

class LspImportCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                self.view.run_command("expand_selection", {"to": "smart"})
                break
        self.view.run_command("auto_complete")
