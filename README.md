# life4a4

[中文文档](README_CN.md)

A simple CLI coding agent – like Claude Code, but smaller and written in Python.

## Features

- Interactive REPL: just type your question or task and press Enter
- Claude-powered via the [Anthropic API](https://docs.anthropic.com/)
- Built-in tools the agent can use automatically:
  - **read_file** – read a file from disk
  - **write_file** – create or overwrite a file
  - **run_command** – execute a shell command
  - **list_files** – list a directory's contents
- `/clear` to reset conversation history, `/exit` to quit

## Installation

```bash
pip install .
```

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
life4a4                          # start the REPL
life4a4 --model claude-3-7-sonnet-20250219   # use a different model
life4a4 --help                   # show options
```

## Development

Run the tests:

```bash
pip install pytest
pytest
```

### Example session

```
life4a4 – a simple coding agent
Commands: /clear  /exit   Ctrl-C to quit
──────────────────────────────────────────────────

> write a hello world script in hello.py
  [write_file] {'path': 'hello.py', 'content': 'print("Hello, world!")'}
  → Successfully wrote to 'hello.py'
```