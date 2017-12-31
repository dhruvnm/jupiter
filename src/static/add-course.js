courseCounter = 1;

function addDiv(divName, option) {
  var parentDiv = document.getElementById(divName);
  var newDiv = document.createElement('div');
  addOptions(newDiv, option);
  parentDiv.appendChild(newDiv);
}

function removeDiv(divName, option) {
  divName = removeOptions(divName, option);
  var element = document.getElementById(divName);
  element.parentNode.removeChild(element);
}

function addOptions(div, option) {
  if (option == 'course') {
    courseCounter++;
    div.setAttribute("id", "course" + courseCounter);
    div.innerHTML = "Course #" + courseCounter + "<br><input type='text' name='classes[]'>";
  }
}

function removeOptions(divName, option) {
  if (option == 'course') {
    return divName + courseCounter--;
  }
}
