# Copyright 2020 The PyWings Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# Import packages
import setuptools

# Read complete description
with open("README.md", mode="r") as fh:
    long_description = fh.read()

# Create setup
setuptools.setup(
    name="pywings",
    version="0.0.2",
    author="Nityan Suman",
    author_email="nityan.suman@gmail.com",
    description="Library that makes your code fly. It extends support for data structures and algorithms for Python.",
    long_description="-",
    long_description_content_type="text/markdown",
    url="https://github.com/nityansuman/pywings",
    license="Apache 2.0",
    packages=setuptools.find_packages(exclude=["python-tutorial", "docs", "tests", ".github"]),
    install_requires=[],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3',
)
