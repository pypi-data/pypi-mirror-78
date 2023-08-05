import os

from setuptools import setup
from setuptools_rust import Binding, RustExtension


def get_long_description() -> str:
    readme_filepath = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_filepath, 'r', encoding='utf-8') as f:
        return f.read()


def get_version():
    version_filepath = os.path.join(
        os.path.dirname(__file__), 'py_src', 'yotsuba', 'version.py'
    )
    with open(version_filepath) as f:
        for line in f:
            if line.startswith('__version__'):
                return line.strip().split()[-1][1:-1]


def get_tests_requires():
    requirements_filepath = os.path.join(
        os.path.dirname(__file__), 'requirements-dev.txt'
    )
    with open(requirements_filepath, 'r') as f:
        return f.read().splitlines()


setup(
    name='yotsuba-python',
    version=get_version(),
    url='https://github.com/yutayamazaki/yotsuba',
    author='Yuta Yamazaki',
    author_email='yu.yamazakii@gmail.com',
    maintainer='Yuta Yamazaki',
    maintainer_email='yu.yamazakii@gmail.com',
    description='a',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    rust_extensions=[
        RustExtension(
            'yotsuba.yotsuba', path='Cargo.toml', binding=Binding.PyO3,
            debug=False
        )
    ],
    package_dir={'': 'py_src'},
    packages=[
        'yotsuba',
    ],
    install_requires=[],
    tests_require=get_tests_requires(),
    zip_safe=False,
    license='MIT',
    keywords='nlp python rust',
)
