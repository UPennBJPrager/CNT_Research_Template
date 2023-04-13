"""Tests for warnings context managers
"""

import os
import sys
import warnings

import numpy as np
import pytest

from ..testing import (
    assert_allclose_safely,
    assert_re_in,
    clear_and_catch_warnings,
    data_path,
    error_warnings,
    get_fresh_mod,
    get_test_data,
    suppress_warnings,
)


def test_assert_allclose_safely():
    # Test the safe version of allclose
    assert_allclose_safely([1, 1], [1, 1])
    assert_allclose_safely(1, 1)
    assert_allclose_safely(1, [1, 1])
    assert_allclose_safely([1, 1], 1 + 1e-6)
    with pytest.raises(AssertionError):
        assert_allclose_safely([1, 1], 1 + 1e-4)
    # Broadcastable matrices
    a = np.ones((2, 3))
    b = np.ones((3, 2, 3))
    eps = np.finfo(np.float64).eps
    a[0, 0] = 1 + eps
    assert_allclose_safely(a, b)
    a[0, 0] = 1 + 1.1e-5
    with pytest.raises(AssertionError):
        assert_allclose_safely(a, b)
    # Nans in same place
    a[0, 0] = np.nan
    b[:, 0, 0] = np.nan
    assert_allclose_safely(a, b)
    # Never equal with nans present, if not matching nans
    with pytest.raises(AssertionError):
        assert_allclose_safely(a, b, match_nans=False)
    b[0, 0, 0] = 1
    with pytest.raises(AssertionError):
        assert_allclose_safely(a, b)
    # Test allcloseness of inf, especially np.float128 infs
    for dtt in np.sctypes['float']:
        a = np.array([-np.inf, 1, np.inf], dtype=dtt)
        b = np.array([-np.inf, 1, np.inf], dtype=dtt)
        assert_allclose_safely(a, b)
        b[1] = 0
        with pytest.raises(AssertionError):
            assert_allclose_safely(a, b)
    # Empty compares equal to empty
    assert_allclose_safely([], [])


def assert_warn_len_equal(mod, n_in_context):
    mod_warns = mod.__warningregistry__
    # Python 3 appears to clear any pre-existing warnings of the same type,
    # when raising warnings inside a catch_warnings block. So, there is a
    # warning generated by the tests within the context manager, but no
    # previous warnings.
    if 'version' in mod_warns:
        assert len(mod_warns) == 2  # including 'version'
    else:
        assert len(mod_warns) == n_in_context


def test_clear_and_catch_warnings():
    # Initial state of module, no warnings
    my_mod = get_fresh_mod(__name__)
    assert getattr(my_mod, '__warningregistry__', {}) == {}
    with clear_and_catch_warnings(modules=[my_mod]):
        warnings.simplefilter('ignore')
        warnings.warn('Some warning')
    assert my_mod.__warningregistry__ == {}
    # Without specified modules, don't clear warnings during context
    with clear_and_catch_warnings():
        warnings.warn('Some warning')
    assert_warn_len_equal(my_mod, 1)
    # Confirm that specifying module keeps old warning, does not add new
    with clear_and_catch_warnings(modules=[my_mod]):
        warnings.warn('Another warning')
    assert_warn_len_equal(my_mod, 1)
    # Another warning, no module spec does add to warnings dict, except on
    # Python 3 (see comments in `assert_warn_len_equal`)
    with clear_and_catch_warnings():
        warnings.warn('Another warning')
    assert_warn_len_equal(my_mod, 2)


class my_cacw(clear_and_catch_warnings):
    class_modules = (sys.modules[__name__],)


def test_clear_and_catch_warnings_inherit():
    # Test can subclass and add default modules
    my_mod = get_fresh_mod(__name__)
    with my_cacw():
        warnings.simplefilter('ignore')
        warnings.warn('Some warning')
    assert my_mod.__warningregistry__ == {}


def test_warn_error():
    # Check warning error context manager
    n_warns = len(warnings.filters)
    with error_warnings():
        with pytest.raises(UserWarning):
            warnings.warn('A test')
    with error_warnings() as w:  # w not used for anything
        with pytest.raises(UserWarning):
            warnings.warn('A test')
    assert n_warns == len(warnings.filters)
    # Check other errors are propagated

    def f():
        with error_warnings():
            raise ValueError('An error')

    with pytest.raises(ValueError):
        f()


def test_warn_ignore():
    # Check warning ignore context manager
    n_warns = len(warnings.filters)
    with suppress_warnings():
        warnings.warn('Here is a warning, you will not see it')
        warnings.warn('Nor this one', DeprecationWarning)
    with suppress_warnings() as w:  # w not used
        warnings.warn('Here is a warning, you will not see it')
        warnings.warn('Nor this one', DeprecationWarning)
    assert n_warns == len(warnings.filters)
    # Check other errors are propagated

    def f():
        with suppress_warnings():
            raise ValueError('An error')

    with pytest.raises(ValueError):
        f()


@pytest.mark.parametrize(
    'regex, entries',
    [
        ['.*', ''],
        ['.*', ['any']],
        ['ab', 'abc'],
        # Sufficient to have one entry matching
        ['ab', ['', 'abc', 'laskdjf']],
        # Tuples should be ok too
        ['ab', ('', 'abc', 'laskdjf')],
        # Should do match not search
        pytest.param('ab', 'cab', marks=pytest.mark.xfail),
        pytest.param('ab$', 'abc', marks=pytest.mark.xfail),
        pytest.param('ab$', ['ddd', ''], marks=pytest.mark.xfail),
        pytest.param('ab$', ('ddd', ''), marks=pytest.mark.xfail),
        # Shouldn't "match" the empty list
        pytest.param('', [], marks=pytest.mark.xfail),
    ],
)
def test_assert_re_in(regex, entries):
    assert_re_in(regex, entries)


def test_test_data():
    assert str(get_test_data()) == str(data_path)  # Always get the same result
    # Works the same as using __file__ and os.path utilities
    assert str(get_test_data()) == os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'tests', 'data')
    )
    # Check action of subdir and that existence checks work
    for subdir in ('nicom', 'gifti', 'externals'):
        assert get_test_data(subdir) == data_path.parent.parent / subdir / 'tests' / 'data'
        assert os.path.exists(get_test_data(subdir))
        assert not os.path.exists(get_test_data(subdir, 'doesnotexist'))

    for subdir in ('freesurfer', 'doesnotexist'):
        with pytest.raises(ValueError):
            get_test_data(subdir)

    assert not os.path.exists(get_test_data(None, 'doesnotexist'))

    for subdir, fname in [
        ('gifti', 'ascii.gii'),
        ('nicom', '0.dcm'),
        ('externals', 'example_1.nc'),
        (None, 'empty.tck'),
    ]:
        assert os.path.exists(get_test_data(subdir, fname))
