"""
Abstract Syntax Tree (AST) Static Dependency Graph Engine
Author: Saksham Singh (24BTRAO035)
Parses Python source files, tracks module imports and symbol hierarchies,
and computes transitive dependency closure across modules and test suites.
"""
import ast
import os
from pathlib import Path
from typing import Dict, Set, List, Optional
import networkx as nx


class ASTDependencyGraph:
    """
    Constructs and queries a Directed Graph G = (V, E) of module dependencies.
    Edge (A -> B) means module A imports or depends on module B.
    Reverse traversal from B yields all modules and tests impacted by changes to B.
    """

    def __init__(self, root_dir: Optional[str] = None):
        self.root_dir = Path(root_dir or os.getcwd()).resolve()
        # forward_graph: module -> modules it imports
        self.forward_graph = nx.DiGraph()
        # reverse_graph: module -> modules that import it (consumers)
        self.reverse_graph = nx.DiGraph()
        self._module_path_map: Dict[str, str] = {}
        self.build_graph()

    def _file_to_module(self, file_path: Path) -> str:
        """Converts relative file path to python module notation (e.g. src.services.billing)."""
        rel = file_path.relative_to(self.root_dir).with_suffix("")
        return ".".join(rel.parts)

    def _module_to_rel_path(self, module_name: str) -> Optional[str]:
        """Maps module name back to relative file path."""
        parts = module_name.split(".")
        cand_py = Path(*parts).with_suffix(".py")
        if (self.root_dir / cand_py).exists():
            return str(cand_py)
        cand_pkg = Path(*parts) / "__init__.py"
        if (self.root_dir / cand_pkg).exists():
            return str(cand_pkg)
        return None

    def build_graph(self) -> None:
        """Scans all Python files in src/ and tests/ and extracts import edges."""
        self.forward_graph.clear()
        self.reverse_graph.clear()
        self._module_path_map.clear()

        py_files: List[Path] = []
        for search_dir in ["src", "tests"]:
            p = self.root_dir / search_dir
            if p.exists():
                py_files.extend(p.rglob("*.py"))

        for file_path in py_files:
            rel_str = str(file_path.relative_to(self.root_dir))
            mod_name = self._file_to_module(file_path)
            self._module_path_map[rel_str] = mod_name
            self.forward_graph.add_node(mod_name, path=rel_str)
            self.reverse_graph.add_node(mod_name, path=rel_str)

        # Parse AST for each file
        for file_path in py_files:
            source_mod = self._file_to_module(file_path)
            try:
                content = file_path.read_text(encoding="utf-8")
                tree = ast.parse(content, filename=str(file_path))
            except Exception:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._add_import_edge(source_mod, alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self._add_import_edge(source_mod, node.module)

    def _add_import_edge(self, source_mod: str, imported_mod: str) -> None:
        """Registers a directional dependency edge."""
        # Find exact or prefix matches in our known internal modules
        matched_target: Optional[str] = None
        for known_mod in self.forward_graph.nodes:
            if imported_mod == known_mod or imported_mod.startswith(known_mod + "."):
                matched_target = known_mod
                break

        if matched_target and source_mod != matched_target:
            self.forward_graph.add_edge(source_mod, matched_target)
            self.reverse_graph.add_edge(matched_target, source_mod)

    def get_direct_dependents(self, file_path: str) -> Set[str]:
        """Returns files that directly import the given file."""
        norm_path = os.path.normpath(file_path)
        mod_name = self._module_path_map.get(norm_path)
        if not mod_name or mod_name not in self.reverse_graph:
            return set()

        dependents: Set[str] = set()
        for consumer_mod in self.reverse_graph.successors(mod_name):
            data = self.reverse_graph.nodes[consumer_mod]
            if "path" in data:
                dependents.add(data["path"])
        return dependents

    def get_transitive_dependents(self, file_path: str) -> Set[str]:
        """
        Computes the complete transitive closure of all modules and tests
        that depend on the specified file directly or indirectly.
        """
        norm_path = os.path.normpath(file_path)
        mod_name = self._module_path_map.get(norm_path)
        if not mod_name or mod_name not in self.reverse_graph:
            return set()

        reachable_mods = nx.descendants(self.reverse_graph, mod_name)
        impacted_paths: Set[str] = set()
        for m in reachable_mods:
            data = self.reverse_graph.nodes[m]
            if "path" in data:
                impacted_paths.add(data["path"])
        return impacted_paths

    def find_impacted_tests(self, changed_files: List[str]) -> Set[str]:
        """
        Given a list of changed source/test files, returns all impacted test file paths.
        """
        impacted_tests: Set[str] = set()

        for f in changed_files:
            norm_f = os.path.normpath(f)
            # If a test file itself changed, it must be run
            if norm_f.startswith("tests/") and norm_f.endswith(".py"):
                impacted_tests.add(norm_f)
                continue

            # If a source file changed, compute transitive dependents
            transitives = self.get_transitive_dependents(norm_f)
            for dep in transitives:
                if dep.startswith("tests/") and dep.endswith(".py"):
                    impacted_tests.add(dep)

        return impacted_tests

    def to_dict(self) -> Dict[str, List[str]]:
        """Exports forward graph as dictionary representation for serialization."""
        return {
            node: list(self.forward_graph.successors(node))
            for node in self.forward_graph.nodes
        }
