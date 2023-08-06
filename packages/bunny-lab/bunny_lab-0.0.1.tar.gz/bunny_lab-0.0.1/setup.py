import setuptools

setuptools.setup(
    name="bunny_lab",
    version="0.0.1",
    author="Simon Pfreundschuh",
    author_email="simon.pfreundschuh@chalmers.se",
    description="An interactive Python quest to save the bunnies.",
    url="https://github.com/simonpf/bunny_lab",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
