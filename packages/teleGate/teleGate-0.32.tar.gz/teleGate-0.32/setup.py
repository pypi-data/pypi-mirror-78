import setuptools

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

PACKAGE_NAME = 'teleGate'
PACKAGE_AUTHOR = 'BYaka'
PACKAGE_AUTHOR_EMAIL = 'byaka.life@gmail.com'
PACKAGE_URL = 'https://gitlab.com/byaka/telegate'
PACKAGE_DESCR = 'Simple logging-gate with http-api.'

with open('README.md', 'r') as f: long_description = f.read()

try:
    from version import __version__ as version
except ImportError:
    exec(f'from {PACKAGE_NAME}.version import __version__ as version')

setuptools.setup(
    name=PACKAGE_NAME,
    version=version,
    author=PACKAGE_AUTHOR,
    author_email=PACKAGE_AUTHOR_EMAIL,
    description=PACKAGE_DESCR,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=PACKAGE_URL,
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[str(s.req) for s in parse_requirements('requirements.txt', session='hack')],
    python_requires='>=3.6',
)
