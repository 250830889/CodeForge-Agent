# CodeForge Agent

[中文](#中文) · [English](#english)

---

## 中文

CodeForge Agent 是一个面向本地代码仓库的 Python 智能编程助手。它将任务规划、工具调用、代码修改、项目分析、本地验证和执行审计整合为可追溯的开发闭环。

### 核心能力

- **代码仓库任务执行**：支持文件读写、精确编辑、代码搜索、Shell 命令、MCP 工具和子 Agent 协作。
- **计划与权限控制**：支持只读计划模式、编辑确认、拒绝模式和受控自动执行模式。
- **项目画像**：通过 `codeforge --profile` 自动识别项目语言、构建清单和可用验证命令。
- **自动验证**：通过 `codeforge --verify` 执行测试发现与 Python 编译检查，并输出可读结果。
- **执行审计**：将工具名称、参数摘要、耗时、执行状态和结果预览写入 JSONL 审计日志。
- **项目级配置**：使用 `.codeforge/` 管理项目规则、技能、子 Agent、计划、记忆与权限配置。

### 快速开始

```bash
python -m venv .venv
.venv/bin/pip install -e .

codeforge --profile
codeforge --verify
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
pip install -e .
```

配置 Anthropic 兼容接口或 OpenAI 兼容接口的 API Key 后，可执行：

```bash
codeforge --plan "为 API 客户端增加输入校验"
codeforge "执行已确认的方案并运行验证"
```

### 架构

`Agent` 负责模型交互与工具编排；`project_profile.py` 建立代码仓库画像；`verifier.py` 执行有边界的本地验证命令；`audit.py` 为每次会话生成追加式 JSONL 审计记录。文件、Shell、搜索、记忆、技能、子 Agent、计划和 MCP 能力均受权限机制约束。

---

## English

CodeForge Agent is a Python coding assistant for local repositories. It brings task planning, tool orchestration, code changes, repository profiling, local verification, and execution auditing into a traceable development workflow.

### Key capabilities

- **Repository task execution**: file operations, precise edits, code search, shell commands, MCP tools, and sub-agent collaboration.
- **Planning and permission control**: read-only planning, edit approval, deny mode, and controlled autonomous execution.
- **Project profiling**: `codeforge --profile` detects project languages, manifests, and available verification commands.
- **Local verification**: `codeforge --verify` runs discovered tests and Python compilation checks with readable output.
- **Execution audit**: JSONL audit logs capture tool names, input summaries, durations, status, and result previews.
- **Project-level configuration**: `.codeforge/` stores rules, skills, sub-agents, plans, memory, and permission settings.

### Quick start

```bash
python -m venv .venv
.venv/bin/pip install -e .

codeforge --profile
codeforge --verify
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -e .
```

After configuring an Anthropic-compatible or OpenAI-compatible API key:

```bash
codeforge --plan "add input validation to the API client"
codeforge "implement the approved plan and run verification"
```

### Architecture

`Agent` coordinates model interactions and tool execution. `project_profile.py` builds a repository profile, `verifier.py` runs bounded local checks, and `audit.py` creates append-only JSONL audit records for each session. File, shell, search, memory, skill, sub-agent, plan, and MCP capabilities remain behind permission controls.

## License and notice / 许可证与声明

CodeForge Agent is distributed under the MIT License. 
