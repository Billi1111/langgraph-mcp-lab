import asyncio
import json
import sys

from graph import build_graph


async def run_async(national_id: str) -> dict:
    """Use with await in notebooks or other async applications."""
    return await build_graph().ainvoke({"national_id": national_id})


def run(national_id: str) -> dict:
    """Synchronous entry point for ordinary Python scripts."""
    return asyncio.run(run_async(national_id))


if __name__ == "__main__":
	national_id = sys.argv[1] if len(sys.argv) > 1 else "12345678901234"
	print(json.dumps(run(national_id), indent=2))
