from setuptools import setup

setup(name="ezconfig",
      version="1.2.0",
      description="Utility class for reading configuration files.",
      author="Nathan Addy",
      author_email="nathan.addy@windfalltechnical.com",
      url="http://bitbucket.org/nathanaddy/ezconfig",
      license="MIT",
      packages=["ezconfig"],
      install_requires = ["dateutils"],
      zip_safe=False
)
