from distutils.core import setup
setup(
  name = 'facebookparser',         # How you named your package folder (MyLib)
  packages = ['facebookparser', 'facebookparser/menu'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='mit',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'based on https://mbasic.facebook.com',   # Give a short description about your library
  author = 'Salis Mazaya',                   # Type in your name
  author_email = 'salismazaya@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/salismazaya/facebookparser',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/salismazaya/facebookparser/archive/v0.0.1.tar.gz',    # I explain this later on
  keywords = ['facebook', 'scraping', 'web scraping'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'bs4',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
  ],
)