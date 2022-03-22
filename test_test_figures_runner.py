from test_figures import Figure
from matplotlib import pyplot as plt
from enum import Enum

class TestResult(Enum):
    PASS=0
    FAIL=1
    SKIP=2

def run_test(test, should_error):
    """
    Runs a test.
    Parameters:
        test (function): the test to run
        should_error (bool): whether the test should produce an error
    Returns:
        (bool): Whether the test passed or not
        (string): The error message if the test fails
    """
    try:
        test()
        if should_error:
            return TestResult.FAIL, f"expected fail, but passed"
        return TestResult.PASS, None
    except AssertionError as msg:
        if should_error:
            return TestResult.PASS, None
        return TestResult.FAIL, msg
    except Exception as msg:
        return TestResult.SKIP, f"The test failed unexpectedly with message: {msg}"



def run_tests(tests):
    total_tests = len(tests)
    fails = 0
    passes = 0
    skips = 0
    for test, should_error in tests:
        print(f"'{test.__name__}': ", end="")
        result, msg = run_test(test, should_error)
        if result == TestResult.PASS:
            passes += 1
            print("Pass")
        elif result == TestResult.FAIL:
            fails += 1
            print(f"FAIL: {msg}")
        elif result == TestResult.SKIP:
            skips += 1
            print(f"SKIP: {msg}")
        else:
            msg = "Unknown test result. Results of test was:\n"
            msg += f"result: {result}, msg: {msg}"
            raise Exception(msg)
        print()

    print("Summary:")
    print(f"Passes: {passes}/{total_tests}, fails: {fails}/{total_tests}, skips: {skips}/{total_tests}")
