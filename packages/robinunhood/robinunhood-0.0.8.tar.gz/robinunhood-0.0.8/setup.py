from distutils.core import setup
setup(
  name = 'robinunhood',         # How you named your package folder (MyLib)
  packages = ['robinunhood'],   # Chose the same as "name"
  version = '0.0.8',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'utilities for working with the Robinhood stock trading platform',   # Give a short description about your library
  long_description = 'utilities for working with the Robinhood stock trading platform',
  author = 'Ashutosh Sanzgiri',                   # Type in your name
  author_email = 'sanzgiri@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/sanzgiri/robinunhood',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/sanzgiri/robinunhood/archive/0.0.8.tar.gz',    # I explain this later on
  keywords = ['robinhood', 'stock lists', 'collections'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)