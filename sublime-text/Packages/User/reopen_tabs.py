# Re-open tabs (browser style)
#
# Based off of openLastClosedFile plugin v1.0.2
# (https://forum.sublimetext.com/t/openlastclosedfile/729/1)
# modified for ST3 by Pat McGowan (https://github.com/p-mcgowan)
#
# Example User keybinding:
# { "keys": ["ctrl+shift+t"], "command": "reopen_tabs" }
#

import sublime, sublime_plugin, os

logfile = '/tmp/reopenTabs.tmp'

class reopenTabsSecure(sublime_plugin.EventListener):

  def on_close(self, view):
    if view.file_name():
      file = open(logfile, 'a')
      file.writelines(view.file_name() + "\n")
      file.close()

class reopenTabsCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    fileName = logfile

    if os.path.isfile(fileName):
      readFile = open(fileName, "r")
      lines = readFile.readlines()
      readFile.close()

      length = len(lines)

      if length > 0:
        lastline = lines[length - 1]
        lastline = lastline.rstrip("\n")

        self.view.window().open_file(lastline, 0, 0)

        writeFile = open(fileName, "w")
        writeFile.writelines([item for item in lines[0 : length - 1]])
        writeFile.close()
