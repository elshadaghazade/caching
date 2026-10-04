import json
import sys
from pathlib import Path

from cli.settings import CliSettings


def read_payload(settings: CliSettings) -> dict[str, str | int]:
    """Return the JSON request body parsed from --json or --input."""
    if settings.json_body is not None:
        return json.loads(settings.json_body)

    raw = _read(settings.input)
    return json.loads(raw)


def write_output(settings: CliSettings, payload: object) -> None:
    """Serialize `payload` as JSON and write to --output."""
    serialized = json.dumps(
        payload,
        indent=2
    )
    _write(settings.output, serialized)


def _read(source: str) -> str:
    if source == "-":
        return sys.stdin.read()
    return Path(source).read_text()


def _write(target: str, data: str) -> None:
    if target == "-":
        sys.stdout.write(data)
        if not data.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.flush()
        return
    Path(target).write_text(data)