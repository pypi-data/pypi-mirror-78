import setuptools
setuptools.setup(
    name="k3str",
    packages=["k3str"],
    version="0.1.1",
    license='MIT',
    description='k3str is a collection of string utilities.',
    long_description='# k3str\n\n[![Build Status](https://travis-ci.com/pykit3/k3str.svg?branch=master)](https://travis-ci.com/pykit3/k3str)\n[![Documentation Status](https://readthedocs.org/projects/k3str/badge/?version=stable)](https://k3str.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3str)](https://pypi.org/project/k3str)\n\nk3str is a collection of string utilities.\n\nk3str is a component of [pykit3] project: a python3 toolkit set.\n\n\n# Install\n\n```\npip install k3str\n```\n\n# Synopsis\n\n```python\n>>> repr(to_bytes(\'我\'))\n"b\'\\\\xe6\\\\x88\\\\x91\'"\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3',
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/drmingdrmer/k3str',
    keywords=['str', 'bytes'],
    python_requires='>=3.0',

    install_requires=['semantic_version~=2.8.5', 'jinja2~=2.11.2', 'PyYAML~=5.3.1', 'sphinx~=3.2.1', 'k3ut==0.1.7'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: Implementation :: PyPy'],
)
