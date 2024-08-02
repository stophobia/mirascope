"""Tests the `_utils.format_template` module."""

from unittest.mock import MagicMock, patch

from mirascope.core.base._utils._format_template import format_template


@patch(
    "mirascope.core.base._utils._format_template.get_template_values",
    new_callable=MagicMock,
)
@patch(
    "mirascope.core.base._utils._format_template.get_template_variables",
    new_callable=MagicMock,
)
def test_format_template(
    mock_get_template_variables: MagicMock, mock_get_template_values: MagicMock
) -> None:
    """Tests the `format_template` function."""
    mock_get_template_variables.return_value = [("genre", None)]
    attrs = {"genre": "fantasy"}
    mock_get_template_values.return_value = attrs
    template = """
    Recommend a {genre} book.
    
    """
    formatted_template = format_template(template, attrs)
    assert formatted_template == "Recommend a fantasy book."
    mock_get_template_variables.assert_called_once_with(
        "Recommend a {genre} book.", True
    )
    mock_get_template_values.assert_called_once_with([("genre", None)], attrs)
