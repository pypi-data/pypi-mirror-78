import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rest_framework_duration_iso_field",
    version="0.0.2",
    author="otto001",
    author_email="",
    description="A DRF serializer field for basic iso8601 duration strings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/otto001/rest_framework_duration_iso_field",
    packages=("rest_framework_duration_iso_field",),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
       "django>=3",
       "djangorestframework>=3"
    ]
)