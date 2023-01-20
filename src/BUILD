load("@pip//:requirements.bzl", "requirement")

py_binary(
    name = "app",
    srcs = ["app.py"],
    deps = [
        "//deps/calculator:calculator",
        requirement("Flask"),
        requirement("python_dateutil"),
        requirement("gunicorn"),
    ],
    visibility = ["//visibility:public"],
)
