# setup.py for touketsu

from setuptools import setup

def _setup():
    # short and long descriptions
    desc_short = ("A package for creating classes that disallow dynamic "
                  "attribute creation.")
    with open("README.rst", "r") as rmf:
        desc_long = rmf.read()
    # version
    with open("VERSION", "r") as vf:
        version = vf.read().rstrip()
    # setup
    setup(name = "touketsu",
          version = version,
          description = desc_short,
          long_description = desc_long,
          long_description_content_type = "text/x-rst",
          url = "https://github.com/phetdam/touketsu",
          author = "Derek Huang",
          author_email = "djh458@stern.nyu.edu",
          packages = ["touketsu"],
          classifiers = ["License :: OSI Approved :: MIT License",
                         "Operating System :: OS Independent",
                         "Programming Language :: Python :: 3.6",
                         "Programming Language :: Python :: 3.7",
                         "Programming Language :: Python :: 3.8"],
          license = "MIT",
          project_urls = {
              "Documentation":"https://touketsu.readthedocs.io/en/latest/",
              "Source": "https://github.com/phetdam/touketsu/"
          },
          python_requires = ">=3.6"
    )

if __name__ == "__main__":
    _setup()
