import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="machnamh-unmakingyou", # Replace with your own username
    version="0.0.23",
    author="Aideen Farrell",
    author_email="aideenf@hotmail.com",
    description="An ipywidgets based package for detecting bias in ML data and Models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aideenf/machnamh",
    packages=setuptools.find_packages(), 
    package_data={
        'machnamh': ['data/law_data.csv',
                    'data/absolute.png',
                    'data/count.png']
    },
    install_requires=[
            'kaleido>=0.0.3',
            'numpy',
             'matplotlib',
             'seaborn',
             'pandas',
             'scikit-learn',
             'pandas-profiling[notebook]',
             'phik',
             'ipywidgets', 
             'plotly',
             'ipyfilechooser',
             'dill',
             'IPython',
             'shap',
             'aequitas',
             'scipy', 
             'typing>=3.7.4.3',
             'benfordslaw>=0.1.3',
             'missingno'
            
        ],
    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    #'Intended Audience :: Data Scientist:: ML practitioner',
    #'Topic :: Machine Learning Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.6',
)
