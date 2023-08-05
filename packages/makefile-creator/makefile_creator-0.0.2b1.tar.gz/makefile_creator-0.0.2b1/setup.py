import setuptools
import makefile_creator.config


with open("README.md", "r") as fh:
    long_description = fh.read()
    fh.close()

# with open('LICENSE', 'r') as fh:
#     li = fh.read()
#     fh.close()
#
# with open('./makefile_creator/README.md', 'w') as fh:
#     fh.write(long_description)
#     fh.close()
#
# with open('./makefile_creator/LICENSE', 'w') as fh:
#     fh.write(li)
#     fh.close()

setuptools.setup(
    name=makefile_creator.config.PACKAGE_NAME,
    version=makefile_creator.config.VERSION,
    author="Romulus-Emanuel Ruja",
    author_email="romulus-emanuel.ruja@tutanota.com",
    description="MakeFile-Creator for makefiles management in c/c++ projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m3sserschmitt/MakeFile-Creator.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English'
    ],
    python_requires='>=3.6',
)
