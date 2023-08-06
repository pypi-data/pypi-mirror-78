from setuptools import setup

with open("README.md", "r") as f:
        long_description = f.read()

setup(
  name = 'domonic',
  version = '0.2.1',
  author="@byteface",
  author_email="byteface@gmail.com",
  license="MIT",
  url = 'https://github.com/byteface/domonic',
  download_url = 'https://github.com/byteface/pypals/archive/0.2.1.tar.gz',
  description = 'generate html with python 3 and quite a bit more',
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords = ['html', 'generate', 'templating', 'dom', 'terminal', 'json', 'web', 'template', 'javascript', 'DOM', 'GUI'],
  classifiers=[
      "Programming Language :: Python :: 3",
      "Programming Language :: JavaScript",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.6",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Development Status :: 4 - Beta",
      "Environment :: Web Environment",
      "Intended Audience :: Developers",
      "Intended Audience :: Other Audience",
      "License :: OSI Approved :: MIT License",
      "Natural Language :: English",
      "Operating System :: OS Independent",
      "Topic :: Internet",
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Multimedia :: Graphics :: Presentation",
      "Topic :: Software Development",
      "Topic :: Software Development :: Code Generators",
      "Topic :: Terminals",
      "Topic :: Utilities"
  ],
  install_requires=[
          'requests', 'python-dateutil', 'urllib3'
  ],
  packages = ['domonic'],
  include_package_data = True,
)
