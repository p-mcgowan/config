# Run with `view.run_command('example_plugin')` in the console, or put
# something like:
# { "caption": "Example Plugin", "command": "example_plugin" }
# in the command pallete.
#
import sublime, sublime_plugin, os, re

class htmlToTsCommand(sublime_plugin.WindowCommand):
  def run(self, extension = None):
    fileName = self.window.active_view().file_name()

    if extension:
      currentExtension = re.sub(r'.*\.', '', fileName)
      self.window.open_file(fileName.replace('.' + currentExtension, '.' + extension))
    else:
      if '.ts' in fileName:
        self.window.open_file(fileName.replace('.ts', '.scss'))
        self.window.open_file(fileName.replace('.ts', '.html'))
      elif '.html' in fileName:
        self.window.open_file(fileName.replace('.html', '.scss'))
        self.window.open_file(fileName.replace('.html', '.ts'))
      elif '.scss' in fileName:
        self.window.open_file(fileName.replace('.scss', '.ts'))
        self.window.open_file(fileName.replace('.scss', '.html'))
