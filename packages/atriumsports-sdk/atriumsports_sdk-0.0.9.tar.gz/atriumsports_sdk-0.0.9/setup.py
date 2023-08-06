import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name="atriumsports_sdk",
        version="0.0.9",
        author="Atrium Sports",
        author_email="python_dev@atriumsports.com",
        description="Python module for integration to Atrium Sports APIs",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/Keemotion/datacore_sdk_python",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=[
            'requests',
            'paho-mqtt',
        ],
    )
