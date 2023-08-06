import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
  name = 'pyquestionit',         # How you named your package folder (MyLib)
  packages = ['pyquestionit'],   # Chose the same as "name"
  version = '1.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Official client for QuestionIt.space API',   # Give a short description about your library
  author = 'Alkihis',                   # Type in your name
  author_email = 'beranger.louis.bio@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/alkihis/pyquestionit',   # Provide either the link to your github or to your website
  # download_url = 'https://github.com/alkihis/pyquestionit/archive/1.0.1.tar.gz', 
  long_description=README,
  long_description_content_type="text/markdown",
  include_package_data=True,
  keywords = ['questionit', 'api client'],
  install_requires=[            
    'requests',
    'requests-toolbelt',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
