import sublime
import sublime_plugin
import re
from time import strftime

isMeeting = re.compile(r'townhall|town hall|meeting|chat|daily|dailies|weekly|refinement|demo|monthly|planning|retro|talk|4-eyes')
isAos = re.compile(r'daily|dailies|refinement|demo|planning|retro|townhall|town hall')
isInterview = re.compile(r'interview|cv review')
isFuntime = re.compile(r'funtime')
is4Eyes = re.compile(r'^4-eyes$')
isTime = re.compile(r'^\d+:\d+$')
shouldRemove = re.compile(r'^(lunch|smoke)$')
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


                if (shouldRemove.search(msg)):
                    # self.view.erase(edit, region)
                    self.view.replace(edit, region, f"// {selText}")
                    continue

                hours = self.roundTime(hours)

                ticketMatch = isTicket.search(msg)
                if ticketMatch:
                    msg = f"{ticketMatch.group(1)} | {ticketMatch.group(2)}"
                    self.view.replace(edit, region, f"{hours} | {ticketMatch.group(1)} | {ticketMatch.group(2)};")
                    continue

                logType = 'dev'
                if (isMeeting.search(msg)):
                    logType = 'meeting'

                projectBilling = 'project|billing'
                if (isAos.search(msg)):
                    projectBilling = 'aos|scrum.*mvp'
                elif (isFuntime.search(msg)):
                    projectBilling = 'inte|team'
                elif (is4Eyes.search(msg)):
                    projectBilling = 'inte|^dev'
                elif (isInterview.search(msg)):
                    projectBilling = 'recr|developer'
                    logType = 'meeting'

                replacement = f"""'{strftime("%d.%m.%Y")}|{projectBilling}|{msg}|{hours}|{logType}',"""
                self.view.replace(edit, region, replacement)

    def roundTime(self, time):
        (hours, minutes) = list(map(lambda s: int(s.strip()), time.split(':')))
        if minutes > 50:
            minutes = "00"
            hours = hours + 1
        elif minutes > 35:
            minutes = 45
        elif minutes > 20:
            minutes = 30
        elif minutes > 5:
            minutes = 15
        else:
            minutes = "00"

        return f"{hours}:{minutes}"

