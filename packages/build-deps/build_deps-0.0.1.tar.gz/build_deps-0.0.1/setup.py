import setuptools
import subprocess

with open("README.md", "r") as fh:
    long_description = fh.read()

version = subprocess.check_output(["git", "describe"]).decode('utf-8')
version = version.replace('v', '')
version = version.replace('\n', '')

setuptools.setup(
    name="build_deps",  # Replace with your own username
    version=version,
    author="Dmitry Khrykib",
    author_email="khrykin@me.com",
    description="A python script to automate building of native dependencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': ['build-deps=build_deps:main'],
    },
    url="https://github.com/khrykin/build_deps",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
