import os
import sublime_plugin
import subprocess
import threading
import re
import sys
import traceback

class PrettierCommand(sublime_plugin.WindowCommand):
    proc = None
    stdout = ""
    stderr = ""

    def run(self, args=[], type=None, cli=False, input=False):
        try:
            self.build()

        except:
            print(traceback.format_exc())

    def build(self):
        if self.window.active_view():
            view = self.window.active_view()
            fname = view.file_name()
            scope = view.scope_name(view.sel()[-1].b)

            config = self.find_config(fname)
            print("found config: %s" % (config))
            command = "npx prettier --config %s --write %s" % (config, fname)

            if re.search(r".*\.html\b", scope):
                command = "npx prettier --config ~/.ngprettierrc --parser angular --write %s" % (fname)

            thread = self.run_thread(command)


    def find_config(self, fname):
        next_dir = os.path.dirname(fname)

        count = 20
        while next_dir != '/' and count > 0:
            if os.path.exists(os.path.join(next_dir, '.prettierrc')):
                return os.path.join(next_dir, '.prettierrc')
            elif os.path.exists(os.path.join(next_dir, '.prettierrc.js')):
                return os.path.exists(os.path.join(next_dir, '.prettierrc.js'))
            elif os.path.exists(os.path.join(next_dir, '.prettierrc.json')):
                return os.path.exists(os.path.join(next_dir, '.prettierrc.json'))
            next_dir = os.path.dirname(next_dir)
            count = count - 1

        return '~/.prettierrc'

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

    def run_thread(self, command):
        thread = threading.Thread(target=self.run_build_in_thread, args=(command,))
        thread.start()

        return thread;

    def run_build_in_thread(self, command):
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
            print("Build failed ({})".format(self.proc.returncode))

        if self.stdout:
            stdout = self.stdout.decode('UTF-8')
            print(stdout)
        if self.stderr:
            stderr = re.sub(r"^[^\n]+\n", '', self.stderr.decode('UTF-8'))

            if stderr:
                self.show(stderr)
                print("error:\n%s" % (stderr))


        return self.proc.returncode
