import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="rbi-oss-awscdk-components-pkg",
    version="0.2.1",

    description="A collection of AWS CDK constructs and utils written in python",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="RBI OSS Initiative",
    author_email="RBI-OSSINITIATIVE_Admins@rbinternational.com",
    url="https://github.com/raiffeisenbankinternational/awscdk-components-py",
    packages=setuptools.find_packages(),

    install_requires=[
        "aws-cdk.core",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Typing :: Typed",
    ],
)
