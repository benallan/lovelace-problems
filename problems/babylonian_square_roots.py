import logging
from typing import Tuple

from numpy.random import uniform, randint

from problems.test_case import TestCase, TestCaseTypeEnum, test_case_solution_correct
from problems.solutions.babylonian_square_roots import babylonian_sqrt

logger = logging.getLogger(__name__)

FUNCTION_NAME = "babylonian_sqrt"
INPUT_VARS = ['n']
OUTPUT_VARS = ['sqrt_n']

STATIC_RESOURCES = []

PHYSICAL_CONSTANTS = {}
ATOL = {}
RTOL = {
    'sqrt_n': 1e-10
}


class TestCaseType(TestCaseTypeEnum):
    ZERO = ("zero", 1)
    NEGATIVE = ("negative number", 1)
    SMALL = ("1 < n < 10", 2)
    LARGE = ("10 < n < 1,000,000", 2)
    SQUARE = ("square number", 1)


class ProblemTestCase(TestCase):
    def input_tuple(self) -> tuple:
        return self.input['n'],

    def output_tuple(self) -> tuple:
        return self.output['sqrt_n'],

    def output_str(self) -> str:
        return str(self.output['sqrt_n'])


def generate_test_case(test_type: TestCaseType) -> ProblemTestCase:
    test_case = ProblemTestCase(test_type)

    if test_type is TestCaseType.ZERO:
        n = 0

    elif test_type is TestCaseType.NEGATIVE:
        n = uniform(-10, -0.01)

    elif test_type is TestCaseType.SMALL:
        n = uniform(1, 10)

    elif test_type is TestCaseType.LARGE:
        n = uniform(10, 1000000)

    elif test_type is TestCaseType.SQUARE:
        n = randint(5, 100)**2

    test_case.input['n'] = n
    test_case.output['sqrt_n'] = babylonian_sqrt(n)

    return test_case


def verify_user_solution(correct_test_case: TestCase, user_input: tuple, user_output: tuple) -> Tuple[bool, str]:
    user_test_case = ProblemTestCase(None, INPUT_VARS, user_input, OUTPUT_VARS, user_output)
    passed, correct_test_case = test_case_solution_correct(correct_test_case, user_test_case, ATOL, RTOL)
    return passed, correct_test_case.output_str()
