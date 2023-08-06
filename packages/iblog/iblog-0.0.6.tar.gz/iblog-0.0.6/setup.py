from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

NAME = "iblog"
VERSION = "0.0.6"
REQUIRES = ["flask>=1.1.2", "kafka-python >= 2.0.1", "pika>=1.1.0", "apscheduler>=3.6.3", "PyGithub>=1.53",
            "pygitee>=1.0.0"]

setup(
    name=NAME,
    version=VERSION,
    # license='MIT',
    description="Issue blog.",
    author="kingreatwill",
    author_email="350840291@qq.com",
    url="https://github.com/openjw/blog",
    keywords=["issue", "blog"],
    packages=find_packages(),
    install_requires=REQUIRES,
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'iblog = iblog.__main__:main'
        ]
    },
)
