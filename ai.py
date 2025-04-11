from ollama import chat
from pydantic import BaseModel


class GradedTODO(BaseModel):
    grade: int
    comment: str


def grade_todo(student_code, ideal_code):    
    prompt = """
    You are grading a student's solution to a coding assignment.

    Context:
    - This snippet is a part of a larger C++ project.
    - Only evaluate the code block shown below.
    - Grade according to the rubric.

    Rubric (out of 4 points):
    - 5/5: Fully correct and equivalent to the ideal solution.
    - 4/5: Minor errors (e.g., style, small bugs, missing edge cases).
    - 3/5: Logic is mostly correct, but syntax or structure is flawed.
    - 2/4: Attempted with visible effort, but mostly incorrect.
    - 1/4: Very little effort or completely unrelated.
    - 0/4: No attempt.

    Instructions:
    - Grade Leniently.
    - Compare the student’s solution to the ideal one.
    - Grade *only this code block*.
    - Return a JSON object with a `grade` and a short `comment`.

    """

    response = chat(
        messages=[
            {"role": "user", "content": prompt + "ideal code is " + ideal_code + " student code is " + student_code},
        ],
        model="llama3.1:8b",
        format=GradedTODO.model_json_schema(),
    )

    results = GradedTODO.model_validate_json(response.message.content)
    
    return {"grade": results.grade, "comment": results.comment}