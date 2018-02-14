# Run with `view.run_command('example_plugin')` in the console, or put
# something like:
# { "caption": "Example Plugin", "command": "example_plugin" }
# in the command pallete.
#
import sublime, sublime_plugin
# class HcDefCommand(sublime_plugin.TextCommand):
class GotoHcdefCommand(sublime_plugin.WindowCommand):
    def run(self, edit):
        # open hc d ts
        window.open_file('/home/pat/source/rebuild/app/assets/definitions/hc.d.ts')
        for region in self.view.sel():
            if not region.empty():
                selText = self.view.substr(region)
                # search for interface (selection)
                view.find('interface ' + selText, 0)
