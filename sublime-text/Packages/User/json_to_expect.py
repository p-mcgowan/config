import sublime_plugin, json
import User.flatten_json

def convert_key_value_to_assertion(key, value):
  return f"expect({key}).equals({value});"

def add_array_length_assertion(key, lines, seen):
  left = key.rfind('[')
  array_key = key[0:left]

  if array_key in seen:
    return

  seen[array_key] = True
  array_length = int(key[left + 1:-1]) + 1
  lines.append(convert_key_value_to_assertion(f"{array_key}.length", array_length))

class JsonToExpectCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    for region in self.view.sel():
      if region.empty():
        continue

      indent = region.begin() -self.view.lines(region)[0].begin()
      replacement = flatten_json(json.loads(self.view.substr(region)))
      lines = []
      keys = list(replacement.keys())
      keys.sort(reverse=True)
      seen = {}

      for key in keys:
        if key[-1] == "]":
          add_array_length_assertion(key, lines, seen)

        value = json.dumps(replacement[key])
        lines.append(convert_key_value_to_assertion(key, value))

      lines.sort()
      self.view.replace(edit, region, f"\n{' ' * indent}".join(lines))
