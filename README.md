# 131-grader-v2
yup. ever tried to automate a 5 hour task but spent 25 hours on it? This is it.

how it works:
  1. run filehandling.py to clean the student submissions. A new folder for each student will be created.
  2. in filehandling.py, keep an eye on the valid files and the submission directory
  3. place files which are not to be graded in c++ development root (the rest of the files .hpp, tests, etc)
  4. then run linux.py (copy ideal solution to ideal_solution folder; other files to c++ dev root as instructed)
  5. send everything over to the mac (because that's where the local LLM is)
  6. run mac.py