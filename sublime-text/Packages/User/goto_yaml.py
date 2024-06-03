import sublime
import sublime_plugin
import re
import os.path

class GotoYamlCommand(sublime_plugin.TextCommand):
    def run(self, edit, event=None):
        # regions = [s for s in self.view.sel() if not s.empty()]
        pt = 0 if not event else self.view.window_to_text((event["x"], event["y"]))


        parts = self.view.file_name().split('/')
        while len(parts) > 0 and parts[-1] != 'src':
            parts.pop()

        project = None
        if parts[-1] == 'src':
            parts.pop()
            project = '/'.join(parts)

        if project == None:
            print('no project?')
            return

        ctx = self.view.expand_to_scope(pt, 'string')
        if not ctx:
            print('no ctx?')
            return
        file = self.view.substr(ctx).replace('"', '').replace("'", '').replace('#', 'src').split('/')
        original = self.view.substr(ctx).replace('"', '').replace("'", '')

        if file[-2] == 'parameters':
            file[-1] = ''.join([file[-1][0].lower(), file[-1][1:], '.yml'])
        else:
            file[-1] = self.convert_to_file(file[-1])

        target = '/'.join([project, '/'.join(file)])
        print(' '.join([original, '=>', target]))

        if not os.path.isfile(target):
            self.show_error('file not found:\n' + ' '.join([original, '=>', target]))
        else:
            sublime.active_window().open_file(target)

    def convert_to_file(self, filename):
        if filename.endswith('Post'):
            return self.kebab(re.sub('Post$', '', filename)) + '/post.yml'
        if filename.endswith('Patch'):
            return self.kebab(re.sub('Patch$', '', filename)) + '/patch.yml'

        is_singular = filename[-1] != 's'
        if is_singular:
            return self.kebab(filename)  + '/model.yml'

        return self.kebab(re.sub('s$', '', filename))  + '/models.yml'

    def show_error(self, message):
        errorTemplate = """
            <body>
                <style>
                    p {
                        white-space: pre-wrap;
                        margin-top: 0;
                    }
                    a {
                        font-family: system;
                        font-size: 1.05rem;
                    }
                </style>
                <p>%s</p>
            </body>
        """ % (re.sub('\n', '<br>', message))

        self.view.show_popup(errorTemplate, max_width=1200)

    def kebab(self, text):
        return '-'.join(re.sub(r'[A-Z]', lambda x: ' ' + x.group().lower(), text).split())

    def is_visible(self, event=None):
        pt = 0 if not event else self.view.window_to_text((event["x"], event["y"]))
        scopes = self.view.scope_name(pt).split();

        return scopes[0] == 'source.yaml'

    def want_event(self):
        return True
