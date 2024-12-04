from asyncio import get_running_loop, wait_for, TimeoutError


def execute_code(code_to_execute):
    safe_globals = {}
    safe_locals = {}

    result = {}


from dotenv import load_dotenv
from os import getenv
from asyncio import get_running_loop, wait_for, TimeoutError

from fastapi import HTTPException
from ..db import Session
from ..db.models import User

load_dotenv()


def execute_code(code_to_execute: str) -> dict:
    safe_globals = {}
    safe_locals = {}

    result = {}

    try:
        exec(code_to_execute, safe_globals, safe_locals)
        result["status"] = "success"
        result["message"] = "Tests passed!"
    except Exception as ex:
        result["status"] = "error"
        result["message"] = f"Failed to execute code: {ex}"

    return result


async def execute_with_timeout(code_to_execute):
    try:
        # TODO: select timeout
        loop = get_running_loop()
        return await wait_for(
            loop.run_in_executor(None, execute_code, code_to_execute), timeout=5
        )
    except TimeoutError:
        return {"status": "error", "message": "Execution timed out"}


async def execute_with_timeout(code_to_execute: str) -> dict:
    try:
        loop = get_running_loop()
        return await wait_for(
            loop.run_in_executor(None, execute_code, code_to_execute),
            timeout=2.0,
            # timeout=float(getenv("MAX_RUNTIME_CODE")),
        )
    except TimeoutError:
        return {"status": "error", "message": "Execution timed out"}
