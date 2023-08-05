# Copyright © 2017-2020 Richard Gebauer, Karlsruhe Institute of Technology.
# All rights reserved.
#
# This file is part of the qiclib package and released under the terms of
# the GNU Lesser General Public License as published by the Free Software
# Foundation, either version 3 of the License, or any later version.
#
# You should have received a copy of the GNU Lesser General Public License
# as part of this package. If not, see <https://www.gnu.org/licenses/>.
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qiclib",
    version="0.0.1",
    author="Quantum Interface",
    author_email="r.gebauer@kit.edu",
    description="Library to connect to Quantum Interface's QiController.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quantuminterface/qiclib",
    packages=["qiclib"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
)
