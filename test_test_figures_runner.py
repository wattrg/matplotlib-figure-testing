from enum import Enum
import traceback

class TestResult(Enum):
    PASS=0
    FAIL=1
    SKIP=2 # the test probably failed to execute

def run_tests(tests):
    total_tests = len(tests)
    fails = 0
    passes = 0
    skips = 0
    print(f"Running {total_tests} tests")
    print()
    for test, should_error in tests:
        print(f"'{test.__name__}': ", end="")
        result, msg = _run_test(test, should_error)
        if result == TestResult.PASS:
            passes += 1
            print("Pass")
        elif result == TestResult.FAIL:
            fails += 1
            print(f"FAIL: {msg}")
        elif result == TestResult.SKIP:
            skips += 1
            print(f"SKIP: {msg}")
            print()
        else:
            msg = "Unknown test result. Results of test was:\n"
            msg += f"result: {result}, msg: {msg}"
            raise Exception(msg)

    print()
    print("Summary:")
    print(f"    Passes: {passes}/{total_tests}\n"
          f"    Fails:  {fails}/{total_tests}\n"
          f"    Skips:  {skips}/{total_tests}")

def _run_test(test, should_error):
    """
    Runs a test.
    Parameters:
        test (function): the test to run
        should_error (bool): whether the test should produce an error
    Returns:
        (bool): Whether the test passed or not
        (string): The failure message (or None if it didn't fail)
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
    except Exception:
        msg = f"The test failed unexpectedly with traceback:\n"
        msg += traceback.format_exc()
        return TestResult.SKIP, msg
