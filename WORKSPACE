# import rules_python
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "48a838a6e1983e4884b26812b2c748a35ad284fd339eb8e2a6f3adf95307fbcd",
    strip_prefix = "rules_python-0.16.2",
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/0.16.2.tar.gz",
)

# https://github.com/bazelbuild/rules_python/issues/932
http_archive(
    name = "bazel_skylib",
    sha256 = "74d544d96f4a5bb630d465ca8bbcfe231e3594e5aae57e1edbf17a6eb3ca2506",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.3.0/bazel-skylib-1.3.0.tar.gz",
        "https://github.com/bazelbuild/bazel-skylib/releases/download/1.3.0/bazel-skylib-1.3.0.tar.gz",
    ],
)

load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")

bazel_skylib_workspace()

load("@rules_python//python:repositories.bzl", "python_register_toolchains")

# toolchain registration
python_register_toolchains(
    name = "python3_10",
    # Available versions are listed in @rules_python//python:versions.bzl.
    # We recommend using the same version your team is already standardized on.
    python_version = "3.10",
)

load("@python3_10//:defs.bzl", "interpreter")
load("@rules_python//python:pip.bzl", "pip_parse")

# Create a central repo that knows about the dependencies needed from
# requirements.txt.
pip_parse(
    name = "pip",
    requirements_lock = ":requirements-lock.txt",
    python_interpreter_target = interpreter,
)

# Load the starlark macro which will define the dependencies.
load("@pip//:requirements.bzl", "install_deps")

# Call it to define repos for the requirements.
install_deps()

http_archive(
    name = "rules_python_pytest",
    sha256 = "334a0ac91a0d6a87df499cdf9b70b525754dc8ca4873763116d67177f759389f",
    strip_prefix = "rules_python_pytest-1.0.2",
    url = "https://github.com/caseyduquettesc/rules_python_pytest/archive/v1.0.2.tar.gz",
)

# Fetches the rules_python_pytest dependencies.
# If you want to have a different version of some dependency,
# you should fetch it *before* calling this.
# Alternatively, you can skip calling this function, so long as you've
# already fetched all the dependencies.
load("@rules_python_pytest//python_pytest:repositories.bzl", "rules_python_pytest_dependencies")

rules_python_pytest_dependencies()
