import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


setup(name='buza',
      version='0.0.1',
      description='buza',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Ctrl Space',
      author_email='dev@buza.com',
      url='None',
      license='BSD',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Django ~=1.11.0',

          # General libraries
          'Pillow',

          # Django libraries
          'django-taggit',
          'social-auth-app-django',
          'django-tinymce',
          'djangorestframework',
      ],
      entry_points={})
