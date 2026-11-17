"""Validate the package version against release metadata before publishing."""

import ast
import os
from pathlib import Path

setup = ast.parse(Path("setup.py").read_text())
call = next(
    node
    for node in ast.walk(setup)
    if isinstance(node, ast.Call)
    and isinstance(node.func, ast.Name)
    and node.func.id == "setup"
)
version = next(
    ast.literal_eval(keyword.value)
    for keyword in call.keywords
    if keyword.arg == "version"
)
assert f"version: {version}" in Path("CITATION.cff").read_text(), "CITATION.cff"
tag = os.environ.get("RELEASE_TAG", "")
if tag:
    assert tag == f"v{version}", f"Tag {tag!r} must match v{version}"
print(f"Validated GSIBerror {version}")
