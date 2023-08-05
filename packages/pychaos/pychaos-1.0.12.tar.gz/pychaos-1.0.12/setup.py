from setuptools import setup, find_packages, Extension

# Note to self: To upload a new version to PyPI, run:
# pip install wheel twine
# python3 setup.py sdist bdist_wheel
# twine upload dist/*


setup(
    name='pychaos',
    version='1.0.12',
    description='A Python extension module that wraps not !CHAOS REST I/O',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Andrea Michelotti',
    author_email='andrea.michelotti@lnf.infn.it',
    url='https://baltig.infn.it/chaos-lnf-control/pychaos',
    packages=find_packages(),
    license='CC0 (copyright waived)',
    keywords="CHAOS,CONTROL, REST",
    install_requires=['requests','kafka-python','bson','pillow'],
    scripts=["test/pyPS.py","test/pyLive.py","test/pySubscribeNode.py","test/pySendCommand.py"],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
)
