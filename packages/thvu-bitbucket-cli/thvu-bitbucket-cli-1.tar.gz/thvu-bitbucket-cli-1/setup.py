from setuptools import setup

setup(
    name="thvu-bitbucket-cli",
    version="1",
    py_modules=["repo"],
    packages=["lib", "lib.bitbucketCLI"],
    include_package_data=True,
    install_requires=["click", "requests"],
    url="https://github.com/thvu11/Bitbucket-CLI.git",
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ],
    entry_points="""
        [console_scripts]
        bb=lib.bb:cli
    """,
)
