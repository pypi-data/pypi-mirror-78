from distutils.core import setup
setup(
  name = 'meroshare',
  packages = ['meroshare'],
  version = '0.2.2', 
  license='MIT', 
  description = 'A python package to interact with meroshare', 
  author = 'Saurav Pathak', 
  author_email = 'saurab.pathak.0@gmail.com', 
  url = 'https://gitlab.com/saurab.pathak.0/meroshare.git',
  download_url = 'https://gitlab.com/saurab.pathak.0/meroshare/-/archive/0.2.2/meroshare-0.2.2.tar.gz',
  keywords = ['nepal', 'meroshareapi', 'stockmarketAPI'],   # Keywords that define your package best
  install_requires=['requests', 'prettytable'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
