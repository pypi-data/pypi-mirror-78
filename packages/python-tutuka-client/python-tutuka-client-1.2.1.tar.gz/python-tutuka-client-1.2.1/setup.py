from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='python-tutuka-client',
    version='1.2.1',
    author='Fondeadora',
    author_email='tech@fondeadora.com',
    description='Tutuka XML-RPC Client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/Fondeadora/tutuka-client',
    keywords=['tutuka', 'client'],
    python_requires='>=3.6',
    install_requires=['requests>=2.24.0', 'cryptography>=2.9.2'],
)
