from nose.tools import eq_

from moban_ansible.engines.line_in_file import line_in_file


def test_append_a_line():
    options = {"create": "yes", "line": "192.168.1.1 foo.bar foo"}

    content = b"127.0.0.1 localhost"

    new_content = line_in_file(content, options)
    expected = "\n".join([content.decode(), options["line"]])

    eq_(new_content, expected.encode())


def test_absent():
    absent_line = "192.168.1.1 foo.bar foo"
    options = {"regexp": ".*foo$", "state": "absent"}

    content = f"127.0.0.1 localhost\n{absent_line}".encode()

    new_content = line_in_file(content, options)
    expected = "127.0.0.1 localhost"

    eq_(new_content, expected.encode())


def test_present():
    present_line = "192.168.1.1 foo.bar foo"
    options = {"regexp": ".*foo$", "line": present_line}

    content = b"127.0.0.1 localhost\n192.162.1.1 foo"

    new_content = line_in_file(content, options)
    expected = ["127.0.0.1 localhost", present_line]

    eq_(new_content, "\n".join(expected).encode())
