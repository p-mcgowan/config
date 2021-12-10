import sublime_plugin, json, re


import sublime, sublime_plugin
# class HcDefCommand(sublime_plugin.TextCommand):
class CustomLayoutCommand(sublime_plugin.WindowCommand):
  def run(self):
    print(self.window.layout())
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
