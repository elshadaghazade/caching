from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class CliSettings(BaseSettings):
    """Validated CLI arguments. Typer parses argv; this model sanitises the result."""

    host: str = Field(..., min_length=1, description="Server URL to send requests to.")
    repeat: int = Field(..., ge=1, description="Number of times to send the request.")
    input: Literal["-"] | str = Field(
        "-", description='Input file path, or "-" to read from stdin.'
    )
    json_body: str | None = Field(
        None, alias="json", description="Inline JSON for the request body (overrides --input)."
    )
    output: Literal["-"] | str = Field(
        "-", description='Output file path, or "-" to write to stdout.'
    )

    model_config = {"populate_by_name": True}