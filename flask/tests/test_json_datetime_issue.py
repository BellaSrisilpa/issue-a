# -*- coding: utf-8 -*-
from datetime import datetime, timezone, timedelta
import email.utils
import flask


def test_timezone_aware_datetime_serializes_with_utc_offset(app):
    tz_sydney = timezone(timedelta(hours=10))
    act_dt = datetime(2017, 1, 1, 12, 0, 0, tzinfo=tz_sydney)

    with app.app_context():
        act_res_http = flask.json.dumps(act_dt)
        act_res = email.utils.parsedate_to_datetime(act_res_http)
    
    exp_dt = datetime(2017, 1, 1, 2, 0, 0)
    with app.app_context():
        exp_res_http = flask.json.dumps(exp_dt)
        exp_res = email.utils.parsedate_to_datetime(exp_res_http)

    # Actual incorrect behaviour: "2017-01-01T12:00:00+00:00" (wrong offset)
    # Expected correct behaviour: "2017-01-01T02:00:00+00:00" (converted to UTC)
    assert act_res == exp_res