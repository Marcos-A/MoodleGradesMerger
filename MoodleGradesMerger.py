#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

"""
MoodleGradesMerger.py
Returns a CSV file with every student sorted by the name, containing his/her email, name and exercise's grades
from a collection of CSV grade files downloaded from Moodle.
Indicate the folder with the Moodle downloaded grade files as an argument when running the script.
In case a percent is indicated, for every exercise this percent is assigned to the maximum achieved grade,
while the rest is distributed between the other grades. Otherwise for every exercise only the highest grade is preserved.
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
EXERCISES_DICT = {}
STUDENTS_EMAIL_DICT = {}
RESULT_FILE = 'result.csv'
ONLY_BETTER_QUALIFICATION_PREVAILS = True
HIGHER_QUALIFICATION_PERCENT = 0

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
Returns the name of the exercise based on the grades file name
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
                    add_student_exercises_dict(student_email)


"""
Adds every exercise to the STUDENTS_EMAIL_DICT and EXERCISES_DICT constants
"""
def get_exercises(grades_folder):
    for file_path in collect_grades_files(grades_folder):
        exercise = get_exercise_name(file_path)
        EXERCISES_DICT[exercise] = 1
        for student_email in STUDENTS_EMAIL_DICT:
            if ONLY_BETTER_QUALIFICATION_PREVAILS is True:
                STUDENTS_EMAIL_DICT[student_email]['exercises'][exercise] = 0.00
            else:
                STUDENTS_EMAIL_DICT[student_email]['exercises'][exercise] = ()
    

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
Adds an exercises dict to the email in the STUDENTS_EMAIL_DICT constant
"""
def add_student_exercises_dict(student_email):
    STUDENTS_EMAIL_DICT[student_email]['exercises'] = {}

"""
Adds the grade to the indicated exercise and student email in the STUDENTS_EMAIL_DICT constant
and updates the EXERCISES_DICT constant
"""
def add_grade(student_email, exercise, comma_separated_grade_string):
    grade = convert_comma_separated_grade_to_float(comma_separated_grade_string)
    if ONLY_BETTER_QUALIFICATION_PREVAILS is True:
        if grade > STUDENTS_EMAIL_DICT[student_email]['exercises'][exercise]:
            STUDENTS_EMAIL_DICT[student_email]['exercises'][exercise] = grade
    else:
        STUDENTS_EMAIL_DICT[student_email]['exercises'][exercise] += (grade,)
        if EXERCISES_DICT[exercise] < len(STUDENTS_EMAIL_DICT[student_email]['exercises'][exercise]):
            EXERCISES_DICT[exercise] = len(STUDENTS_EMAIL_DICT[student_email]['exercises'][exercise])


