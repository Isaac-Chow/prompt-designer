"""
    This assignment guides you through building a Prompt Designer agent
    that uses Pydantic AI to test different prompting techniques with
    web search (DuckDuckGo), ArXiv, and PubMed search tools.

    Phase 1 - Define Pydantic Models for Structured Outputs
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    In this file you will create the data models that the agent uses
    to return validated, structured responses.
"""


# TODO:
# Phase 1 — Imports
#
# > Import BaseModel and Field from pydantic
# Reference: https://docs.pydantic.dev/latest/concepts/models/
# Reference: https://docs.pydantic.dev/latest/concepts/fields/

# > Import field_validator from pydantic
# Reference: https://docs.pydantic.dev/latest/concepts/validators/#field-validators
#
# > Import Optional from typing
# Reference: https://docs.python.org/3/library/typing.html#typing.Optional
#
# > Import datetime from the datetime module
# Reference: https://docs.python.org/3/library/datetime.html
#
# > Import uuid for generating unique session IDs
# Reference: https://docs.python.org/3/library/uuid.html
# YOUR CODE STARTS HERE
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import uuid
# YOUR CODE ENDS HERE


# TODO:
# Task 1 — Create the SearchResult model
#
# > Create a class called SearchResult that inherits from BaseModel
# Reference: https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage
#
# > Inside the class, create a field called title of type str
# Reference: https://docs.pydantic.dev/latest/concepts/fields/
#
# > Inside the class, create a field called url of type str
# Reference: https://docs.pydantic.dev/latest/concepts/fields/
#
# > Inside the class, create a field called snippet of type str
# Reference: https://docs.pydantic.dev/latest/concepts/fields/
#
# > Inside the class, create a field called source of type str with a default value of "web"
#   This tracks where the result came from: "web", "arxiv", or "pubmed"
# Reference: https://docs.pydantic.dev/latest/concepts/fields/#default-values
#
# > Inside the class, create a __str__ method that returns a formatted string
#   showing the title, url, and snippet in markdown link format
# Reference: https://docs.python.org/3/reference/datamodel.html#object.__str__
# YOUR CODE STARTS HERE
class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source: str = "web"

    def __str__(self) -> str:
        return f"[{self.title}]({self.url}): {self.snippet}"

# YOUR CODE ENDS HERE


# TODO:
# Task 2 — Create the Reference model with URL validation
#
# > Create a class called Reference that inherits from BaseModel
# Reference: https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage
#
# > Inside the class, create a field called title of type str using Field with
#   the description "Title of the source"
# Reference: https://docs.pydantic.dev/latest/concepts/fields/#field-function
#
# > Inside the class, create a field called url of type str using Field with
#   the description "Unique URL of the source"
# Reference: https://docs.pydantic.dev/latest/concepts/fields/#field-function
#
# > Inside the class, create a field called snippet of type Optional[str] using Field
#   with a default of None and description "Relevant excerpt from the source"
# Reference: https://docs.pydantic.dev/latest/concepts/fields/#field-function
#
# > Add a field_validator for the url field that checks the URL starts with
#   "http://" or "https://", and raises a ValueError if it does not
# Reference: https://docs.pydantic.dev/latest/concepts/validators/#field-validators
# YOUR CODE STARTS HERE
class References(BaseModel):
    title: str = Field(..., description="Title of the source")
    url: str = Field(..., description="Unique URL of the source")
    snippet: Optional[str] = Field(None, description="Relevant excerpt from the source")

    @field_validator('url')
    def validate_url(cls, value):
        if not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("URL must start with 'http://' or 'https://'")
        return value

# YOUR CODE ENDS HERE


