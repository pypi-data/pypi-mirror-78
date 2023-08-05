"""
tests.functional.utils.processes.bases.test_factory_script_base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test saltfactories.utils.processes.bases.FactoryScriptBase
"""
import os
import sys

import pytest

from saltfactories.exceptions import ProcessTimeout
from saltfactories.utils.processes.bases import FactoryScriptBase


@pytest.mark.parametrize("exitcode", [0, 1, 3, 9, 40, 120])
def test_exitcode(exitcode, tempfiles):
    shell = FactoryScriptBase(sys.executable)
    script = tempfiles.makepyfile(
        """
        # coding=utf-8
        import time
        time.sleep(0.125)
        exit({})
        """.format(
            exitcode
        )
    )
    result = shell.run(script)
    assert result.exitcode == exitcode


def test_timeout_defined_on_class_instantiation(tempfiles):
    shell = FactoryScriptBase(sys.executable, default_timeout=0.5)
    script = tempfiles.makepyfile(
        """
        # coding=utf-8
        import time
        time.sleep(1)
        exit(0)
        """
    )
    with pytest.raises(ProcessTimeout):
        shell.run(script)


def test_timeout_defined_run(tempfiles):
    shell = FactoryScriptBase(sys.executable)
    script = tempfiles.makepyfile(
        """
        # coding=utf-8
        import time
        time.sleep(0.5)
        exit(0)
        """
    )
    result = shell.run(script)
    assert result.exitcode == 0

    script = tempfiles.makepyfile(
        """
        # coding=utf-8
        import time
        time.sleep(0.5)
        exit(0)
        """
    )
    with pytest.raises(ProcessTimeout):
        shell.run(script, _timeout=0.1)


@pytest.mark.parametrize(
    "input_str,expected_object",
    [
        # Good JSON
        ('{"a": "a", "1": 1}', {"a": "a", "1": 1}),
        # Bad JSON
        ("{'a': 'a', '1': 1}", None),
    ],
)
def test_json_output(input_str, expected_object, tempfiles):
    shell = FactoryScriptBase(sys.executable)
    script = tempfiles.makepyfile(
        """
        # coding=utf-8
        import sys
        sys.stdout.write('''{}''')
        exit(0)
        """.format(
            input_str
        )
    )
    result = shell.run(script)
    assert result.exitcode == 0
    if result.json:
        assert result.json == expected_object
    assert result.stdout == input_str


def test_stderr_output(tempfiles):
    input_str = "Thou shalt not exit cleanly"
    shell = FactoryScriptBase(sys.executable)
    script = tempfiles.makepyfile(
        """
        # coding=utf-8
        exit("{}")
        """.format(
            input_str
        )
    )
    result = shell.run(script)
    assert result.exitcode == 1
    assert result.stderr.replace(os.linesep, "\n") == input_str + "\n"


@pytest.mark.skipif(
    sys.version_info < (3,), reason="This test will fail on Py2 and we do not support Py2"
)
def test_unicode_output(tempfiles):
    shell = FactoryScriptBase(sys.executable)
    script = tempfiles.makepyfile(
        r"""
        # coding=utf-8
        from __future__ import print_function
        import sys
        sys.stdout.write(u'STDOUT F\xe1tima')
        sys.stdout.flush()
        sys.stderr.write(u'STDERR F\xe1tima')
        sys.stderr.flush()
        exit(0)
        """
    )
    result = shell.run(script)
    assert result.exitcode == 0, str(result)
    assert result.stdout == "STDOUT Fátima"
    assert result.stderr == "STDERR Fátima"
