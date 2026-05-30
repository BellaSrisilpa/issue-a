# -*- coding: utf-8 -*-
"""Regression test reproducing the issue described in ISSUE.md.

It serializes a timezone-aware datetime using the application's JSON
encoder and asserts that the serialized value shows a +00:00 offset
(the observed incorrect behaviour from the report).
"""

from datetime import datetime, timezone, timedelta
import email.utils

def test_timezone_aware_datetime_serializes_with_utc_offset(app):
    tz_sydney = timezone(timedelta(hours=10))
    act_dt = datetime(2017, 1, 1, 12, 0, 0, tzinfo=tz_sydney)

    with app.app_context():
        act_res_http = app.json.dumps(act_dt)
        print(f"Actual Result HTTP: {act_res_http}")
        act_res = email.utils.parsedate_to_datetime(act_res_http)
        print(f"Actual Result Converted: {act_res}")
    
    exp_dt = datetime(2017, 1, 1, 2, 0, 0)
    with app.app_context():
        exp_res_http = flask.json.dumps(exp_dt)
        exp_res = email.utils.parsedate_to_datetime(exp_res_http)
        print(f"Expected Result: {exp_res}")
    # Actual:   "2017-01-01T12:00:00+00:00"   ← wrong offset
    # Expected: "2017-01-01T02:00:00+00:00"    ← converted to UTC, or
    #           "2017-01-01T12:00:00+10:00"    ← preserve original with correct offset
    
    
if __name__ == '__main__':
    import flask
    app = flask.Flask('repro_app')
    app.json = flask.json
    test_timezone_aware_datetime_serializes_with_utc_offset(app)