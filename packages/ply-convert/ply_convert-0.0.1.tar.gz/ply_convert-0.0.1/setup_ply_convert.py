from setuptools import setup, Extension, find_packages
import re

def find_version(fname):
    with open(fname,'r') as file:
        version_file=file.read()
        version_match = re.search(r"__VERSION__ = ['\"]([^'\"]*)['\"]",version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open("ply/README.md", "r") as handle:
    conv_description = handle.read()

version=find_version("ply/ply_convert.py")

setup(
     name='ply_convert',
     version=version,



     author="Serge Dmitrieff",
     description="A minimal ply conversion tools",
     long_description=conv_description,
     long_description_content_type='text/markdown',
     url="https://github.com/SergeDmi/Python-Tools/",
     install_requires=[
          'sklearn',
          'numpy',
          'plyfile',
          'sio_tools'
      ],
     packages=find_packages(),
     scripts=['ply/bin/ply_convert','ply/ply_convert.py']
 )
