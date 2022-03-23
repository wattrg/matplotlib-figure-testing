from enum import Enum
import traceback

_tests = []

class TestResult(Enum):
    PASS=0 # successful test
    FAIL=1 # the test failed
    SKIP=2 # the test bailed out early

class colours:
    PASS="\033[92m"
    FAIL="\033[91m"
    SKIP="\033[93m"
    ENDC="\033[0m"

def run_tests():
    total_tests = len(_tests)
    fails = 0
    passes = 0
    skips = 0
    print(f"Running {total_tests} tests")
    print()
    for test, should_error in _tests:
        print(f"{test.__name__}: ", end="")
        result, msg = _run_test(test, should_error)
        if result == TestResult.PASS:
            passes += 1
            print(f"{colours.PASS}PASS.{colours.ENDC}")
        elif result == TestResult.FAIL:
            fails += 1
            print(f"{colours.FAIL}FAIL{colours.ENDC}. {msg}")
        elif result == TestResult.SKIP:
            skips += 1
            print(f"{colours.SKIP}SKIP{colours.ENDC}. {msg}")
            print()
        else:
            msg = "Unknown test result. The test returned:\n"
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

def register_test(should_fail=False):
    def _register_test(test):
        _tests.append((test, should_fail))
    return _register_test
