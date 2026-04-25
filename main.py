def _build_err_msg(
    msg: str,
    expected: object = None,
    actual: object = None,
    _path: str | None = None,
    _index: int | None = None,
) -> str:
    exp_msg = str(expected)[:50] + "... " if len(str(expected)) > 50 else str(expected)
    act_msg = str(actual)[:50] + "... " if len(str(actual)) > 50 else str(actual)

    exp = f"Expected: {exp_msg} ({type(expected).__name__})"
    act = f"Actual: {act_msg} ({type(actual).__name__})"
    idx = f"[{_index}]" if _index is not None else ""
    pth = f"[{_path}]" if _path else "[root]"

    return f"\n{pth}{idx} {msg} \n{exp} \n{act}"


def _handle_dict(expected, actual, ignore, _path):
    for key in expected:
        curr_path = f"{_path}.{key}" if _path else key

        if curr_path in ignore:
            continue

        if key not in actual:
            yield _build_err_msg("Param not found", key, None, curr_path)
            continue

        yield from _iterate(expected[key], actual[key], ignore, curr_path)


def _handle_list(expected, actual, ignore, _path):
    if len(expected) != len(actual):
        yield _build_err_msg("List length mismatch", len(expected), len(actual), _path)
        return

    for _index, (exp_value, act_value) in enumerate(zip(expected, actual)):
        yield from _iterate(exp_value, act_value, ignore, _path, _index)


def _iterate(expected, actual, ignore, _path=None, _index=None):
    is_both_digits = all(isinstance(x, (int, float)) for x in (expected, actual))
    if type(expected) is not type(actual) and not is_both_digits:
        yield _build_err_msg("Type mismatch", expected, actual, _path)
        return

    match expected:
        case dict():
            yield from _handle_dict(expected, actual, ignore, _path)
        case list():
            yield from _handle_list(expected, actual, ignore, _path)
        case _:
            if expected != actual:
                yield _build_err_msg("Value mismatch", expected, actual, _path, _index)


def compare(
    expected: dict | list | str | int | float | bool,
    actual: dict | list | str | int | float | bool,
    ignore: list[str] | None = None,
):
    """
    Recursive comparison of JSON-like structures.

    Reports:
    - missing keys in dict
    - type mismatch
    - value mismatch
    - list length difference

    Comparison rules:
    - dicts compared by `expected` keys (extra keys in `actual` will be ignored)
    - lists are compared by index (order matters)
    - int and float are treated as compatible numeric types
    - anything other than dict/list will be compared as is

    :param expected:
    :param actual:
    :param ignore: Optional list of dot-separated paths to ignore during comparison

    Example: compare(dict1, dict2, ignore=["user_info.description", ...])
    """
    errors: list[str] = list(_iterate(expected, actual, ignore or list()))
    if errors:
        raise AssertionError("\n" + "\n".join(errors))
