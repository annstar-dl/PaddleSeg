import paddle
import re

try:
    from packaging.version import parse as _parse_version
except Exception:
    try:
        from pkg_resources import parse_version as _parse_version
    except Exception:
        _parse_version = None


def is_paddle_version_at_least(min_version='2.6.1'):
    """Return True if installed PaddlePaddle version is >= min_version.

    Uses packaging/version parsing when available; falls back to numeric
    component comparison if necessary.
    """
    pv = getattr(paddle, '__version__', None)
    if pv is None:
        return False

    if _parse_version is not None:
        try:
            return _parse_version(pv) >= _parse_version(min_version)
        except Exception:
            pass

    def _to_nums(v):
        parts = re.findall(r"\d+", v)
        return [int(x) for x in parts]

    nums = _to_nums(pv)
    min_nums = _to_nums(min_version)
    maxlen = max(len(nums), len(min_nums), 3)
    nums += [0] * (maxlen - len(nums))
    min_nums += [0] * (maxlen - len(min_nums))

    # Element-wise comparison: compare components from most-significant to
    # least-significant; if all equal, consider versions equal (>= True).
    for a, b in zip(nums, min_nums):
        if a > b:
            return True
        if a < b:
            return False
    return True


def is_paddle_ge_2_6_1():
    """Convenience helper to check PaddlePaddle >= 2.6.1."""
    return is_paddle_version_at_least('2.6.1')