from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'NLPyPort',         # How you named your package folder (MyLib)
  packages = ['.',
  'NLPyPort/',
  "NLPyPort/LemPyPort/normalization",
"NLPyPort/LemPyPort",
"NLPyPort/LemPyPort/dictionary",
"NLPyPort/LemPyPort/rank",
"NLPyPort/LemPyPort/resources/replacements",
"NLPyPort/LemPyPort/resources/acdc",
"NLPyPort/LemPyPort/resources/config",
"NLPyPort/LemPyPort/resources/label",
"NLPyPort/LemPyPort/resources/dictionaries",
"NLPyPort/TagPyPort",
"NLPyPort/TokPyPort",
"NLPyPort/TagPyPort/resources/config",
"NLPyPort/TagPyPort/resources/PoSModels",
"NLPyPort/TokPyPort/config",
"NLPyPort/TokPyPort/resources/config",
"NLPyPort/TokPyPort/resources/replacements",
"NLPyPort/TokPyPort",
"NLPyPort/CRF",
"NLPyPort/config",
"NLPyPort/CRF/trainedModels"
  ], 
  package_data={
"NLPyPort/LemPyPort/resources/replacements":['*'],
"NLPyPort/LemPyPort/resources/acdc":['*'],
"NLPyPort/LemPyPort/resources/config":['*'],
"NLPyPort/LemPyPort/resources/label":['*'],
"NLPyPort/LemPyPort/resources/dictionaries":['*'],
"NLPyPort":['*'],
"NLPyPort/config":['*'],
"NLPyPort/config/":['*'],
"NLPyPort/TagPyPort/resources/config":['*'],
"NLPyPort/TagPyPort/resources/PoSModels":['*'],
"NLPyPort/TokPyPort/resources/replacements":['*'],
"NLPyPort/TokPyPort/resources/config":['*'],
"NLPyPort/TokPyPort/config":['*'],
"NLPyPort/CRF":['*'],
"NLPyPort/CRF/.vscode":['*'],
"NLPyPort/CRF/trainedModels":['*'],
},  # Chose the same as "name"
  version = '2.2.3',      # Start with a small number and increase it with every change you make
  license='cc0-1.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python NLP for Portuguese',   # Give a short description about your library
  author = 'Joao Ferreira',                   # Type in your name
  author_email = 'jdhtml5@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/jdportugal/NLPyPort',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/jdportugal/NLPyPort',    # I explain this later on
  keywords = ['NLP', 'PORTUGUESE', 'PYTHON'],   # Keywords that define your package best
  long_description=long_description,
  long_description_content_type='text/markdown',
  install_requires=[            # I get to this in a second
         "nltk",
"numpy",
"pandas",
"python-crfsuite",
"python-dateutil",
"pytz",
"scikit-learn",
"scipy",
"singledispatch",
"six",
"sklearn",
"sklearn-crfsuite",
"tabulate",
"tqdm",
"xmltodict",

      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)