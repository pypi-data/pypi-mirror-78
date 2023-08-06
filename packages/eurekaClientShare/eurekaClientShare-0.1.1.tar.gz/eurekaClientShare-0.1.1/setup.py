import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eurekaClientShare",
    version="0.1.1",
    author="Santiago Melo Medina",
    author_email="santiagodevelopment001@gmail.com",
    description="Simple eureka client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/santiagoMeloMedina/eurekaClientShare",
    packages=["eurekaClientShare/asset", "eurekaClientShare/client", "eurekaClientShare/constant", "eurekaClientShare/util"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    python_requires='>=3.6'
)
