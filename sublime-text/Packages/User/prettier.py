import os
import sublime
import sublime_plugin
import subprocess
import threading
import re
import sys
import traceback

class FormatCommand(sublime_plugin.WindowCommand):
    proc = None
    stdout = ""
    stderr = ""

    def run(self, args=[], type=None, cli=False, input=False):
        try:
            self.run_thread()

        except:
            print(traceback.format_exc())

    def run_thread(self):
        if not self.window.active_view():
            return

        command, cwd = self.get_command()

        # view = self.window.active_view()
        # fname = view.file_name()
        # scope = view.scope_name(view.sel()[-1].b)

        # #
        # config = self.find_config(fname)
        # print("found config?: %s" % (config))
        # command = "npx prettier %s --write %s" % (config, fname)

        # if re.search(r".*\.html\b", scope):
        #     command = "npx prettier %s --parser angular --write %s" % (config, fname)
        # #

        print("command")
        print(command)
        print("cwd")
        print(cwd)

        thread = threading.Thread(target=self.run_build_in_thread, args=(command,cwd,))
        thread.start()

        return thread;


        sublime.run_command('revert')

        return self.proc.returncode

    def run_build_in_thread(self, command, cwd):
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
            self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, cwd=cwd, shell=True, startupinfo=info)

        else:
            env["GNOME_TERMINAL_SCREEN"] = ""
            print(command)
            print(cwd)
            self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, env=env, cwd=cwd, shell=True)

        self.stdout, self.stderr = self.proc.communicate()

        print("done")
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

    def is_enabled(self):
        return True

class PrettierCommand(FormatCommand):
    config_files = ['.prettierrc', '.prettierrc.js', '.prettierrc.json']

    def get_command(self):
        view = self.window.active_view()
        fname = view.file_name()
        scope = view.scope_name(view.sel()[-1].b)
        config = self.find_config(fname)
        print("found config?: %s" % (config))
        command = "npx prettier %s --write %s" % (config, fname)

        if re.search(r".*\.html\b", scope):
            command = "npx prettier %s --parser angular --write %s" % (config, fname)

        return (command, None)

    def check_folder(self, folder):
        for filename in self.config_files:
            fullpath = os.path.join(folder, filename)
            if os.path.exists(fullpath):
                return "--config %s" % (fullpath)

    def find_config(self, fname):
        next_dir = os.path.dirname(fname)

        count = 20
        while next_dir != '/' and count > 0:
            exists = self.check_folder(next_dir)
            if exists:
                return exists
            next_dir = os.path.dirname(next_dir)
            count = count - 1

        env = os.environ.copy()
        exists = self.check_folder(os.path.join(env["HOME"], 'tmp'))
        if exists:
            return exists

        return ''

class LintCommand(FormatCommand):
    config_files = ['.eslintrc.js', '.eslintrc.json', 'eslint.config.js', 'eslint.config.mjs', 'eslint.config.cjs']

    def get_command(self):
        view = self.window.active_view()
        fname = view.file_name()
        scope = view.scope_name(view.sel()[-1].b)
        config = self.find_config(fname)
        print("found config?: %s" % (config))
        if config is not None:
            command = "npx eslint --config %s --fix %s" % (config, fname)
        else:
            self.show('cannot find eslint config')
            raise Exception('no config')

        return (command, os.path.dirname(config))

    def check_folder(self, folder):
        for filename in self.config_files:
            fullpath = os.path.join(folder, filename)
            if os.path.exists(fullpath):
                return fullpath

    def find_config(self, fname):
        next_dir = os.path.dirname(fname)

        count = 20
        while next_dir != '/' and count > 0:
            exists = self.check_folder(next_dir)
            if exists:
                return exists
            next_dir = os.path.dirname(next_dir)
            count = count - 1

        env = os.environ.copy()
        exists = self.check_folder(env["HOME"])
        if exists:
            return exists

        return None
