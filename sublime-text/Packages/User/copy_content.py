import sublime_plugin
import sublime
import os

class CopyContentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                # read file
                # copy to clipboard
                filename = self.view.substr(region)
                if (filename[0] == '"' and filename[len(filename) - 1] == '"') or (filename[0] == "'" and filename[len(filename) - 1] == "'"):
                    filename = filename[1:-1]

                if filename[0] != '/':
                    filename = os.path.join(os.path.dirname(self.view.file_name()), filename)

                print(filename)
                with open(filename) as fp:
                    # print(fp.read())
                    sublime.set_clipboard(fp.read())
                return
