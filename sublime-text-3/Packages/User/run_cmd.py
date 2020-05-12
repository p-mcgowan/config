import os
import sublime
import sublime_plugin
import subprocess
import re
from string import Template

errorTemplate = Template("""
<body id="my-plugin-feature">
    <style>
        display: block;
        div.error {
            margin: 5px;
        }
    </style>
    <div class="error">${error}</div>
</body>
""")
# <style>body { height: 100%; width: 100%; } div { margin: 5px; white-space: nowrap; }</style>
# <div>${error}</div>

class RunOnCommand(sublime_plugin.WindowCommand):
    """Exec command here with DIRNAME and FILENAME subs."""

    def run(self, command, app="", args=[], type=None, cli=False, input=False):
        if self.window.active_view():
            fname = self.window.active_view().file_name()

            dirName = os.path.dirname(fname)

            command = re.sub('DIRNAME', dirName, command)
            command = re.sub('FILENAME', fname, command)

            # running gnome-terminal fails sometimes
            env = os.environ.copy()
            env["GNOME_TERMINAL_SCREEN"] = ""
            p = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=env, shell=True)

            print(command)

            stdout = p.stdout.read()
            stderr = p.stderr.read()

            if stderr:
                content = ''.join(map(lambda x: '<div><code>' + re.sub(' ', '&nbsp;', x) + '</code></div>', stderr.decode('UTF-8').split('\n')))
                print(content)
                content = errorTemplate.substitute({ "error": content })
                max_width = min(self.window.active_view().viewport_extent()[0], 800)
                # self.window.active_view().show_popup(content, max_width=self.window.active_view().viewport_extent()[0], max_height=400)
                self.window.active_view().show_popup(content, max_width=max_width, max_height=400)
                print(stderr.decode('UTF-8'))
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
            command = re.sub('DIRNAME', dirName, command)
            command = re.sub('FILENAME', fname, command)
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
