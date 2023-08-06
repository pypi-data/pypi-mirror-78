import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="besos",
    version="1.7.0",
    description="A library for Building and Energy Simulation, Optimization and Surrogate-modelling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(
        exclude="pytests"
    ),  # should this by pytest or test ?
    # should we have package_dir={"": "besos"} ?
    url="https://gitlab.com/energyincities/besos",
    author="Ralph Evins",
    author_email="revins@uvic.ca",
    include_package_data=True,
    install_requires=[
        "dask[complete]",
        "dataclasses",  # only used in objectives
        "Deprecated",
        "eppy",
        "geomeppy",
        "ipython",  # only used by example_ui
        "ipywidgets",  # only used by example_ui
        "matplotlib",  # only used by IDF_class
        "numpy",
        "pandas",
        "platypus-opt",
        "PuLP<=2.1",
        "pyDOE2",
        "pyehub",  # E-Hub only
        "pyomo<5.7",
        "PyUtilib<6",
        "rbfopt<=4.1.1",  # Pinned due to test output changing. Can probably unpin
        "Shapely",  # only used in eppy funcs
        "tqdm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "complete": [  # for use on the hub
            "ipysheet",
            "jupyter",
            "papermill",
            "pvlib",
            "pyKriging",
            "PyYAML",
            "SALib",
            "scikit-learn",
            "scipy",
            "seaborn",
            "sklearn",
        ],
    },
)
