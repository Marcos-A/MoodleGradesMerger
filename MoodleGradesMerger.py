#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

"""
MoodleGradesMerger.py
Returns a CSV file with every student sorted by the name, containing his/her email, name and exercise's grades
from a collection of CSV grade files downloaded from Moodle.
Indicate the folder with the Moodle downloaded grade files as an argument when running the script.
Column's name indications are set to Catalan:
- "Adreça electrònica" for Email
- "Nom" for Name
- "Cognoms" for Surname
- "Qualificació" for Grade
"""

import csv
import os
from sys import argv
import unicodedata

DOWNLOADED_GRADES_FOLDER = argv[1]
EXERCISES_LIST = []
STUDENTS_EMAIL_DICT = {}
RESULT_FILE = 'result.csv'


"""
Returns as list every CSV grades file in the folder
"""
def collect_grades_files(grades_folder):
    files_list = []
    for file in os.listdir(grades_folder):
        if file.endswith('.csv') and file != RESULT_FILE:
            files_list.append(os.path.join(DOWNLOADED_GRADES_FOLDER, file))
    
    return files_list


"""
Returns the CSV column index that contains the text to be found
"""
def get_column_index_in_csv(file_path, text_to_find):
    with open (file_path, 'r', encoding='utf-8') as moodle_grades:
        moodle_grades_reader = csv.reader(moodle_grades)
        moodle_grades_header = next(moodle_grades_reader)
        for index, column_name in enumerate(moodle_grades_header):
            if text_to_find in column_name:
                return index


"""
Returns the name of the exercise based no the grades file name
"""
def get_exercise_name(file_path):
    file_name = file_path.split('/')[-1]
    # Rewrite ampersands parsed as special chars in filepaths
    file_name = file_name.replace('amp;', '&')
    return file_name.replace('-qualificacions.csv', '')


"""
Returns a float from a number in a comma-separated string format
"""
def convert_comma_separated_grade_to_float(comma_separated_grade_string):
    if comma_separated_grade_string == '-':
        return 0.00
    else:
        return float(comma_separated_grade_string.replace(',', '.'))


"""
Returns a comma-separated string formatted number with 2 decimals from a float
"""
def convert_float_to_comma_separated_grade(float_number):
    if isinstance(float_number, str):
        print(float_number)
    return(str('{:.2f}'.format(float_number)).replace('.', ','))


"""
Removes every accent from a string
"""
def strip_accents(student_name):
   return ''.join(c for c in unicodedata.normalize('NFD', student_name)
                  if unicodedata.category(c) != 'Mn')


"""
Returns a list of emails alphabetically sorted by the student name
"""
def sort_emails_by_student_name():
    students_email_name_dict = {}
    for student_email in STUDENTS_EMAIL_DICT:
        student_name = STUDENTS_EMAIL_DICT[student_email].get('nom')
        student_name_normalized = strip_accents(student_name)
        students_email_name_dict[student_name_normalized] = student_email

    sorted_student_normalized_names_list = sorted([strip_accents(STUDENTS_EMAIL_DICT[student_email].get('nom'))
                                                  for student_email
                                                  in STUDENTS_EMAIL_DICT])

    sorted_student_emails = [students_email_name_dict.get(student_name_normalized) for student_name_normalized
                             in sorted_student_normalized_names_list]

    return sorted_student_emails


"""
Adds every student email and name to the STUDENTS_EMAIL_DICT constant
"""
def get_students(grades_folder):
    for file_path in collect_grades_files(grades_folder):
        with open(file_path, 'r', encoding='utf-8') as moodle_grades:
            moodle_grades_reader = csv.reader(moodle_grades, delimiter=',')
            next(moodle_grades_reader)

            email_column = get_column_index_in_csv(file_path, 'Adreça electrònica')
            name_column = get_column_index_in_csv(file_path, 'Nom')
            surname_column = get_column_index_in_csv(file_path, 'Cognoms')

            for row in moodle_grades_reader:
                student_email = row[email_column]
                if student_email:
                    add_student_email(student_email)
                    name = row[name_column]
                    surname = row[surname_column]
                    add_student_name(student_email, name, surname)


"""
Adds every exercise to the STUDENTS_EMAIL_DICT and EXERCISES_LIST constants
"""
def get_exercises(grades_folder):
    for file_path in collect_grades_files(grades_folder):
        exercise = get_exercise_name(file_path)
        EXERCISES_LIST.append(exercise)
        for student_email in STUDENTS_EMAIL_DICT:
            STUDENTS_EMAIL_DICT[student_email][exercise] = 0.00
    
    EXERCISES_LIST.sort()


"""
Adds every student grade to the STUDENTS_EMAIL_DICT constant
"""
def get_grades(grades_folder):
    for file_path in collect_grades_files(grades_folder):
        with open(file_path, 'r', encoding='utf-8') as moodle_grades:
            moodle_grades_reader = csv.reader(moodle_grades, delimiter=',')
            next(moodle_grades_reader)

            email_column = get_column_index_in_csv(file_path, 'Adreça electrònica')
            grade_column = get_column_index_in_csv(file_path, 'Qualificació')
            
            exercise = get_exercise_name(file_path)

            for row in moodle_grades_reader:
                student_email = row[email_column]
                if student_email:
                    grade_string = row[grade_column]
                    add_grade(student_email, exercise, grade_string)


"""
Returns the complete path of the grades file
"""
def get_file_path(file):
    return os.path.join(DOWNLOADED_GRADES_FOLDER, file)


"""
Adds the student email to the STUDENTS_EMAIL_DICT constant
"""
def add_student_email(student_email):
    if student_email not in STUDENTS_EMAIL_DICT:
        STUDENTS_EMAIL_DICT[student_email] = {}


"""
Adds the student name to the email in the STUDENTS_EMAIL_DICT constant
"""
def add_student_name(student_email, name, surname):
    STUDENTS_EMAIL_DICT[student_email]['nom'] = surname + ", " + name


"""
Adds the grade to the indicated exercise and student email in the STUDENTS_EMAIL_DICT constant
"""
def add_grade(student_email, exercise, comma_separated_grade_string):
    grade = convert_comma_separated_grade_to_float(comma_separated_grade_string)
    if STUDENTS_EMAIL_DICT[student_email].get(exercise) < grade:
        STUDENTS_EMAIL_DICT[student_email][exercise] = grade


"""
Generates a CSV file with every student sorted by the name, containing his/her email, name and exercise's grades
"""
def generate_result_file():
    with open(RESULT_FILE, 'w', newline='', encoding='utf-8') as result:
        result_writer = csv.writer(result)

        exercises_list_header = [exercise for exercise in EXERCISES_LIST]
        result_writer.writerow(["Correu electrònic"] + ['Nom'] + exercises_list_header)
        
        for student_email in sort_emails_by_student_name():
            student_name = STUDENTS_EMAIL_DICT[student_email].get('nom')
            student_grades_list = [convert_float_to_comma_separated_grade(STUDENTS_EMAIL_DICT[student_email].get(exercise))
                                   for exercise
                                   in EXERCISES_LIST]
            result_writer.writerow([student_email] + [student_name] + student_grades_list)


if __name__ == "__main__":
    get_students(DOWNLOADED_GRADES_FOLDER)
    get_exercises(DOWNLOADED_GRADES_FOLDER)
    get_grades(DOWNLOADED_GRADES_FOLDER)
    generate_result_file()
