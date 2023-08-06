from dataclasses import dataclass
from math import sin, sqrt

from respice.components.PeriodicVoltageSource import PeriodicVoltageSource


@dataclass(eq=False)
class VoltageSourceAC(PeriodicVoltageSource):
    """
    An AC voltage supply.

    You might alternatively set the current amplitude by specifying an effective voltage.
    Be sure to assign to the property `effective_amplitude` after initialization.

    amplitude:
        The current amplitude of the sine emitted by the supply (measured in Amperes).
    """
    amplitude: float = 1.0

    @property
    def effective_amplitude(self):
        """
        The effective amplitude (:math:`A_{RMS}`) is easily derived
        according to the formula for RMS (see https://en.wikipedia.org/wiki/Root_mean_square and
        https://en.wikipedia.org/wiki/RMS_amplitude)

        .. math:
             A_{RMS} &= \sqrt{\frac{1}{T} \int_{0}^{T}{f^2(t) dt}} \\
                     &= A \cdot
                        \sqrt{
                            \frac{1}{2 \pi}
                                \left (
                                    \int_{0}^{T}{\sin^2{(\varphi)} d\varphi}
                                \right )
                            } \\
                     &= A / \sqrt{2}
        :return:
            The effective amplitude current (measured in Amperes).
        """
        return self.amplitude / sqrt(2)

    @effective_amplitude.setter
    def effective_amplitude(self, value: float):
        """
        Sets the amplitude of this supply by means of an effective value (RMS).

        This function just multiplies the given value with sqrt(2).

        .. math:
             A = \sqrt{2} \cdot A_{RMS}

        :param value:
            The effective amplitude value.
        """
        self.amplitude = value * sqrt(2)

    def get_signal(self, phase):
        return self.amplitude * sin(phase)
