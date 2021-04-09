import os
import sublime
import sublime_plugin
import subprocess
import re
import threading
import sys
from string import Template

class GotoBuildCommand(sublime_plugin.WindowCommand):
    def run(self):
        if self.window.active_view():
            fname = self.window.active_view().file_name()
            js_path = fname.replace('/src/', '/build/src/').replace('.ts', '.js')
            print(js_path)
            self.window.open_file(js_path)
