import sublime
import sublime_plugin
import subprocess

class GnomeTerminalHereCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        subprocess.call(["/usr/bin/gnome-terminal", "."])
