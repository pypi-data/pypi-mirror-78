#!/usr/bin/env python
# coding: utf-8


from setuptools import setup
import os
# Relative-first
from nabu import version, __nabu_modules__

def setup_package():
    packages_folders = __nabu_modules__
    packages = ["nabu"]
    package_dir = {"nabu": "nabu"}
    for f in packages_folders:
        modulename = str("nabu.%s" % f)
        packages.append(modulename)
        package_dir[modulename] = os.path.join("nabu", f)

        module_test_dirname = os.path.join(package_dir[modulename], "tests")
        if os.path.isdir(module_test_dirname):
            modulename_test = str("%s.tests" % modulename)
            packages.append(modulename_test)
            package_dir[modulename_test] = module_test_dirname

    other_modules = ["nabu.resources.cli"]
    for mod in other_modules:
        packages.append(mod)
        package_dir[mod] = os.path.join(*(mod.split(".")))

    doc_requires = [
        'sphinx',
        'cloud_sptheme',
        'recommonmark',
        'nbsphinx',
    ]

    setup(
        name='nabu',
        author='Pierre Paleo',
        version=version,
        author_email = "pierre.paleo@esrf.fr",
        maintainer = "Pierre Paleo",
        maintainer_email = "pierre.paleo@esrf.fr",

        packages=packages,
        package_dir = package_dir,
        package_data = {
            'nabu.cuda': [
                'src/*.cu',
                'src/*.h',
            ],
            'nabu.resources': [
                'templates/*.ini',
            ],
        },
        install_requires = [
            'psutil',
            'pytest',
            'numpy > 1.9.0',
            'silx >= 0.12.0',
            'distributed', # >= 2.10.0',
            'dask_jobqueue',
            # ~ 'pycuda',
            # ~ 'pyopencl',
            'tomoscan >= 0.3.2',
        ],
        long_description = """
        Nabu - Tomography software
        """,

        entry_points = {
            'console_scripts': [
                "nabu-test=nabu.tests:nabu_test",
                "nabu-config=nabu.resources.cli.bootstrap:bootstrap",
                "nabu=nabu.resources.cli.reconstruct:main",
            ],
        },

        zip_safe=True
    )


if __name__ == "__main__":
    setup_package()
