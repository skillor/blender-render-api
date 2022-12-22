#!/usr/bin/env python

from setuptools import setup

with open("README_PACKAGE.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [x for x in fh.read().splitlines() if x]

setup(name='Blender Renderer',
      packages=['blender_renderer'],
      version='1.2',
      description='Render blender scenes',
      author='skillor',
      author_email='skillor@gmx.net',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      url='https://github.com/skillor/blender-render-api',
      keywords=['blender', 'render', 'api'],
      classifiers=['Programming Language :: Python :: 3 :: Only',
                   'Topic :: Multimedia :: Graphics'],
      setup_requires=["wheel"],
      install_requires=requirements,
      python_requires='>=3',
      package_data={
          '': ['scripts/*.py'],
      },
      )
