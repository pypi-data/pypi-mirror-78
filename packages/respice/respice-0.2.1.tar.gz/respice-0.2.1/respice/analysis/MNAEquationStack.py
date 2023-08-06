from dataclasses import dataclass, field
from typing import List, Tuple, Hashable, Union, Iterable, Set

import numpy as np
from ordered_set import OrderedSet

from respice.analysis import UniqueEdgeMultiDiGraph
from respice.components import Branch
from respice.components.Branch import VoltageBranch, CurrentBranch

from networkx.algorithms.components import weakly_connected_components


@dataclass
class KirchhoffEquationTerm:
    negative: bool
    branch: CurrentBranch
    coupled_branches: List[Union[VoltageBranch, CurrentBranch]]


@dataclass
class KirchhoffEquationBranchConsecutiveTerm:
    negative: bool
    branch: VoltageBranch


@dataclass
class KirchhoffEquation:
    terms: List[Union[KirchhoffEquationTerm, KirchhoffEquationBranchConsecutiveTerm]] = field(default_factory=list)


@dataclass
class BranchConsecutiveEquation:
    branch: VoltageBranch
    potentials: Tuple[Hashable, Hashable]
    coupled_branches: List[Union[VoltageBranch, CurrentBranch]]


class MNAEquationStack:
    """
    Manages the master equation that comprises an electrical circuit system using the so called MNA - Modified Nodal
    Analysis. Used inside the simulation algorithm to find the final solution.

    The MNA equation stack automatically generates an inner representation of all mathematical terms and equations
    necessary to describe the problem. The problem is a multivariate non-linear root-finding problem.

    This class is majorly to be used via solvers like scipy's fsolve function, where you feed in evaluate() or
    the optimized expression returned by lambdify().

    For more information about the MNA itself, see https://en.wikipedia.org/wiki/Modified_nodal_analysis
    """

    def __init__(self, graph: UniqueEdgeMultiDiGraph, couplings: Iterable[List[Branch]]):
        self._graph: UniqueEdgeMultiDiGraph = graph
        self._reference_nodes: Set[Hashable] = set()

        # Stores the vector-index relations to potential nodes.
        self._nodes: OrderedSet[Hashable] = OrderedSet()
        # Stores the vector-index relations to branch currents when voltage-branches are used. The branch consecutive
        # currents are stored after the nodes in the input vector for evaluate().
        self._currents: OrderedSet[VoltageBranch] = OrderedSet()

        self._kirchhoff_equations: List[KirchhoffEquation] = []
        self._branch_consecutive_equations: List[BranchConsecutiveEquation] = []

        self._coupling_dictionary = {branch: coupled_branches
                                     for coupled_branches in couplings
                                     for branch in coupled_branches}

        for subset in weakly_connected_components(graph):
            # First element of a disjoint subset graph is always a reference potential.

            subset_iter = iter(subset)
            # This one is safe and needs no StopIteration check. Otherwise there would be no subset yielded by
            # weakly_connected_components.
            self._reference_nodes.add(next(subset_iter))

            for potential in subset_iter:
                self._nodes.add(potential)

                kirchhoff_equation = KirchhoffEquation()

                for negative, branches in [(False, graph.in_edges(potential, keys=True)),
                                           (True, graph.out_edges(potential, keys=True))]:
                    for source, target, branch in branches:
                        # Add equations according to MNA (Modified Nodal Analysis) technique.
                        if isinstance(branch, CurrentBranch):
                            term = KirchhoffEquationTerm(
                                negative=negative,
                                branch=branch,
                                coupled_branches=self._coupling_dictionary[branch],
                            )
                        elif isinstance(branch, VoltageBranch):
                            term = KirchhoffEquationBranchConsecutiveTerm(
                                negative=negative,
                                branch=branch,
                            )

                            # Branch consecutive equations are processed in a later step for more efficient iteration
                            # over nodes. Since branches are always connected between two nodes, but we can just have
                            # one branch consecutive equation per branch, we would need to track that information if we
                            # do it here.

                        else:
                            raise ValueError(f'Unknown branch type encountered: {type(branch)}')

                        kirchhoff_equation.terms.append(term)

                self._kirchhoff_equations.append(kirchhoff_equation)

        # Now processing branch consecutive equations.
        for source, target, branch in graph.edges(keys=True):
            if isinstance(branch, VoltageBranch):
                self._branch_consecutive_equations.append(BranchConsecutiveEquation(
                    branch=branch,
                    potentials=(source, target),
                    coupled_branches=self._coupling_dictionary[branch],
                ))

                self._currents.add(branch)

    def __len__(self):
        """
        :return:
            The number of equations inside the equation stack.
        """
        return len(self._nodes) + len(self._currents)

    def _expand_jacobi_vector(self, jacobi, coupled_branches: List[Union[VoltageBranch, CurrentBranch]]) -> np.ndarray:
        # Properly creates a Jacobian vector suiting the problem from a component-tailored Jacobian.

        jacobi_vector = np.zeros(len(self))

        for i, branch in enumerate(coupled_branches):
            if isinstance(branch, VoltageBranch):
                jacobi_vector[self._currents.index(branch) + len(self._nodes)] += jacobi[i]
            elif isinstance(branch, CurrentBranch):
                source, target = self._graph.get_nodes(branch)

                # Although the Jacobian is calculated for the voltage difference over the branch, one can easily
                # prove that it can still be used to get the right Jacobian suited for the target problem. Assume
                # that the voltage over a branch v = b - a. b is the target voltage and a the source voltage. Our
                # problem is that we have df/dv at hand, but we need df/da and df/db instead.
                # Using substitution rule one can derive dv = db and dv = -da. Then we get
                # df/dv = df/db and -df/dv = df/da.
                if target in self._nodes:
                    jacobi_vector[self._nodes.index(target)] += jacobi[i]
                if source in self._nodes:
                    jacobi_vector[self._nodes.index(source)] += -jacobi[i]
            else:
                raise AssertionError(f'Unknown branch type encountered: {type(branch)}')

        return jacobi_vector

    def _create_coupled_v_i_vector(self,
                                   v_i: np.ndarray,
                                   coupled_branches: List[Union[VoltageBranch, CurrentBranch]]) -> np.ndarray:
        vec = []

        for branch in coupled_branches:
            if isinstance(branch, VoltageBranch):
                val = v_i[self._currents.index(branch) + len(self._nodes)]
            elif isinstance(branch, CurrentBranch):
                source, target = self._graph.get_nodes(branch)
                val = (
                    # If the nodes are not there, they were classified as reference nodes and would have a value of
                    # zero.
                    (v_i[self._nodes.index(target)] if target in self._nodes else 0) -
                    (v_i[self._nodes.index(source)] if source in self._nodes else 0)
                )
            else:
                raise AssertionError(f'Unknown branch type encountered: {type(branch)}')

            vec.append(val)

        return np.array(vec)

    def evaluate(self, v_i: np.ndarray, t1: float, t2: float) -> np.ndarray:
        """
        Evaluates the equation stack.

        :param v_i:
            The voltages (measured in Volts) and branch consecutive currents (measured in Ampere) as input.
        :param t1:
            Previous point in time (measured in seconds).
        :param t2:
            Present point in time (measured in seconds).
        :return:
            The result.
        """
        out_vector = []

        for kirchhoff_equation in self._kirchhoff_equations:
            summation = 0.0

            for term in kirchhoff_equation.terms:
                if isinstance(term, KirchhoffEquationTerm):
                    summation += (-1 if term.negative else 1) * term.branch.get_current(
                        self._create_coupled_v_i_vector(v_i, term.coupled_branches),
                        t1,
                        t2,
                    )
                elif isinstance(term, KirchhoffEquationBranchConsecutiveTerm):
                    summation += (
                        (-1 if term.negative else 1) *
                        v_i[self._currents.index(term.branch) + len(self._nodes)]
                    )
                else:
                    raise AssertionError(f'Invalid term type encountered: {type(term)}')

            out_vector.append(summation)

        for branch_consecutive_equation in self._branch_consecutive_equations:
            source, target = branch_consecutive_equation.potentials

            out_vector.append(
                branch_consecutive_equation.branch.get_voltage(
                    self._create_coupled_v_i_vector(v_i, branch_consecutive_equation.coupled_branches),
                    t1,
                    t2,
                )
                + (v_i[self._nodes.index(source)] if source in self._nodes else 0)
                - (v_i[self._nodes.index(target)] if target in self._nodes else 0)
            )

        return np.array(out_vector)

    def get_voltage_between_nodes(self, solution: np.ndarray, source, target):
        """
        Returns the voltage between two nodes from a calculated solution.

        :param solution:
            The solution vector.
        :param source:
            The source node.
        :param target:
            The target node.
        :return:
            The voltage between `source` and `target` nodes.
        """
        return (
            (solution[self._nodes.index(target)] if target in self._nodes else 0) -
            (solution[self._nodes.index(source)] if source in self._nodes else 0)
        )

    def get_voltage(self, solution: np.ndarray, branch: CurrentBranch):
        """
        Returns the voltage for a given current-branch from a calculated solution.

        Since only this stack knows how branches and their voltages and currents are tracked in the solution vector,
        use this function afterwards to reassign those values back to the actual branches.

        :param solution:
            The solution vector.
        :param branch:
            The current-branch to get the voltage for.
        :return:
            The voltage for `branch`.
        """
        source, target = self._graph.get_nodes(branch)
        return self.get_voltage_between_nodes(solution, source, target)

    def get_current(self, solution: np.ndarray, branch: VoltageBranch):
        """
        Returns the current for a given voltage-branch from a calculated solution.

        Since only this stack knows how branches and their voltages and currents are tracked in the solution vector,
        use this function afterwards to reassign those values back to the actual branches.

        :param solution:
            The solution vector.
        :param branch:
            The voltage-branch to get the current for.
        :return:
            The current for `branch`.
        """
        return solution[self._currents.index(branch) + len(self._nodes)]

    def _create_lambdified_coupled_v_i_vector(self, coupled_branches: List[Union[VoltageBranch, CurrentBranch]]) -> List[str]:
        coupled_entries = []

        for branch in coupled_branches:
            if isinstance(branch, VoltageBranch):
                coupled_val = f'v_i[{self._currents.index(branch) + len(self._nodes)}]'
            elif isinstance(branch, CurrentBranch):
                source, target = self._graph.get_nodes(branch)

                coupled_val = ''
                if target in self._nodes:
                    coupled_val += f'v_i[{self._nodes.index(target)}]'
                if source in self._nodes:
                    coupled_val += f'-v_i[{self._nodes.index(source)}]'
            else:
                raise AssertionError(f'Unknown branch type encountered: {type(branch)}')

            coupled_entries.append(coupled_val)

        return coupled_entries

    def lambdify(self):
        """
        Optimizes the MNA equation stack by returning a lambdified expression.

        This function compiles a Python function that immediately computes `evaluate()`.

        Note that the returned object is immediately callable and does not have an `evaluate()` member function.
        Also later updates on the instance of the MNA equation stack will not reflect into already lambdified
        expressions. In this case it has to be recompiled.

        :return:
            A function that is callable like `evaluate()` and behaves exactly like it.
        """
        mapped_branches = OrderedSet()
        code_globals = {'branches': mapped_branches}

        vector_entries = []

        for equation in self._kirchhoff_equations:
            terms = []

            for term in equation.terms:
                if isinstance(term, KirchhoffEquationTerm):
                    val = (f'branches[{mapped_branches.add(term.branch)}]'
                           f'.get_current(np.array(['
                           f'{",".join(self._create_lambdified_coupled_v_i_vector(term.coupled_branches))}'
                           f']),t1,t2)')

                elif isinstance(term, KirchhoffEquationBranchConsecutiveTerm):
                    val = f'v_i[{self._currents.index(term.branch) + len(self._nodes)}]'
                else:
                    raise AssertionError(f'Unexpected equation term type: {type(term)}')

                if term.negative:
                    val = '-' + val

                terms.append(val)

            vector_entries.append('+'.join(terms))

        for equation in self._branch_consecutive_equations:
            source, target = equation.potentials
            vector_entries.append(
                f'branches[{mapped_branches.add(equation.branch)}]'
                f'.get_voltage(np.array(['
                f'{",".join(self._create_lambdified_coupled_v_i_vector(equation.coupled_branches))}'
                f']),t1,t2)'
                f'{f"+v_i[{self._nodes.index(source)}]" if source in self._nodes else ""}'
                f'{f"-v_i[{self._nodes.index(target)}]" if target in self._nodes else ""}'
            )

        code = [
            'import numpy as np',
            'def eq(v_i: np.ndarray, t1: float, t2: float) -> np.ndarray:',
            ' return np.array([',
        ] + [entry + ',' for entry in vector_entries] + [
            ' ])',
        ]

        # Compile the expression and get back the set up eq() function.
        code_object = compile('\n'.join(code), '<lambdified-mna-equation-stack>', 'exec')
        exec(code_object, code_globals)
        return code_globals['eq']

    def jacobian(self, v_i: np.ndarray, t1: float, t2: float) -> np.ndarray:
        """
        Evaluates the Jacobian of the equation stack.

        :param v_i:
            The voltages (measured in Volts) and branch consecutive currents (measured in Ampere) as input.
        :param t1:
            Previous point in time (measured in seconds).
        :param t2:
            Present point in time (measured in seconds).
        :return:
            The result.
        """
        jacobi_matrix = []

        for kirchhoff_equation in self._kirchhoff_equations:
            jacobi_vector = np.zeros(len(self))

            for term in kirchhoff_equation.terms:
                if isinstance(term, KirchhoffEquationTerm):
                    jacobi_vector += (-1 if term.negative else 1) * self._expand_jacobi_vector(
                        term.branch.get_jacobian(
                            self._create_coupled_v_i_vector(v_i, term.coupled_branches),
                            t1,
                            t2,
                        ),
                        term.coupled_branches,  # TODO Maybe I should move all this into a function, since I reuse coupled_branches twice.
                    )
                elif isinstance(term, KirchhoffEquationBranchConsecutiveTerm):
                    jacobi_vector[self._currents.index(term.branch) + len(self._nodes)] += 1.0
                else:
                    raise AssertionError(f'Invalid term type encountered: {type(term)}')

            jacobi_matrix.append(jacobi_vector)

        for branch_consecutive_equation in self._branch_consecutive_equations:
            jacobi_vector = np.zeros(len(self))

            source, target = branch_consecutive_equation.potentials

            jacobi_vector += self._expand_jacobi_vector(
                branch_consecutive_equation.branch.get_jacobian(
                    self._create_coupled_v_i_vector(v_i, branch_consecutive_equation.coupled_branches),
                    t1,
                    t2,
                ),
                branch_consecutive_equation.coupled_branches,  # TODO Maybe I should move all this into a function, since I reuse coupled_branches twice.
            )

            # We have 2 additional entries for branch consecutive equations: 1 and -1
            # respectively for source and target voltage Jacobians.
            if source in self._nodes:
                jacobi_vector[self._nodes.index(source)] = 1.0
            if target in self._nodes:
                jacobi_vector[self._nodes.index(target)] = -1.0

            jacobi_matrix.append(jacobi_vector)

        return np.array(jacobi_matrix)

    def lambdify_jacobian(self):
        mapped_branches = OrderedSet()
        code_globals = {'branches': mapped_branches}

        jacobi_matrix = []

        for kirchhoff_equation in self._kirchhoff_equations:
            jacobi_vector = [[] for _ in range(len(self))]

            for term in kirchhoff_equation.terms:
                if isinstance(term, KirchhoffEquationTerm):
                    jacobi = f'{"-" if term.negative else ""}jacobians[{mapped_branches.add(term.branch)}]'

                    for i, branch in enumerate(term.coupled_branches):
                        jacobi_value = f'{jacobi}[{i}]'
                        if isinstance(branch, VoltageBranch):
                            jacobi_vector[self._currents.index(branch) + len(self._nodes)].append(jacobi_value)
                        elif isinstance(branch, CurrentBranch):
                            source, target = self._graph.get_nodes(branch)
                            if target in self._nodes:
                                jacobi_vector[self._nodes.index(target)].append(jacobi_value)
                            if source in self._nodes:
                                jacobi_vector[self._nodes.index(source)].append('-' + jacobi_value)
                        else:
                            raise AssertionError(f'Unknown branch type encountered: {type(branch)}')
                elif isinstance(term, KirchhoffEquationBranchConsecutiveTerm):
                    jacobi_vector[self._currents.index(term.branch) + len(self._nodes)].append('1')
                else:
                    raise AssertionError(f'Invalid term type encountered: {type(term)}')

            jacobi_matrix.append(jacobi_vector)

        for branch_consecutive_equation in self._branch_consecutive_equations:
            jacobi_vector = [[] for _ in range(len(self))]

            source, target = branch_consecutive_equation.potentials

            jacobi = f'jacobians[{mapped_branches.add(branch_consecutive_equation.branch)}]'

            for i, branch in enumerate(branch_consecutive_equation.coupled_branches):
                jacobi_value = f'{jacobi}[{i}]'
                if isinstance(branch, VoltageBranch):
                    jacobi_vector[self._currents.index(branch) + len(self._nodes)].append(jacobi_value)
                elif isinstance(branch, CurrentBranch):
                    source, target = self._graph.get_nodes(branch)
                    if target in self._nodes:
                        jacobi_vector[self._nodes.index(target)].append(jacobi_value)
                    if source in self._nodes:
                        jacobi_vector[self._nodes.index(source)].append('-' + jacobi_value)
                else:
                    raise AssertionError(f'Unknown branch type encountered: {type(branch)}')

            if source in self._nodes:
                jacobi_vector[self._nodes.index(source)].append('1')
            if target in self._nodes:
                jacobi_vector[self._nodes.index(target)].append('-1')

            jacobi_matrix.append(jacobi_vector)

        precalculated_jacobians = [
            (f'branches[{i}].get_jacobian(np.array(['
             f'{",".join(self._create_lambdified_coupled_v_i_vector(self._coupling_dictionary[branch]))}'
             f']),t1,t2)')
            for i, branch in enumerate(mapped_branches)
        ]

        jacobi_matrix_rows = [
            f'[{",".join("+".join(column if column else ["0"]) for column in row)}]'
            for row in jacobi_matrix
        ]

        code = [
            f'import numpy as np',
            f'def jac(v_i: np.ndarray, t1: float, t2: float) -> np.ndarray:',
            f' jacobians = [{",".join(precalculated_jacobians)}]',
            f' return np.array([{",".join(jacobi_matrix_rows)}])',
        ]

        # Compile the expression and get back the set up eq() function.
        code_object = compile('\n'.join(code), '<lambdified-mna-equation-stack-jacobian>', 'exec')
        exec(code_object, code_globals)
        return code_globals['jac']
