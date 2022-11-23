import sublime, sublime_plugin
import json, re

class CustomLayoutCommand(sublime_plugin.WindowCommand):
  def run(self, layout):
    print(self.window.layout())
    print(layout)

    # self.window.set_layout({ 'cells': [ [0, 0, 1, 1], [1, 0, 2, 1] ], 'cols': [0.0, 0.5, 1.0], 'rows': [0.0, 0.5, 1.0] })
    # {'cells': [[0, 0, 1, 1], [1, 0, 2, 1]], 'cols': [0.0, 0.5, 1.0], 'rows': [0.0, 1.0]}

    # todo: the maths
    # set layout 1 2 1 = 1 wide row, 1 split row in the middle, 1 more wide row....
    # window.set_layout({ 'cells': [ [0, 0, 1, 1], [1, 0, 2, 1] ], 'cols': [0.0, 0.5, 1.0], 'rows': [0.0, 0.5, 1.0] })
    # window.set_layout({ 'cells': [ [0, 0, 1, 1], [1, 0, 2, 2], [0, 1, 1, 2], [1, 1, 2, 2]], 'cols': [0.0, 0.5, 1.0], 'rows': [0.0, 0.5, 1.0]})
    # window.set_layout({ 'cells': [
    #   [0, 0, 1, 1],
    #   [0, 1, 1, 2],
    #   [0, 2, 1, 3]
    # ], 'cols': [0.0, 1.0], 'rows': [0.0, 0.33, 0.66, 1.0]})
    # for region in self.view.sel():
    #   if not region.empty():
    #     selText = self.view.substr(region)
    #     # search for interface (selection)
    #     view.find('interface ' + selText, 0)

# class CustomLayoutPromptCommand(sublime_plugin.TextCommand):
#     """Prompt for command."""

#     def run(self, edit):
#         return self.view.window().show_input_panel('Set layout:', '', self.on_done, None, None)

#     def on_done(self, layout):
#         self.view.window().run_command('custom_layout', { 'layout': layout })



#         import sublime_plugin
#         import sublime
#         import os

#         class InputHandler(sublime_plugin.TextInputHandler):
#             def __init__(self, view):
#                 self.view = view

#             def name(self):
#                 return "new_layout"

#             def placeholder(self):
#                 return "Columns"

#             # def initial_text(self):
#             #     old = self.view.file_name()

#             #     if old is None:
#             #         return self.view.name()
#             #     else:
#             #         branch, leaf = os.path.split(old)
#             #         return leaf

#             def validate(self, name):
#                 return True
#                 # if self.view.file_name() is None:
#                 # else:
#                 #     return len(name) > 0


#         class CustomLayoutCommand(sublime_plugin.WindowCommand):
#             def run(self, new_layout):
#                 view = self.window.active_view()
#                 # old = view.file_name()

#                 print(new_layout, type(new_layout))
#                 colJump = 1 / int(new_layout)
#                 print(colJump)
#                 i = colJump
#                 j = 1
#                 cols = [0]
#                 cells = [[0, 0, 1, 1]]
#                 while i < 1:
#                     cols.append(i)
#                     cells.append([j, 1, j + 1, 1])
#                     i = i + colJump
#                     j = j + 1
#                 cols.append(1)
#                 # cells.append([j, 1, j + 1, 1])
#                 print(cols)
#                 print(cells)
#                 self.window.run_command("set_layout", {
#                     "cells": cells,
#                     "cols": cols,
#                     "rows": [
#                         0.0, 1.0
#                     ]
#                 })
#                 # if old is None:
#                 #     # Unsaved file
#                 #     view.set_name(new_layout)
#                 # else:
#                 #     branch, leaf = os.path.split(old)
#                 #     new = os.path.join(branch, new_layout)

#                 #     if new == old:
#                 #         return

#                 #     try:
#                 #         if os.path.isfile(new) and not self.is_case_change(old, new):
#                 #             raise OSError("File already exists")

#                 #         os.rename(old, new)

#                 #         if view:
#                 #             view.retarget(new)
#                 #     except OSError as e:
#                 #         sublime.status_message("Unable to rename: " + str(e))
#                 #     except:
#                 #         sublime.status_message("Unable to rename")

#             def input(self, args):
#                 if "new_layout" not in args:
#                     return InputHandler(self.window.active_view())
#                 else:
#                     return None

#             # def is_case_change(self, old, new):
#             #     if old.lower() != new.lower():
#             #         return False
#             #     if os.stat(old).st_ino != os.stat(new).st_ino:
#             #         return False
#             #     return True
