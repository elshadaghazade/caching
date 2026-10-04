"""Send transformed string lists to the service and save the response."""

import sys, time
from typing import Annotated, Optional, TypedDict

import httpx
import typer

from cli.io import read_payload, write_output
from cli.settings import CliSettings

app = typer.Typer(add_completion=False)

class PerfResult(TypedDict):
    id: int
    elapsed: float


@app.command()
def main(
    host: Annotated[str, typer.Option(help="Host URL")],
    repeat: Annotated[int, typer.Option(help="Number of iterations", min=1)],
    input_: Annotated[
        str, typer.Option("--input", help='Input file ("-" for stdin)')
    ] = "-",
    json_body: Annotated[
        Optional[str],
        typer.Option("--json", help="input argument in json form (properly escaped)"),
    ] = None,
    output: Annotated[
        str, typer.Option("--output", help='output file ("-" for stdout)')
    ] = "-",
) -> None:
    settings = CliSettings(
        host=host,
        repeat=repeat,
        input=input_,
        json=json_body,
        output=output,
    )

    body = read_payload(settings)
    responses: list[PerfResult] = []

    with httpx.Client(base_url=settings.host, timeout=60.0) as client_:
        for _ in range(settings.repeat):
            t1 = time.perf_counter()
            response = client_.post("/payload", json=body)
            response.raise_for_status()
            t2 = time.perf_counter()
            resp = response.json()
            payload: PerfResult = {
                "id": resp["id"],
                "elapsed": t2 - t1
            }
            responses.append(payload)

    if len(responses) == 1:
        write_output(settings, responses[0])
    else:
        write_output(settings, responses)


if __name__ == "__main__":
    sys.exit(app())