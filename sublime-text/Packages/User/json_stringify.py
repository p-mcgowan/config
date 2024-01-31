import sublime_plugin
import json
import re
import os


class JsonStringifyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                selText = self.view.substr(region)
                trimmed = re.sub(r"\s+", "", selText)
                replacement = json.dumps(trimmed, separators=(",", ":"))
                self.view.replace(edit, region, replacement)


class JsonUnstringifyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                selText = self.view.substr(region)
                replacement = json.loads(selText)
                self.view.replace(edit, region, replacement)


class JsonStringifyFromJsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                selText = self.view.substr(region)
                cmd = f'node -p "JSON.stringify({selText})"'
                response = os.popen(cmd).read()
                self.view.replace(edit, region, response)
