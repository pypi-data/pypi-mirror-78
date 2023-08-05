import os
from setuptools import setup, find_packages


def clean():
    """Custom clean command to tidy up the project root."""
    if "posix" in os.name:
        os.system("rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./*__pycache__/")
    elif "nt" == os.name:
        # possible to-do: also remove directories as above
        os.system(r"del /s /q .\build .\dist .\*.pyc .\*.tgz")


install_reqs = ["numpy"]
dev_reqs = ["pytest", "pytest-cov"]

include_files = {}


if __name__ == "__main__":

    setup(
        name="hiker",
        version="0.1.2",
        license="MIT",
        author="Mimo Tilbich",
        email="haux.johannes@gmail.com",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        packages=find_packages(exclude=["tests", "test.*"]),
        package_data=include_files,
        install_requires=install_reqs,
        extras_require={"dev": dev_reqs},
        python_requires=">=3.7",
    )
