# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import pytz
import tzlocal
import datetime

def get_best_local_timezone():
    zone_name = tzlocal.get_localzone().zone
    if zone_name in pytz.all_timezones:
        return zone_name
    if time.daylight:
        local_offset = time.altzone
        localtz = time.tzname[1]
    else:
        local_offset = time.timezone
        localtz = time.tzname[0]
    local_offset = datetime.timedelta(seconds=-local_offset)
    for zone_name in pytz.all_timezones:
        timezone = pytz.timezone(zone_name)
        if not hasattr(timezone,'_tzinfos'):
            continue
        for utcoffset,daylight,tzname in timezone._tzinfos:
            if utcoffset == local_offset and tzname == localtz:
                return zone_name