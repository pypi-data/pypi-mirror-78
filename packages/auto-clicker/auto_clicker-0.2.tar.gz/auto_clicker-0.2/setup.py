from distutils.core import setup
setup(
  name = 'auto_clicker',         # How you named your package folder (MyLib)
  packages = ['auto_clicker'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='agpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'You can search for an image on screen and click, hover or hold it.',   # Give a short description about your library
  author = 'Finn Pfaff',                   # Type in your name
  author_email = 'pfaff_finn@yahoo.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Warfare03/auto_clicker/archive/0.2.tar.gz',    # I explain this later on
  keywords = ['image', 'find image', 'click'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pyautogui',
          'numpy',
          'opencv-python',
          'pynput',
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
    'Programming Language :: Python :: 3.8',
  ],
)
