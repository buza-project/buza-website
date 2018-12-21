import os
import subprocess

from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


extra_kwargs = dict(use_scm_version=True)

if subprocess.call(
        "git rev-parse", shell=True,
        stderr=subprocess.DEVNULL) != 0:
    print("Disabling setuptools-scm")
    extra_kwargs['use_scm_version'] = False


setup(
    name='buza-website',
    description='buza',
    version='0.0.1',
    long_description=README,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Ctrl Space',
    author_email='dev@buza.com',
    url='None',
    license='BSD',

    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,

    setup_requires=['setuptools-scm'],

    install_requires=[
        'Django >2.0',

        # General libraries
        'Pillow',

        # Django libraries
        'django-crispy-forms',
        'django-environ',
        'django-taggit',
        'social-auth-app-django',
    ],
    entry_points={},
    **extra_kwargs,

)
