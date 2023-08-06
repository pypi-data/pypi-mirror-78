from distutils.core import setup
import setuptools

def readme():
    with open(r'README.txt') as f:
        README = f.read()
    return README

setup(
    name = 'pymyfile',
    packages = setuptools.find_packages(),
    version = '1.0.0',
    license='MIT',
    description = 'PyMyFile is a python library for advance file handeling in the easiest possible way',
    author = 'Ankit Raj Mahapatra',
    author_email = 'ankitrajjitendra816@gmail.com',
    url = 'https://github.com/Ankit404butfound/PyMyFile',
    download_url = 'https://github.com/Ankit404butfound/PyMyFile/archive/1.0.0.tar.gz',
    keywords = [
          'numpihy',
          'denumiphy',
          'bulletiphy',
          'debulletiphy',
          'asteriphy',
          'deasteriphy',
          'read',
          
          
      ],
    install_requires=[],
    include_package_data=True,
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    ],
)
