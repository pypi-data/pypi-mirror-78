#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Control flow graph for Python programs.
"""
# Aurelien Coet, 2018.

from typing import List, Optional, Iterator
import ast  # type: ignore
from _ast import Compare  # type: ignore
import astor  # type: ignore
import graphviz as gv  # type: ignore
from graphviz.dot import Digraph  # type: ignore


class Block(object):
    """
    Basic block in a control flow graph.

    Contains a list of statements executed in a program without any control
    jumps. A block of statements is exited through one of its exits. Exits are
    a list of Links that represent control flow jumps.
    """

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


class Link(object):
    """
    Link between blocks in a control flow graph.

    Represents a control flow jump between two blocks. Contains an exitcase in
    the form of an expression, representing the case in which the associated
    control jump is made.
    """

    __slots__ = ["source", "target", "exitcase"]

    def __init__(
        self, source: Block, target: Block, exitcase: Optional[Compare] = None
    ) -> None:
        assert type(source) == Block, "Source of a link must be a block"
        assert type(target) == Block, "Target of a link must be a block"
        # Block from which the control flow jump was made.
        self.source = source
        # Target block of the control flow jump.
        self.target = target
        # 'Case' leading to a control flow jump through this link.
        self.exitcase = exitcase

    def __str__(self) -> str:
        return "link from {} to {}".format(str(self.source), str(self.target))

    def __repr__(self) -> str:
        if self.exitcase is not None:
            return "{}, with exitcase {}".format(str(self), ast.dump(self.exitcase))
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

    def __init__(self, name: str, asynchr: bool = False) -> None:
        assert type(name) == str, "Name of a CFG must be a string"
        assert type(asynchr) == bool, "Async must be a boolean value"
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
        self.shapes = {
            "if": "diamond",
            "loop": "hexagon",
            "calls": "tab",
            "return": "parallelogram",
            "default": "rectangle",
            "input": "parallelogram",
        }
        self.colors = {
            "if": "#FF6752",  # Pale Red
            "loop": "#FFBE52",  # Pale Orange
            "calls": "#E552FF",  # Pale Purple
            "return": "#98fb98",  # Pale Green
            "input": "#afeeee",  # Pale Turquoise
            "default": "#FFFB81",
        }  # Pale Yellow

    def __str__(self) -> str:
        return "CFG for {}".format(self.name)

    def _build_key_subgraph(self, format) -> Digraph:
        # Generates a key for the CFG
        key_subgraph = gv.Digraph(
            name="cluster_KEY", format=format, graph_attr={"label": "KEY"}
        )
        key_subgraph.node(
            name="if",
            _attributes={
                "shape": self.shapes["if"],
                "style": "filled",
                "fillcolor": self.colors["if"],
            },
        )
        key_subgraph.node(
            name="loop",
            _attributes={
                "shape": self.shapes["loop"],
                "style": "filled",
                "fillcolor": self.colors["loop"],
            },
        )
        key_subgraph.node(
            name="calls",
            _attributes={
                "shape": self.shapes["calls"],
                "style": "filled",
                "fillcolor": self.colors["calls"],
            },
        )
        key_subgraph.node(
            name="return",
            _attributes={
                "shape": self.shapes["return"],
                "style": "filled",
                "fillcolor": self.colors["return"],
            },
        )
        key_subgraph.node(
            name="default",
            _attributes={
                "shape": self.shapes["default"],
                "style": "filled",
                "fillcolor": self.colors["default"],
            },
        )
        key_subgraph.node(
            name="input",
            _attributes={
                "shape": self.shapes["input"],
                "style": "filled",
                "fillcolor": self.colors["input"],
            },
        )
        key_subgraph.edge("if", "input", _attributes={"style": "invis"})
        key_subgraph.edge("input", "calls", _attributes={"style": "invis"})
        key_subgraph.edge("loop", "return", _attributes={"style": "invis"})
        key_subgraph.edge("return", "default", _attributes={"style": "invis"})
        return key_subgraph

    def _visit_blocks(
        self, graph: Digraph, block: Block, visited: List[int] = [], calls: bool = True
    ) -> None:
        # Don't visit blocks twice.
        if block.id in visited:
            return

        nodelabel = block.get_source()  # label = nodelabel
        # Use the first statement to find out what's in the node
        # Just convert it to a string for simplicity
        # This saves us from parsing the entire label and having to handle strings
        # or even variable names that contain keywords
        node_type = str(type(block.statements[0]))

        nodeshape = self.shapes["default"]
        nodecolor = self.colors["default"]
        # _ast.Expr is the generic case (think base-level AST node),
        # _ast.Assign is also unused here in case we want to highlight them differently
        if "_ast.ClassDef" in node_type:
            nodelabel = nodelabel.splitlines()[0] + " ...\n"
        if "_ast.If" in node_type:
            nodeshape = self.shapes["if"]
            nodecolor = self.colors["if"]
        elif ("_ast.For" in node_type) or ("_ast.While" in node_type):
            nodeshape = self.shapes["loop"]
            nodecolor = self.colors["loop"]
        elif "_ast.Return" in node_type:
            nodeshape = self.shapes["return"]
            nodecolor = self.colors["return"]
        else:
            # Left-align all remaining blocks
            tmp = ""
            for line in nodelabel.splitlines():
                line += "\l"
                tmp += line
            nodelabel = tmp

        graph.node(
            str(block.id),
            label=nodelabel,
            _attributes={"style": "filled", "shape": nodeshape, "fillcolor": nodecolor},
        )
        visited.append(block.id)

        # Show the block's function calls in a node.
        # TODO(jstuder) Include conditional blocks in "calls" edges
        if calls and block.func_calls:
            calls_node = str(block.id) + "_calls"
            # Remove any duplicates by splitting on newlines and creating a set
            calls_label = block.get_calls().strip()
            tmp = ""
            for line in calls_label.splitlines():
                if "input" in line:
                    nodeshape = self.shapes["input"]
                    nodecolor = self.colors["input"]
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
            graph.node(
                calls_node,
                label=calls_label,
                _attributes={
                    "shape": self.shapes["calls"],
                    "style": "filled",
                    "fillcolor": self.colors["calls"],
                },
            )

            graph.edge(
                str(block.id),
                calls_node,
                label="calls",
                _attributes={"style": "dashed"},
            )

        # Recursively visit all the blocks of the CFG.
        for exit in block.exits:
            edgecolor = "black"
            self._visit_blocks(graph, exit.target, visited, calls=calls)
            edgelabel = exit.get_exitcase().strip()
            if (
                ("_ast.If" in node_type)
                or ("_ast.For" in node_type)
                or ("_ast.While" in node_type)
            ):
                edgecolor = "red"
                if (edgelabel in nodelabel) and (len(edgelabel) > 0):
                    edgecolor = "green"
            if "_ast.ClassDef" in node_type:
                insert_edge = False

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
            subgraph = self.classcfgs[subcfg]._build_visual(format=format, calls=calls)
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
