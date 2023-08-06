# ======================================================================
# Copyright CERFACS (August 2019)
# Contributor: Adrien Suau (adrien.suau@cerfacs.fr)
#
# This software is governed by the CeCILL-B license under French law and
# abiding  by the  rules of  distribution of free software. You can use,
# modify  and/or  redistribute  the  software  under  the  terms  of the
# CeCILL-B license as circulated by CEA, CNRS and INRIA at the following
# URL "http://www.cecill.info".
#
# As a counterpart to the access to  the source code and rights to copy,
# modify and  redistribute granted  by the  license, users  are provided
# only with a limited warranty and  the software's author, the holder of
# the economic rights,  and the  successive licensors  have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using, modifying and/or  developing or reproducing  the
# software by the user in light of its specific status of free software,
# that  may mean  that it  is complicated  to manipulate,  and that also
# therefore  means that  it is reserved for  developers and  experienced
# professionals having in-depth  computer knowledge. Users are therefore
# encouraged  to load and  test  the software's  suitability as  regards
# their  requirements  in  conditions  enabling  the  security  of their
# systems  and/or  data to be  ensured and,  more generally,  to use and
# operate it in the same conditions as regards security.
#
# The fact that you  are presently reading this  means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
# ======================================================================

# See https://packaging.python.org/guides/creating-and-discovering-plugins/#using-naming-convention

import importlib
import pkgutil
import inspect


class _LazyModuleLoader(dict):
    def __init__(self, prefix: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._prefix = prefix
        self._imported_keys = set()

    def _import_module_if_not_imported(self, item):
        if not inspect.ismodule(super().__getitem__(item)):
            try:
                super().__setitem__(item, importlib.import_module(self._prefix + item))
                self._imported_keys.add(item)
            except ImportError:
                del self[item]

    def __getitem__(self, item):
        self._import_module_if_not_imported(item)
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        if not key.startswith(self._prefix):
            raise RuntimeError()
        super().__setitem__(key[len(self._prefix) :], value)

    def items(self):
        # First, iterate over the already imported modules
        for key in self._imported_keys:
            yield (key, self.__getitem__(key))
        # Then, if needed, iterate over the other keys
        for key in filter(lambda k: k not in self._imported_keys, list(self.keys())):
            yield (key, self.__getitem__(key))


frameworks = _LazyModuleLoader(prefix="qprof_")
for package_info in pkgutil.iter_modules():
    name = package_info.name
    if name.startswith("qprof_"):
        frameworks[name] = None
