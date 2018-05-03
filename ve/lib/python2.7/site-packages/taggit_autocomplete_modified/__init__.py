# -*- coding: utf-8 -*-
#
#  This file is part of django-taggit-autocomplete-modified.
#
#  django-taggit-autocomplete-modified provides autocomplete functionality
#  to the tags form field of django-taggit.
#
#  Development Web Site:
#    - http://www.codetrax.org/projects/django-taggit-autocomplete-modified
#  Public Source Code Repository:
#    - https://source.codetrax.org/hgroot/django-taggit-autocomplete-modified
#
#  Copyright 2011-2016 George Notaras <gnot [at] g-loaded.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# Scheme: <major>.<minor>.<maintenance>.<maturity>.<revision>
# maturity: final/beta/alpha

VERSION = (0, 1, 0, 'beta', 6)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2] is not None:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3] != 'final':
        if VERSION[4] > 0:
            version = '%s%s%s' % (version, VERSION[3][0], VERSION[4])
        else:
            version = '%s%s' % (version, VERSION[3][0])
    return version

__version__ = get_version()

def get_status_classifier():
    if VERSION[3] == 'final':
        return 'Development Status :: 5 - Production/Stable'
    elif VERSION[3] == 'beta':
        return 'Development Status :: 4 - Beta'
    elif VERSION[3] == 'alpha':
        return 'Development Status :: 3 - Alpha'
    raise NotImplementedError
