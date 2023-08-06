import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

files = ["resources/*"]

setuptools.setup(
    name="take-a-break",
    author="Paul Brodner",
    author_email="paulbrodner@gmail.com",
    description="Reminds you to take breaks",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/paulbrodner/take-a-break",
    project_urls={
        'Source': 'https://github.com/paulbrodner/take-a-break',
        'Tracker': 'https://github.com/paulbrodner/take-a-break/issues',
    },
    packages=setuptools.find_packages(),
    package_data={'take_a_break': files},
    install_requires=[
        'requests',
        'Pillow'
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Utilities",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
