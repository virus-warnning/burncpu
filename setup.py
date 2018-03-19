from setuptools import setup

# Load reStructedText description.
# Online Editor   - http://rst.ninjs.org/
# Quick Reference - http://docutils.sourceforge.net/docs/user/rst/quickref.html
readme = open('README.rst', 'r')
longdesc = readme.read()
readme.close()

setup(
  name='burncpu',
  version='0.0.14',
  description='A worker dispatcher with multiprocessing and multithreading.',
  long_description=longdesc,
  url='https://github.com/virus-warnning/burncpu',
  license='MIT',
  author='Raymond Wu',
  python_requires='>=3.6'
)
