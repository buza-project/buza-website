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

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from taggit.forms import TagField
from taggit.managers import TaggableManager

from widgets import TagAutocomplete


class TaggableManagerAutocomplete(TaggableManager):
    def formfield(self, form_class=TagField, **kwargs):
        field = super(TaggableManagerAutocomplete, self).formfield(form_class, **kwargs)
        field.widget = TagAutocomplete()
        return field


if 'south' in settings.INSTALLED_APPS:
    try:
        from south.modelsinspector import add_ignored_fields
    except ImportError:
        pass
    else:
        add_ignored_fields(["^taggit_autocomplete_modified\.managers"])
