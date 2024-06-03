import sublime_plugin
import re
import sublime

class ArraySortCommand(sublime_plugin.TextCommand):
    splitRe = re.compile(r',[ \s\n\r]+')

    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                return
            parts = list(set(list(filter(lambda x: len(x.strip()) > 0, self.splitRe.split(self.view.substr(region).replace('\n+', ''))))))
            parts.sort()
            sortedText = ', '.join(parts)
            self.view.replace(edit, region, sortedText)
