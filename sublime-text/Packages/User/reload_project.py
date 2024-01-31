import sublime_plugin

class ReloadProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        project = self.window.project_data()
        project['folders'].append({"path": "noop"})
        self.window.set_project_data(project)
        project['folders'].pop()
        self.window.set_project_data(project)
