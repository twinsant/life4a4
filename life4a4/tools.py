"""Tool implementations: file I/O, shell commands, directory listing."""

import subprocess
from pathlib import Path


def read_file(path: str) -> str:
    """Return the text contents of *path*."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Error: file '{path}' not found"
    except PermissionError:
        return f"Error: permission denied reading '{path}'"
    except Exception as exc:
        return f"Error reading file: {exc}"


def write_file(path: str, content: str) -> str:
    """Write *content* to *path*, creating parent directories as needed."""
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Successfully wrote to '{path}'"
    except PermissionError:
        return f"Error: permission denied writing to '{path}'"
    except Exception as exc:
        return f"Error writing file: {exc}"


def run_command(command: str, timeout: int = 30) -> str:
    """Run a shell command and return its combined stdout/stderr."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"
        if result.returncode != 0:
            output += f"\nExit code: {result.returncode}"
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Error: command timed out after {timeout} seconds"
    except Exception as exc:
        return f"Error running command: {exc}"


def list_files(directory: str = ".") -> str:
    """List files and directories inside *directory*."""
    try:
        p = Path(directory)
        if not p.exists():
            return f"Error: directory '{directory}' not found"
        items = [
            (f"{item.name}/" if item.is_dir() else item.name)
            for item in sorted(p.iterdir())
        ]
        return "\n".join(items) if items else "(empty directory)"
    except PermissionError:
        return f"Error: permission denied accessing '{directory}'"
    except Exception as exc:
        return f"Error listing files: {exc}"
