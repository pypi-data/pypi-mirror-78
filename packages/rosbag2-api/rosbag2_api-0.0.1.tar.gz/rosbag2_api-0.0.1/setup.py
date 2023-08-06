import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

package_name = 'rosbag2_api'

setuptools.setup(
    name=package_name,
    version="0.0.1",
    description="Package for reading bag files and convert to csv.",
    url="https://github.com/biospine/reading_rosbag",
    author="Ana de Sousa",
    author_email="anacsousa@lara.unb.br",
    license='GNU GPLv3',
    packages=[package_name],
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='rosbag',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'rosidl_runtime_py',
    ],
    python_requires='>=3.6',
)