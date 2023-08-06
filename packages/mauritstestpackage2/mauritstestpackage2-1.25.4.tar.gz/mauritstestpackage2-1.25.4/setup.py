from setuptools import setup, find_packages

version = "1.25.4"

setup(
    name="mauritstestpackage2",
    version=version,
    description="Test package from Maurits for uploading to PyPI.",
    long_description=(open("README.rst").read() + "\n\n" + open("CHANGES.rst").read()),
    # Get strings from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="test release pypi",
    author="Maurits van Rees",
    author_email="maurits@vanrees.org",
    url="https://github.com/mauritsvanrees/mauritstestpackage",
    license="GPL",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points="""
      # -*- Entry points: -*-
      """,
)
