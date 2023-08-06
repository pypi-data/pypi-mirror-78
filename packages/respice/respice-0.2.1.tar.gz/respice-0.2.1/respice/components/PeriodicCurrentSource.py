from dataclasses import dataclass, field
from math import pi

from .TwoTerminalCurrentComponent import TwoTerminalCurrentComponent


@dataclass(eq=False)
class PeriodicCurrentSource(TwoTerminalCurrentComponent):
    """
    A periodic current supply.

    This class is a building block to define your own voltage/current invariant periodic sources easily. Subclasses
    override the `get_signal()` function that supplies the signal values inside a single period.

    frequency:
        The current frequency (measured in Hertz).
    phase:
        The initial phase angle (measured in rad).
    """
    frequency: float = 1.0
    phase: float = 0.0

    def get_current(self, v: float, t1: float, t2: float) -> float:
        phi = t2 * 2 * pi * self.frequency + self.phase
        return self.get_signal(phi % (2 * pi))

    def get_jacobian(self, v: float, t1: float, t2: float) -> float:
        return 0

    def get_signal(self, phase):
        """
        Returns the signal.

        :param phase:
            The momentary angular phase, inside the range [0, 2pi).
        :return:
            The signal value at `phase`.
        """
        raise NotImplementedError
