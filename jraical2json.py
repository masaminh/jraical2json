"""JRA公開の重賞カレンダーの内容をjsonにする."""
import json
import sys
from argparse import ArgumentParser, FileType

from icalendar import Calendar


def ical2json(icalstr):
    """icalendar文字列からjsonを取得する.

    Arguments:
        icalstr {str} -- icalendar文字列

    Returns:
        str -- json

    """
    cal = Calendar.from_ical(icalstr)
    events = (ev for ev in cal.walk() if ev.name == 'VEVENT')

    items = [icalevent2item(ev) for ev in events]
    jsonstr = json.dumps(items, ensure_ascii=False)
    return jsonstr


def icalevent2item(event):
    """icalendarイベントからjson用itemを取得する.

    Arguments:
        event {Event} -- icalendarイベント

    Returns:
        dict -- json用item

    """
    item = dict()
    summary = event.decoded('SUMMARY').decode()
    last_paren = summary.rfind('(')
    race_name = summary[:last_paren]
    item['Name'] = race_name
    race_date = event.decoded('DTSTART').strftime('%Y%m%d')
    item['Date'] = race_date
    race_course = event.decoded('LOCATION').decode()
    item['Course'] = race_course

    return item


def main():
    """メイン関数."""
    p = ArgumentParser(
        description='JRA公開の重賞カレンダーの内容をjsonにする')
    p.add_argument(
        '-o', '--output', type=FileType('w'), default=sys.stdout, help='出力先')
    p.add_argument(
        'calendar', type=FileType('r'), help='JRA公開の重賞カレンダー')
    args = p.parse_args()
    icalstr = args.calendar.read()
    jsonstr = ical2json(icalstr=icalstr)

    args.output.write(jsonstr)


if __name__ == "__main__":
    main()
