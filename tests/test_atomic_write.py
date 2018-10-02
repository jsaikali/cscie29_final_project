#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by: Joanna Saikali
Purpose: Tests for `atomic_write` package.
"""


import pytest

""" 
Ensuring that a file is made with a simple test 
"""


@pytest.fixture
def response_success():
    from pset_02.atomic_writes import atomic_write
    filename = "hello.txt"
    with atomic_write(filename) as f:
        f.write("hello world!")
    return filename


def test_content_success(response_success):
    import os
    filename = response_success
    assert os.path.exists(filename)
    if os.path.exists(filename):
        os.remove(filename)

""" 
Ensuring that error is thrown when writing two files with the same name 
"""


def test_file_exists():
    import os

    with pytest.raises(FileExistsError):
        from pset_02.atomic_writes import atomic_write
        filename = "hello.txt"
        with atomic_write(filename) as f:
            f.write("hello world!")
        with atomic_write(filename) as f:
            f.write("hello world!")
    if os.path.exists(filename):
        os.remove(filename)

""" 
Ensuring that error is thrown if there is an issue mid-writing
"""
def test_writing_error():
    import os
    with pytest.raises(Exception):
        from pset_02.atomic_writes import atomic_write
        filename = "hello.txt"
        with atomic_write(filename, mode='abcd') as f:
            f.write("hello world!")
    assert not os.path.exists(filename)
