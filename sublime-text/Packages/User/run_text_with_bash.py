import sublime
import sublime_plugin
import re
import os
import subprocess
import sys

class RunTextWithBashCommand(sublime_plugin.TextCommand):
    proc = None
    stdout = ""
    stderr = ""

    def run(self, edit):
        ran = False
        for region in self.view.sel():
            if not region.empty():
                selText = self.view.substr(region)
                with open('/tmp/sub.sh', 'w') as f:
                    f.write("shopt -s expand_aliases\nsource ~/.bash_aliases\n")
                    f.write(selText)
                    f.close()

                ran = True
                self.run_in_thread(f"bash /tmp/sub.sh", region, edit)

        if ran == False:
            self.run_in_thread("bash %s" % (self.view.file_name()))


    def run_in_thread(self, command, region = None, edit = None):
        fname = self.view.file_name() or os.getcwd()
        dirName = os.path.dirname(fname)

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
            self.proc = subprocess.Popen(command, cwd=dirName, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=True, startupinfo=info)

        else:
            env["GNOME_TERMINAL_SCREEN"] = ""
            self.proc = subprocess.Popen(command, cwd=dirName, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=env, shell=True, executable="/bin/bash")

        self.stdout, self.stderr = self.proc.communicate()

        if self.proc.returncode != 0:
            print("Open failed ({})".format(self.proc.returncode))
            print("stdout {}\n\nstderr {}".format(self.stdout, self.stderr))

        if self.stdout:
            stdout = self.stdout.decode('UTF-8')
            print(stdout)
            if region is not None:
                self.view.replace(edit, region, stdout[:-1] if stdout[-1] == '\n' else stdout)
            else:
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

        self.view.show_popup(errorTemplate, max_width=1200)

        # msg, line, col = re.search(r': (.*) \((\d+):(\d+)\)', content).group(1, 2, 3)
        # point = self.window.active_view().text_point(int(line), int(col))
        # self.window.active_view().show_popup(errorTemplate, max_width=1200, location=point)
