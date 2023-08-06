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

class State:
    def __init__(self):
        self.has_hooked_import = False
        self.real_import = builtins.__import__

        self.packages = []
        self.site_packages = pathlib.Path(tempfile.mkdtemp())

        sys.path.insert(0, str(self.site_packages))

        # cleanup later
        atexit.register(self._cleanup_site_packages)

        for i in dir(self):
            thing = getattr(self, i)
            if callable(thing) and not i.startswith('_'):
                globals()[i] = thing

    def _cleanup_site_packages(self):
        shutil.rmtree(self.site_packages, ignore_errors=True)

    @classmethod
    def _install_package_to_location(cls, package, loc, qualifier=''):
        try:
            output = subprocess.check_output(f'{PIP} install --target={loc} {package}{qualifier}', shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as ex:
            raise PackageUnavailable(ex.output)

        return 0

    def _install_package(self, package, qualifier=''):
        self.packages.append(package)
        return self._install_package_to_location(package, self.site_packages, qualifier)

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

    def disable_cleanup(self):
        atexit.unregister(self._cleanup_site_packages)

    def remove_site_packages_from_sys_path(self):
        for p in list(set(sys.path)):
            if 'site-packages' in p:
                 sys.path.remove(p)


_state = State()