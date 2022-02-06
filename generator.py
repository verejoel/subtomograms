from cmath import pi
from math import degrees

import numpy as np


class Generator(object):
    def __init__(
        self,
        subtomograms: int,
        projections_per_subtomogram: int,
        full_circle: bool = True,
        degrees: bool = True,
    ):
        # subtomograms must be a power of 2
        self.M = subtomograms
        self.N = projections_per_subtomogram
        self.total_projections = self.M * self.N

        # total angle is either 2pi or pi
        self.full_circle = 360 if degrees else 2 * np.pi
        self.total_angle = self.full_circle if full_circle else 0.5 * self.full_circle


class GoldenRatio(Generator):
    """Generator for subtomograms"""

    PHI = 0.5 * (1 + np.sqrt(5))

    def __init__(
        self,
        subtomograms: int,
        projections_per_subtomogram: int,
        full_circle: bool = True,
        degrees: bool = True,
        wrap: bool = False,
    ):
        super().__init__(
            subtomograms, projections_per_subtomogram, full_circle, degrees
        )
        self.wrap = wrap
        print(self.PHI)

    def generate_angles(self):
        i_vec = np.arange(self.total_projections)
        theta_vec = (self.PHI * np.pi * i_vec) % np.pi
        print(theta_vec)


class BinaryGenerator(Generator):
    def __init__(
        self,
        subtomograms: int,
        projections_per_subtomogram: int,
        full_circle: bool = True,
        degrees: bool = True,
    ):
        super().__init__(
            subtomograms, projections_per_subtomogram, full_circle, degrees
        )

        # psi_d represents the angular increment between chronologically consequent projections
        self.psi_d = self.total_angle / self.N

        # K is the topmost nesting level
        self.K = np.log2(self.M)
        if round(self.K) != self.K:
            raise ValueError("Number of subtomograms must be a power of 2")

        print(
            f"Initialised!\nTotal projections: {self.total_projections}\nStep size per subtomogram: {self.psi_d}\nTotal step size: {self.psi_d/self.M}"
        )

    def generate_sequence(self):
        self.A = np.array([0])
        for i in range(int(self.K)):
            self.A = np.append(self.A, self.A + self.M / 2 ** (i + 1))

    def generate_angles(self):
        try:
            len(self.A)
        except AttributeError:
            self.generate_sequence()

        self.angles = {}
        for i in range(len(self.A)):
            j = np.arange(self.N)
            angles = self.psi_d * (self.A[i] / self.M + j)
            self.angles[i] = angles
        print(self.angles)


# calculate step size within each subtomogram
# calculate total step size
