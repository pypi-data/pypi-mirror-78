import math
import warnings
from typing import Callable, Hashable, List

import numpy as np
from scipy.optimize import root, OptimizeResult

from respice.collections import OneToManyInvertibleMapping
from respice.components import Branch, Component
from respice.components.Branch import CurrentBranch, VoltageBranch
from respice.itertools import pairwise, flatten
from respice.itertools.custom import compact, uncompact
from .MNAEquationStack import MNAEquationStack
from .TransientSimulationResult import TransientSimulationResult
from .TransientSteadyStateSimulationResult import TransientSteadyStateSimulationResult
from .UniqueEdgeMultiDiGraph import UniqueEdgeMultiDiGraph


class UnmetPrecisionWarning(UserWarning):
    def __init__(self, msg: str, result: OptimizeResult):
        super().__init__(msg)

        self.result = result


class Circuit:
    def __init__(self):
        self._graph = UniqueEdgeMultiDiGraph()

        # Enforces uniqueness of elements across all graph edges (additionally, since uniqueness is effectively already
        # enforced by the special MultiDiGraph type used, because same branches of components can't be added twice as
        # well). Since adding the same component twice would cause the data in its branches to become mixed up, since
        # multiple results get appended to the same branch instance.
        self._component_branches = OneToManyInvertibleMapping()

    def add(self, component: Component, *terminals: Hashable):
        """
        Adds a new component to the circuit.

        :param component:
            The component to connect.
        :param terminals:
            The nodes/potentials to connect the component to. See each component's documentation about the order of
            each terminal to be specified.
        """
        if component in self._component_branches:
            raise KeyError(f'given component {repr(component)} already added to circuit.')

        component_branches = component.connect(*terminals)

        for source, target, branch in component_branches:
            self._component_branches[component] = branch
            self._graph.add_edge(source, target, branch)

    def remove(self, component: Component):
        """
        Removes a component from the circuit.

        If the component does not exists, this function is a no-op.

        :param component:
            The component to remove from the circuit.
        """
        if component in self._component_branches:
            for branch in self._components_branches[component]:
                self._graph.remove_edge(branch)

        del self._component_branches[component]

    @property
    def components(self):
        """
        :return:
            All components added to this circuit.
        """
        return self._component_branches.keys()

    def _get_coupled_branches(self, branch: Branch) -> List[Branch]:
        component = self._component_branches.reverse[branch]
        return self._component_branches[component]

    def _disturb_solution(self, trial: int, solution: OptimizeResult, factor_multiplier=100) -> np.ndarray:
        """
        Disturbs the result of a solution. This function is used when retrying the solution because convergence
        didn't succeed and has gotten so worse that the solver stops further trying. Trying with a different starting
        point is the recommended method.

        This function specifically applies relative disturbance and considers the direction of the Jacobian matrix
        to effectively over-shoot the current (non-converged) solution. The higher the trial number, the higher
        the overshooting.

        :param trial:
            The current trial number (starts from 1).
        :param solution:
            The `OptimizationResult` as received from `scipy.optimize.root`.
        :param factor_multiplier:
            The disturbance factor to the trial.
        :return:
            The disturbed solution vector.
        """
        directional_multiplier = np.array([(-1 if v < 0 else 1) for v in solution.fjac @ solution.x])
        return directional_multiplier * factor_multiplier**trial * solution.x

    def _solve(self, eq: Callable, x0: np.ndarray, args=tuple(), jac=None) -> OptimizeResult:
        """
        Attempts to solve the given electrical-circuit-governing system equation.

        Additionally employs retries if convergence tolerances are not reached with different starting points
        utilizing `_disturb_solution`. If `_disturb_solution` does yield conversion to the same (or rather very close
        point), then again a retry is attempted, but with a point that's more far away. If other points are hit that
        still don't fulfill convergence restrictions, retries are attempted on them as well. Retries are tracked per
        solution, so in case that we encounter cycles where we jump to different but non-satisfying solutions and come
        back to a solution we already had, `_disturb_solution` will attempt a different start vector never used before
        to not end up in useless wastes of trials.

        By default int((math.log10(len(start_vector)) + 1) * 4) trials will be attempted if needed, so for larger
        systems more points are investigated for bad convergence. To not increase evaluation time too much, the
        logarithm is used to only scale to the order of the system.

        :param eq:
            The system equation function to solve.
        :param t1:
            Previous point in time (measured in seconds).
        :param t2:
            Present point in time (measured in seconds).
        :param x0:
            The initial start vector.
        :param:
            The Jacobian (function) of eq.
        :return:
            The best found result to the system.
        """
        unsatisfying_results = []
        trials = {}
        retries = int((math.log10(len(x0)) + 1) * 4)
        for trial in range(retries):
            result = root(
                eq,
                x0,
                args=args,
                method='hybr',
                jac=jac,
            )

            if result.success:
                break

            unsatisfying_results.append(result)

            # Result disturbance is a bit smarter and resets the trial count if we really found a different point,
            # so in case the next different value again does not converge, we do not overshoot extremely just because
            # this happened at a high trial count. However, if we might re-encounter the same solution, then the old
            # trial count gets restored again. That ensures that we really always try out new values and aren't driven
            # into useless re-evaluation of the same points until all trials are exhausted.
            for solution in trials:
                if math.isclose(np.linalg.norm(solution), np.linalg.norm(result.x)):
                    trials[solution] += 1
                    result_trials = trials[solution]
                    break
            else:
                trials[tuple(result.x)] = 1  # numpy arrays are not hashable, so we produce a hashable vector.
                result_trials = 1

            x0 = self._disturb_solution(result_trials, result)
        else:
            # Filter out best result closest to zero.
            result = min(unsatisfying_results, key=lambda x: np.linalg.norm(x.fun))

            warnings.warn(UnmetPrecisionWarning(
                'Failed to converge after several retries. Taking the closest result as granted.',
                result,
            ))

        return result

    def simulate(self, ts1: float, ts2: float, steps: int):
        """
        Perform a circuit simulation.

        States after a simulation remain. This means you can chain simulations
        together altering parameters in between (for example turning off a voltage supply by removing
        it from the circuit or changing a resistance value).

        :param ts1:
            Initial point in time to start simulation from.
        :param ts2:
            Point in time to simulate up to.
        :param steps:
            The number of steps to simulate between `t1` and `t2`.
        :return:
            A `TransientSimulationResult` object containing the result of the simulation.
        """
        master_equation = MNAEquationStack(self._graph, self._component_branches.values())

        # Performance improvement: Lambdify equations by compiling a real Python expression out of them. This now
        # becomes a plain callable instead of having an evaluate() function.
        optimized_master_equation = master_equation.lambdify()
        optimized_jacobian = master_equation.lambdify_jacobian()

        ts = np.linspace(ts1, ts2, steps + 1)

        x0 = np.zeros(len(master_equation))
        results = []
        branch_results_v = {branch: [] for branch in self._component_branches.reverse.keys()}
        branch_results_i = {branch: [] for branch in self._component_branches.reverse.keys()}
        state_results = {component: [] for component in self._component_branches}
        for t1, t2 in pairwise(ts):
            result = self._solve(
                optimized_master_equation,
                x0,
                args=(t1, t2),
                jac=optimized_jacobian,
            ).x

            results.append(result)

            # Behaviour is usually smooth, so use the last result as a starting point for next evaluation.
            x0 = result

            # Map back calculated voltages and currents to actual elements.
            for component in self._component_branches:
                coupled_v_i = []
                for coupled_branch in self._component_branches[component]:
                    if isinstance(coupled_branch, CurrentBranch):
                        val = master_equation.get_voltage(result, coupled_branch)
                    elif isinstance(coupled_branch, VoltageBranch):
                        val = master_equation.get_current(result, coupled_branch)
                    else:
                        raise AssertionError(f'Unknown branch type encountered: f{type(coupled_branch)}')

                    coupled_v_i.append(val)

                coupled_v_i = np.array(coupled_v_i)

                for branch in self._component_branches[component]:
                    if isinstance(branch, CurrentBranch):
                        v = master_equation.get_voltage(result, branch)
                        i = branch.get_current(coupled_v_i, t1, t2)
                        branch.update(v, coupled_v_i, t1, t2)
                    elif isinstance(branch, VoltageBranch):
                        i = master_equation.get_current(result, branch)
                        v = branch.get_voltage(coupled_v_i, t1, t2)
                        branch.update(i, coupled_v_i, t1, t2)
                    else:
                        raise AssertionError(f'Unknown branch type encountered: f{type(branch)}')

                    branch_results_v[branch].append(v)
                    branch_results_i[branch].append(i)

                # Save state results now that components are updated.
                state_results[component].append(component.state)

        # The current simulation result class requires to additionally pass the results per branch
        # (branch_results_v and branch_results_i). In fact, they are redundant and can be calculated back from the
        # raw results by means of the master_equation. However, it's faster to pass them again as they are being
        # calculated regardless above. In the future the result might become simplified and improved to avoid this
        # redundancy while still maintaining performance.
        # See https://gitlab.com/Makman2/respice/-/issues/58.
        return TransientSimulationResult(
            self._component_branches,
            master_equation,
            ts[1:],
            results,
            branch_results_v,
            branch_results_i,
            state_results,
        )

    def simulate_efm(self, t0: float, T: float, interval_steps: int, skips: List[int]):
        """
        Simulates the circuit using the envelope-following-method (EFM).

        The EFM is beneficial to analyze systems faster with the trade-off of accuracy.
        With appropriate parameters and a suitable circuit this method can simulate significantly faster.
        This is especially beneficial for multi-rate systems with highly different intrinsical frequencies.

        The EFM requires you to know the intrinsical period time T where jumps can be properly made from.
        After that you define how many steps a single interval is simulated with and how many skips (`m`) should be
        performed.
        With this information the EFM performs skips according to following implicit equation:

        .. math::

            f(t + m T) = f(t) + \\frac12 m [f(t+T) - f(t) + f(t + (m+1) T) - f(t + mT)]

        The solution is then the so called "envelope", the guiding solution of the system.

        You can choose arbitrary consecutive skips organized in a list. If you simply want constant skipping, you can
        do `[s] * n` instead of writing out `[s, s, ..., s]`.

        For reference, see the paper at https://ieeexplore.ieee.org/document/4342106.

        :param t0:
            The initial time to start simulation from.
        :param T:
            Period time of a single interval.
        :param interval_steps:
            How many steps to simulate for a single interval.
        :param skips:
            Consecutive skips to perform encoded in a list.
        :return:
            A `TransientSimulationResult` object containing the result of the simulation.
        """

        if len(skips) <= 0:
            raise ValueError('skips must contain at least one value')
        if interval_steps < 1:
            raise ValueError('interval_steps must be greater than 1')

        sims = []

        # shorthand prefixes for variables: li -> left interval, ri -> right interval

        li_ts1 = t0
        for s in skips:
            m = s + 1  # The skip parameter used inside equations below.

            li_ts2 = li_ts1 + T

            li_state1, state_compactification = compact([component.state for component in self.components])
            li_state1 = np.array(li_state1)
            sim = self.simulate(li_ts1, li_ts2, interval_steps)
            li_state2, _ = compact([component.state for component in self.components])
            li_state2 = np.array(li_state2)
            li_state_delta = li_state2 - li_state1

            sims.append(sim)

            ri_ts1 = li_ts1 + m * T
            ri_ts2 = ri_ts1 + T

            def efm_equation(ri_state1):
                for component, state in zip(self.components, uncompact(ri_state1, state_compactification)):
                    component.state = state

                ri_state1 = np.array(ri_state1)
                self.simulate(ri_ts1, ri_ts2, interval_steps)
                ri_state2, _ = compact([component.state for component in self.components])
                ri_state2 = np.array(ri_state2)
                ri_state_delta = ri_state2 - ri_state1

                # The equations are an adjusted version with better solution consistency.
                # Instead of calculating up to the end of the second interval, the efm-equations have to hold only up to
                # the beginning of the second interval. Effectively, m was changed from the original m to m - 1.
                return li_state1 - ri_state1 + m * 0.5 * (li_state_delta + ri_state_delta)

            initial_guess = li_state1 + m * li_state_delta  # Initial guess by forward euler approximation.
            satisfying_state = self._solve(efm_equation, initial_guess).x

            states = uncompact(satisfying_state, state_compactification)
            for component, state in zip(self.components, states):
                component.state = state

            li_ts1 = ri_ts1

        # With steps > 0 being enforced above, referencing i won't cause any problems. The loop runs at least once.
        li_ts2 = li_ts1 + T
        sim = self.simulate(li_ts1, li_ts2, interval_steps)

        sims.append(sim)

        # FIXME Accessing "protected" underscored members is not ideal, but currently I don't have any other nice idea.
        return TransientSimulationResult(
            sims[0]._components_to_branches,
            sims[0]._mna_equation,
            list(flatten(sim.get_timesteps() for sim in sims)),
            list(flatten(sim._raw_solutions for sim in sims)),
            {branch: list(flatten(sim.get_voltages(branch) for sim in sims)) for branch in self._component_branches.reverse},
            {branch: list(flatten(sim.get_currents(branch) for sim in sims)) for branch in self._component_branches.reverse},
            {component: list(flatten(sim.get_states(component) for sim in sims)) for component in self._component_branches},
        )

    def steadystate(self, T, steps, t0=0):
        """
        Finds the periodic steady-state solution of the circuit.

        Periodic steady-states occur for example for all linear circuits where complex analysis can be applied
        (i.e. circuits with sinusoidal sources, resistors, capacitors, inductors).
        This function requires you to pass ahead a suitable period `T` that denotes the circuit system's period time.
        For multivariate circuits (i.e. with many sinusoidal sources), `T` becomes the least common multiple of all
        those period times Ts (the least common multiple is here extended to rational numbers - for non-rational
        frequencies, T can be approximated by rationalizing).

        The steady-state result is stored as a single period simulation inside the circuit's components and can be
        accessed exactly like with `simulate`. If the state-solution itself is of interest, respective states can
        be queried by using `component.state`.

        :param T:
            The circuit system's characteristic period time `T`.
        :param steps:
            Steps to simulate per period `T`.
            For sinusoidal sources, can be approximately set to `10 * T / min(Ts)`.
        :param t0:
            Initial time to start simulation from.
        """
        state0, state_compactification = compact([component.state for component in self.components])

        ts1 = t0
        ts2 = t0 + T

        def problem(compacted_state):
            states = uncompact(compacted_state, state_compactification)

            for component, state in zip(self.components, states):
                component.state = state

            self.simulate(ts1, ts2, steps)

            new_state, _ = compact([component.state for component in self.components])

            return compacted_state - np.array(new_state)

        state_result = self._solve(problem, state0).x

        states = uncompact(state_result, state_compactification)
        for component, state in zip(self.components, states):
            component.state = state

        sim = self.simulate(ts1, ts2, steps)
        return TransientSteadyStateSimulationResult.init_from(sim)

    def multivariate_steadystate(self, t0, T_fast, T_slow, T_fast_steps=10, subdivisions=8):
        """
        Finds the periodic steady-state solution of the circuit using the envelope-following-method (EFM) for
        multivariate systems (in particular dual-variate systems).

        Periodic steady-states occur for example for all linear circuits where complex analysis can be applied
        (i.e. circuits with sinusoidal sources, resistors, capacitors, inductors).
        This function requires you to pass ahead a suitable period `T` that denotes the circuit system's period time.
        For multivariate circuits (i.e. with many sinusoidal sources), `T` becomes the least common multiple of all
        those period times Ts (the least common multiple is here extended to rational numbers - for non-rational
        frequencies, T can be approximated by rationalizing).

        In contrast to a single-variate system, dual-variate systems have two intrinsic frequencies. If they are
        vastly different, simulation can be extremely time-consuming because the fastest frequency has to be simulated
        in accordance to not miss out on its effects.
        Usually, such systems "main behavior" is only slightly influenced by the fast-rate frequency. For this case,
        the EFM can be utilized and many fast-rate intervals can be safely skipped to increase performance without
        missing on accuracy.

        For the EFM-equations, see method `simulate_efm`.

        For reference, see the paper at https://ieeexplore.ieee.org/document/4342106.

        :param t0:
            The starting time.
        :param T_fast:
            The fast-rate period time.
        :param T_slow:
            The slow-rate period time.
        :param T_fast_steps:
            The steps to simulate inside a single fast-rate interval.
        :param subdivisions:
            How many steps shall be simulated via EFM inside the slow-rate interval.
            Effectively determines the skip intervals for the EFM.
        :return:
            A simulation result containing the steady-state solution.
        """
        if subdivisions < 0:
            raise ValueError('parameter subdivisions must be 0 or greater')

        # Quantization step to find properly aligned intervals / skips that can be used for EF-method.
        subdivisions = min(subdivisions, T_slow // T_fast - 2)  # To avoid duplicate time steps.
        skips = np.diff(np.floor(np.linspace(0, T_slow // T_fast - 1, subdivisions + 2))) - 1

        state0, state_compactification = compact([component.state for component in self.components])

        def problem(first_interval_state):
            states = uncompact(first_interval_state, state_compactification)
            for component, state in zip(self.components, states):
                component.state = state

            self.simulate_efm(t0, T_fast, T_fast_steps, skips)

            final_interval_state, _ = compact([component.state for component in self.components])
            final_interval_state = np.array(final_interval_state)
            return first_interval_state - final_interval_state

        steadystate_vector = self._solve(problem, state0).x

        states = uncompact(steadystate_vector, state_compactification)
        for component, state in zip(self.components, states):
            component.state = state

        sim = self.simulate_efm(t0, T_fast, T_fast_steps, skips)
        return TransientSteadyStateSimulationResult.init_from(sim)
