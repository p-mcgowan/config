import os
import sublime_plugin
import subprocess
import re
import sys

class PrettierCommand(sublime_plugin.WindowCommand):
    def run(self, args=[], type=None, cli=False, input=False):
        if self.window.active_view():
            view = self.window.active_view()
            fname = view.file_name()
            scope = view.scope_name(view.sel()[-1].b)

            command = "npx prettier --config ~/.prettierrc --write %s" % (fname)

            if re.search(r".*\.html\b", scope):
                command = "npx prettier --config ~/.ngprettierrc --parser angular --write %s" % (fname)

            env = os.environ.copy()
            self.stdout = ""
            self.stderr = ""

            if sys.platform == "win32":
                if "start" not in command:
                    command = "start \"\" " + command

                p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=True)

                if p.stdout:
                    p.stdout.close()

                if p.stderr:
                    p.stderr.close()

            else:
                env["GNOME_TERMINAL_SCREEN"] = ""
                p = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=env, shell=True)
                self.stdout, self.stderr = p.communicate()

            exitCode = p.wait()

            if self.stderr:
                stderr = re.sub(r"^[^\n]+\n", '', self.stderr.decode('UTF-8'))

                if stderr:
                    self.show(stderr)
                    print("error:\n%s" % (stderr))

            if self.stdout:
                stdout = self.stdout.decode('UTF-8')
                print(stdout)

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

    def is_enabled(self):
        return True
