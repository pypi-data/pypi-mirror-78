import sys

import setuptools
import setuptools.command.test


# -*- Command: setup.py test -*-


class pytest(setuptools.command.test.test):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to pytest')]

    def initialize_options(self):
        setuptools.command.test.test.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest as _pytest
        sys.exit(_pytest.main(self.pytest_args))


setuptools.setup(
    name='arkio',
    cmdclass={'test': pytest},
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ark = ark.__main__:main',
        ]
    },
)
