from setuptools import setup

def readme():
    with open('README.md') as f:
        README=f.read()
    return README




setup(
    name="cryptopy-cli",
    version="1.0.0",
    description="A CLI based encryption-decryption tool using SHA256",
    long_description=readme() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    author="M.Yavuz Yagis",
    author_email="mehmetyavuzyagis@gmail.com",
    packages=['cryptopy'],
    install_requires=['click','pyfiglet','termcolor','pycryptodome'],
    url="https://github.com/MYavuzYAGIS/cryptopy",
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
    entry_points={
        "console_scripts": [
            "cryptopy-cli=cryptopy.cryptopy:main",
        ]
    })