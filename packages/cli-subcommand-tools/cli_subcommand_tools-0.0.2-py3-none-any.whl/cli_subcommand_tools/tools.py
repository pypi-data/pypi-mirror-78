import asyncio
import inspect
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Callable, Awaitable, Dict


class AsyncTool(ABC):
    @property
    @abstractmethod
    def help(self) -> str:
        pass

    @abstractmethod
    def make_parser(self, parser: ArgumentParser):
        pass

    @abstractmethod
    def make_tool(self) -> Callable[..., Awaitable[None]]:
        """
        Return an async callable to be invoked with keyword-only arguments populated from the CLI options.
        """
        pass


def make_tool_parsers(parser: ArgumentParser, tools: Dict[str, AsyncTool]):
    sub_parser = parser.add_subparsers()
    for tool_name, tool in tools.items():
        tool_parser = sub_parser.add_parser(tool_name, help=tool.help)
        tool.make_parser(tool_parser)
        tool_parser.set_defaults(tool=tool)


def run_tool(tool: AsyncTool, options: Namespace):
    func = tool.make_tool()
    kwargs = {arg: getattr(options, arg) for arg in inspect.getfullargspec(tool).kwonlyargs}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func(**kwargs))


def main(tools: Dict[str, AsyncTool]):
    parser = ArgumentParser()
    make_tool_parsers(parser, tools)
    options = parser.parse_args()

    try:
        tool: AsyncTool = options.tool

    except AttributeError:
        parser.print_help()
        raise SystemExit(1)

    else:
        run_tool(tool, options)
