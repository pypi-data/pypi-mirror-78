from typing import Hashable, Tuple, Dict

import networkx as nx


class UniqueEdgeMultiDiGraph(nx.MultiDiGraph):
    """
    Extends the NetworkX MultiDiGraph with useful functions when edge-keys must be unique across all edges.
    """
    def __init__(self, data=None, **attr):
        self._edge_keys_to_nodes: Dict[Hashable, Tuple[Hashable, Hashable]] = {}
        super().__init__(data, **attr)

    def add_edge(self, u_for_edge: Hashable, v_for_edge: Hashable, key: Hashable, **attr) -> Hashable:
        if key in self._edge_keys_to_nodes:
            raise KeyError(f'Edge {key} already existing!')

        super().add_edge(u_for_edge, v_for_edge, key, **attr)

        self._edge_keys_to_nodes[key] = (u_for_edge, v_for_edge)

        return key

    def remove_edge(self, key: Hashable):
        if key not in self._edge_keys_to_nodes:
            raise nx.NetworkXError(f'Edge {key} does not exist.')

        super().remove_edge(*self._edge_keys_to_nodes[key], key)

        del self._edge_keys_to_nodes[key]

    def get_nodes(self, edge: Hashable) -> Tuple[Hashable, Hashable]:
        return self._edge_keys_to_nodes[edge]
