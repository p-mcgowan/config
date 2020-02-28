import os
import sublime
import sublime_plugin
import subprocess

class gopenCommand(sublime_plugin.WindowCommand):

    def run(self, app="", args=[], type=None, cli=False, input=False):
        if self.window.active_view():
            fname = self.window.active_view().file_name()
            dirName = os.path.dirname(fname)
            syscmd = '/usr/bin/gnome-terminal --working-directory="' + dirName + '" "/bin/bash -il"'
            env = os.environ.copy()
            env["GNOME_TERMINAL_SCREEN"] = ""
            p = subprocess.Popen(syscmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=env, shell=True)

            print(syscmd)
            stdout = p.stdout.read()
            stderr = p.stdout.read()

            if stderr:
                print(stderr)
            if stdout:
                print(stdout)

    def is_enabled(self):
        return True
