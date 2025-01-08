<a name="readme-top"></a>

<div align="center">
<img src="https://microsoft.github.io/autogen/0.2/img/ag.svg" alt="AutoGen Logo" width="100">

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40pyautogen)](https://twitter.com/pyautogen)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Company?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/105812540)
[![Discord](https://img.shields.io/badge/discord-chat-green?logo=discord)](https://aka.ms/autogen-discord)
[![GitHub Discussions](https://img.shields.io/badge/Discussions-Q%26A-green?logo=github)](https://github.com/microsoft/autogen/discussions)

[![PyPi autogen-core](https://img.shields.io/badge/PyPi-autogen--core-blue?logo=pypi)](https://pypi.org/project/autogen-core/)
[![PyPi autogen-agentchat](https://img.shields.io/badge/PyPi-autogen--agentchat-blue?logo=pypi)](https://pypi.org/project/autogen-agentchat/)
[![PyPi autogen-ext](https://img.shields.io/badge/PyPi-autogen--ext-blue?logo=pypi)](https://pypi.org/project/autogen-ext/)
</div>


# AutoGen

**AutoGen** is a framework for creating intelligent multi-agent systems that can act autonomously or work alongside humans.

### Quick Start

```bash
pip install autogen-agentchat autogen-ext[openai]
```

If you are upgrading from AutoGen v0.2, please refer to the [Migration Guide](https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/migration-guide.html) for detailed instructions on how to update your code and configurations.

### Minimal Python Example
Code for setting up a multi-agent system to plot stock prices:
```python
# pip install "autogen-agentchat" "autogen-ext[openai]" "yfinance" "matplotlib"
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool

async def main() -> None:
    tool = PythonCodeExecutionTool(LocalCommandLineCodeExecutor(work_dir="coding"))
    agent = AssistantAgent("assistant", OpenAIChatCompletionClient(model="gpt-4o"), tools=[tool], reflect_on_tool_use=True)
    await Console(agent.run_stream(task="Create a plot of MSFT stock prices in 2024 and save it to a file. Use yfinance and matplotlib."))
asyncio.run(main())
```


### Why Use AutoGen?

<div align="center">
  <img src="autogen-landing.jpg" alt="AutoGen Landing" width="600">
</div>

- **Essential building blocks for agents**: AutoGen provides everything you need to create intelligent agents, including tools, LLMs, multi-agent teams, and capabilities like code/tool execution and human-in-the-loop workflows. AutoGen also provides state-of-the-art agents like Magentic-One for top performance and reliability, supports distributed agents and cross-language support in Python and .NET.

- **Rapid prototyping and flexibility**: AutoGen uses a modular, extensible design with clearly divided responsibilities between layers. The Core API implements message passing, event-driven agents, and runtime for flexibility and power, the AgentChat API implements a simpler but opinionated API rapid for prototyping, or the Extensions API enables first- and third-party extensions continuously expanding framework capabilities. Additionally, AutoGen Studio enables a beautiful GUI for no-code agent development.

- **Community and ecosystem**: Join and contribute to a thriving ecosystem. We host weekly office hours and talks with maintainers and community. We also have a [Discord server](https://aka.ms/autogen-discord) for real-time chat, GitHub Discussions for Q&A, and a blog for tutorials and updates.

## Where to go next?

<div align="center">

|                      | [![Python](https://img.shields.io/badge/AutoGen-Python-blue?logo=python&logoColor=white)](./python)                                                                                     | [![.NET](https://img.shields.io/badge/AutoGen-.NET-green?logo=.net&logoColor=white)](./dotnet)              | [![Studio](https://img.shields.io/badge/AutoGen-Studio-purple?logo=visual-studio&logoColor=white)](https://github.com/microsoft/autogen/tree/gagb-readme/python/packages/autogen-studio)              |
|----------------------|--------------------------------------------------------------------------------------------|-------------------|-------------------|
| Installation    | [![Installation](https://img.shields.io/badge/Install-blue)](https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/installation.html) | *    | [![Install](https://img.shields.io/badge/Install-purple)](https://microsoft.github.io/autogen/dev/user-guide/autogenstudio-user-guide/installation.html)    |
| Quickstart | [![Quickstart](https://img.shields.io/badge/Quickstart-blue)](https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/quickstart.html#) | *    | *    |
| Tutorial        | [![Tutorial](https://img.shields.io/badge/Tutorial-blue)](https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/tutorial/models.html)  | *| * |
| API Reference   | [![API](https://img.shields.io/badge/Docs-blue)](https://microsoft.github.io/autogen/dev/reference/index.html#) | *    | [![API](https://img.shields.io/badge/Docs-purple)](https://microsoft.github.io/autogen/dev/user-guide/autogenstudio-user-guide/usage.html) |
| Packages        | [![PyPi autogen-core](https://img.shields.io/badge/PyPi-autogen--core-blue?logo=pypi)](https://pypi.org/project/autogen-core/) <br> [![PyPi autogen-agentchat](https://img.shields.io/badge/PyPi-autogen--agentchat-blue?logo=pypi)](https://pypi.org/project/autogen-agentchat/) <br> [![PyPi autogen-ext](https://img.shields.io/badge/PyPi-autogen--ext-blue?logo=pypi)](https://pypi.org/project/autogen-ext/) | *    | [![PyPi autogenstudio](https://img.shields.io/badge/PyPi-autogenstudio-purple?logo=pypi)](https://pypi.org/project/autogenstudio/) |

</div>

_*Releasing soon_

Interested in contributing? See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on how to get started. We welcome contributions of all kinds, including bug fixes, new features, and documentation improvements. Join our community and help us make AutoGen better!

Have questions? Check out our [Frequently Asked Questions (FAQ)](./FAQ.md) for answers to common queries. If you don't find what you're looking for, feel free to ask in our [GitHub Discussions](https://github.com/microsoft/autogen/discussions) or join our [Discord server](https://aka.ms/autogen-discord) for real-time support.


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
