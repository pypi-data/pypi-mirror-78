from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="varun",
    version="1.0.0",
    description="A Python package to get my name",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/agmukul63",
    author="Punit Modi",
    author_email="puitmodi11@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["kedia"],
    include_package_data=True,
    #install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "varun=kedia.abc:deep",
        ]
    },
)
