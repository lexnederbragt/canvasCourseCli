import sys
import argparse
from api import get_course, split_url
from collections import Counter
import pandas as pd
from pprint import pprint

test_student = 128521

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Lists the page titles + their full url for a course on Canvas in alphabetical order.",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                      ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The url of the course, ending with the course id", required = True)
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def main(args):
    args = parse_args(args)

    # extract course information from url and get course
    API_URL, course_id, new_folder_name = split_url(args.url, expected = 'url only')
    course =  get_course(API_URL, course_id, args.config_file)

    # ----------------
    # get all assignments in the course
    assignments = course.get_assignments()
    
    assignment_names = [assignment.name for assignment in assignments]
    # add name column to start
    assignment_names.insert(0, 'name')
    # Add assignment names to new dataframe
    grades_table = pd.DataFrame(columns=assignment_names)



    students = course.get_users(enrollment_type=['student'])

    for student in students:
        if student.id == test_student:
            # add student to grades table
            grades_table.loc[student.id] = 0
            # add student name to grades table
            grades_table.loc[student.id, 'name'] = student.name        
            assignment_data = course.get_user_in_a_course_level_assignment_data(test_student)
            # add assignment scores to grades table
            for assignment in assignment_data:
                grades_table.loc[student.id, assignment['title']] = assignment['submission']['score']
            
    # save grades table to csv
    grades_table.to_csv('grades.csv', index=False)
    

    print(grades_table)



    # students = []
    # for assignment in course.get_assignments():
    #     print(assignment.name)
    #     scores = []
    #     for s in assignment.get_submissions():
    #         scores.append(s.score)

    #         if s.user_id == test_student:
    #             user = course.get_user(s.user_id)
    #             print(s.user_id, user.name, s.score)
    #     print(Counter(scores))

if __name__ == "__main__":
    main(sys.argv[1:])
