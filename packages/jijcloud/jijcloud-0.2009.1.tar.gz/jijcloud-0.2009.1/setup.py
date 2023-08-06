from setuptools import setup, find_packages

setup(
    name="jijcloud",
    version="0.2009.1",
    author_email='info@j-ij.com',
    author='Jij Inc.',
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests',
    license='MIT',
    install_requires=['jupyter', 'pyqubo', 'grpcio >= 1.29.0', 'grpcio-tools >= 1.29.0', 'requests', 'toml'],
)