"""
Generates a CSV file with every student sorted by the name, containing his/her email, name and exercise's grades
"""
def generate_result_file():
    with open(RESULT_FILE, 'w', newline='', encoding='utf-8') as result:
        result_writer = csv.writer(result)

        sorted_exercises_dict_keys = sorted(EXERCISES_DICT.keys(), key=lambda x:x)

        # Write headers
        if ONLY_BETTER_QUALIFICATION_PREVAILS is True:
            exercises_list_header = [exercise for exercise in sorted_exercises_dict_keys]
            result_writer.writerow(["Correu electrònic"] + ['Nom'] + exercises_list_header)

        else:
            exercises_list_header = []
            exercises_list_subheader = ["",""]
            # Append empty spaces for email and name positions
            for exercise in sorted_exercises_dict_keys:
                if EXERCISES_DICT[exercise] == 1:
                    exercises_list_header.append(exercise)
                    exercises_list_subheader.append("intent 1")
                else:
                    attemps = EXERCISES_DICT[exercise]
                    exercises_list_header.append(exercise)
                    exercises_list_subheader.append("intent 1")
                    i = 2
                    while i <= attemps:
                        exercises_list_header.append("")
                        exercises_list_subheader.append("intent " + str(i))
                        i += 1
                    exercises_list_header.append("")
                    exercises_list_subheader.append("total")
            result_writer.writerow(["Correu electrònic"] + ['Nom'] + exercises_list_header)
            result_writer.writerow(exercises_list_subheader)
        
        # Write students' grades
        for student_email in sort_emails_by_student_name():
            student_name = STUDENTS_EMAIL_DICT[student_email].get('nom')

            if ONLY_BETTER_QUALIFICATION_PREVAILS is True:
                student_grades_list = [convert_float_to_comma_separated_grade(STUDENTS_EMAIL_DICT[student_email]['exercises'].get(exercise))
                                       for exercise
                                       in sorted_exercises_dict_keys]
                result_writer.writerow([student_email] + [student_name] + student_grades_list)

            else:
                # Append empty spaces for email and name positions
                grades_percents_list = ["",""]
                student_grades_list = []
                for exercise in sorted_exercises_dict_keys:
                    if EXERCISES_DICT[exercise] == 1:
                        student_grades_list.append(STUDENTS_EMAIL_DICT[student_email]['exercises'].get(exercise)[0])
                        grades_percents_list.append("")
                    else:
                        exercise_qualifications = []
                        for qualification in STUDENTS_EMAIL_DICT[student_email]['exercises'].get(exercise):
                            student_grades_list.append(qualification)
                            exercise_qualifications.append(qualification)
                        total_qualification = obtain_total_qualification_from_multiple_grades_and_percents_distribution(
                                                                                exercise_qualifications)
                        student_grades_list.append(total_qualification)
                student_grades_list = [convert_float_to_comma_separated_grade(grade) for grade in student_grades_list]
                result_writer.writerow([student_email] + [student_name] + student_grades_list)


"""
Calculates total grade when ONLY_BETTER_QUALIFICATION_PREVAILS is set to False, assigning
the HIGHER_QUALIFICATION_PERCENT constant to the maximum grade, and distributing the
remaning percent between the rest of the grades. Grades not greater than zero are discarded.
In case every grade is zero but for one (for instace, when only a single attempt was made) the single
grade greater than zero will prevail.
"""
def obtain_total_qualification_from_multiple_grades_and_percents_distribution(exercise_grades):
    max_grade = max(exercise_grades)
    max_grade_index = exercise_grades.index(max(exercise_grades))
    
    total_qualification = max_grade * HIGHER_QUALIFICATION_PERCENT
    qualifications_except_max_percent_value = (1 - HIGHER_QUALIFICATION_PERCENT) / (len(exercise_grades)-1)
    
    exercise_grades.pop(max_grade_index)
    grades_except_max = exercise_grades
    # If a single attempt was made or every attempt is zero but one, the only attempt with a grade greater than zero prevails
    if all(grade == 0 for grade in grades_except_max):
        total_qualification = max_grade
    else:
        total_qualification = max_grade * HIGHER_QUALIFICATION_PERCENT
        # Grades with a zero are discarded
        grades_except_max = [grade for grade in grades_except_max if grade > 0]
        qualifications_except_max_percent_value = (1 - HIGHER_QUALIFICATION_PERCENT) / len(grades_except_max)
        for qualification in grades_except_max:
            total_qualification += qualification * qualifications_except_max_percent_value

    return total_qualification


"""
Adds a zero for every missing grade in the STUDENDTS_EMAIL_DICT constant
"""
def add_missing_grades():
    for student_email in STUDENTS_EMAIL_DICT.keys():
        for exercise in STUDENTS_EMAIL_DICT[student_email]['exercises'].keys():
            exercise_attemps = EXERCISES_DICT.get(exercise)
            while(len(STUDENTS_EMAIL_DICT[student_email]['exercises'][exercise]) < exercise_attemps):
                STUDENTS_EMAIL_DICT[student_email]['exercises'][exercise] += (0.00,)


if __name__ == "__main__":
    if len(argv) > 2:
        ONLY_BETTER_QUALIFICATION_PREVAILS = False
        HIGHER_QUALIFICATION_PERCENT = float(argv[2])
    get_students(DOWNLOADED_GRADES_FOLDER)
    get_exercises(DOWNLOADED_GRADES_FOLDER)
    get_grades(DOWNLOADED_GRADES_FOLDER)
    if ONLY_BETTER_QUALIFICATION_PREVAILS is False:
        add_missing_grades()
    generate_result_file()
