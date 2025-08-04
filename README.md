# 131-grader-v2
> yup. ever tried to automate a 5 hour task but spent 25 hours on it? This is it.

A semi-automated grading pipeline for C++ assignments, designed to streamline the evaluation process by organizing submissions, compiling code, and leveraging a local AI for code analysis.

## Features

- **Automated Submission Handling:** Automatically processes and organizes student submissions from `.zip` archives and individual `.cpp` files.
- **Structured File Organization:** Creates a clean, per-student directory structure for easy management.
- **Interactive Build & Run:** A guided process to compile and run student projects on a Linux environment.
- **AI-Powered Grading:** For non-compiling or non-running code, it uses a local Large Language Model (LLM) to grade specific `// TO-DO` sections against an ideal solution.
- **Detailed Logging:** Generates logs for submission status, missing files, and final grades.

## Workflow

The grading process is a multi-stage pipeline, executed in a specific order:

1.  **File Pre-processing (`filehandling.py`):**
    - Cleans and validates student submission files.
    - Extracts required files (`main.cpp`, `GroceryItemDatabase.cpp`, etc.).
    - Organizes them into individual student folders.
    - Generates logs (`submission_log.txt`, `completed_students.txt`, `incomplete_students.txt`).

2.  **Manual Evaluation (`linux.py`):**
    - Designed to be run on a Linux machine with `g++`.
    - Iterates through students with complete submissions.
    - Copies student files into a dedicated C++ development environment.
    - Runs a `Build.sh` script to compile the code.
    - Prompts the grader to manually execute the compiled program and provide a preliminary grade based on runtime performance.

3.  **AI-Assisted Grading (`mac.py`):**
    - Designed to be run on a machine with access to a local LLM (e.g., Ollama).
    - Processes students who received a `0` in the previous step.
    - Compares `// TO-DO` code blocks from the student's files with a provided ideal solution.
    - Sends the code pairs to the LLM for grading based on a defined rubric.
    - Aggregates scores and generates final reports (`total_scores.txt`, `grading_comments.txt`).

## Technologies Used

- **Backend:** Python
- **AI Integration:** Ollama with `llama3.1:8b`
- **Build Process:** `g++`, Shell Scripting

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd 131-grader-v2
    ```
2.  **Project Structure:**
    - Place student submissions in a `submissions/` directory.
    - Place the ideal solution files in an `ideal_solution/` directory.
    - Configure your C++ development environment in a `C++ Development Root/` directory.
3.  **Python Dependencies:**
    - The project requires `ollama` and `pydantic`. Install them using pip:
    ```bash
    pip install ollama pydantic
    ```

4.  **AI Setup:**
    - Ensure you have Ollama installed and running.
    - Pull the required model: `ollama pull llama3.1:8b`

## Usage

Execute the scripts in the following order:

1.  **Process submissions:**
    ```bash
    python filehandling.py
    ```
2.  **Manually grade runnable projects:**
    ```bash
    python linux.py
    ```
3.  **Run AI grading for remaining projects:**
    ```bash
    python mac.py
    ```
