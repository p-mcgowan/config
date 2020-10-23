import sublime
import sublime_plugin


def plugin_loaded():
    value = get_setting()
    sublime.log_input(value);
    sublime.log_commands(value);
    sublime.log_result_regex(value);

def get_setting():
    preferences = sublime.load_settings("Preferences.sublime-settings")
    result = preferences.get("debug")
    if result is None:
        result = False
    return result
