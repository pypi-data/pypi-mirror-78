from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(
    name='3dof-hexapod-ik-generator',
    author = "Alex Pylypenko (macaquedev)",
    url = "https://github.com/macaquedev",
    author_email = "macaquedev@gmail.com",
    license = 'MIT',
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"

    ],
    version='1.0.0',
    description="This is a module which calculates IK servo angles for leaning and shifting a 3dof hexapod's body.",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    packages=["ikengine"],
    package_dir = {'': 'sample'},
    include_package_data=True,
)
