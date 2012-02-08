from setuptools import setup, find_packages

version = "0.5"

setup(name="openstack.nose_plugin",
      version=version,
      description="openstack run_tests.py style output for nosetests",
      long_description=open("README.rst").read(),
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords="nose",
      author="Jason K\xc3\xb6lker",
      author_email="jason@koelker.net",
      url="https://github.com/jkoelker/openstack-nose",
      license="Apache Software License",
      packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
      install_requires=[
          "nose",
          "colorama",
          "termcolor",
      ],
      entry_points="""
      # -*- Entry points: -*-
[nose.plugins.0.10]
openstack.nose_plugin = openstack.nose_plugin:Openstack
      """,
      namespace_packages=['openstack'],
      )
