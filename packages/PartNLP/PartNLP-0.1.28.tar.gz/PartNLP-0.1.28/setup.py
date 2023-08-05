import setuptools

with open('README.rst', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='PartNLP',
    version='0.1.28',
    # Author details
    author='Part DP',
    author_email='info@partdp.ai',
    description="A Python NLP Library for Persian language, by PartDP AI",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url="https://github.com/partdpai/PartNLP",
    packages=setuptools.find_packages(),
    classifiers=[
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    keywords='natural-language-processing nlp natural-language-understanding',
    install_requires=['hazm', 'parsivar', 'stanza', 'nltk',
                      'dash', 'dash_bootstrap_components',
                      'terminaltables', 'psutil'],
    python_requires='>=3.7',
    nltk_requires='== 3.4'
    )
