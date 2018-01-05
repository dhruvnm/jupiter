from json import load
from pprint import pprint
from urllib.request import urlopen
from urllib.error import HTTPError
from flask import Flask, render_template, request
from sections import Section, Meeting
from itertools import product

app = Flask(__name__)
url = 'http://api.umd.io/v0/courses/'

@app.route('/', methods = ['GET'])
def submit():
    return render_template('submit.html')

@app.route('/result/', methods = ['GET', 'POST'])
def result():
    if request.method == 'POST':
        get_classes(request)
        with open('schedules.txt', 'r') as f:
            content = f.read()
        return render_template('result.html', content=content)
    else:
        return render_template('result.html', content='You haven\'t entered any classes!')

def get_classes(request):
    classes = request.form.getlist('classes[]')
    mod = list()
    for c in classes:
        c = c.strip()
        c = c.lower()
        if len(c) > 0 and c not in mod:
            mod.append(c)

    class_json = list()

    for c in mod:
        c_url = ''.join([url, c, '/sections'])
        try:
            result = urlopen(c_url)
        except HTTPError:
            continue

        class_info = load(result)
        if isinstance(class_info, list) is False:
            class_info = [class_info]
        class_json.append(class_info)

    class_json = apply_filters(class_json, request)
    class_json.sort(key=len)
    schedules = make_schedules(class_json)
    write_schedules(schedules)

def apply_filters(classes, request):
    i = 1
    mod = list()
    for cl in classes:
        inc = request.form.getlist(''.join(['course', str(i), '-inc[]']))
        sori = request.form.getlist(''.join(['course', str(i), '-sori[]']))
        vals = request.form.getlist(''.join(['course', str(i), '-vals[]']))
        to_include = list()
        d_include = list()
        #Split into lists of things to include and things not to include
        for x, y, z in zip(inc, sori, vals):
            if x == 'include':
                to_include.append((y, z,))
            else:
                d_include.append((y, z,))

        good_secs = list()
        #determine which sections abide by the include rules
        for section in cl:
            for typ, val in to_include:
                if typ == 'section':
                    actual = section['section_id'].lower()
                    check = val.lower()
                    if check in actual:
                        good_secs.append(section)
                        break
                else:
                    found = False
                    for instructor in section['instructors']:
                        actual = instructor.lower()
                        check = val.lower()
                        if check in actual:
                            good_secs.append(section)
                            found = True
                            break
                    if found:
                        break

        if len(good_secs) == 0:
            good_secs = cl

        #remove any sections that should not be included
        j = -1
        to_remove = list()
        for section in good_secs:
            j = j + 1
            for typ, val in d_include:
                if typ == 'section':
                    actual = section['section_id'].lower()
                    check = val.lower()
                    if check in actual:
                        to_remove.append(j)
                        break
                else:
                    found = False
                    for instructor in section['instructors']:
                        actual = instructor.lower()
                        check = val.lower()
                        if check in actual:
                            to_remove.append(j)
                            found = True
                    if found:
                        break

        to_remove = list(reversed(to_remove))
        for idx in to_remove:
            good_secs.pop(idx)

        mod.append(good_secs)
        i = i + 1

    return mod

def write_schedules(schedules):
    with open('schedules.txt', 'w') as f:
        i = 1
        if schedules == None or len(schedules) == 0:
            f.write('No possible schedules!')
            return

        for schedule in schedules:
            f.write(''.join(['Schedule #', str(i), '\n']))
            for cl in schedule:
                l = [cl.section_id]
                for instructor in cl.instructors:
                    l.append(instructor)
                l.append('\n')
                f.write(' '.join(l))
                for meeting in cl.meetings:
                    f.write(' '.join([meeting.days,
                        meeting.start_time.strftime('%I:%M%p'), '-',
                        meeting.end_time.strftime('%I:%M%p'), '\n']))
            i = i + 1
            f.write('\n')

def make_schedules(classes):
    # No schedules possible if there are no classes
    if len(classes) == 0:
        return None

    schedules = convert(classes[0])

    i = 1;
    while i < len(classes):
        new_list = convert(classes[i]) # next classes sections
        # cartesian product of current schedules with new sections to get all
        # new possible sections
        schedules = list(product(schedules, new_list))
        conflicts = list()
        j = 0
        # iterate over all schedules to detect conflicts
        while j < len(schedules):
            for section in schedules[j][0]: # iterates over all old classes in schedule
                # checks to see if new section is a conflict
                if schedules[j][1][0].is_conflict(section) is True:
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

    return schedules

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
