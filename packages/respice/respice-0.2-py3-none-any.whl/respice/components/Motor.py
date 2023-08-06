from dataclasses import dataclass
from typing import Callable

from .TwoTerminalCurrentComponent import TwoTerminalCurrentComponent


@dataclass(eq=False)
class Motor(TwoTerminalCurrentComponent):
    r"""
    Describes a motor model (without back-EMF) according to following model:

    .. math::

            K_t i - T_L = J \dot \omega + D \omega

    where :math:`i` denotes input current.

    The model supports an additional load torque, which can be an arbitrary function of time.

    R:
        Terminal resistance measured in Ohm (:math:`\Omega`).
    L:
        Internal inductance measured in Henry (:math:`H`).
    KT:
        Torque constant measured in :math:`Nm / A`.
    J:
        Moment of inertia of rotor measured in :math:`kg \cdot m^2`.
    D:
        Damping constant due to viscous friction in :math:`Nm`.
    TL:
        A time-(only)-variate function specifying a load-torque depending on time. By default 0.
    state_voltage:
        The initial voltage of the motor. By default 0.
    state_current:
        The initial current of the motor. By default 0.
    state_angular_frequency:
        The initial angular frequency of the motor axis. By default 0.
    """

    R: float
    L: float
    KT: float
    J: float
    D: float
    TL: Callable[[float], float] = lambda t: 0
    state_voltage: float = 0
    state_current: float = 0
    state_angular_frequency: float = 0

    def get_current(self, v: float, t1: float, t2: float) -> float:
        dt = t2 - t1
        return (
            (self.state_current + 0.5 * dt / self.L * (self.state_voltage + v - self.R * self.state_current)) /
            (1 + 0.5 * dt * self.R / self.L)
        )

    def get_jacobian(self, v: float, t1: float, t2: float) -> float:
        dt = t2 - t1
        return dt / (2 * self.L + dt * self.R)

    def get_angular_frequency(self, i: float, t1: float, t2: float) -> float:
        dt = t2 - t1
        return (
            (self.state_angular_frequency + 0.5 * dt / self.J *
             (self.KT * (self.state_current + i) -
              self.TL(t1) - self.TL(t2) -
              self.D * self.state_angular_frequency)) /
            (1 + 0.5 * dt * self.D / self.J)
        )

    def update(self, v: float, t1: float, t2: float):
        # Calculation of angular frequency requires the old state values, so don't set them yet.
        i = self.get_current(v, t1, t2)
        self.state_angular_frequency = self.get_angular_frequency(i, t1, t2)

        self.state_current = i
        self.state_voltage = v

    @property
    def state(self):
        return self.state_current, self.state_voltage, self.state_angular_frequency

    @state.setter
    def state(self, val):
        self.state_current, self.state_voltage, self.state_angular_frequency = val
