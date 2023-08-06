from distutils.core import setup
setup(
  name = 'vterm',         # How you named your package folder (MyLib)
  packages = ['vterm'],   # Chose the same as "name"
  version = '1.1',
  license = "MIT",
  description = 'A virtual terminal for making interactive games in python.',   # Give a short description about your library
  author = 'Ian Bhatt',                   # Type in your name
  author_email = 'ianbhatt@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/DESTROYER3999/vterm',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/DESTROYER3999/vterm/archive/1.1.tar.gz',    # I explain this later on
  keywords = ['game', 'terminal', 'text', 'based', 'tkinter', 'gui', 'simple'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'threading'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)