from setuptools import setup

CLIENT_VERSION = "0.1.1"
PACKAGE_NAME = "kubernetes_leaderelection_asyncio"

with open('requirements.txt') as f:
    REQUIRES = f.readlines()

setup(
    name=PACKAGE_NAME,
    version=CLIENT_VERSION,
    description="Leader electrion for kubernetes asyncio client",
    author_email="",
    author="",
    license="Apache License Version 2.0",
    url="https://github.com/ollytheninja/kubernetes_leaderelection_asyncio",
    keywords=[],
    python_requires='>3.7',
    install_requires=REQUIRES,
    packages=[
        'leaderelection',
        'leaderelection.resourcelock',
        ],
    include_package_data=True,
    long_description="""\
        a copy of the leader election code from the Official Python client library for kubernetes to make it compatible with it's not so official asyncio counterpart.     
    """,
)
