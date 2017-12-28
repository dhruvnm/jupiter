from datetime import time
from re import findall

class Section:

    def __init__(self, section_id, instructors):
        self.meetings = list()
        self.section_id = section_id
        self.instructors = instructors

    def add_meeting(self, meeting):
        self.meetings.append(meeting)

    # Check if any meetings in this section object conflict with any meetings in
    # another section object
    def is_conflict(self, other):
        for other_meeting in other.meetings:
            for this_meeting in self.meetings:
                if (other_meeting.is_conflict(this_meeting)) is True:
                    return True
        return False

class Meeting:

    def __init__(self, days, start_time, end_time):
        self.days = days

        # The following code parses a string like 12:30pm and saves it as a time object
        t = start_time.split(':')
        if start_time[-2:] == 'am' or start_time[:2] == '12':
            self.start_time = time(int(t[0]), int(t[1][:-2]))
        else:
            self.start_time = time(int(t[0]) + 12, int(t[1][:-2]))

        t = end_time.split(':')
        if end_time[-2:] == 'am' or end_time[:2] == '12':
            self.end_time = time(int(t[0]), int(t[1][:-2]))
        else:
            self.end_time = time(int(t[0]) + 12, int(t[1][:-2]))

    def is_conflict(self, other):
        # Split 'MWF' into ['M', 'W', 'F'], etc.
        other_days = findall('[A-Z][^A-Z]*', other.days)

        # Check if the two meetings share any days
        day_conflict = False
        for day in other_days:
            if day in self.days:
                day_conflict = True
                break

        # if there is a day conlict, check the times
        if day_conflict is True:
            if ((other.start_time >= self.start_time and
               other.start_time <= self.end_time) or
               (other.end_time >= self.start_time and
               other.end_time <= self.end_time)):
                return True

        return False
