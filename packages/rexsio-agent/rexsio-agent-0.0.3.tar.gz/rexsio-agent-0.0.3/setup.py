import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rexsio-agent",
    version=os.getenv('RELEASE_VERSION'),
    entry_points={
        'console_scripts': [
            'agent = agent.__main__:main'
        ]
    },
    author="rexs.io sp. z o.o.",
    author_email="hello@rexs.io",
    description="Rexsio Agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rexsio/agent",
    packages=setuptools.find_packages(exclude=['tests']),
    test_suite="tests",
    tests_require=[],
    install_requires=['autobahn==20.2.1',
                      'Twisted==19.10.0',
                      'requests==2.22.0',
                      'psutil==5.6.7',
                      'docker==4.2.0',
                      'pyOpenSSL==19.1.0',
                      'service_identity==18.1.0',
                      'python-dotenv==0.12.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
