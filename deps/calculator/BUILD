py_library(
    name = "calculator",
    srcs = ["calculator.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "calculator_test",
    srcs = ["tests/calculator_test.py"],
    deps = [":calculator"],
    size = "small",
)
