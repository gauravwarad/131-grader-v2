# this code is to be run somewhere, where you have access to locally run LLMs.
# or can be configured to make API calls to cloud LLMs.

'''
you know what to do.
for students in studentlist:
		if they scored 0:
			open their folder
			for each file:
				open corresponding ideal solution file
				extract todo sections from solution file and student file
				for each todo section:
					ai_grader()
					save_grade()
				

'''

import os
import shutil
import subprocess
import time
from ai import grade_todo


SUBMISSIONS_DIR = 'hw2_submissions'
IDEALSOLUTION_DIR = 'ideal_solution'
STUDENT_LIST_FILE = os.path.join(SUBMISSIONS_DIR, 'graded_students.txt') # graded students only.
# txt files
# graded_students.txt - with previously graded students
# total_scores.txt - with students and their total scores
# grade_comments.txt - with student names, todo wise grades and comments


def find_todos(file_content):
    todos = []
    start_line = None

    for i, line in enumerate(file_content):
        if "///////////////////////// TO-DO" in line:
            start_line = i
        if "/////////////////////// END-TO-DO" in line and start_line is not None:
            todos.append((start_line, i))
            start_line = None
    print(f"Found TODO sections: {todos}")
    return todos


def main():
    # Read student names
    with open(STUDENT_LIST_FILE, 'r') as f:
        students = [line.strip() for line in f.readlines()]

    # updated_students = []
    total_scores = []
    grading_comments = []
    for row in students:
        student, score = row.split(',')
        score = int(score)
        print(f"\nProcessing student: {student}")
        if score != 0:
            print(f"Skipping {student} as they have already been graded.")
            # updated_students.append({"name": student, "score": score, "message": "Already graded"})
            total_scores.append(f"{student},{score}, Already graded")
            continue
        student_folder = os.path.join(SUBMISSIONS_DIR, student)

        if not os.path.isdir(student_folder):
            print(f"Warning: Folder for {student} not found. Skipping.")
            # updated_students.append({"name": student, "score": 0, "message": "folder not found"})
            total_scores.append(f"{student},0, folder not found")
            continue

        grading_comments.append(f"\n{student}")
        for item in os.listdir(student_folder):
            # for each file in the student folder
            # open corresponding ideal solution file
            # extract todo sections from solution file and student file
            # for each todo section:
            # ai_grader()
            # save_grade()
            with open(os.path.join(student_folder, item), 'r') as f:
                student_code = f.readlines()
            with open(os.path.join(IDEALSOLUTION_DIR, item), 'r') as f:
                ideal_code = f.readlines()
            grading_comments.append(f"{item}")
            student_todos = find_todos(student_code)
            ideal_todos = find_todos(ideal_code)

            if len(student_todos) != len(ideal_todos):
                print(f"Warning: Number of TODO sections do not match for {student} , {item}. Skipping file.")
                # updated_students.append({"name": student, "score": 0, "message": f"TODO sections mismatch for file {item}"})
                print(f"TODO sections mismatch for file {item}")
                grading_comments.append(f"TODO sections mismatch for file {item}")
                continue
            else:
                for i in range(len(student_todos)):
                    student_start, student_end = student_todos[i]
                    ideal_start, ideal_end = ideal_todos[i]

                    student_todo = student_code[student_start:student_end]
                    ideal_todo = ideal_code[ideal_start:ideal_end]
                    print(f"Grading TODO section {i+1} for {student} in {item}:")
                    
                    print(f"\nStudent TODO: \n{"".join(student_todo)}")
                    print(f"\nIdeal TODO: \n{"".join(ideal_todo)}")

                    # Call AI grader here
                    # response = ai_grader(student_todo, ideal_todo)
                    response = grade_todo("".join(student_todo), "".join(ideal_todo))
                    grade = response['grade']
                    comment = response['comment']

                    
                    print(f"Grade: {grade}")
                    print(f"Comment: {comment}")
                    if grade < 3 or grade > 5:
                        what_do_i_say = input("Do you agree? (y/n): ")
                        if what_do_i_say.lower() == "y":
                            # Save grade and comment
                            grading_comments.append(f"TODO {i+1}; grade: {grade}; {comment}")
                            
                        else:
                            new_grade = input("What grade would you give this TODO? (0-4): ")
                            comment = ""
                            grading_comments.append(f"TODO {i+1}; grade: {new_grade}; {comment}")
                            
                    else:
                        grading_comments.append(f"TODO {i+1}; grade: {grade}; {comment}")
                    score += grade

        print(f"Total score for {student}: {score}")
        total_scores.append(f"{student},{score}")

        
    # Write grades back to the txt
    graded = os.path.join(os.getcwd(), "total_scores.txt")
    with open(graded, 'w') as f:
        for entry in total_scores:
            f.write(entry + '\n')

    comments = os.path.join(os.getcwd(), "grading_comments.txt")
    with open(comments, 'w') as f:
        for entry in grading_comments:
            f.write(entry + '\n')

    print("\nGrading complete!")

if __name__ == "__main__":
    main()
