import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('VERSION', 'r') as fh:
    version = fh.read()

setuptools.setup(
    name="django_page_visibility",
    version=version,
    author="Alex Fischer",
    author_email="alex@quadrant.net",
    description="Implements a function to test whether a given url is currently visible to a given user.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quadrant-newmedia/django_page_visibility",
    packages=['django_page_visibility'],
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["Django>=2.2,<3.1"],
)