import atexit
import builtins
import contextlib
import pathlib
import shutil
import subprocess
import sys
import tempfile

PIP = f'{sys.executable} -m pip'

class PackageUnavailable(ImportError):
    pass

def install_package_to_location(package, loc, qualifier=''):
    # todo save output to use on raising PackageUnavailable
    ret_code = subprocess.call(f'{PIP} install -y --target={loc} {package}{qualifier}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if ret_code != 0:
        raise PackageUnavailable
    return ret_code

class State:
    def __init__(self):
        self.has_hooked_import = False
        self.real_import = builtins.__import__

        self.packages = []
        self.site_packages = pathlib.Path(tempfile.mkdtemp())

        sys.path.insert(0, str(self.site_packages))

        # cleanup later
        atexit.register(lambda: shutil.rmtree(self.site_packages, ignore_errors=True))

        for i in dir(self):
            thing = getattr(self, i)
            if callable(thing) and not i.startswith('_'):
                globals()[i] = thing

    def _install_package(self, package, qualifier=''):
        self.packages.append(package)
        return install_package_to_location(package, self.site_packages, qualifier)

    def ensure_package(self, package, qualifier=''):
        if package not in self.packages:
            self._install_package(package, qualifier)

        return self.real_import(package)

    def _ensure_package_for_hook(self, *args):
        with self.force_unhook():
            try:
                package = self.real_import(*args)
            except ImportError as ex:
                package = self.ensure_package(args[0])

        return package

    def hook(self):
        if not self.has_hooked_import:
            builtins.__import__ = self._ensure_package_for_hook
            self.has_hooked_import = True

    def unhook(self):
        if self.has_hooked_import:
            builtins.__import__ = self.real_import
            self.has_hooked_import = False

    @contextlib.contextmanager
    def force_unhook(self):
        do_stuff = self.has_hooked_import
        if do_stuff:
            self.unhook()

        try:
            yield
        finally:
            # if needed, get us rehooked
            if do_stuff:
                self.hook()


_state = State()