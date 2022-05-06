import sublime
import sublime_plugin
import re
from time import strftime

isMeetingRe = re.compile(r'meeting|chat|daily|refinement|demo|monthly|planning|retro|talk|4-eyes')

class ToLogTimeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                selText = self.view.substr(region)

                (msg, hours) = list(map(lambda s: s.strip(), selText.split('|')))
                logType = 'dev'
                if (isMeetingRe.search(msg)):
                    logType = 'meeting'

                replacement = f"""'{strftime("%d.%m.%Y")}|project|billing|{msg}|{hours}|{logType}',"""
                self.view.replace(edit, region, replacement)
