import os
import sublime
import sublime_plugin
import subprocess

f = open("/home/pat/tmp/gopen.py.log", "w+")

class gopenCommand(sublime_plugin.WindowCommand):

  def run(self, app="", args=[], type=None, cli=False, input=False):
    if self.window.active_view():
      fname = self.window.active_view().file_name()
      dirName = os.path.dirname(fname)
      syscmd = '/usr/bin/gnome-terminal --working-directory="' + dirName + '" "/bin/bash -il"'
      p = subprocess.Popen(syscmd, shell=True, stdout=subprocess.PIPE)

      print(dirName)
      print(syscmd)
      print(p)

  def is_enabled(self):
    return True

# import os
# import sublime
# import sublime_plugin
# import subprocess

# f = open("/home/pat/tmp/gopen.py.log", "w+")

# class gopenCommand(sublime_plugin.WindowCommand):

#   def run(self, app="", args=[], type=None, cli=False, input=False):
#     if self.window.active_view():
#       fname = self.window.active_view().file_name()
#       dirName = os.path.dirname(fname)
#       # syscmd = '/usr/bin/gnome-terminal --working-directory="' + dirName + '" "/bin/bash -il"'
#       # syscmda = ['/usr/bin/gnome-terminal', '--working-directory="' + dirName + '"', '/bin/bash -il']
#       syscmd = '/bin/bash /home/pat/.config/sublime-text-3/Packages/User/runterm.sh "' + dirName + '"'
#       # p = os.system('/bin/bash /home/pat/.config/sublime-text-3/Packages/User/runterm.sh "' + dirName + '"')
#       # syscmd = '/usr/bin/bash ./runterm.sh "' + dirName + '"'
#       p = subprocess.Popen(syscmd, shell=True, stdout=subprocess.PIPE)
#       # p = subprocess.call(syscmd, shell=True, stdout=subprocess.PIPE)
#       # /home/pat/.config/sublime-text-3/Packages/User/gopen.py
#       print(dirName)
#       # print(syscmd)
#       print(p)

#   def is_enabled(self):
#     return True
