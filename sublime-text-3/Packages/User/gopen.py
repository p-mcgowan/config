import os
import sublime
import sublime_plugin
import subprocess

class gopenCommand(sublime_plugin.WindowCommand):

  def run(self, app="", args=[], type=None, cli=False, input=False):
    if self.window.active_view():
      fname = self.window.active_view().file_name()
      dirName = os.path.dirname(fname)
      syscmd = '/usr/bin/gnome-terminal --working-directory="' + dirName + '"; exec /bin/bash -il'
      p = subprocess.Popen(syscmd, shell=True, stdout=subprocess.PIPE)

      print(dirName)
      print(syscmd)
      print(p)

  def is_enabled(self):
    return True
