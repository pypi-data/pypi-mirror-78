from setuptools import setup
from setuptools import find_packages

def rd():
    with open("README.md") as f:
        return f.read()

setup(name='pydlmafs',
      version='0.0.1',
      description='Python basic Deep Learning maths package',
      long_description=rd(),
      long_description_content_type='text/markdown',
      url="https://github.com/booleangabs/pydlmafs",
      download_url = 'https://github.com/booleangabs/pydlmafs/releases/download/v001/pydlmafs-0.0.1.tar.gz',
      author='José Gabriel Pereira Tavares',
      author_email='jgpt@cin.ufpe.br',
      keywords=['math', 'deeplearning', 'python3'],
      license = 'MIT',
      packages=find_packages(),
      classifiers=["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",],
      python_requires='>=3.6',
      install_requires='matplotlib')