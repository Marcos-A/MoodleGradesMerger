# MoodleGradesMerger
Returns a CSV file with every student sorted by the name, containing his/her email, name and exercise's grades
from a collection of CSV grade files downloaded from Moodle.

## Requirements
Column's name indications are set to Catalan:
- "Adreça electrònica" for Email
- "Nom" for Name
- "Cognoms" for Surname
- "Qualificació" for Grade

Change them according to your Moodle CSV downloaded grade files language and column names.

## Running
Run from Terminal:
```
python path/to/MoodleGradesMerger.py /path/to/CSVFilesFolder
```
In case you have both Python versions, 2 and 3, installed in your computer:
```
python3 path/to/MoodleGradesMerger.py /path/to/CSVFilesFolder
```
