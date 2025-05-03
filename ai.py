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

    Rubric (out of 7 points):
    - 7/7: Fully correct and equivalent to the ideal solution.
    - 6/7: Minor errors (e.g. small bugs, missing edge cases).
    - 5/7: Logic is mostly correct, but syntax or structure is flawed.
    - 3/7: Attempted with visible effort, but mostly incorrect.
    - 2/7: Very little effort or completely unrelated.
    - 0/7: No attempt.

    Instructions:
    - Grade Leniently, Assume the rest of the project fills in the context unless clearly contradicted.
    - Compare the student’s solution to the ideal one.
    - Grade *only this code block*.
    - Ignore cosmetic issues. Focus on logic and structure.
    - Return a JSON object with a `grade` and a short `comment`, comment should be a short phrase (e.g. "missing base case", "incorrect logic", etc.).

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