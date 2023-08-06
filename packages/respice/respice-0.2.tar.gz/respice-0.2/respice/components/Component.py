from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Hashable, Tuple

from .Branch import Branch


@dataclass(eq=False)
class Component:
    """
    The base class for all electrical components.

    Each component consists of at least one `Edge`. An edge represents a potential difference between two terminals.
    Since a component can be multi-terminal, it must itself specify what edges are created between a given amount
    of terminal by the user. Those terminals are passed in order to the `connect` function. See `connect()`.

    name:
        An optional name to set for the component. Can be set after initialization.
    """
    name: str = field(default=None, init=False)

    def connect(self, *terminals: Hashable) -> List[Tuple[Hashable, Hashable, Branch]]:
        """
        Specifies how the component gets connected in the underlying circuit graph representation.

        When calling `circuit.add_element`, the order of the terminals specified matters. The elements `connect`
        function is called with the terminals to connect with in order. This function shall establish edges in the
        graph representation of the circuit and add so called "couplings". Couplings are equations that further
        constraint the behaviour between different edges (or the behaviour on the edge itself, then the element
        is "self-coupled").

        For example:
        - A resistance is a self-coupled element. Its current is immediately depending on its voltage.
        - A coupled inductance is a mutually-coupled element. Its current depends on the voltage of the other side
          and vice versa. The edges describing the two coils on each side are mutually coupled by one
          additional equation each.

        :param graph:
            The graph to establish edges/connections in.
        :param terminals:
            The potentials (aka terminals) to connect the element's ports with.
        :return:
            A list of edges in the form of `(terminal1, terminal2, edge)`. The order is respected in the voltage-vector
            when invoking each edge's `get_current` function.
        """
        raise NotImplementedError("I don't know how to connect this element between the given terminals")

    @property
    def state(self):
        """
        The whole state of the component.

        A few components (such as inductors or capacitors) have internal state, i.e. depending on the inner state,
        calculated currents and voltages change.

        This function provides a general interface to access the state of components. It is especially used to calculate
        steady-state solutions where the solver must know the state of the components to determine whether indeed a
        steady state has been found.

        If your component does not have any state, do not override this property.

        :return:
            A list or tuple of the state values. Be sure that the order of the state variables does not change.

            When the component has no state, an empty tuple is returned by default.
        """
        return tuple()

    @state.setter
    def state(self, val):
        """
        Sets the component's state.

        :param val:
            The new state.
        """
        pass

    @property
    def default_branch(self):
        """
        Returns the default or main branch of the component. If `None` no default branch is set.

        This field is used for convenient lookup of simulation results by component.
        """
        return None

    def __str__(self):
        if self.name is None or self.name is '':
            return repr(self)
        return self.name
