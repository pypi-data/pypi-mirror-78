from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ipay_sdk',
    version='0.0.3',
    description='Ipay SDK',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sartim/ipay-sdk',
    author='write2sartim@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'marshmallow',
        'requests',
        'tox'
    ],
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
