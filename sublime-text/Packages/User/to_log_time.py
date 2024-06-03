import sublime_plugin
import re
import sublime
from time import strftime
from itertools import takewhile
import math

# pull from config
# {
#   "vars": {
#     "dryProjectBilling": "dry|cycle 17"
#   },
#   "rules": [
#     {
#       "when": "townhall|town hall|meeting|chat|daily|dailies|biweekly|weekly|refinement|demo|monthly|planning|retro|talk|4-eyes|sync|estimations?",
#       "logType": "meeting",
#       "continue": true
#     },
#     {
#       "when": "interview|cv review|recruiting|offerzen|recr",
#       "projectBilling": "recr|developer",
#       "logType": "meeting"
#     },
#     {
#       "when": "\\b(dry|dryday)\\b",
#       "projectBilling": "$dryProjectBilling"
#     },
#     {
#       "when": "\\b(fbm|fbmrefresh)\\b",
#       "case": "ignore",
#       "projectBilling": "fbm|general"
#     }
#   ]
# }

isTime = re.compile(r'^\d+:\d+$')
isTicket = re.compile(r'^([\d, ]+)\ (.*)')

def roundUpTime(time):
    (hours, minutes) = list(map(lambda s: int(s.strip()), time.split(':')))
    if minutes > 45:
        minutes = "00"
        hours = hours + 1
    elif minutes > 30:
        minutes = 45
    elif minutes > 15:
        minutes = 30
    elif hours > 0 and minutes < 7:
        minutes = "00"
    else:
        minutes = 15

    return f"{hours}:{minutes}"

def roundTime(time):
    (hours, minutes) = list(map(lambda s: int(s.strip()), time.split(':')))
    if minutes > 50:
        minutes = "00"
        hours = hours + 1
    elif minutes > 35:
        minutes = 45
    elif minutes > 20:
        minutes = 30
    elif hours > 0 and minutes < 7:
        minutes = "00"
    else:
        minutes = 15

    return f"{hours}:{minutes}"

class ToLogTimeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.parse_rules()
        print('\n\n\n')

        lines = []
        selectedRegion = None

        for region in self.view.sel():
            if not region.empty():
                if selectedRegion is None:
                    selectedRegion = sublime.Region(region.begin(), region.end())
                else:
                    selectedRegion.b = region.end()

                for selText in self.view.substr(region).split('\n'):
                    replacement = self.entryFromInput(selText)
                    if replacement is not None:
                        lines.append(replacement)

        lines.sort()
        self.view.replace(edit, selectedRegion, '\n'.join(lines))

    def parse_rules(self):
        self.settings = sublime.load_settings("to-log-time.sublime-settings")
        # self.settings = self.view.settings().get('logtime')
        self.rules = []
        self.vars = self.settings.get('vars', {})
        for rule in self.settings.get('rules', []):
            if not rule.get('when'):
                self.rules.append(rule)
                continue

            rule['when'] = re.compile(rule['when'], re.I if rule.get('case', None) == 'ignore' else 0)
            for var in self.vars:
                if rule.get('projectBilling'):
                    rule['projectBilling'] = rule['projectBilling'].replace(f'${var}', self.vars.get(var))
                if rule.get('logType'):
                    rule['logType'] = rule['logType'].replace(f'${var}', self.vars.get(var))
            self.rules.append(rule)

    def replaceMessage(self, ruleMessage, msg):
        if ruleMessage is None:
            return msg

        result = ruleMessage.replace('$msg', msg)

        for var in self.vars:
            result = result.replace(f'${var}', self.vars.get(var))

        return result

    def entryFromInput(self, string):
        if string is None or len(string.strip()) == 0:
            return None;
        # indent = ''.join(' ' for _ in takewhile(str.isspace, string))

        (hours, msg) = list(map(lambda s: s.strip(), string.split('|')))
        if (isTime.search(msg)):
            (msg, hours) = (hours, msg)

        # if shouldRemove.search(msg):
        #     return f"// {string}"

        ticketMatch = isTicket.search(msg)
        if ticketMatch:
            hours = roundTime(hours)
            # hours = roundUpTime(hours)
            return f"{hours} | {ticketMatch.group(1).replace(' ', ',')} | {ticketMatch.group(2)};"

        projectBilling = 'PROJECT|BILLING'
        logType = 'meeting'

        # print('\n\n=========================')
        # print(string)

        for rule in self.rules:
            # print(rule)

            if not rule.get('when'):
                projectBilling = rule.get('projectBilling', projectBilling)
                logType = rule.get('logType', logType)
                msg = self.replaceMessage(rule.get('msg'), msg)
                # print('----')
                continue

            if not rule.get('when').search(msg):
                # print('----')
                continue

            msg = self.replaceMessage(rule.get('msg'), msg)

            if rule.get('projectBilling') is None and rule.get('logType') is None:
                # print(f'nil return: {msg}')
                return msg

            projectBilling = rule.get('projectBilling', projectBilling)
            logType = rule.get('logType', logType)

            if rule.get('continue') != True:
                break

        # print(f"""end return: '{strftime("%d.%m.%Y")}|{projectBilling}|{msg}|{hours}|{logType}',""")
        return f"""'{strftime("%d.%m.%Y")}|{projectBilling}|{msg}|{hours}|{logType}',"""

class GroupLogsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                continue

            hours = None
            date = None
            project = None
            billing = None
            time = None
            billingType = None
            descriptions = []

            entries = self.view.substr(region).split('\n')
            for selText in entries:
                if selText is None or len(selText.strip()) == 0:
                    continue
                (date, project, billing, desc, time, billingType) = selText.split('|')

                if desc not in descriptions:
                    descriptions.append(desc)
                hours = self.addTime(time, hours);

            time = roundUpTime(hours)
            if len(entries) == 1:
                time = roundTime(hours)

            joined = '|'.join([
                date,
                project,
                billing,
                '; '.join(descriptions),
                time,
                billingType
            ])

            self.view.replace(edit, region, joined)

    def addTime(self, timeA, timeB):
        if timeB is None:
            return timeA

        (h1, m1) = timeB.split(':')
        (h2, m2) = timeA.split(':')
        h = int(h1) + int(h2)
        m = int(m1) + int(m2)
        h = h + math.floor(m / 60)
        m = m % 60

        return f"{h}:{m}"
