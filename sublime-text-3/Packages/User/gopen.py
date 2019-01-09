import os
import sublime
import sublime_plugin
import subprocess

class gopenCommand(sublime_plugin.WindowCommand):

  def run(self, app="", args=[], type=None, cli=False, input=False):
    if self.window.active_view():
      fname = self.window.active_view().file_name()
      dirName = os.path.dirname(fname)
      syscmd = 'gnome-terminal --working-directory="' + dirName + '"'
      p = subprocess.Popen(syscmd, shell=True)

      print(dirName)
      print(syscmd)
      print(p)

  def is_enabled(self):
    return True
