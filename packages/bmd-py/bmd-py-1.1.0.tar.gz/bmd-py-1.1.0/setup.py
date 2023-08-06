from setuptools import setup, find_packages

PACKAGE_NAME = "bmd-py"
VERSION = '1.1.0'

INCLUDE_DATA = [
  "requirements.txt",
  "README.md"
]

def find_description ():
  long_description = ''

  with open('README.md') as f:
    long_description = f.read()

  return long_description

def find_requirements():
  requirements = []

  with open('requirements.txt') as f:
    for line in f:
      if (not line.startswith("#")):
        requirements.append(line.strip())

  return requirements

if __name__ == '__main__':
    setup(
      name=PACKAGE_NAME,
      version=VERSION,
      install_requires=find_requirements(),
      python_requires='>=3.7.8',
      scripts=['src/bmd.py'],
      description='Change scripts into Markdown documentation',
      long_description=find_description(),
      long_description_content_type='text/markdown',
      author='vlnk',
      author_email='vlnk@protonmail.com',
      license='GPLv3+',
      url='https://git.sr.ht/~vlnk/bmd'
    )
