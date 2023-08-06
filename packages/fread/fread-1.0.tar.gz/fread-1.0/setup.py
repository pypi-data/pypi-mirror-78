from setuptools import setup


def getReadme():
    with open("README.md") as f:
        description = f.read()
        return description


setup(
    name="fread",
    version="1.0",
    description="A python package to change from Interaction console based code to file based code",
    long_description=getReadme(),
    long_description_content_type='text/markdown',
    url="",
    author="Venkata Sai Srinivas Paila",
    author_email="pailasaisrinivas7668@gmail.com",
    license="MIT",
    classifiers=[
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=["fread"],
    include_package_data=True,
)
