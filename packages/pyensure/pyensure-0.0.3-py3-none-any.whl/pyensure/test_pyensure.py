import os
import pathlib
import pytest
import subprocess
import sys
from unittest.mock import patch, MagicMock

THIS_DIR = os.path.dirname(__file__)
sys.path.append(THIS_DIR)
import state as _state

THIS_DIR_WITH_QUOTES = f"'{THIS_DIR}'"

@pytest.fixture()
def state(tmpdir):
    os.chdir(tmpdir)

    pytest = sys.modules['pytest']
    saved_path = sys.path[:]
    s = _state.State()
    s.disable_cleanup()
    try:
        yield s
    finally:
        sys.path = saved_path
        sys.modules['pytest'] = pytest
        s.unhook()
        s._cleanup_site_packages()

def test_pip_remove_and_reinstall(state):
    '''
    remove pytest, get it back via an import, reinstall it for real
    '''
    try:
        subprocess.call(f'{sys.executable} -m pip uninstall -y pytest', shell=True)
        assert subprocess.call(f'{sys.executable} -c "import pytest"', shell=True) != 0, "pytest did not get removed"
        assert subprocess.call(f'{sys.executable} -c "import sys;sys.path.append(r{THIS_DIR_WITH_QUOTES});import state; state.hook(); import pytest; print(pytest.mark)"', shell=True) == 0, "pytest was NOT able to be imported after removal and hook"
    finally:
        subprocess.call(f'{sys.executable} -m pip install pytest', shell=True)

def test_remove_site_packages_from_sys_path(state):
    state.remove_site_packages_from_sys_path()
    pytest = sys.modules['pytest']
    del sys.modules['pytest']
    
    with pytest.raises(ImportError):
        import pytest

def test_install_and_import_via_hook_then_unhook(state):
    state.remove_site_packages_from_sys_path()
    pytest = sys.modules['pytest']
    del sys.modules['pytest']

    state.hook()
    import pytest as _pytest
    assert _pytest != pytest
    del sys.modules['pytest']

    state.unhook()
    state._cleanup_site_packages()
    with pytest.raises(ImportError):
        import pytest as __pytest

def test_running_as_module_main(state):
    SCRIPT = '''
import sys
from pyensure import remove_site_packages_from_sys_path
remove_site_packages_from_sys_path()

import pytest
import serial
import psutil

assert pytest
assert serial
assert psutil

assert sys.argv[-1] == \'hello\''''
    script = pathlib.Path('script.py').absolute()
    script.write_text(SCRIPT)

    assert subprocess.call(f'{sys.executable} -m pyensure {script} hello', shell=True, cwd=f'{THIS_DIR}/../') == 0

