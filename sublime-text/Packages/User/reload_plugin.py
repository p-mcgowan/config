import sublime_plugin

class ReloadPluginCommand(sublime_plugin.WindowCommand):
    def run(self, name):
        sublime_plugin.reload_plugin(name)
