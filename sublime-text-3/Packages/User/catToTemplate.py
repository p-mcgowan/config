# Run with `view.run_command('example_plugin')` in the console, or put
# something like:
# { "caption": "Example Plugin", "command": "example_plugin" }
# in the command pallete.
#
import sublime, sublime_plugin, re

# function (stringInput) {
#     if (!stringInput) { return; }

#     const tokens = stringInput.split('+').map(s => s.trim());
#     if (tokens.length === 1) {
#         return tokens[0];
#     }

#     const res = tokens.map(function(token) {
#       if (/["'`]/.test(token)) {
#         return token.replace(/["'`]/g, '');
#       } else {
#         return `\${${token}}`);
#       }
#     }
#     return res.join('');
# }

# class HcDefCommand(sublime_plugin.WindowCommand):
def parse_tokens(token):
    if not re.match(r'["\'`]', token) is None:
        reg = re.compile(r'["\'`]')
        return reg.sub('', token)
    else:
        return '${' + token + '}'

class CatToTemplateCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                selText = self.view.substr(region)
                tokens = list(map(lambda s: s.strip(), selText.split('+')))

                if len(tokens) is 1:
                    return

                replacement = ''.join(list(map(parse_tokens, tokens)))
                self.view.replace(edit, region, '`' + replacement + '`')
