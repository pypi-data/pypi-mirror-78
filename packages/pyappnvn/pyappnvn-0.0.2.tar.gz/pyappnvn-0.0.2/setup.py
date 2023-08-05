from setuptools import setup,find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="pyappnvn",
    packages=find_packages(),
    version="0.0.2",
    description="A Python package for excel and create app.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/nhuannguyen1/site-packages",
    author="Nhuan Nguyen",
    author_email="nguyenvannhuan90123@gmail.com",
    license="MIT",
    classifiers=[
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.7",
                ],
    include_package_data=True,
    install_requires=["requests"],
)