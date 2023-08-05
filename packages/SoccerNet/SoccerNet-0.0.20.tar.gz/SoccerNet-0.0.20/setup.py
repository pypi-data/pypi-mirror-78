from distutils.core import setup
# from setuptools import setup, find_packages

from SoccerNet import __version__, __authors__, __author_email__, __github__

setup(
  name = 'SoccerNet',         # How you named your package folder (MyLib)
  packages=['SoccerNet'],   # Chose the same as "name"
  version = __version__,      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'SoccerNet SDK',   # Give a short description about your library
  author=__authors__,                   # Type in your name
  author_email=__author_email__,      # Type in your E-Mail
  url=__github__,   # Provide either the link to your github or to your website
  # download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['SoccerNet', 'SDK', 'Spotting', 'Football', 'Soccer', 'Video'],   # Keywords that define your package best
  # package_data={'SoccerNet': ['data/SoccerNetGames.json']},
  # include_package_data=True,
  install_requires=[            # I get to this in a second
          'tqdm',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
