load("@pip//:requirements.bzl", "requirement")
load("@rules_python_pytest//python_pytest:defs.bzl", "py_pytest_test")

py_pytest_test(
    name = "pytest",
    size = "small",
    srcs = ["conftest.py", "test_api.py"],
    deps = [
        "//src:app",
        requirement("pytest"),
    ],
)
