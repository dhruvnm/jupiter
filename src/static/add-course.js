counter = 1;

function addCourse(divName) {
  counter++;
  var parentDiv = document.getElementById(divName);
  var newDiv = document.createElement('div');
  newDiv.setAttribute("id", "course" + counter);
  newDiv.innerHTML = "Course #" + counter + "<br><input type='text' name='classes[]'>";
  parentDiv.appendChild(newDiv);
}

function removeCourse(divName) {
  divName += counter;
  var element = document.getElementById(divName);
  element.parentNode.removeChild(element);
  counter--;
}
