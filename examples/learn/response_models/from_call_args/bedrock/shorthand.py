from typing import Annotated

from mirascope.core import FromCallArgs, bedrock
from pydantic import BaseModel, model_validator
from typing_extensions import Self


class Book(BaseModel):
    title: str
    author: str


class Books(BaseModel):
    texts: Annotated[list[str], FromCallArgs()]
    books: list[Book]

    @model_validator(mode="after")
    def validate_output_length(self) -> Self:
        if len(self.texts) != len(self.books):
            raise ValueError("length mismatch...")
        return self


@bedrock.call("anthropic.claude-3-haiku-20240307-v1:0", response_model=Books)
def extract_books(texts: list[str]) -> str:
    return f"Extract the books from these texts: {texts}"


texts = [
    "The Name of the Wind by Patrick Rothfuss",
    "Mistborn: The Final Empire by Brandon Sanderson",
]
print(extract_books(texts))
# Output: texts=['The Name of the Wind by Patrick Rothfuss', 'Mistborn: The Final Empire by Brandon Sanderson'] books=[Book(title='The Name of the Wind', author='Patrick Rothfuss'), Book(title='Mistborn: The Final Empire', author='Brandon Sanderson')]
