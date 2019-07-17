import logging
from typing import Tuple

import numpy as np

from problems.test_case import TestCase, TestCaseTypeEnum, test_case_solution_correct
from problems.solutions.rocket_science import rocket_fuel

logger = logging.getLogger(__name__)

FUNCTION_NAME = "rocket_fuel"
INPUT_VARS = ['v']
OUTPUT_VARS = ['m_fuel']

STATIC_RESOURCES = []

PHYSICAL_CONSTANTS = {
    'v_e': 2550,  # [m/s]
    'M': 250000   # [kg]
}

ATOL = {}
RTOL = {
    'm_fuel': 1e-6
}


class TestCaseType(TestCaseTypeEnum):
    EARTH = ('Earth', 1)
    MOON = ('Moon', 1)
    JUPITER = ('Jupiter', 1)
    PLUTO = ('Pluto', 1)
    PHOBOS = ('Phobos', 1)
    RANDOM = ('Random', 1)


class ProblemTestCase(TestCase):
    def input_tuple(self) -> tuple:
        return self.input['v'],

    def output_tuple(self) -> tuple:
        return self.output['m_fuel'],

    def output_str(self) -> str:
        return str(self.output['m_fuel'])


def generate_test_case(test_type: TestCaseType) -> ProblemTestCase:
    test_case = ProblemTestCase(test_type)

    if test_type is TestCaseType.EARTH:
        v = 11186

    elif test_type is TestCaseType.MOON:
        v = 2380

    elif test_type is TestCaseType.JUPITER:
        v = 60200

    elif test_type is TestCaseType.PLUTO:
        v = 1230

    elif test_type is TestCaseType.PHOBOS:
        v = 1.139

    elif test_type is TestCaseType.RANDOM:
        v = float(np.random.uniform(1.0, 100.0, 1)[0])

    test_case.input['v'] = v
    return test_case


def solve_test_case(test_case: ProblemTestCase) -> None:
    v = test_case.input['v']
    test_case.output['m_fuel'] = rocket_fuel(v)


def verify_user_solution(user_input: tuple, user_output: tuple) -> Tuple[bool, str]:
    user_test_case = ProblemTestCase(None, INPUT_VARS, user_input, OUTPUT_VARS, user_output)
    passed, correct_test_case = test_case_solution_correct(user_test_case, ATOL, RTOL, ProblemTestCase, solve_test_case)
    return passed, correct_test_case.output_str()
