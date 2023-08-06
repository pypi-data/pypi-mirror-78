import setuptools

setuptools.setup(
    name="pubsub_utils",
    version="1.0.0b0",
    author="Wonderful Agency",
    author_email="web.devops@wonderful.com",
    description="Pub sub package ",
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/wonderfulagency/pubsub-utils",
    packages=setuptools.find_packages(),
    install_requires=["google-cloud-pubsub==1.7.0"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires="~=3.7",
)

