import sublime_plugin, json, re

def flatten_json(nested_json):
    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name[:-1] + '[' + str(i) + '].')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

class FlattenJsonCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                selText = self.view.substr(region)
                replacement = json.dumps(flatten_json(json.loads(selText)))
                self.view.replace(edit, region, replacement)

