from setuptools import setup, find_packages

# classifiers list ref: https://pypi.org/pypi?%3Aaction=list_classifiers
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: MacOS :: MacOS 9',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='gmsdict2csv',
  version='0.0.1',
  description='PyPi package coverts a flat list to a csv file and saves it in at the given path.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Gumshoe Media Inc. Team',
  author_email='gumshoe.media.inc@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords=['data', 'list', 'csv', 'file'],
  packages=find_packages(),
  install_requires=['']
)
