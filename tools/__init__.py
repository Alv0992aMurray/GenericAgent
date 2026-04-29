"""Tools package for GenericAgent.

This package provides built-in tools that the agent can use during execution.
Each tool module should define a `schema` dict (JSON Schema for the LLM) and
a callable that implements the tool logic.
"""

from pathlib import Path
import importlib
import json
import os

# Directory containing tool modules
TOOLS_DIR = Path(__file__).parent

# Set to True to see which tools are loaded at startup (useful during development)
DEBUG_TOOL_LOADING = os.environ.get("GENERIC_AGENT_DEBUG_TOOLS", "").lower() in ("1", "true", "yes")


def discover_tools(tools_dir: Path = TOOLS_DIR) -> dict:
    """Discover and load all tool modules in the tools directory.

    Each tool module must expose:
        - `schema` (dict): JSON Schema object describing the tool for the LLM.
        - `run` (callable): Function that executes the tool.

    Returns:
        dict mapping tool name -> {"schema": ..., "run": ...}
    """
    tools = {}
    for path in sorted(tools_dir.glob("*.py")):
        if path.stem.startswith("_"):
            continue  # skip __init__ and private modules
        module_name = f"tools.{path.stem}"
        try:
            module = importlib.import_module(module_name)
        except ImportError as exc:
            print(f"[tools] Warning: could not import {module_name}: {exc}")
            continue

        if not hasattr(module, "schema") or not hasattr(module, "run"):
            print(f"[tools] Warning: {module_name} missing 'schema' or 'run', skipping.")
            continue

        tool_name = module.schema.get("name") or path.stem
        tools[tool_name] = {
            "schema": module.schema,
            "run": module.run,
        }
        if DEBUG_TOOL_LOADING:
            print(f"[tools] Loaded tool: {tool_name} (from {path.name})")

    if DEBUG_TOOL_LOADING:
        print(f"[tools] Total tools loaded: {len(tools)}")

    return tools


def load_schemas(tools: dict) -> list:
    """Extract a list of JSON Schema dicts from the tools mapping.

    Args:
        tools: Mapping returned by :func:`discover_tools`.

    Returns:
        List of schema dicts suitable for passing to the LLM API.
    """
    return [tool["schema"] for tool in tools.values()]


# Pre-load all tools when the package is imported so other modules can do:
#   from tools import TOOLS
TOOLS: dict = discover_tools()
