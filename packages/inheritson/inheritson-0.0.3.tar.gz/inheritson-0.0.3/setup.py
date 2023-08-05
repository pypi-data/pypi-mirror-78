import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inheritson",
    version="0.0.3",
    author="Serhiy Zahoriya",
    author_email="serhiy.int@gmail.com",
    description="Fill in missing data that is inherited by a reference field "
    "in a flat list of dictionaries without inheritance depth limit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/int-ua/inheritson",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.8',
)
