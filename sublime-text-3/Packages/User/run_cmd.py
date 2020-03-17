import os
import sublime
import sublime_plugin
import subprocess
import re

class RunOnCommand(sublime_plugin.WindowCommand):
    """Exec command here with DIRNAME and FILENAME subs."""

    def run(self, command, app="", args=[], type=None, cli=False, input=False):
        if self.window.active_view():
            fname = self.window.active_view().file_name()

            dirName = os.path.dirname(fname)

            command = re.sub('DIRNAME', dirName, command)
            command = re.sub('FILENAME', fname, command)

            env = os.environ.copy()
            p = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=env, shell=True)

            print(command)

            stdout = p.stdout.read()
            stderr = p.stdout.read()

            if stderr:
                print(stderr)
            if stdout:
                print(stdout)

    def is_enabled(self):
        return True

class RunCmdCommand(sublime_plugin.WindowCommand):
    """Exec command here."""

    def run(self, command, app="", args=[], type=None, cli=False, input=False):
        if self.window.active_view():
            fname = self.window.active_view().file_name()
            dirName = os.path.dirname(fname)
            syscmd = 'cd ' + dirName + ' && ' + command
            env = os.environ.copy()
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

class RunCommandExecPromptCommand(sublime_plugin.TextCommand):
    """Prompt for command."""

    def run(self, edit):
        self.view.window().show_input_panel('Run command:', '', self.on_done, None, None)

    def on_done(self, text):
        self.view.window().run_command('run_cmd', { 'command': text })
