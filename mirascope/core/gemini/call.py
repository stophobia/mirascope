"""The `gemini_call` decorator for functions as LLM calls."""

from functools import partial
from typing import (
    Callable,
    Iterable,
    Literal,
    ParamSpec,
    TypeVar,
    Unpack,
    overload,
)

from google.generativeai.types import GenerateContentResponse  # type: ignore
from pydantic import BaseModel

from ..base import BaseTool, _utils
from ._create import create_decorator
from ._extract import extract_decorator
from ._stream import GeminiStream, stream_decorator
from ._structured_stream import structured_stream_decorator
from .call_params import GeminiCallParams
from .call_response import GeminiCallResponse
from .call_response_chunk import GeminiCallResponseChunk
from .function_return import GeminiCallFunctionReturn

_P = ParamSpec("_P")
_ResponseModelT = TypeVar("_ResponseModelT", bound=BaseModel | _utils.BaseType)
_ParsedOutputT = TypeVar("_ParsedOutputT")


@overload
def gemini_call(
    model: str,
    *,
    stream: Literal[False] = False,
    tools: list[type[BaseTool] | Callable] | None = None,
    response_model: None = None,
    output_parser: None = None,
    **call_params: Unpack[GeminiCallParams],
) -> Callable[
    [Callable[_P, GeminiCallFunctionReturn]],
    Callable[_P, GeminiCallResponse],
]: ...  # pragma: no cover


@overload
def gemini_call(
    model: str,
    *,
    stream: Literal[False] = False,
    tools: list[type[BaseTool] | Callable] | None = None,
    response_model: type[_ResponseModelT],
    output_parser: None = None,
    **call_params: Unpack[GeminiCallParams],
) -> Callable[
    [Callable[_P, GeminiCallFunctionReturn]],
    Callable[_P, _ResponseModelT],
]: ...  # pragma: no cover


@overload
def gemini_call(
    model: str,
    *,
    stream: Literal[True],
    tools: list[type[BaseTool] | Callable] | None = None,
    response_model: None = None,
    output_parser: None = None,
    **call_params: Unpack[GeminiCallParams],
) -> Callable[
    [Callable[_P, GeminiCallFunctionReturn]],
    Callable[_P, GeminiStream[GenerateContentResponse]],
]: ...  # pragma: no cover


@overload
def gemini_call(
    model: str,
    *,
    stream: Literal[True],
    tools: list[type[BaseTool] | Callable] | None = None,
    response_model: type[_ResponseModelT],
    output_parser: None = None,
    **call_params: Unpack[GeminiCallParams],
) -> Callable[
    [Callable[_P, GeminiCallFunctionReturn]],
    Callable[_P, Iterable[_ResponseModelT]],
]: ...  # pragma: no cover


def gemini_call(
    model: str,
    *,
    stream: bool = False,
    tools: list[type[BaseTool] | Callable] | None = None,
    response_model: type[_ResponseModelT] | None = None,
    output_parser: Callable[[GeminiCallResponse], _ParsedOutputT]
    | Callable[[GeminiCallResponseChunk], _ParsedOutputT]
    | None = None,
    **call_params: Unpack[GeminiCallParams],
) -> Callable[
    [Callable[_P, GeminiCallFunctionReturn]],
    Callable[
        _P,
        GeminiCallResponse
        | GeminiStream[GenerateContentResponse | _ParsedOutputT]
        | _ResponseModelT
        | Iterable[_ResponseModelT],
    ],
]:
    '''A decorator for calling the Gemini API with a typed function.

    This decorator is used to wrap a typed function that calls the Gemini API. It parses
    the docstring of the wrapped function as the messages array and templates the input
    arguments for the function into each message's template.

    Example:

    ```python
    @gemini_call(model="gemini-1.5-pro")
    def recommend_book(genre: str):
        """Recommend a {genre} book."""

    response = recommend_book("fantasy")
    ```

    Args:
        model: The Gemini model to use in the API call.
        stream: Whether to stream the response from the API call.
        tools: The tools to use in the Gemini API call.
        **call_params: The `GeminiCallParams` call parameters to use in the API call.

    Returns:
        The decorator for turning a typed function into an Gemini API call.
    '''

    if response_model:
        if stream:
            return partial(
                structured_stream_decorator,
                model=model,
                response_model=response_model,
                call_params=call_params,
            )
        else:
            return partial(
                extract_decorator,
                model=model,
                response_model=response_model,
                call_params=call_params,
            )
    if stream:
        return partial(
            stream_decorator,
            model=model,
            tools=tools,
            output_parser=output_parser,
            call_params=call_params,
        )
    return partial(
        create_decorator,
        model=model,
        tools=tools,
        output_parser=output_parser,
        call_params=call_params,
    )
