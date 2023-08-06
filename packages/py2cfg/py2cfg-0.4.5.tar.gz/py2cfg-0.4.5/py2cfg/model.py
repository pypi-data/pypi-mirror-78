#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Control flow graph for Python programs.
"""
# Aurelien Coet, 2018.

from typing import Any, Tuple, List, Optional, Iterator
import ast  # type: ignore
from _ast import Compare  # For type-hinting
import astor  # type: ignore
import graphviz as gv  # type: ignore
from graphviz.dot import Digraph  # type: ignore
import re


class Block(object):
    """
    Basic block in a control flow graph.

    Contains a list of statements executed in a program without any control
    jumps. A block of statements is exited through one of its exits. Exits are
    a list of Links that represent control flow jumps.
    """

    # Look into ctypes.Structure
    __slots__ = ["id", "statements", "func_calls", "predecessors", "exits"]

    def __init__(self, id: int) -> None:
        # Id of the block.
        self.id = id
        # Statements in the block.
        self.statements = []
        # Calls to functions inside the block (represents context switches to
        # some functions' CFGs).
        self.func_calls = []
        # Links to predecessors in a control flow graph.
        self.predecessors = []
        # Links to the next blocks in a control flow graph.
        self.exits = []

    def __str__(self) -> str:
        if self.statements:
            return "block:{}@{}".format(self.id, self.at())
        return "empty block:{}".format(self.id)

    def __repr__(self) -> str:
        txt = "{} with {} exits".format(str(self), len(self.exits))
        if self.statements:
            txt += ", body=["
            txt += ", ".join([ast.dump(node) for node in self.statements])
            txt += "]"
        return txt

    def at(self) -> Optional[int]:
        """
        Get the line number of the first statement of the block in the program.
        """
        if self.statements and self.statements[0].lineno >= 0:
            return self.statements[0].lineno
        return None

    def is_empty(self) -> bool:
        """
        Check if the block is empty.

        Returns:
            A boolean indicating if the block is empty (True) or not (False).
        """
        return len(self.statements) == 0

    def get_source(self) -> str:
        """
        Get a string containing the Python source code corresponding to the
        statements in the block.

        Returns:
            A string containing the source code of the statements.
        """
        src = ""
        for statement in self.statements:
            if type(statement) in [ast.If, ast.For, ast.While]:
                src += (astor.to_source(statement)).split("\n")[0] + "\n"
            elif (
                type(statement) == ast.FunctionDef
                or type(statement) == ast.AsyncFunctionDef
            ):
                src += (astor.to_source(statement)).split("\n")[0] + "...\n"
            else:
                src += astor.to_source(statement)
        return src

    def get_calls(self) -> str:
        """
        Get a string containing the calls to other functions inside the block.

        Returns:
            A string containing the names of the functions called inside the
            block.
        """
        txt = ""
        for func_name in list(set(self.func_calls)):
            txt += func_name + "\n"
        return txt

    def type(self, default: None=None) -> Any:
        default = ast.Pass if default is None else default
        return type(self.statements[0]) if self.statements else default


class Link(object):
    """
    Link between blocks in a control flow graph.

    Represents a control flow jump between two blocks. Contains an exitcase in
    the form of an expression, representing the case in which the associated
    control jump is made.
    """

    __slots__ = ["source", "target", "exitcase"]

    def __init__(
        self, source: Block, target: Block, exitcase: Optional[ast.Compare] = None,
    ) -> None:
        assert isinstance(target, Block), "Source of a link must be a block"
        assert isinstance(target, Block), "Target of a link must be a block"
        # Block from which the control flow jump was made.
        self.source = source
        # Target block of the control flow jump.
        self.target = target
        # 'Case' leading to a control flow jump through this link.
        self.exitcase = exitcase

    def __str__(self) -> str:
        return f"link from {self.source} to {self.target}"

    def __repr__(self) -> str:
        # This isn't how repr is supposed to be used... We should be able to
        # deep copy this object by calling eval(repr(link))`.
        if self.exitcase is not None:
            return f"{self}, with exitcase {ast.dump(self.exitcase)}"
        return str(self)

    def get_exitcase(self) -> str:
        """
        Get a string containing the Python source code corresponding to the
        exitcase of the Link.

        Returns:
            A string containing the source code.
        """
        if self.exitcase:
            return astor.to_source(self.exitcase)
        return ""


class CFG(object):
    """
    Control flow graph (CFG).

    A control flow graph is composed of basic blocks and links between them
    representing control flow jumps. It has a unique entry block and several
    possible 'final' blocks (blocks with no exits representing the end of the
    CFG).
    """

    # Also serves as graph Key table
    node_styles = {
        "input": ("parallelogram", "#afeeee"),  # Pale Turquoise
        "default": ("rectangle", "#FFFB81"),  # Pale Yellow
        ast.If: ("diamond", "#FF6752"),  # Pale Red
        ast.For: ("hexagon", "#FFBE52"),  # Pale Orange
        ast.While: ("hexagon", "#FFBE52"),  # Pale Orange
        ast.Call: ("tab", "#E552FF"),  # Pale Purple
        ast.Return: ("parallelogram", "#98fb98"),  # Pale Green
    }
    DEFAULT = node_styles["default"]

    def __init__(self, name: str, asynchr: bool = False, short: bool = True) -> None:
        assert isinstance(name, str), "Name of a CFG must be a string"
        assert isinstance(asynchr, bool), "Async must be a boolean value"
        # Name of the function or module being represented.
        self.name = name
        # Type of function represented by the CFG (sync or async). A Python
        # program is considered as a synchronous function (main).
        self.asynchr = asynchr
        # Entry block of the CFG.
        self.entryblock = None
        # Final blocks of the CFG.
        self.finalblocks = []
        # Sub-CFGs for functions defined inside the current CFG.
        self.functioncfgs = {}
        # Sub-CFGs
        self.classcfgs = {}
        self.isShort = short

    def __str__(self) -> str:
        return "CFG for {}".format(self.name)

    def _build_key_subgraph(self, format: str) -> Digraph:
        # Generates a key for the CFG
        key_subgraph = gv.Digraph(
            name="cluster_KEY", format=format, graph_attr={"label": "KEY"}
        )
        for typeobj, (shape, color) in zip(
            self.node_styles.keys(), self.node_styles.values()
        ):
            key_subgraph.node(
                name=(
                    typeobj.__name__.lower()
                    if isinstance(typeobj, type)
                    else str(typeobj)
                ),
                _attributes={"shape": shape, "style": "filled", "fillcolor": color,},
            )

        # Adding edge helps with alignment.
        key_subgraph.edge("if", "input", _attributes={"style": "invis"})
        key_subgraph.edge("input", "call", _attributes={"style": "invis"})
        key_subgraph.edge("for", "return", _attributes={"style": "invis"})
        key_subgraph.edge("return", "default", _attributes={"style": "invis"})
        return key_subgraph

    # default handler for graph nodes
    def _style_handler(self, block: Block, typeobject: Any) -> Tuple[str, str, str]:

        shape, color = self.node_styles.get(typeobject, self.DEFAULT)
        # Left-align all remaining blocks
        text = "\l".join(line for line in block.get_source().splitlines())
        return shape, color, text

    # default handler for graph edges
    def _edge_handler(self, link: Link) -> Tuple[None, str, str]:
        return None, "black", link.get_exitcase().strip()

    def stylize_node(self, block: Block, default: None=None) -> tuple:
        # Since we're modelling ast objects, we might as well copy how they
        # implement handlers. This should allow us to implement new node types
        # simply defining a method `node_ASTNAME`
        typeobject = block.type(default)
        name = typeobject.__name__ if isinstance(typeobject, type) else typeobject
        style = getattr(self, f"node_{name}", self._style_handler,)(block, typeobject)
        assert len(style) == 3, "Style handler must return (shape, color, label)"
        assert all(
            isinstance(attr, str) or attr or attr is None for attr in style
        ), "Style attributes must be str or NoneType"
        return style

    def stylize_edge(self, link: Link, default: None=None, default_target: None=None,) -> tuple:
        typeobject = link.source.type(default)
        name = typeobject.__name__ if isinstance(typeobject, type) else typeobject
        target_type = link.target.type(default_target)
        target_name = (
            target_type.__name__ if isinstance(typeobject, type) else typeobject
        )
        # Do specific attribute search of source->dest
        style_fn = getattr(self, f"{name}_to_{target_name}", None)

        # Do generic attribute search of source->any
        if style_fn is None:
            style_fn = getattr(self, f"edge_{name}", self._edge_handler)
        style = style_fn(link)
        assert len(style) == 3, "style handler must return (shape, color, label)"
        assert all(
            isinstance(attr, str) or attr is None for attr in style
        ), "style attributes must be str or NoneType"
        return style

    def _visit_blocks(
        self, graph: Digraph, block: Block, visited: List[int] = [], calls: bool = True,
    ) -> None:
        # Don't visit blocks twice.
        if block.id in visited:
            return
        visited.append(block.id)
        nodeshape, nodecolor, nodelabel = self.stylize_node(block)
        node_type = block.type()
        original_nodelabel = nodelabel
        nodelabel = ""
        if (
            self.isShort
            and not isinstance(node_type, ast.ClassDef)
            and not isinstance(node_type, ast.FunctionDef)
            and not isinstance(node_type, ast.If)
            and not isinstance(node_type, ast.While)
        ):
            sub_pattern = r"""(\"|')                # Group 1: " or '
                              (?=[^\"'\r\n]{20,})   # Enforce min length of 20
                              ([^\"'\r\n]{,20})     # Group 2: Words that stay
                              ([^\"'\r\n]{,9999})   # Group 3: Shorten these 
                              (\"|')"""  # Group 4: " or '
            original_nodelabel = original_nodelabel.replace("\l", "\n")
            for line in original_nodelabel.splitlines():
                tmp_line = re.sub(sub_pattern, r"\1\2...\4", line, flags=re.VERBOSE)
                nodelabel += tmp_line + "\l"
        else:
            nodelabel = original_nodelabel

        graph.node(
            str(block.id),
            label=nodelabel,
            _attributes={
                "style": "filled",
                "shape": nodeshape,
                "fillcolor": nodecolor,
            },
        )

        # Show the block's function calls in a node.
        # TODO(jstuder) Include conditional blocks in "calls" edges
        if calls and block.func_calls:
            calls_node = str(block.id) + "_calls"
            # Remove any duplicates by splitting on newlines and creating a set
            calls_label = block.get_calls().strip()
            tmp = ""
            for line in calls_label.splitlines():
                if "input" in line:
                    nodeshape, nodecolor = self.node_styles["input"]
                    graph.node(
                        str(block.id) + "_input",
                        label=line,
                        _attributes={
                            "style": "filled",
                            "shape": nodeshape,
                            "fillcolor": nodecolor,
                        },
                    )
                    graph.edge(str(block.id) + "_input", str(block.id))
                    # _attributes={'style': 'dashed'})
                else:
                    line += "\l"
                    tmp += line
            calls_label = tmp
            shape, color = self.node_styles[ast.Call]
            graph.node(
                calls_node,
                label=calls_label,
                _attributes={"shape": shape, "style": "filled", "fillcolor": color,},
            )

            graph.edge(
                str(block.id),
                calls_node,
                label="calls",
                _attributes={"style": "dashed"},
            )

        # Recursively visit all the blocks of the CFG.
        for exit in block.exits:
            assert block == exit.source
            self._visit_blocks(graph, exit.target, visited, calls=calls)
            edgeshape, edgecolor, edgelabel = self.stylize_edge(exit)
            graph.edge(
                str(block.id),
                str(exit.target.id),
                label=edgelabel,
                _attributes={"color": edgecolor},
            )

    def _build_visual(self, format: str = "pdf", calls: bool = True) -> Digraph:
        graph = gv.Digraph(
            name="cluster" + self.name,
            format=format,
            graph_attr={"label": self.name, "rankdir": "TB", "ranksep": "0.02"},
        )
        self._visit_blocks(graph, self.entryblock, visited=[], calls=calls)
        # Build the subgraphs for the function definitions in the CFG and add
        # them to the graph.
        for subcfg in self.classcfgs:
            subgraph = self.classcfgs[subcfg]._build_visual(format=format, calls=calls,)
            graph.subgraph(subgraph)

        for subcfg in self.functioncfgs:
            subgraph = self.functioncfgs[subcfg]._build_visual(
                format=format, calls=calls
            )
            graph.subgraph(subgraph)
        return graph

    def build_visual(
        self, filepath: str, format: str, calls: bool = True, show: bool = True
    ) -> None:
        """
        Build a visualisation of the CFG with graphviz and output it in a DOT
        file.

        Args:
            filename: The name of the output file in which the visualisation
                      must be saved.
            format: The format to use for the output file (PDF, ...).
            show: A boolean indicating whether to automatically open the output
                  file after building the visualisation.
        """
        graph = self._build_visual(format, calls)
        graph.subgraph(self._build_key_subgraph(format))

        graph.render(filepath, view=show)

    def __iter__(self) -> Iterator[Block]:
        """
        Generator that yields all the blocks in the current graph, then
        recursively yields from any sub graphs
        """
        visited = set()
        to_visit = [self.entryblock]

        while to_visit:
            block = to_visit.pop(0)
            visited.add(block)
            for exit_ in block.exits:
                if exit_.target in visited or exit_.target in to_visit:
                    continue
                to_visit.append(exit_.target)
            yield block

        for subcfg in self.classcfgs.values():
            yield from subcfg

        for subcfg in self.functioncfgs.values():
            yield from subcfg

    def node_ClassDef(self, block: Block, typeobj: type) -> Tuple[str, str, str]:
        text = block.get_source().splitlines()[0] + "...\n"
        return (*self.node_styles.get(typeobj, self.DEFAULT), text)

    def edge_If(self, link: Link) -> Tuple[None, str, str]:
        _, _, nodelabel = self.stylize_node(link.source)
        color = "red"
        edgelabel = link.get_exitcase().strip()
        if edgelabel in nodelabel:
            color = "green"
        return None, color, edgelabel

    def edge_While(self, link: Link) -> Tuple[None, str, str]:
        _, _, nodelabel = self.stylize_node(link.source)
        color = "red"
        edgelabel = link.get_exitcase().strip()
        if edgelabel in nodelabel:
            color = "green"
        return None, color, edgelabel

    def edge_For(self, link: Link) -> Tuple[None, str, str]:
        _, _, nodelabel = self.stylize_node(link.source)
        color = "red"
        edgelabel = link.get_exitcase().strip()
        if edgelabel in nodelabel:
            color = "green"
        return None, color, edgelabel
