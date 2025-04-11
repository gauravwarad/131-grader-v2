# this code is to be run on linux machine with proper g++ setup.

# part 2:
# in ./hw2_submissions, there are folders for each student.
'''
for each student in submissions/studentlist.txt (list of students with complete submissions)
  get the student folder (named studentname in the submissions folder)
  paste all student files to c++ development root/sourcecode/
  cd to that folder
  run ../Build.sh and such that it opens up terminal window
  wait for my input in code cmd
    if I give go ahead (press y):
      execute ./project_g++ similar to previous such that a terminal window opens up.
      I will verify execution in terminal and give grades
      wait for my input
      write down the given grades next to the student in the studentlist.txt
      delete the student files from the sourcecode folder.
      delete ./project_g++ and ./project_clang++ if they are present in the folder.
    else if i press n or anything else:
      skip that student, write 0 as grade next to the student in the studentlist.txt
      move on to the next student on the list....

'''



import os
import shutil
import subprocess
import time

SUBMISSIONS_DIR = 'hw2_submissions'
SOURCECODE_DIR = 'C++ Development Root/SourceCode'
STUDENT_LIST_FILE = os.path.join(SUBMISSIONS_DIR, 'completed_students.txt')
BUILD_SCRIPT = '../Build.sh'
EXECUTABLES = ['./project_g++', './project_clang++']

def open_terminal_and_run(command, cwd):
    # Open a new terminal window and run a command there
    # subprocess.Popen(
    #     ['gnome-terminal', '--', 'bash', '-c', f'cd "{cwd}" && {command}; exec bash'],
    #     stdout=subprocess.DEVNULL,
    #     stderr=subprocess.DEVNULL
    # )
    old_cwd = os.getcwd()  # Save current directory
    try:
        os.chdir(cwd)
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"Command was: {e.cmd}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        os.chdir(old_cwd)  # Restore directory

def clean_source_folder():
    # Remove all files in SOURCECODE_DIR
    for filename in os.listdir(SOURCECODE_DIR):
        file_path = os.path.join(SOURCECODE_DIR, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
# only remove pasted student files.
def delete_student_files(copied_files):
    for f in copied_files:
        path = os.path.join(SOURCECODE_DIR, f)
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
def delete_executables():
    for exe in EXECUTABLES:
        exe_path = os.path.join(SOURCECODE_DIR, exe)
        if os.path.exists(exe_path):
            os.remove(exe_path)

def main():
    # Read student names
    with open(STUDENT_LIST_FILE, 'r') as f:
        students = [line.strip() for line in f.readlines()]

    updated_students = []

    for student in students:
        print(f"\nProcessing student: {student}")

        student_folder = os.path.join(SUBMISSIONS_DIR, student)

        if not os.path.isdir(student_folder):
            print(f"Warning: Folder for {student} not found. Skipping.")
            updated_students.append(f"{student},0")
            continue

        # Copy files to sourcecode
        # clean_source_folder()
        copied_files = []
        for item in os.listdir(student_folder):
            s = os.path.join(student_folder, item)
            d = os.path.join(SOURCECODE_DIR, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
            copied_files.append(item)

        # Build project
        print(f"Building project for {student}...")
        open_terminal_and_run(BUILD_SCRIPT, SOURCECODE_DIR)
        input("Press Enter after build is complete...")

        proceed = input(f"Do you want to run {student}'s project? (y/n): ").strip().lower()

        if proceed == 'y':
            # Run project
            open_terminal_and_run('./project_g++', SOURCECODE_DIR)
            input("Press Enter after verifying the project...")

            # Get grade
            grade = input(f"Enter grade for {student}: ").strip()
            updated_students.append(f"{student},{grade}")

        else:
            print(f"Skipping {student}. Assigning grade 0.")
            updated_students.append(f"{student},0")

        # Clean up
        # clean_source_folder()
        delete_student_files(copied_files)
        delete_executables()

    # Write grades back to the txt
    graded = os.path.join(SUBMISSIONS_DIR, "graded_students.txt")
    with open(graded, 'w') as f:
        for entry in updated_students:
            f.write(entry + '\n')

    print("\nGrading complete!")

if __name__ == "__main__":
    main()
