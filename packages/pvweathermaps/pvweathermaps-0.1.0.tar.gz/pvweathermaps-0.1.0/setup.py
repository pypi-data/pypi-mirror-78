import setuptools

setuptools.setup(
    name="pvweathermaps",
    version="0.1.0",
    author="Julián Ascencio-Vásquez",
    author_email="julian.ascencio@fe.uni-lj.si",
    description="Easy access to the Photovoltaic Weather Maps",
    url="https://gitlab.com/jascenciov/pvweathermaps",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['numpy','pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)