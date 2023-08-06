import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dpsbin",
    version="0.0.0",
    author="Hans Musgrave",
    author_email="Hans.Musgrave@gmail.com",
    description="Compute exact DPS for turn-based games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hmusgrave/dpsbin",
    download_url="https://github.com/hmusgrave/dpsbin/archive/0.0.0.tar.gz",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'scipy>=1.0.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
