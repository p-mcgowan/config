import sublime_plugin
import re
from time import strftime

isMeeting = re.compile(r'townhall|town hall|meeting|chat|daily|dailies|weekly|refinement|demo|monthly|planning|retro|talk|4-eyes')
isAos = re.compile(r'daily|dailies|refinement|demo|planning|retro|townhall|town hall')
isInterview = re.compile(r'interview|cv review')
isFuntime = re.compile(r'funtime')
is4Eyes = re.compile(r'^4-eyes$')
isTime = re.compile(r'^\d+:\d+$')
isFst = re.compile(r'^fst$')
shouldRemove = re.compile(r'^(lunch|smoke|out)$')
isTicket = re.compile(r'^(\d+)\ (.*)')

class ToLogTimeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        lines = []

        for region in self.view.sel():
            if not region.empty():
                selText = self.view.substr(region)

                (hours, msg) = list(map(lambda s: s.strip(), selText.split('|')))
                if (isTime.search(msg)):
                    (msg, hours) = (hours, msg)

                if shouldRemove.search(msg):
                    # self.view.erase(edit, region)
                    self.view.replace(edit, region, f"// {selText}")
                    continue

                # hours = self.roundTime(hours)
                hours = self.roundUpTime(hours)

                ticketMatch = isTicket.search(msg)
                if ticketMatch:
                    msg = f"{ticketMatch.group(1)} | {ticketMatch.group(2)}"
                    self.view.replace(edit, region, f"{hours} | {ticketMatch.group(1)} | {ticketMatch.group(2)};")
                    continue

                logType = 'dev'
                if isMeeting.search(msg):
                    logType = 'meeting'

                projectBilling = 'project|billing'
                if isAos.search(msg):
                    projectBilling = 'aos|general'
                elif isFuntime.search(msg):
                    projectBilling = 'inte|team'
                elif is4Eyes.search(msg):
                    projectBilling = 'inte|^dev'
                elif isInterview.search(msg):
                    projectBilling = 'recr|developer'
                    logType = 'meeting'
                elif isFst.search(msg):
                    projectBilling = 'dry|cycle 9'
                    msg = f"ACRDDF-56 2021-05-28 filesystem-template (ACRDDF-34) - fst"

                replacement = f"""'{strftime("%d.%m.%Y")}|{projectBilling}|{msg}|{hours}|{logType}',"""
                self.view.replace(edit, region, replacement)

    def roundUpTime(self, time):
        (hours, minutes) = list(map(lambda s: int(s.strip()), time.split(':')))
        if minutes > 45:
            minutes = "00"
            hours = hours + 1
        elif minutes > 30:
            minutes = 45
        elif minutes > 15:
            minutes = 30
        # elif minutes > 7:
        #     minutes = 15
        elif hours > 0 and minutes < 7:
            minutes = "00"
        else:
            minutes = 15

        return f"{hours}:{minutes}"

    def roundTime(self, time):
        (hours, minutes) = list(map(lambda s: int(s.strip()), time.split(':')))
        if minutes > 50:
            minutes = "00"
            hours = hours + 1
        elif minutes > 35:
            minutes = 45
        elif minutes > 20:
            minutes = 30
        # elif minutes > 7:
        #     minutes = 15
        elif hours > 0 and minutes < 7:
            minutes = "00"
        else:
            minutes = 15

        return f"{hours}:{minutes}"

