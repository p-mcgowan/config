""" Run an external command on the current file.
Usage: run command `external_command` and giving it the executable name as the
`executable` argument. The external command with be invoked with the current
file path and name, as its first and single argument.
"""
import sublime_plugin
class ExternalCommandCommand(sublime_plugin.WindowCommand):
    def run(self, executable):
        variables = self.window.extract_variables()
        # {
        #     'file_path'      : '/home/pat/tmp',
        #     'file'           : '/home/pat/tmp/test.tex',
        #     'file_base_name' : 'test',
        #     'platform'       : 'Linux',
        #     'file_name'      : 'test.tex',
        #     'folder'         : '/home/pat/git/os161',
        #     'file_extension' : 'tex',
        #     'packages'       : '/home/pat/.config/sublime-text-3/Packages'
        # }

        if "file" in variables:
            file = variables["file"]
            print(executable)
            self.window.run_command("exec", {"cmd": [executable, file]})
        else:
            sublime.status_message("Error: no file")

def description(self):
    return (
        "Run an external command with the current file path and name as "
        "a single argument.")

def description(self):
    return (
        "Run an external command "
        "with the current file path "
        "and name as a single argument.")
