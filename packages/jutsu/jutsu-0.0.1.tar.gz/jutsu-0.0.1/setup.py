import setuptools
from jutsu import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="jutsu",
        version=__version__,
        author="Merwane Drai",
        author_email="merwane@6conf.com",
        description="Independently verify the Bitcoin supply",
        long_description = long_description,
        long_description_content_type = "text/markdown",
        url = "https://github.com/merwane/jutsu",
        download_url = "https://github.com/merwane/jutsu",
        license='MIT',
        keywords={
            "bitcoin",
            "bitcoin-verification",
            "bitcoin-cli"
            },
        classifiers=(
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8'
            ),
        install_requires=("oogway", "PyInquirer", "pyfiglet", "colorama", "yaspin"),
        tests_require=["pytest"],
        packages = setuptools.find_packages(),
        entry_points='''
            [console_scripts]
            jutsu=jutsu.cli:cli
        ''',
        include_package_data = True
        )