import asyncio
import inspect
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Callable, Awaitable, Dict, Optional


class Tool(ABC):
    """
    Tool base-class to define an interface for all tools to implement.
    """

    @property
    @abstractmethod
    def help(self) -> str:
        pass

    @abstractmethod
    def make_parser(self, parser: ArgumentParser):
        """
        Set up the CLI argument parser for this tool.
        """
        pass

    @abstractmethod
    def run_tool(self, options: Namespace):
        pass


class SyncTool(Tool):
    """
    Run a tool synchronously.
    Should be sub-classed to create a new tool.
    """

    @abstractmethod
    def make_tool(self) -> Callable[..., None]:
        """
        Return a callable to be invoked with keyword-only arguments populated from the CLI options.
        """
        pass

    def run_tool(self, options: Namespace):
        func = self.make_tool()
        kwargs = {arg: getattr(options, arg) for arg in inspect.getfullargspec(func).kwonlyargs}
        func(**kwargs)


class AioTool(Tool):
    """
    Run a tool via an asyncio event loop.
    Should be sub-classed to create a new tool.
    """

    @abstractmethod
    def make_tool(self) -> Callable[..., Awaitable[None]]:
        """
        Return an async callable to be invoked with keyword-only arguments populated from the CLI options.
        """
        pass

    def run_tool(self, options: Namespace):
        func = self.make_tool()
        kwargs = {arg: getattr(options, arg) for arg in inspect.getfullargspec(func).kwonlyargs}
        loop = asyncio.get_event_loop()
        loop.run_until_complete(func(**kwargs))


class ToolContainer(Tool):
    """
    A container for other tools.
    Should not need to be derived from, just instantiated.
    """

    def __init__(self, tools: Dict[str, Tool], *, help: str):
        self.__tools = tools
        self.__help = help
        self.__parser: Optional[ArgumentParser] = None

    @property
    def help(self) -> str:
        return self.__help

    def make_parser(self, parser: ArgumentParser):
        make_tool_parsers(parser, self.__tools)
        self.__parser = parser

    def run_tool(self, options: Namespace):
        self.__parser.print_help()
        raise SystemExit(1)


def make_tool_parsers(parser: ArgumentParser, tools: Dict[str, Tool]):
    sub_parser = parser.add_subparsers()
    for tool_name, tool in tools.items():
        tool_parser = sub_parser.add_parser(tool_name, help=tool.help)
        tool.make_parser(tool_parser)
        tool_parser.set_defaults(tool=tool)


def main(tools: Dict[str, Tool], prog: Optional[str] = None):
    parser = ArgumentParser(prog=prog)
    make_tool_parsers(parser, tools)
    options = parser.parse_args()

    try:
        tool: Tool = options.tool

    except AttributeError:
        parser.print_help()
        raise SystemExit(1)

    else:
        tool.run_tool(options)
