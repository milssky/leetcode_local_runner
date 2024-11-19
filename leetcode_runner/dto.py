from pydantic import BaseModel, Field, computed_field


class Snippet(BaseModel):
    lang: str
    lang_slug: str = Field(..., alias='langSlug')
    code: str


class BaseQuestion(BaseModel):
    question_id: int = Field(..., alias='questionId')


class Question(BaseQuestion):
    title: str
    difficulty: str
    content: str
    snippets: list[Snippet] = Field(..., alias='codeSnippets')
    sample_test_case: str = Field(..., alias='sampleTestCase')


class Problem(BaseModel):
    question: Question


class TestQuestion(BaseQuestion):
    test_cases: list[str] = Field(..., alias='exampleTestcaseList')


class Tests(BaseModel):
    question: TestQuestion
