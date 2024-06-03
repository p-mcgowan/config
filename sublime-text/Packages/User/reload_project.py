import sublime_plugin
import re
# import inspect
# print(inspect.getmembers(self.window))

class ReloadProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        print(self.window.project_file_name())

        project = self.window.project_data()
        project['folders'].append({"path": "noop"})
        self.window.set_project_data(project)
        project['folders'].pop()
        self.window.set_project_data(project)

        with open(self.window.project_file_name(), 'r') as project_file:
            contents = project_file.read()
            print(contents)
            updated = re.sub(r'\n\/\*\{\n\W+"path": "noop"\n\W+\},\*\/', '', contents)

        with open(self.window.project_file_name(), 'w') as project_file:
            project_file.write(updated)
