# what this script does?
# it looks for specific files that I want to grade and saves it in a student named folder.

import os
import shutil
import re
import zipfile

# Set this to your submissions folder
submissions_folder = "./hw2_submissions"  # <- Update this
temp_extract_folder = os.path.join(submissions_folder, "__temp_extracted__")

# Files to look for
valid_filenames = ["main.cpp", "GroceryList.cpp"]
valid_filenames_set = set(valid_filenames)

# Dynamically create patterns based on valid filenames
valid_basenames = [os.path.splitext(f)[0] for f in valid_filenames]
valid_basenames_pattern = "|".join(re.escape(name) for name in valid_basenames)

cpp_pattern = re.compile(rf'^([a-zA-Z0-9]+)(?:_LATE)?_[^_]+_[^_]+_({valid_basenames_pattern})(?:Finished)?(?:-\d+)?\.cpp$')
zip_pattern = re.compile(r'^([a-zA-Z0-9]+)(?:_LATE)?_[^_]+_[^_]+.*\.zip$')

# Tracking
student_submissions = {}

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def move_valid_file(src_path, student_dir, base_name, student_name):
    dst_path = os.path.join(student_dir, base_name)
    shutil.copy2(src_path, dst_path)
    student_submissions[student_name]["submitted"].add(base_name)
    print(f"Saved: {dst_path}")

def process_zip(file_path, student_name):
    extract_path = os.path.join(temp_extract_folder, student_name)
    ensure_dir(extract_path)

    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile:
        print(f"Bad zip file: {file_path}")
        student_submissions[student_name]["errors"].append("Bad zip file")
        return

    for root, _, files in os.walk(extract_path):
        for file in files:
            if file in valid_filenames_set:
                full_src = os.path.join(root, file)
                student_dir = os.path.join(submissions_folder, student_name)
                ensure_dir(student_dir)
                move_valid_file(full_src, student_dir, file, student_name)

    os.remove(file_path)  # Delete zip after processing

def process_cpp(file, match):
    student_name = match.group(1)
    base_name = match.group(2) + ".cpp"
    src_path = os.path.join(submissions_folder, file)
    student_dir = os.path.join(submissions_folder, student_name)
    ensure_dir(student_dir)

    move_valid_file(src_path, student_dir, base_name, student_name)
    os.remove(src_path)  # Remove original file

# Make sure temp folder is clean
if os.path.exists(temp_extract_folder):
    shutil.rmtree(temp_extract_folder)
ensure_dir(temp_extract_folder)

# Main loop
for file in os.listdir(submissions_folder):
    full_path = os.path.join(submissions_folder, file)
    if os.path.isfile(full_path):
        cpp_match = cpp_pattern.match(file)
        zip_match = zip_pattern.match(file)

        if cpp_match:
            student_name = cpp_match.group(1)
            student_submissions.setdefault(student_name, {"submitted": set(), "errors": []})
            process_cpp(file, cpp_match)

        elif zip_match:
            student_name = zip_match.group(1)
            student_submissions.setdefault(student_name, {"submitted": set(), "errors": []})
            process_zip(full_path, student_name)

        else:
            os.remove(full_path)  # Delete invalid files

# Clean up temp extracted folder
shutil.rmtree(temp_extract_folder)

# Generate the log
log_path = os.path.join(submissions_folder, "submission_log.txt")
with open(log_path, "w") as log:
    for student, data in sorted(student_submissions.items()):
        submitted = data["submitted"]
        errors = data["errors"]
        log.write(f"Student: {student}\n")
        log.write(f"  Submitted files: {', '.join(submitted) if submitted else 'None'}\n")
        missing = [f for f in valid_filenames if f not in submitted]
        if missing:
            log.write(f"Missing: {', '.join(missing)}\n")
        if errors:
            log.write(f"Errors: {', '.join(errors)}\n")
        log.write("\n")

print(f"\nDone! Log saved to: {log_path}")

# saving the student names with complete submissions
students = os.path.join(submissions_folder, "completed_students.txt")
with open(students, "w") as student:
    for s, data in sorted(student_submissions.items()):
        submitted = data["submitted"]
        errors = data["errors"]
        missing = [f for f in valid_filenames if f not in submitted]
        if not missing:
            student.write(f"{s}\n")
print("\nstudents list saved")
