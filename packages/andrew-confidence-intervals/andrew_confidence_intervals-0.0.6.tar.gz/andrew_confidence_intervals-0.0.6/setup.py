from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Science/Research',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='andrew_confidence_intervals',
  version='0.0.6',
  description='Package for calculation of confidence intervals.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type = 'text/x-rst',
  url='https://github.com/Cliefspring/andrew_confidence_intervals',  
  author='Andrey Vazhentsev',
  author_email='vazhentsev@inbox.ru',
  license='MIT', 
  classifiers=classifiers,
  keywords='confidence intervals', 
  packages=find_packages(),
  install_requires=['numpy', 'scipy'] 
)