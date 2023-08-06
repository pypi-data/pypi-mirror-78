"""
Run a series of test invocation making sure each test case works with both 'pytest' and
 'python -m pytest' over all working directories between the project root and the directory
  containing the test script.

Each 'Group' set of tests are run in parallel (default is all parallel).  Separate tests
 into non-conflicting groups.
"""
import os
import shlex
import subprocess
import time
from os import PathLike
from pathlib import Path, PurePath
from typing import List, Union, Sequence, Dict, NamedTuple, NewType, Optional, Tuple

from run_all_the_tests.test_case import Group, TestType, TestCase

ENV: Dict[str, str] = os.environ.copy()
ENV.update({"PYTHONDONTWRITEBYTECODE": "-1"})

POpenArgs = NewType(
    "POpenArgs", Union[bytes, str, Sequence[Union[bytes, str, PathLike]]]
)


class _RunningTestCase(NamedTuple):
    """
    Named tuple associated with a currently running test case.
    """

    group: Group
    test_type: TestType
    time_to_wait: float
    cwd: PurePath
    process: Optional[subprocess.Popen]

    def wait_until_test_finished(self) -> int:
        return self.process.wait(self.time_to_wait)

    def __str__(self) -> str:
        args: POpenArgs = self.process.args
        which_test_how: str = f"unknown: {args[-1]}"
        if isinstance(args, list):
            args: Sequence = args
            if self.test_type == TestType.PYTHON:
                which_test_how = f"(Group {self.group}) script: {args[-1]}"
            elif self.test_type == TestType.PYTHON_PYTEST:
                which_test_how = f"(Group {self.group}) Python pytest: {args[-1]}"
            elif self.test_type == TestType.PYTEST:
                which_test_how = f"(Group {self.group}) pytest: {args[-1]}"
        return f"{which_test_how} from {self.cwd}"


def _run_test(
    test_type: TestType, work_directory: PurePath, test_case: TestCase
) -> Optional[_RunningTestCase]:
    """
    Run a python script base on the test_type.

    None: is returned if the test case can't be run with the requested test_type.

    :param test_type: enum to determine if a pytest (or a python-pytest) or
     a regular runnable script
    :param work_directory: working directory from whence the script is run
    :param test_case: manage test case paths relative to project root and current working directory
    :return: a _RunningTestCase containing reference to the running process(Popen object)
     and data associated with
    how the process was started
    """

    command: str = test_case.python_command(test_type)
    if not command:
        return None

    cwd_relative_to_test_case_project: PurePath = test_case.cwd_relative_to_project(
        work_directory
    )
    test_case_relative_to_cwd: PurePath = test_case.test_case_relative_to_cwd(
        work_directory
    )
    print(
        f"Starting: {command} {test_case_relative_to_cwd} from {cwd_relative_to_test_case_project}"
    )

    command = f"{command} {test_case_relative_to_cwd}"
    process: subprocess.Popen = subprocess.Popen(
        shlex.split(command),
        cwd=str(Path(work_directory).absolute()),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
        env=ENV,
    )

    return _RunningTestCase(
        test_case.group,
        test_type,
        test_case.time_to_wait,
        cwd_relative_to_test_case_project,
        process,
    )


def _get_group_tests(
    test_cases: Tuple[TestCase, ...], group: Group
) -> Tuple[TestCase, ...]:
    return tuple(tcp for tcp in test_cases if group == tcp.group)


def run_all_tests(test_cases: Tuple[TestCase, ...] = tuple()) -> None:
    start_time: float = time.perf_counter()
    running_test_cases: List[_RunningTestCase] = []
    test_count: int = 0
    tests_passed: int = 0

    # Start all tests
    for group in Group:
        for test_case in _get_group_tests(test_cases, group):
            # ... over all test_case types
            test_type_count = len(TestType.all_test_types) - 1
            for test_type in TestType:
                test_type_count -= 1
                if test_type not in test_case.test_types:
                    continue
                # ... changing the work dir from the project root to directory containing script
                working_directories = test_case.working_directories
                working_directory_count = len(working_directories)
                for working_directory in working_directories:
                    working_directory_count -= 1
                    running_test_case = _run_test(
                        test_type, working_directory, test_case
                    )

                    if running_test_case:
                        test_count += 1
                        if test_case.is_dir_test_case or (
                            test_case.is_wait_between_test_types
                            and (test_type_count > 0 or working_directory_count > 0)
                        ):
                            print("Waiting...")
                            tests_passed = report_on_test(
                                running_test_case, tests_passed
                            )
                        else:
                            running_test_cases.append(running_test_case)

        # Print them out when each complete (in order)
        for running_test_case in running_test_cases:
            tests_passed = report_on_test(running_test_case, tests_passed)

        running_test_cases.clear()

    if tests_passed == test_count:
        print(
            f"\nAll {test_count} tests passed! ({time.perf_counter() - start_time}sec)"
        )
    else:
        print(
            f"\n{tests_passed} tests out of {test_count} passed "
            f"({time.perf_counter() - start_time}sec)"
        )


def report_on_test(running_test_case, tests_passed):
    if running_test_case.wait_until_test_finished() != 0:
        print(f"\nCompleted (w/ error): {running_test_case}\n\t")
        # pylint: disable=expression-not-assigned
        [print(f"\t{line}", end="") for line in running_test_case.process.stdout]
        # pylint: enable=expression-not-assigned
    else:
        tests_passed += 1

    print(f"\nCompleted: {running_test_case}\n\t")
    # pylint: disable=expression-not-assigned
    [print(f"\t{line}", end="") for line in running_test_case.process.stdout]
    # pylint: enable=expression-not-assigned

    return tests_passed
