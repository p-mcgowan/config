# Run with `view.run_command('example_plugin')` in the console, or put
# something like:
# { "caption": "Example Plugin", "command": "example_plugin" }
# in the command pallete.
#
import sublime, sublime_plugin

def copy(view, text):
    sublime.set_clipboard(text)
    view.hide_popup()
    sublime.status_message('Scope name copied to clipboard')

class ExamplePluginCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        scope = self.view.scope_name(self.view.sel()[-1].b)

        html = """
<style>
body { margin: 0 8; }
</style>
<p>%s</p><p><a href="%s">Copy</a></p>
""" % (scope.replace(' ', '<br>'), scope.rstrip())

        self.view.show_popup(html, on_navigate=lambda x: copy(self.view, x))
