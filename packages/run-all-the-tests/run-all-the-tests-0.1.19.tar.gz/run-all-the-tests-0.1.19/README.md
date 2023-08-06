Run a series of test invocation making sure each test case works with both 'pytest' and
 'python -m pytest' over all working directories between the project root and the directory
  containing the test script.

```
├─ src
│
│<-- # run selected __main__'s from this working directory
│
│  └─ __init__.py
│  └─ foo.py
│  ├─ bar
│  │   └─ __init__.py
│  │   └─ bar.py
│  │
│  │<-- # run selected __main__'s from this working directory
│  │
│  └─ run_foo_main.py
│  └─ run_bar_main.py
│
│<-- # run selected test cases from this working directory
│
├─ tests
│  │
│  │<-- # run selected test cases from this working directory
│  │
│  └─ test_foo.py
│  └─ bar
│        │<-- # run selected bar test cases from this working directory
│        │
│        └─ test_bar.py
└─ setup.py
```

Your `run_all_my_tests.py`:
```
from run_all_the_tests import TestCasePath, TestCase, Group, TestType

if __name__ == '__main__': 
    project_path: PurePath = Path(__file__).absolute().parent.parent


    def gen_test_case_path(test_case: str) -> TestCasePath:
        return TestCasePath(project_path, PurePath(test_case))


    all_test_cases: Tuple[TestCase, ...] = (
        TestCase.gen_test_case(gen_test_case_path('tests/test_foo.py')),
        TestCase.gen_test_case(gen_test_case_path('tests/bar/test_bar.py')),
    )

    run_all_tests(all_test_cases)
```

Each set of tests are run in parallel within `Group.ONE`. Designate
tests to run within non-conflicting groups of parallel runs by assigning
all test cases that can run without conflict to the same `Group`.

```
    all_test_cases: Tuple[TestCase, ...] = (
        TestCase.gen_test_case(gen_test_case_path('tests/test_foo.py')),
        TestCase.gen_test_case(gen_test_case_path('tests/bar/test_bar.py'), Group.TWO),
    )
```

`TestCase.gen_test_case()` also supports the following agrs:
```
    pytest_filter: str = None
    :param pytest_filter: pytest -k string
 
    test_types: Tuple[TestType, ...] = TestType.all_test_types()
    :param test_types: for exceptional situations, limit a TestCase to run for limited set of TestType's
```
