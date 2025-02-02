<a name="readme-top"></a>

<div align="center">
<img src="https://i.ibb.co/C1FQyp4/Capture-d-e-cran-2025-01-18-a-17-12-43.png" alt="AutoGen Logo" width="100">

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40NexAgents)](https://x.com/AgentsNode)
[![Documentation](https://img.shields.io/badge/Documentation-NodeAgents-blue?logo=read-the-docs)](https://microsoft.github.io/NodeAgents/)

</div>

# NodeAgents

**NodeAgents** is a framework for creating multi-agent AI applications that can act autonomously or work alongside humans.

## Installation

NodeAgents requires **Python 3.10 or later**.

```bash
# Install AgentChat and OpenAI client from Extensions
pip install -U "NodeAgents-agentchat" "NodeAgents-ext[openai]"
```

The current stable version is v0.4. If you are upgrading from NodeAgents v0.2, please refer to the [Migration Guide](https://microsoft.github.io/NodeAgents/dev/user-guide/agentchat-user-guide/migration-guide.html) for detailed instructions on how to update your code and configurations.

```bash
# Install NodeAgents Studio for no-code GUI
pip install -U "autogenstudio"
```

## Quickstart

### Hello World

Create an assistant agent using OpenAI's GPT-4o model.

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main() -> None:
    agent = AssistantAgent("assistant", OpenAIChatCompletionClient(model="gpt-4o"))
    print(await agent.run(task="Say 'Hello World!'"))

asyncio.run(main())
```

### Team

Create a group chat team with an assistant agent, a web surfer agent, and a user proxy agent
for web browsing tasks. You need to install [playwright](https://playwright.dev/python/docs/library).

```python
# pip install -U NodeAgents-agentchat NodeAgents-ext[openai,web-surfer]
# playwright install
import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer

async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    assistant = AssistantAgent("assistant", model_client)
    web_surfer = MultimodalWebSurfer("web_surfer", model_client)
    user_proxy = UserProxyAgent("user_proxy")
    termination = TextMentionTermination("exit") # Type 'exit' to end the conversation.
    team = RoundRobinGroupChat([web_surfer, assistant, user_proxy], termination_condition=termination)
    await Console(team.run_stream(task="Find information about NodeAgents and write a short summary."))

asyncio.run(main())
```

### NodeAgents Studio

Use NodeAgents Studio to prototype and run multi-agent workflows without writing code.

```bash
# Run NodeAgents Studio on http://localhost:8080
autogenstudio ui --port 8080 --appdir ./my-app
```

## Why Use NodeAgents?

<div align="center">
  <img src="NodeAgents-landing.jpg" alt="NodeAgents Landing" width="500">
</div>

The NodeAgents ecosystem provides everything you need to create AI agents, especially multi-agent workflows -- framework, developer tools, and applications.

The _framework_ uses a layered and extensible design. Layers have clearly divided responsibilities and build on top of layers below. This design enables you to use the framework at different levels of abstraction, from high-level APIs to low-level components.

- [Core API](./python/packages/NodeAgents-core/) implements message passing, event-driven agents, and local and distributed runtime for flexibility and power. It also support cross-language support for .NET and Python.
- [AgentChat API](./python/packages/NodeAgents-agentchat/) implements a simpler but opinionated API rapid for prototyping. This API is built on top of the Core API and is closest to what users of v0.2 are familiar with and supports familiar multi-agent patterns such as two-agent chat or group chats.
- [Extensions API](./python/packages/NodeAgents-ext/) enables first- and third-party extensions continuously expanding framework capabilities. It support specific implementation of LLM clients (e.g., OpenAI, AzureOpenAI), and capabilities such as code execution.

The ecosystem also supports two essential _developer tools_:

<div align="center">
  <img src="https://media.githubusercontent.com/media/microsoft/NodeAgents/refs/heads/main/python/packages/NodeAgents-studio/docs/ags_screen.png" alt="NodeAgents Studio Screenshot" width="500">
</div>

- [NodeAgents Studio](./python/packages/NodeAgents-studio/) provides a no-code GUI for building multi-agent applications.
- [NodeAgents Bench](./python/packages/agbench/) provides a benchmarking suite for evaluating agent performance.

You can use the NodeAgents framework and developer tools to create applications for your domain. For example, [Magentic-One](./python/packages/magentic-one-cli/) is a state-of-art multi-agent team built using AgentChat API and Extensions API that can handle variety of tasks that require web browsing, code execution, and file handling.

With NodeAgents you get to join and contribute to a thriving ecosystem. We host weekly office hours and talks with maintainers and community. We also have a [Discord server](https://aka.ms/NodeAgents-discord) for real-time chat, GitHub Discussions for Q&A, and a blog for tutorials and updates.

## Where to go next?

<div align="center">

|               | [![Python](https://img.shields.io/badge/NodeAgents-Python-blue?logo=python&logoColor=white)](./python)                                                                                                                                                                                                                                                                                                                | [![.NET](https://img.shields.io/badge/NodeAgents-.NET-green?logo=.net&logoColor=white)](./dotnet) | [![Studio](https://img.shields.io/badge/NodeAgents-Studio-purple?logo=visual-studio&logoColor=white)](./python/packages/NodeAgents-studio)                     |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Installation  | [![Installation](https://img.shields.io/badge/Install-blue)](https://microsoft.github.io/NodeAgents/dev/user-guide/agentchat-user-guide/installation.html)                                                                                                                                                                                                                                                            | \*                                                                                             | [![Install](https://img.shields.io/badge/Install-purple)](https://microsoft.github.io/NodeAgents/dev/user-guide/autogenstudio-user-guide/installation.html) |
| Quickstart    | [![Quickstart](https://img.shields.io/badge/Quickstart-blue)](https://microsoft.github.io/NodeAgents/dev/user-guide/agentchat-user-guide/quickstart.html#)                                                                                                                                                                                                                                                            | \*                                                                                             | [![Usage](https://img.shields.io/badge/Quickstart-blue)](https://microsoft.github.io/NodeAgents/dev/user-guide/autogenstudio-user-guide/usage.html#)        |
| Tutorial      | [![Tutorial](https://img.shields.io/badge/Tutorial-blue)](https://microsoft.github.io/NodeAgents/dev/user-guide/agentchat-user-guide/tutorial/models.html)                                                                                                                                                                                                                                                            | \*                                                                                             | [![Usage](https://img.shields.io/badge/Quickstart-blue)](https://microsoft.github.io/NodeAgents/dev/user-guide/autogenstudio-user-guide/usage.html#)        |
| API Reference | [![API](https://img.shields.io/badge/Docs-blue)](https://microsoft.github.io/NodeAgents/dev/reference/index.html#)                                                                                                                                                                                                                                                                                                    | \*                                                                                             | [![API](https://img.shields.io/badge/Docs-purple)](https://microsoft.github.io/NodeAgents/dev/user-guide/autogenstudio-user-guide/usage.html)               |
| Packages      | [![PyPi NodeAgents-core](https://img.shields.io/badge/PyPi-NodeAgents--core-blue?logo=pypi)](https://pypi.org/project/NodeAgents-core/) <br> [![PyPi NodeAgents-agentchat](https://img.shields.io/badge/PyPi-NodeAgents--agentchat-blue?logo=pypi)](https://pypi.org/project/NodeAgents-agentchat/) <br> [![PyPi NodeAgents-ext](https://img.shields.io/badge/PyPi-NodeAgents--ext-blue?logo=pypi)](https://pypi.org/project/NodeAgents-ext/) | \*                                                                                             | [![PyPi autogenstudio](https://img.shields.io/badge/PyPi-autogenstudio-purple?logo=pypi)](https://pypi.org/project/autogenstudio/)                       |

</div>

\*_Releasing soon_

Interested in contributing? See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on how to get started. We welcome contributions of all kinds, including bug fixes, new features, and documentation improvements. Join our community and help us make NodeAgents better!

Have questions? Check out our [Frequently Asked Questions (FAQ)](./FAQ.md) for answers to common queries. If you don't find what you're looking for, feel free to ask in our [GitHub Discussions](https://github.com/microsoft/NodeAgents/discussions) or join our [Discord server](https://aka.ms/NodeAgents-discord) for real-time support.

## Legal Notices

Microsoft and any contributors grant you a license to the Microsoft documentation and other content
in this repository under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/legalcode),
see the [LICENSE](LICENSE) file, and grant you a license to any code in the repository under the [MIT License](https://opensource.org/licenses/MIT), see the
[LICENSE-CODE](LICENSE-CODE) file.

Microsoft, Windows, Microsoft Azure, and/or other Microsoft products and services referenced in the documentation
may be either trademarks or registered trademarks of Microsoft in the United States and/or other countries.
The licenses for this project do not grant you rights to use any Microsoft names, logos, or trademarks.
Microsoft's general trademark guidelines can be found at <http://go.microsoft.com/fwlink/?LinkID=254653>.

Privacy information can be found at <https://go.microsoft.com/fwlink/?LinkId=521839>

Microsoft and any contributors reserve all other rights, whether under their respective copyrights, patents,
or trademarks, whether by implication, estoppel, or otherwise.

<p align="right" style="font-size: 14px; color: #555; margin-top: 20px;">
  <a href="#readme-top" style="text-decoration: none; color: blue; font-weight: bold;">
    ↑ Back to Top ↑
  </a>
</p>
