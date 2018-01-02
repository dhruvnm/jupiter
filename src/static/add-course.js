courseCounter = 1;
optionIdCounter = 1;


function addCourse(divName) {
  var parentDiv = document.getElementById(divName);
  var newDiv = document.createElement('div');
  courseCounter++;
  newDiv.setAttribute("id", "course" + courseCounter);
  newDiv.innerHTML = "Course #" + courseCounter + "<br><input type=\"text\" name=\"classes[]\">\n"
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
