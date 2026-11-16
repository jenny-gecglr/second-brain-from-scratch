#!/usr/bin/env python3
"""list_export_titles.py: list the conversations inside a chat export zip, titles only.

It is step 1 of the scope rule: you must SEE the categories before anything is imported.
It reads the zip in place (nothing is extracted, nothing is written unless you pass --out).

Usage:
  python -I -X utf8 scripts/list_export_titles.py <export.zip> [--out titles.md]

Written for two layouts as they are commonly described. It was tested on synthetic files only, so
confirm it on your real export (formats can change, see docs/04 and docs/05):
  Claude export   conversations.json: list of {"name", "created_at", "chat_messages": [...]}
  ChatGPT export  conversations.json: list of {"title", "create_time", "mapping": {...}}
If the layout is different, the script says so and stops: it never guesses.
"""
import json, sys, zipfile, datetime


def fmt_ts(v):
    if v is None:
        return '?'
    if isinstance(v, (int, float)):
        return datetime.datetime.fromtimestamp(v).strftime('%Y-%m-%d')
    return str(v)[:10]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        return 2
    out_path = None
    if '--out' in sys.argv:
        out_path = sys.argv[sys.argv.index('--out') + 1]
        if out_path in args:
            args.remove(out_path)
    with zipfile.ZipFile(args[0]) as z:
        names = [n for n in z.namelist() if n.lower().endswith('conversations.json')]
        if not names:
            print('No conversations.json found in the zip. Files seen:', z.namelist()[:15])
            return 1
        data = json.loads(z.read(names[0]).decode('utf-8'))
    if not isinstance(data, list) or not data:
        print('conversations.json is not a non-empty list. Layout unknown, stopping.')
        return 1
    first = data[0]
    rows = []
    if 'chat_messages' in first or 'name' in first:
        kind = 'Claude'
        for c in data:
            rows.append((fmt_ts(c.get('created_at')), (c.get('name') or '(untitled)').strip() or '(untitled)',
                         len(c.get('chat_messages') or [])))
    elif 'mapping' in first or 'title' in first:
        kind = 'ChatGPT'
        for c in data:
            msgs = sum(1 for n in (c.get('mapping') or {}).values() if (n or {}).get('message'))
            rows.append((fmt_ts(c.get('create_time')), (c.get('title') or '(untitled)').strip() or '(untitled)', msgs))
    else:
        print('Layout not recognised. Keys of the first item:', sorted(first.keys())[:20])
        return 1
    rows.sort(key=lambda r: r[0])
    lines = ['# ' + kind + ' export: ' + str(len(rows)) + ' conversations', '',
             '| # | date | title | messages |', '|---|---|---|---|']
    for i, (d, t, n) in enumerate(rows, 1):
        lines.append('| ' + str(i) + ' | ' + d + ' | ' + t.replace('|', '/') + ' | ' + str(n) + ' |')
    text = '\n'.join(lines) + '\n'
    if out_path:
        with open(out_path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        print('wrote', out_path, '(' + str(len(rows)), 'conversations)')
    else:
        sys.stdout.write(text)
    return 0


if __name__ == '__main__':
    sys.exit(main())
