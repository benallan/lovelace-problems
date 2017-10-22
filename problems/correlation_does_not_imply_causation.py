import logging
import numpy as np
from problems.test_case import TestCase, TestCaseTypeEnum

logger = logging.getLogger(__name__)


class TestCaseI7Type(TestCaseTypeEnum):
    SPECIFIC_DATASET = ('specific dataset', '', 1)
    RANDOM_DATASET = ('random dataset', '', 1)
    UNKNOWN = ('unknown case', '', 0)


class TestCaseI7(TestCase):
    def input_filename(self) -> str:
        return self.input['filename']

    def input_str(self) -> str:
        return ''

    def output_str(self) -> str:
        return str(self.output['r'])


TEST_CASE_TYPE_ENUM = TestCaseI7Type
TEST_CASE_CLASS = TestCaseI7

RESOURCES = []

PHYSICAL_CONSTANTS = {}

TESTING_CONSTANTS = {
    'error_tol': 0.0001  # tolerance on correlation coefficient
}


def write_random_dataset_csv(x, y):
    import csv
    outfile = open('random_xy.csv', "wb")
    xy_writer = csv.writer(outfile, delimiter=',')

    for i in range(len(x)):
        xy_writer.writerow([x[i], y[i]])

    outfile.close()


def generate_input(test_type: TestCaseI7Type) -> TestCaseI7:
    test_case = TestCaseI7(test_type)

    if test_type is TestCaseI7Type.SPECIFIC_DATASET:
        dataset_filename = 'specific_xy.dat'
    elif test_type is TestCaseI7Type.RANDOM_DATSET:
        N = np.random.randint(10, 100)
        x = np.random.rand(N, 1)
        y = np.random.rand(N, 1)
        write_random_dataset_csv(x, y)
        dataset_filename = 'random_xy.dat'
    else:
        raise ValueError

    test_case.input['dataset_filename'] = dataset_filename
    return test_case


def solve_test_case(test_case: TestCaseI7) -> None:
    import csv

    x = []
    y = []

    with open('xy.csv') as csvfile:
        xy_reader = csv.reader(csvfile, delimiter=',')
        for row in xy_reader:
            x.append(float(row[0]))
            y.append(float(row[1]))

    N = len(x)
    x = np.array(x)
    y = np.array(y)

    x_bar = x.mean()
    y_bar = y.mean()

    cov_XY = 0
    sigma_X = 0
    sigma_Y = 0

    for i in range(N):
        cov_XY = cov_XY + (x[i] - x_bar) * (y[i] - y_bar)
        sigma_X = sigma_X + (x[i] - x_bar) ** 2
        sigma_Y = sigma_Y + (y[i] - y_bar) ** 2

    sigma_X = np.sqrt(sigma_X)
    sigma_Y = np.sqrt(sigma_Y)

    r = cov_XY / (sigma_X * sigma_Y)

    test_case.output['r'] = r
    return


def verify_user_solution(user_input_str: str, user_output_str: str) -> bool:
    logger.info("Verifying user solution...")
    logger.debug("User input string: %s", user_input_str)
    logger.debug("User output string: %s", user_output_str)

    # Build TestCase object out of user's input string.
    tmp_test_case = TestCaseI7(TestCaseI7Type.UNKNOWN)

    # TODO: How do we know which dataset the user loaded in???

    # Solve the problem with this TestCase so we have our own solution, and extract the solution.
    solve_test_case(tmp_test_case)
    r = tmp_test_case.output['r']

    # Extract user solution.
    user_r = float(user_output_str)

    error_tol = TESTING_CONSTANTS['error_tol']
    error_r = abs(r - user_r)

    logger.debug("User solution:")
    logger.debug("r = {}".format(user_r))
    logger.debug("Engine solution:")
    logger.debug("r = {}".format(r))
    logger.debug("Error tolerance = %e. Error r: %e.", error_tol, error_r)

    if error_r < error_tol:
        logger.info("User solution correct.")
        return True
    else:
        logger.info("User solution incorrect.")
        return False
