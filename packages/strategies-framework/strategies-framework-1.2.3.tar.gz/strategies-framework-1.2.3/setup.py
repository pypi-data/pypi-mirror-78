import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

__author__ = 'aaron'
__date__ = '2020/09/03'

setuptools.setup(
    name="strategies-framework",
    version="1.2.3",
    author="Aaron",
    author_email="103514303@qq.com",
    description="StrategiesFramework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StarsAaron",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    install_requires=['requests', 'logbook', 'zmq'],
    include_package_data=True,
    zip_safe=True
)