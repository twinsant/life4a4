# life4a4

一个简单的命令行编程助手 —— 类似 Claude Code，但更轻量，由 Python 编写。

## 功能特性

- 交互式 REPL：直接输入问题或任务，按回车即可
- 通过 [Anthropic API](https://docs.anthropic.com/) 接入 Claude
- 内置工具（智能体可自动调用）：
  - **read_file** – 读取磁盘上的文件
  - **write_file** – 创建或覆盖文件
  - **run_command** – 执行 Shell 命令
  - **list_files** – 列出目录内容
- `/clear` 重置对话历史，`/exit` 退出程序

## 安装

```bash
pip install .
```

设置 Anthropic API 密钥：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

## 使用方式

```bash
life4a4                          # 启动 REPL
life4a4 --model claude-3-7-sonnet-20250219   # 使用指定模型
life4a4 --help                   # 查看帮助
```

## 开发

运行测试：

```bash
pip install pytest
pytest
```

### 示例会话

```
life4a4 – a simple coding agent
Commands: /clear  /exit   Ctrl-C to quit
──────────────────────────────────────────────────

> 用 hello.py 写一个 Hello World 脚本
  [write_file] {'path': 'hello.py', 'content': 'print("Hello, world!")'}
  → Successfully wrote to 'hello.py'
```
