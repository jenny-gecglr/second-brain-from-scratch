#!/usr/bin/env python3
"""youtube_list.py: list a channel's videos with yt-dlp and keep a resume file.

List a channel:
  python -I -X utf8 scripts/youtube_list.py <channel_url> <out_dir> [--tab videos|shorts]
Mark progress on one video (the agent or you call this after each step):
  python -I -X utf8 scripts/youtube_list.py --mark <out_dir> <video_id> <status>
  status is one of: added, transcript, summary, checked, unavailable (no transcript could be fetched)

Files written inside <out_dir>:
  videos.json       the fast listing (id, title, views, duration). Dates and descriptions are NOT in the fast
                    listing; get them with a second pass (see docs/08).
  _processed.json   resume file {video_id: status}. Created if missing, never overwritten by a listing run.
  new_videos.txt    ids in videos.json that are not in _processed.json at all
  incomplete.txt    ids in _processed.json whose status is not "checked" or "unavailable" yet (continue these first)

Run the listing again later: only new videos show up in new_videos.txt. Nothing is skipped unless
its status was recorded with --mark, so the file is only as accurate as the marks.
Requires: pip install yt-dlp
"""
import json, os, subprocess, sys

STATUSES = ('added', 'transcript', 'summary', 'checked', 'unavailable')
DONE = ('checked', 'unavailable')


def load_processed(out_dir):
    p = os.path.join(out_dir, '_processed.json')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as fh:
            return json.load(fh)
    return {}


def save_processed(out_dir, data):
    with open(os.path.join(out_dir, '_processed.json'), 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=1)


def mark(argv):
    i = argv.index('--mark')
    rest = argv[i + 1:]
    if len(rest) != 3 or rest[2] not in STATUSES:
        print('usage: --mark <out_dir> <video_id> <' + '|'.join(STATUSES) + '>')
        return 2
    out_dir, vid, status = rest
    os.makedirs(out_dir, exist_ok=True)
    data = load_processed(out_dir)
    data[vid] = status
    save_processed(out_dir, data)
    print('marked', vid, '->', status)
    return 0


def listing(argv):
    args = [a for a in argv if not a.startswith('--')]
    tab = 'videos'
    if '--tab' in argv:
        if argv.index('--tab') + 1 >= len(argv):
            print('--tab needs a value: videos or shorts')
            return 2
        tab = argv[argv.index('--tab') + 1]
        if tab not in ('videos', 'shorts'):
            print('--tab must be videos or shorts')
            return 2
        if tab in args:
            args.remove(tab)
    if len(args) < 2:
        print(__doc__)
        return 2
    url, out_dir = args[0].rstrip('/') + '/' + tab, args[1]
    os.makedirs(out_dir, exist_ok=True)
    cmd = [sys.executable, '-m', 'yt_dlp', '--flat-playlist', '--dump-single-json', '--no-warnings', url]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if res.returncode != 0:
        print('yt-dlp failed:', res.stderr[-400:])
        return 1
    data = json.loads(res.stdout)
    vids = []
    for e in data.get('entries') or []:
        if e and e.get('id'):
            vids.append({'id': e['id'], 'title': e.get('title'), 'views': e.get('view_count'),
                         'duration': e.get('duration')})
    with open(os.path.join(out_dir, 'videos.json'), 'w', encoding='utf-8') as fh:
        json.dump(vids, fh, ensure_ascii=False, indent=1)
    processed = load_processed(out_dir)
    if not os.path.exists(os.path.join(out_dir, '_processed.json')):
        save_processed(out_dir, processed)
    new = [v['id'] for v in vids if v['id'] not in processed]
    incomplete = [k for k, s in processed.items() if s not in DONE]
    with open(os.path.join(out_dir, 'new_videos.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(new) + ('\n' if new else ''))
    with open(os.path.join(out_dir, 'incomplete.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(incomplete) + ('\n' if incomplete else ''))
    print('listed', len(vids), 'videos |', len(processed), 'in resume file |', len(new), 'new |', len(incomplete), 'incomplete')
    return 0


def main():
    if '--mark' in sys.argv:
        return mark(sys.argv)
    return listing(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(main())
