# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import unicodedata
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import (resolve,reverse,NoReverseMatch,get_script_prefix)
from django.shortcuts import redirect
from django.utils.encoding import smart_text
from django.utils.http import is_safe_url
from django.utils import translation

def admin_url(model, url, object_id=None):
    opts = model._meta
    url = "admin:%s_%s_%s" % (opts.app_label,opts.object_name.lower(),url)
    args = ()
    if object_id is not None:
        args = (object_id,)
    return reverse(url,args=args)
