from setuptools import setup

long_description = open('README.md').read()

setup(
    name="xontrib-xlsd",
    version="0.0.1",
    license="GPLv3",
    url="https://github.com/cafehaine/xontrib-xlsd",
    download_url="https://github.com/DangerOnTheRanger/xonsh-apt-tabcomplete/tarball/v0.1.6",
    description="An improved ls for xonsh, inspired by lsd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CaféHaine",
    author_email="kilian.guillaume@gmail.com",
    packages=['xontrib'],
    package_dir={'xontrib': 'xontrib'},
    package_data={'xontrib': ['*.xsh']},
    zip_safe=False,
    classifiers=[
        "Environment :: Console",
        "Environment :: Plugins",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3"
    ]
)
