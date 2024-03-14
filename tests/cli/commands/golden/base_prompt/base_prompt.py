"""A prompt for recommending movies of a particular genre."""
from mirascope import BasePrompt


class MovieRecommendationPrompt(BasePrompt):
    prompt_template = "Please recommend a list of movies in the {genre} category."

    genre: str
