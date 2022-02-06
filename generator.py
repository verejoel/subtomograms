from cmath import pi
from math import degrees

import numpy as np


class Generator(object):
    # decimal places (for printed output)
    DP = 3

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


class GoldenGenerator(Generator):
    """Generator for subtomograms"""

    # golden ratio
    PHI = 0.5 * (1 + np.sqrt(5))

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

    def generate_angles(self):
        i_vec = np.arange(self.total_projections)
        p_vec = i_vec + 1
        self.angles = (self.PHI * 0.5 * self.full_circle * i_vec) % self.total_angle
        print(np.c_[p_vec, np.round(self.angles, self.DP)])

    def generate_subscans(self):
        # matrix of (i, j) tuples
        matrix = np.array([[(i, j) for j in range(self.N)] for i in range(self.M)])

        # vector for N
        vector = np.array([self.N, 1])
        self.subscans = (
            np.dot(matrix, vector) * self.PHI * 0.5 * self.full_circle
        ) % self.total_angle

    def sort_subscans(self):
        try:
            self.subscans.shape
        except AttributeError:
            self.generate_subscans()

        self.subscans.sort()

    def calculate_diffs(self):
        try:
            self.subscans.shape
        except AttributeError:
            self.generate_subscans()

        self.sort_subscans()
        self.subscan_diffs = np.diff(self.subscans)

    def calculate_entropy(self):
        try:
            self.subscan_diffs
        except AttributeError:
            self.calculate_diffs()

        # get the histogram of the diffs
        hist = np.histogram(self.subscan_diffs)

        # strip zeros and get the discrete PDF
        pdf = hist[0][hist[0] != 0] / hist[0].sum()

        # calculate information entropy for each bin
        h = pdf * np.log(pdf)

        # strip nan (arising from 0 histogram bins) and sum to get entropy
        self.H = -h.sum()

        return self.H


def entropy(i_vec, M=50):
    return np.vectorize(lambda n: GoldenGenerator(M, n).calculate_entropy())(i_vec)


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

    def print_angles(self):
        try:
            (len(self.angles))
        except AttributeError:
            self.generate_angles()

        print(f"Subtomogram\tAngles")
        for k, v in self.angles.items():
            print(f"{k}\t\t{np.round(v, self.DP)}")


# calculate step size within each subtomogram
# calculate total step size
