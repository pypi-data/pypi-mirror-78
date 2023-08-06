import pkg_resources
import setuptools

pkg_resources.require("setuptools>=40.9.0")
setuptools.setup(
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*"]),
    package_data={
        "": [
            "py.typed",
            "*.pyi"
        ]
    }
)
