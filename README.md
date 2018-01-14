# jupiter
An interactive scheduler for UMD students.

## Overview
Jupiter is a system built to make scheduling easier for students at the University of Maryland - College Park. It is meant to improve upon the existing scheduler the university provides called "Venus." Jupiter uses the umd.io API to get all of its course information.

## Usage
Clone the repository and then change directory to `jupiter/src`. Run the command below to begin the web service.
```
python3 jupiter.py
```
Then navigate to `127.0.0.1:5000` to access the system.

## Important Notes

### Text Inputs
Jupiter uses case-insentive substring matching for all text inputs. For example if you want to take CMSC132 with Larry Herman, you can enter `larry`, `Herman`, or `LArrY HerMan` and they will all match to Herman's sections of CMSC132. If you enter an input that cannot match to a substring, for example `larry_herman`, then the sections will not be matched. 

Similarly, the best way to match a specific section is to enter the full four digit section number. For example if you want to take CMSC132-0101, you can enter `cmsc131-0101` or just `0101`. Note that entering just `101` could potentially match a section that has a section number starting with `101`. This is why it's usually best to use all four digits. 

### Filter Order
Jupiter will process all `include` filter options first. After that, Jupiter will take all of the remaining sections and process them with all `don't include` filter options. In the event that there are no sections remaining after the `include` phase, the `don't include` phase will be carried out on all the sections of that class. 
