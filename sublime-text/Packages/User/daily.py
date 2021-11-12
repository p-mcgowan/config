"""
<snippet>
    <content>
<![CDATA[
${1:2021-10-28}
================================================================================
YID
  - $0
TIW
  - 
IABB
  - 


]]>
    </content>
    <!-- Optional: Set a tabTrigger to define how to trigger the snippet -->
    <tabTrigger>daily</tabTrigger>
    <!-- Optional: Set a scope to limit where the snippet will trigger -->
    <!-- <scope>source.ts, source.js, source.tsx</scope> -->
</snippet>
"""


import sublime
import sublime_plugin
from time import strftime

# Keybinds
# { "keys": ["ctrl+alt+shift+r"], "command": "close_to_right" }
# { "keys": ["ctrl+alt+shift+o"], "command": "close_others" }
# Pallete:
# { "command": "close_to_right", "caption": "Close Tabs to the Right" },
# { "command": "close_others", "caption": "Close Other Tabs" }


class DailyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():

            template = f"""
{strftime("%Y-%m-%d")}
================================================================================
YID
  -
TIW
  -
IABB
  -
"""
            self.view.replace(edit, region, template)
