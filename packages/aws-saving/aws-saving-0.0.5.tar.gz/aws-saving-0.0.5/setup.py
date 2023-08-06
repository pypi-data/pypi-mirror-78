import setuptools
import aws_saving

setuptools.setup(
    name="aws-saving",
    version=aws_saving.__version__,
    author=aws_saving.__author__,
    author_email="alessandra.bilardi@gmail.com",
    description="AWS saving Python package",
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    url="https://aws-saving.readthedocs.io/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        "Source":"https://github.com/bilardi/aws-saving",
        "Bug Reports":"https://github.com/bilardi/aws-saving/issues",
        "Funding":"https://donate.pypi.org",
    },
)
