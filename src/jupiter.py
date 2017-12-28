from json import load
from pprint import pprint
from urllib.request import urlopen
from urllib.error import HTTPError
from flask import Flask, render_template, request
from sections import Section, Meeting
from itertools import product

app = Flask(__name__)
url = 'http://api.umd.io/v0/courses/'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        result = request.form
        get_classes(result['classes'])
        return result['classes']

def get_classes(classes):
    classes = classes.split(',')
    mod = list()
    for c in classes:
        c = c.strip()
        c = c.lower()
        mod.append(c)

    class_json = list()

    for c in mod:
        c_url = ''.join([url, c, '/sections'])
        try:
            result = urlopen(c_url)
        except HTTPError:
            continue

        class_info = load(result)
        class_json.append(class_info)

    class_json.sort(key=len)
    make_schedules(class_json)

def make_schedules(classes):
    # No schedules possible if there are no classes
    if len(classes) is 0:
        return None

    schedules = convert(classes[0])

    i = 1;
    while i < len(classes):
        new_list = convert(classes[i]) # next classes sections
        # cartesian product of current schedules with new sections to get all
        # new possible sections
        schedules = product(schedules, new_list)
        conflicts = list()
        j = 0
        # iterate over all schedules to detect conflicts
        while j < len(schedules):
            for section in schedules[j][0]: # iterates over all old classes in schedule
                # checks to see if new section is a conflict
                if schedules[j][1].is_conflict(section) is True:
                    conflicts.append(j)
                    break
            j = j + 1

        # remove all schedules with conflicts
        conflicts = list(reversed(conflicts))
        for idx in conflicts:
            schedules.pop(idx)

        # flatten list. i.e [((1,), (2,))] -> [(1, 2,)]
        new_schedules = list()
        for elt in schedules:
            new_schedules.append(tuple([section for tupl in elt for section in tupl]))
        schedules = new_schedules
        i = i + 1

# Converts a list of sections into a list of section objects in a tuple
def convert(sections):
    obj_list = list()
    for section in sections:
        section_obj = Section(section['section_id'], section['instructors'])
        for meeting in section['meetings']:
            section_obj.add_meeting(Meeting(meeting['days'], meeting['start_time'], meeting['end_time']))
        obj_list.append((section_obj,))
    return obj_list

if __name__ == '__main__':
    app.run()
