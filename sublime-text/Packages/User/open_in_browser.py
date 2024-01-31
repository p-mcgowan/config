import sublime_plugin
import re
import os
import subprocess
import sys

class OpenInBrowserCommand(sublime_plugin.TextCommand):
    proc = None
    stdout = ""
    stderr = ""
    urlRegex = re.compile(r'.*(https?://[^\]) ]+).*')
    projectRegex = re.compile(r'.*(AOSRE-\d+).*')

    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                selText = self.view.substr(region)
            else:
                selText = self.view.substr(self.view.expand_to_scope(region.a, self.view.scope_name(region.a)))
                if '\n' in selText or (not re.search(self.urlRegex, selText) and not re.search(self.projectRegex, selText)):
                    selText = self.view.substr(self.view.line(region.a))

            print(selText)

            match = re.search(self.urlRegex, selText)
            if not match:
                match = re.findall(self.projectRegex, selText)
                if not match:
                    return
                selText = ""
                for (ticket) in match:
                    selText = f"{selText} -w https://atc.bmwgroup.net/jira/browse/{ticket}"
            else:
                selText = f"-w {match.group(1)}"

            print(f"$HOME/bin/google {selText}")
            self.run_in_thread(f"$HOME/bin/google {selText}");

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
        if self.stderr:
            stderr = re.sub(r"^[^\n]+\n", '', self.stderr.decode('UTF-8'))

            if stderr:
                self.show(stderr)
                print("error:\n%s" % (stderr))

        return self.proc.returncode
