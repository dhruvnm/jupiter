courseCounter = 1;
optionIdCounter = 1;
timeIdCounter = 1;

function addCourse(divName) {
  var parentDiv = document.getElementById(divName);
  var newDiv = document.createElement('div');
  courseCounter++;
  newDiv.setAttribute("id", "course" + courseCounter);
  newDiv.innerHTML = "Course #" + courseCounter + "<br><input type=\"text\" name=\"classes[]\" required>\n"
                   + "<input type=\"button\" value=\"add option\" onclick=\"addOption('course" + courseCounter + "')\">";
  parentDiv.appendChild(newDiv);
}

function removeCourse() {
  var element = document.getElementById('course' + courseCounter);
  courseCounter--;
  element.parentNode.removeChild(element);
}

function addOption(divName) {
  var parentDiv = document.getElementById(divName);
  var newDiv = document.createElement('div');
  newDiv.setAttribute("id", "option" + optionIdCounter);

  newDiv.innerHTML = "<select name='" + divName + "-inc[]'>"
                     + "<option value='include'>Include</option>"
                     + "<option value='d_include'>Don't include</option>"
                     + "</select>"
                     + "<select name='" + divName + "-sori[]'>"
                     + "<option value='section'>Section</option>"
                     + "<option value='instructor'>Instructor</option>"
                     + "</section>"
                     + "<input type='text' name='" + divName + "-vals[]'>"
                     + "<input type='button' value='remove' onclick=\"removeOption('option" + optionIdCounter +"')\">";
  optionIdCounter++;
  parentDiv.appendChild(newDiv);
}

function removeOption(divName) {
  var element = document.getElementById(divName);
  element.parentNode.removeChild(element);
}

function addTRes() {
  var parentDiv = document.getElementById('timeRestriction');
  var newDiv = document.createElement('div');
  newDiv.setAttribute('id', 'time' + timeIdCounter);

  newDiv.innerHTML = "<select name='time-inc[]'>"
                   + "<option value='include'>Include</option>"
                   + "<option value='d_include'>Don't Include</option>"
                   + "</select>"
                   + "<select name='time-day[]'>"
                   + "<option value='M'>Monday</option>"
                   + "<option value='Tu'>Tuesday</option>"
                   + "<option value='W'>Wednesday</option>"
                   + "<option value='Th'>Thursday</option>"
                   + "<option value='F'>Friday</option>"
                   + "</select>"
                   + "<input type='time' name='time-top[]' required> to "
                   + "<input type='time' name='time-bot[]' required>"
                   + "<input type='button' value='remove' onclick=\"removeOption('time" + timeIdCounter +"')\">";
  timeIdCounter++;
  parentDiv.appendChild(newDiv);
}
