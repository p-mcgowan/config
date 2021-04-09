import sublime, sublime_plugin
import re

class WrapAtCommand(sublime_plugin.TextCommand):
    def run(self, edit, count):
        count = int(count or '80')
        for region in self.view.sel():
            if not region.empty():
                selected = self.view.substr(region)
                replacements = list(map(lambda s: re.sub(r"([^\r\n]{0,%s}(?=\s|$))\ ?" % count, r"\1\n", s), selected.splitlines()))
                self.view.replace(edit, region, ''.join(replacements))

class WrapAtExecPromptCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().show_input_panel('Wrap text at [80]:', '', self.on_done, None, None)

    def on_done(self, count):
        self.view.window().run_command('wrap_at', { 'count': count })
