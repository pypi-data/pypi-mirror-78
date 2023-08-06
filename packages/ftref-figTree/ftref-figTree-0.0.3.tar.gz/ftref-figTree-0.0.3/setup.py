import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="ftref-figTree",
        author="Jesse Lapere",
        author_email="lapere.j@gmail.com",
        description="An extension to Kivy's Label widget",
        version='0.0.3',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url = "https://gitlab.com/figTree/reflabel",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Topic :: Software Development :: User Interfaces",
            "Topic :: Text Processing",
            ],
        python_requires='>=3.6',
)
