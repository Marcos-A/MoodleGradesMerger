# MoodleGradesMerger
Returns a CSV file with every student sorted by the name, containing his/her email, name and the highest exercise grade in case of multiple attempts
from a collection of CSV grade files downloaded from Moodle.
In case a percent is indicated, for every exercise this percent is assigned to the maximum achieved grade,
while the rest is distributed between the other grades.

For instance, if there has been 3 attemps for an exercise and 0.7 is set as a percent, 70% of the exercise qualification will be assigned to the highest grade, while 15% will be assigned to the remaining attempts.

## Requirements
Column's name indications are set to Catalan:
- "Adreça electrònica" for Email
- "Nom" for Name
- "Cognoms" for Surname
- "Qualificació" for Grade

Change them according to your Moodle CSV downloaded grade files language and column names.

## Running
If you only want to preserve the highest grade for every exercise:
- Run from Terminal:
```
python path/to/MoodleGradesMerger.py /path/to/CSVFilesFolder
```
- In case you have both Python versions, 2 and 3, installed in your computer:
```
python3 path/to/MoodleGradesMerger.py /path/to/CSVFilesFolder
```

In case you want to assign a percent to the the highest grade for every exercise, and distribute the remaining one between the other ones:
```
python path/to/MoodleGradesMerger.py /path/to/CSVFilesFolder percent
```
e.g. python path/to/MoodleGradesMerger.py /path/to/CSVFilesFolder 0.65
- In case you have both Python versions, 2 and 3, installed in your computer:
```
python3 path/to/MoodleGradesMerger.py /path/to/CSVFilesFolder percent
```
e.g. python3 path/to/MoodleGradesMerger.py /path/to/CSVFilesFolder 0.65