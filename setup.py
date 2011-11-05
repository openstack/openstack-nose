from setuptools import setup

version = "0.1"

setup(name="novanose",
      version=version,
      description="nova run_tests.py style output for nosetests",
      long_description=open("README.rst").read(),
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords="nose",
      author="Jason K\xc3\xb6lker",
      author_email="jason@koelker.net",
      url="https://github.com/jkoelker/novanose",
      license="Apache License",
      py_modules=["novanose"],
      install_requires=[
          "nose",
      ],
      entry_points="""
      # -*- Entry points: -*-
[nose.plugins.0.10]
novanose = novanose:NovaNose
      """,
      )
