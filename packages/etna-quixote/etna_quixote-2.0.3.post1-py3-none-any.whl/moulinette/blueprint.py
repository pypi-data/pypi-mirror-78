import quixote
from quixote.build import apt
from quixote.fetch import copy as fetch
from quixote.inspection.exec import bash
from quixote.inspection.check import fail, expect_true, testing, using, assert_true
from quixote.inspection.build import gcc

blueprint = quixote.Blueprint(
    name="strcmp",
    author="Clément 'Doom' Doumergue",
)


@quixote.builder
def install_gcc():
    apt.update()
    apt.install("gcc")


@quixote.fetcher
def fetch_delivery():
    print(quixote.get_context())
    fetch.copy("deliveries/")


@quixote.inspector(critical=True)
def compile_delivery():
    delivery_path = quixote.get_context()["delivery_path"]
    resources_path = quixote.get_context()["resources_path"]
    gcc(
        f"{delivery_path}/strcmp.c", f"{resources_path}/main.c",
        options=["-Wall", "-Wextra", "-Werror"],
        output_file="student"
    ).check("cannot compile your delivery")


def student_strcmp(s1: str, s2: str) -> int:
    result = bash(f"./student '{s1}' '{s2}'", timeout=10).check("invalid exit status")
    try:
        return int(result.stdout)
    except (UnicodeDecodeError, ValueError, TypeError):
        fail("your function must not output anything")


@quixote.inspector
def test():
    with testing("strcmp"):
        with using("identical strings"):
            strings = ["abc", "a", ""]
            for string in strings:
                with using(f'"{string}" as argument', hidden=True):
                    ret_val = student_strcmp(string, string)
                    expect_true(ret_val == 0, f"expected a return value of 0, got {ret_val}")

        with using("a lexicographically superior string for s1"):
            strings_pairs = [("bcd", "abc"), ("a", ""), ("abca", "abc")]
            for s1, s2 in strings_pairs:
                with using(f'"{s1}", "{s2}" as arguments', hidden=True):
                    ret_val = student_strcmp(s1, s2)
                    expect_true(ret_val > 0, f"expected a return value greater than 0, got {ret_val}")

        with using("a lexicographically inferior string for s1"):
            strings_pairs = [("abc", "bcd"), ("", "a"), ("abc", "abca")]
            for s1, s2 in strings_pairs:
                with using(f'"{s1}", "{s2}" as arguments', hidden=True):
                    ret_val = student_strcmp(s1, s2)
                    expect_true(ret_val < 0, f"expected a return value lesser than 0, got {ret_val}")
        assert False, "whoopsie"
