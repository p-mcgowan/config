import sublime_plugin, json, re

class JsonStringifyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                selText = self.view.substr(region)
                trimmed = re.sub(r'\s+', "", selText)
                replacement = json.dumps(trimmed, separators=(',', ':'))
                self.view.replace(edit, region, replacement)

class JsonUnstringifyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                selText = self.view.substr(region)
                replacement = json.loads(selText)
                self.view.replace(edit, region, replacement)
