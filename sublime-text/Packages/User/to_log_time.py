import sublime_plugin
import re
import sublime
from time import strftime
from itertools import takewhile
import math

isMeeting = re.compile(r'townhall|town hall|meeting|chat|daily|dailies|biweekly|weekly|refinement|demo|monthly|planning|retro|talk|4-eyes|sync|estimations?')
isAos = re.compile(r'\baos\b')
isInterview = re.compile(r'interview|cv review')
isFuntime = re.compile(r'funtime|funday')
is4Eyes = re.compile(r'^4[- ]eyes$')
isTime = re.compile(r'^\d+:\d+$')
isFst = re.compile(r'\bfst\b')
shouldRemove = re.compile(r'^(lunch|smoke|out)$')
isTicket = re.compile(r'^([\d, ]+)\ (.*)')
isDevopsMeeting = re.compile(r'devops biweekly|devops 4-eyes')
isDevBiweekly = re.compile(r'dev (monthly|biweekly|meeting)')
isLeadBiweekly = re.compile(r'lead (monthly|biweekly|meeting)')
isIdeation = re.compile(r'ideation')
isDry = re.compile(r'\b(dry|dryday)\b')
isLbsi = re.compile(r'\b((2|bmw)?lbsi|inapp|cdcl)\b')
isBmwk = re.compile(r'\bbmwi?(k|\ know)')
isFbm = re.compile(r'\bfbm\b', re.I)
isInteDev = re.compile(r'inte dev')
isInteTeam = re.compile(r'inte team')

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

    def entryFromInput(self, string):
        if string is None or len(string.strip()) == 0:
            return None;
        # indent = ''.join(' ' for _ in takewhile(str.isspace, string))

        (hours, msg) = list(map(lambda s: s.strip(), string.split('|')))
        if (isTime.search(msg)):
            (msg, hours) = (hours, msg)

        if shouldRemove.search(msg):
            return f"// {string}"

        ticketMatch = isTicket.search(msg)
        if ticketMatch:
            hours = roundTime(hours)
            # hours = roundUpTime(hours)
            return f"{hours} | {ticketMatch.group(1).replace(' ', ',')} | {ticketMatch.group(2)};"

        logType = 'meeting' if isMeeting.search(msg) else 'dev'

        projectBilling = 'PROJECT|BILLING'
        if isFst.search(msg):
            projectBilling = 'dry|cycle 14'
            msg = f'ACRDDF-56 2021-05-28 filesystem-template (ACRDDF-34) - {msg}'
            logType = 'dev'
        elif isLbsi.search(msg):
            projectBilling = 'lbsi|^inApp.*post mvp'
        elif isDry.search(msg):
            projectBilling = 'dry|cycle 14'
        elif isFuntime.search(msg) or isInteTeam.search(msg):
            projectBilling = 'inte|team.*2024'
            logType = 'meeting'
        elif isInterview.search(msg):
            projectBilling = 'recr|developer'
            logType = 'meeting'
        elif isDevopsMeeting.search(msg):
            projectBilling = 'devops|2024'
            logType = 'meeting'
        # elif isIdeation.search(msg):
        #     projectBilling = 'devops|2024'
        #     logType = 'meeting'
        elif isBmwk.search(msg):
            projectBilling = 'inte|intern.*2024'
            logType = 'meeting'
        elif isAos.search(msg):
            projectBilling = 'aos|general'
        elif isFbm.search(msg):
            projectBilling = 'fbm|general'
            logType = 'meeting'
        elif isDevBiweekly.search(msg) or isLeadBiweekly.search(msg) or is4Eyes.search(msg) or isInteDev.search(msg):
            projectBilling = 'inte|^devel.*2024'
            logType = 'meeting'

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
