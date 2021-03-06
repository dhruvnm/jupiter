from json import load
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
        schedules = get_classes(request)
        n = ''.join(['There are <b>', str(len(schedules)), '</b> schedules possible'])
        written = write_schedules(schedules)
        return render_template('result.html', n=n, schedules=written)
    else:
        return render_template('result.html', n='', schedules=['You haven\'t entered any classes!'])

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
    class_json = apply_time(class_json, request)
    class_json.sort(key=len)
    schedules = make_schedules(class_json)
    return schedules

def apply_time(classes, request):
    inc = request.form.getlist('time-inc[]')
    day = request.form.getlist('time-day[]')
    top = request.form.getlist('time-top[]')
    bot = request.form.getlist('time-bot[]')

    to_include = list()
    d_include = list()

    #split into lists of thinggs to include and not to include
    for w, x, y, z in zip(inc, day, top, bot):
        if w == 'include':
            to_include.append((x, y, z,))
        else:
            d_include.append((x, y, z,))

    mod = list()
    for cl in classes:
        good_secs = list()
        #determine which sections abide by the include rules
        for section in cl:
            good = True
            for d, start, end in to_include:
                for meeting in section['meetings']:
                    if d in meeting['days']:
                        met = Meeting(meeting['days'], meeting['start_time'], meeting['end_time'])
                        if not  met.violates_res(start, end):
                            good = False
                            break

                if not good:
                    break

            if good:
                good_secs.append(section)

        if len(good_secs) == 0:
            good_secs = cl

        #remove any sections that should not be included
        to_remove = list()
        i = 0
        for section in good_secs:
            remove = False
            for d, start, end in d_include:
                for meeting in section['meetings']:
                    if d in meeting['days']:
                        met = Meeting(meeting['days'], meeting['start_time'], meeting['end_time'])
                        if met.violates_res(start, end):
                            remove = True
                            break

                if remove:
                    break

            if remove:
                to_remove.append(i)

            i = i + 1

        to_remove = list(reversed(to_remove))
        for idx in to_remove:
            good_secs.pop(idx)

        mod.append(good_secs)

    return mod


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
                    check = check.strip()
                    if check in actual:
                        good_secs.append(section)
                        break
                else:
                    found = False
                    for instructor in section['instructors']:
                        actual = instructor.lower()
                        check = val.lower()
                        check = check.strip()
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
                    check = check.strip()
                    if check in actual:
                        to_remove.append(j)
                        break
                else:
                    found = False
                    for instructor in section['instructors']:
                        actual = instructor.lower()
                        check = val.lower()
                        check = check.strip()
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
    i = 1
    if schedules == None or len(schedules) == 0:
        return ['No possible schedules!']

    written = list()

    for schedule in schedules:
        header = ''.join(['<hr>', '<b>Schedule #', str(i), '</b>'])
        c_list = [header]
        for cl in schedule:
            start = [cl.section_id]
            start.append('<em>')
            for instructor in cl.instructors:
                start.append(instructor)
            start.append('</em>')
            start.append('<br>')
            start_text = ' '.join(start)

            m_list = list()
            for meeting in cl.meetings:
                m_list.append(' '.join(['<p style=\"text-indent :5em;\" >', meeting.days,
                    meeting.start_time.strftime('%I:%M%p'), '-',
                    meeting.end_time.strftime('%I:%M%p'), '</p>']))
            m_text = ''.join(m_list)
            c_list.append(''.join([start_text, m_text]))

        written.append('<br>'.join(c_list))
        i = i + 1

    return written

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
            if meeting['days'] == '':
                pass
            else:
                section_obj.add_meeting(Meeting(meeting['days'], meeting['start_time'], meeting['end_time']))

        obj_list.append((section_obj,))
    return obj_list

if __name__ == '__main__':
    app.run()
