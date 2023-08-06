import setuptools

setuptools.setup(
    name="AIInfo",
    version="0.10.0",
    license='MIT',
    author="Packager",
    author_email="aiinfo@gmail.com",
    description="Package",
    long_description=open('README.md').read(),
    url="https://github.com",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)