# TODO:
# Task 3 — Create the AgentResponse model with confidence validation
#
# > Create a class called AgentResponse that inherits from BaseModel
# Reference: https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage
#
# > Inside the class, create a field called `answer` of type str using Field with
#   description "The comprehensive answer to the question"
# Reference: https://docs.pydantic.dev/latest/concepts/fields/#field-function
#
# > Inside the class, create a field called `confidence` of type str using Field with
#   a default of "medium" and description "Confidence level: high, medium, or low"
# Reference: https://docs.pydantic.dev/latest/concepts/fields/#field-function
#
# > Inside the class, create a field called `key_points` of type list[str] using Field
#   with default_factory=list and description "Key takeaways as bullet points"
# Reference: https://docs.pydantic.dev/latest/concepts/fields/#field-function
#
# > Inside the class, create a field called `references` of type list[Reference] using Field
#   with min_length=1 and description "List of unique references with URLs"
# Reference: https://docs.pydantic.dev/latest/concepts/fields/#field-function
#
# > Add a field_validator for the confidence field that normalizes the value to lowercase
#   and defaults to "medium" if the value is not one of "high", "medium", or "low"
# Reference: https://docs.pydantic.dev/latest/concepts/validators/#field-validators
#
# > Add a field_validator for the references field that ensures all URLs are unique
#   by comparing the list of urls to a set of urls, and raises a ValueError if duplicates exist
# Reference: https://docs.pydantic.dev/latest/concepts/validators/#field-validators
# YOUR CODE STARTS HERE
class AgentResponse(BaseModel):
    answer: str = Field(..., description="The comprehensive answer to the question")
    confidence: str = Field("medium", description="Confidence level: high, medium, or low")
    key_points: list[str] = Field(default_factory=list, description="Key takeaways as bullet points")
    references: list[References] = Field(..., min_length=1, description="List of unique references with URLs")

    @field_validator('confidence')
    def validate_confidence(cls, value):
        """Validate confidence of the response"""
        value = value.lower()
        if value not in {"high", "medium", "low"}:
            return "medium"
        return value

    @field_validator('references')
    def validate_unique_references(cls, value):
        """Validate the references generated"""
        urls = [ref.url for ref in value]
        if len(urls) != len(set(urls)):
            raise ValueError("All reference URLs must be unique")
        return value

# YOUR CODE ENDS HERE


# TODO:
# Task 4 — Create the PromptTemplate model
#
# > Create a class called PromptTemplate that inherits from BaseModel
# Reference: https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage
#
# > Inside the class, create fields: name (str), version (str),
#   system_prompt (str), user_template (str), and file_path (str)
# Reference: https://docs.pydantic.dev/latest/concepts/fields/
#
# > Inside the class, create a method called format_user_prompt that takes
#   question (str) and search_results (str) as parameters, and returns a string
#   by calling self.user_template.format(question=question, search_results=search_results)
# Reference: https://docs.python.org/3/library/stdtypes.html#str.format
# YOUR CODE STARTS HERE
class PromptTemplate(BaseModel):
    name: str
    version: str
    system_prompt: str
    user_template: str
    file_path: str

    def format_user_prompt(self, question: str, search_results: str) -> str:
        """Format the user prompt with the given question and search results"""
        return self.user_template.format(question=question, search_results=search_results)

# YOUR CODE ENDS HERE


# TODO:
# Task 5 — Create the QuerySession model to track queries
#
# > Create a class called QuerySession that inherits from BaseModel
# Reference: https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage
#
# > Inside the class, create a field called session_id of type str using Field with
#   a default_factory that generates a short uuid (first 8 characters)
#   Hint: use lambda: str(uuid.uuid4())[:8]
# Reference: https://docs.pydantic.dev/latest/concepts/fields/#field-function
# Reference: https://docs.python.org/3/library/uuid.html#uuid.uuid4
#
# > Inside the class, create the following fields:
#   - question: str
#   - prompt_used: str
#   - model_used: str
#   - timestamp: datetime with default_factory=datetime.now
#   - response: Optional[AgentResponse] with default None
#   - raw_response: Optional[str] with default None
#   - search_results: list[SearchResult] with default_factory=list
#   - execution_time_seconds: Optional[float] with default None
# Reference: https://docs.pydantic.dev/latest/concepts/fields/#field-function
# YOUR CODE STARTS HERE
class QuerySession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    question: str
    prompt_used: str
    model_used: str
    timestamp: datetime = Field(default_factory=datetime.now)
    response: Optional[AgentResponse] = None
    raw_response: Optional[str] = None
    search_results: list[SearchResult] = Field(default_factory=list)
    execution_time_seconds: Optional[float] = None

# YOUR CODE ENDS HERE
