from os.path import join, dirname, abspath

from setuptools import setup, find_namespace_packages

from setux.main import __version__

curdir = abspath(dirname(__file__))
readme = open(join(curdir, 'README.rst')).read()

setup(
    name             = 'setux',
    version          = __version__,
    description      = 'System deployment',
    long_description = readme,
    keywords         = ['utility', ],
    url              = 'https://framagit.org/louis-riviere-xyz/setux',
    author           = 'Louis RIVIERE',
    author_email     = 'louis@riviere.xyz',
    license          = 'MIT',
    classifiers      = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    python_requires='>3.6',
    install_requires = [
        'setux_core>=0.3.5',
        'setux_distros>=0.4.1',
        'setux_targets>=0.3.1',
        'setux_managers>=0.4.1',
        'setux_modules>=0.3.2',
        'setux_logger>=0.2.0',
        'setux_repl>=0.4.2',
    ],
    packages = find_namespace_packages(
        include=['setux.*']
    ),
    entry_points = dict(
        console_scripts = (
            'setux=setux.main.main:main',
        ),
    ),
)
