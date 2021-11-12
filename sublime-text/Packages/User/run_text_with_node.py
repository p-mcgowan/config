import sublime
import sublime_plugin
import re
import os
import subprocess
import sys

class RunTextWithNodeCommand(sublime_plugin.WindowCommand):
    proc = None
    stdout = ""
    stderr = ""

    def run(self):
        view = self.window.active_view()
        for region in view.sel():
            if not region.empty():
                selText = view.substr(region)
                repl = re.sub(r"'", "'\"'", selText)
                self.run_in_thread(f"node -p '{repl}'")

    def run_in_thread(self, command):
        env = os.environ.copy()
        self.stdout = ""
        self.stderr = ""

        if self.proc is not None:
            self.proc.terminate()
            self.proc = None

        if sys.platform == "win32":
            SW_HIDE = 0
            info = subprocess.STARTUPINFO()
            info.dwFlags = subprocess.STARTF_USESHOWWINDOW
            info.wShowWindow = SW_HIDE

            if "start" not in command:
                command = "start \"\" " + command

            # self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=True)
            self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=True, startupinfo=info)

        else:
            env["GNOME_TERMINAL_SCREEN"] = ""
            self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=env, shell=True)

        self.stdout, self.stderr = self.proc.communicate()

        if self.proc.returncode != 0:
            print("Open failed ({})".format(self.proc.returncode))

        if self.stdout:
            stdout = self.stdout.decode('UTF-8')
            print(stdout)
            self.show(stdout)
        if self.stderr:
            stderr = re.sub(r"^[^\n]+\n", '', self.stderr.decode('UTF-8'))

            if stderr:
                self.show(stderr)
                print("error:\n%s" % (stderr))

        return self.proc.returncode

    def show(self, content):
        content = re.sub('\n', '<br>', content)

        errorTemplate = """
            <body id=show-scope>
                <style>
                    p {
                        white-space: pre-wrap;
                        margin-top: 0;
                    }
                    a {
                        font-family: system;
                        font-size: 1.05rem;
                    }
                </style>
                <p>%s</p>
            </body>
        """ % (content)

        self.window.active_view().show_popup(errorTemplate, max_width=1200)

        # msg, line, col = re.search(r': (.*) \((\d+):(\d+)\)', content).group(1, 2, 3)
        # point = self.window.active_view().text_point(int(line), int(col))
        # self.window.active_view().show_popup(errorTemplate, max_width=1200, location=point)
