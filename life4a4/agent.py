"""Agent: manages the conversation with Claude and executes tool calls."""

import anthropic

from life4a4.tools import list_files, read_file, run_command, write_file

_TOOLS: list[dict] = [
    {
        "name": "read_file",
        "description": "Read the text contents of a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to read"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": (
            "Write content to a file, creating it (and any parent directories) "
            "if it does not already exist."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to write"},
                "content": {"type": "string", "description": "Content to write"},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "run_command",
        "description": "Run a shell command and return its output.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command to run"},
            },
            "required": ["command"],
        },
    },
    {
        "name": "list_files",
        "description": "List files and sub-directories inside a directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory to list (defaults to current directory)",
                },
            },
            "required": [],
        },
    },
]

_TOOL_FUNCTIONS = {
    "read_file": lambda args: read_file(args["path"]),
    "write_file": lambda args: write_file(args["path"], args["content"]),
    "run_command": lambda args: run_command(args["command"]),
    "list_files": lambda args: list_files(args.get("directory", ".")),
}

_SYSTEM = (
    "You are a helpful coding assistant running as a CLI tool. "
    "You can read and write files, run shell commands, and help with any coding task. "
    "Be concise and practical."
)


class Agent:
    """Stateful agent that maintains conversation history across turns."""

    def __init__(self, model: str = "claude-3-5-haiku-20241022") -> None:
        self.client = anthropic.Anthropic()
        self.model = model
        self.messages: list[dict] = []

    def clear(self) -> None:
        """Reset the conversation history."""
        self.messages = []

    def chat(self, user_message: str, on_tool_call=None) -> str:
        """Send *user_message* and return the assistant's final text reply.

        *on_tool_call* is an optional callback called with ``(name, input, result)``
        each time a tool is executed.
        """
        self.messages.append({"role": "user", "content": user_message})

        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=_SYSTEM,
                tools=_TOOLS,
                messages=self.messages,
            )

            text_parts: list[str] = []
            tool_uses: list = []

            for block in response.content:
                if block.type == "text":
                    text_parts.append(block.text)
                elif block.type == "tool_use":
                    tool_uses.append(block)

            self.messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn" or not tool_uses:
                return "\n".join(text_parts)

            tool_results = []
            for tool_use in tool_uses:
                result = _TOOL_FUNCTIONS[tool_use.name](tool_use.input)
                if on_tool_call is not None:
                    on_tool_call(tool_use.name, tool_use.input, result)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": result,
                    }
                )

            self.messages.append({"role": "user", "content": tool_results})
