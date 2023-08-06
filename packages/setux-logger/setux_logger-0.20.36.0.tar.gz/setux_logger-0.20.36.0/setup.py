from os.path import join, dirname, abspath

from setuptools import setup, find_namespace_packages


curdir = abspath(dirname(__file__))
readme = open(join(curdir, 'README.rst')).read()

setup(
    name             = 'setux_logger',
    version          = '0.20.36.0',
    description      = 'System deployment',
    long_description = readme,
    keywords         = ['utility', ],
    url              = 'https://gitlab.com/dugres/setux_logger',
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
    install_requires = [
        'pybrary>=0.20.36.2',
    ],
    packages = find_namespace_packages(
        include=['setux.*']
    ),
)
