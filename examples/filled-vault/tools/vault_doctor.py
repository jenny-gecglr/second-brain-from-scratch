#!/usr/bin/env python3
"""vault_doctor.py: structural health check for the vault.

READ-ONLY. It never edits, deletes or moves a note. It writes one report:
  outputs/vault-doctor/vault-doctor-report.md   (overwritten on every run)

Usage (from the vault root or anywhere):
  python -I -X utf8 tools/vault_doctor.py             # check and write the report
  python -I -X utf8 tools/vault_doctor.py --snapshot  # record the expected state of raw/ (tools/raw_manifest.json)
  python -I -X utf8 tools/vault_doctor.py --quiet     # summary lines only

Checks: broken wikilinks, empty (0 byte) files, unexpected files in the vault root,
pages missing from the index, orphan pages, missing frontmatter, privacy field on
imported chat notes, encoding problems (BOM, mojibake), log format, canvas targets,
changes inside raw/ (against the snapshot), duplicate page names, decision fields,
future-dated entries, density of [UNVERIFIED], AGENTS.md length, skill list.
Standard library only (Python 3.8+). It checks STRUCTURE, not whether facts are true.
"""
import os, re, sys, json, datetime, collections, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.dirname(HERE)
SKIP_DIRS = {'.obsidian', '.git', 'node_modules', '__pycache__'}
ROOT_ALLOWED = {'AGENTS.md', 'CLAUDE.md', 'GEMINI.md', 'Welcome.md', '.gitignore'}
INDEX_NAMES = ('wiki/INDEX.md', 'wiki/log.md')
MANIFEST = os.path.join(HERE, 'raw_manifest.json')
QUIET = '--quiet' in sys.argv
TODAY = datetime.date.today().isoformat()


def rel(p):
    return os.path.relpath(p, VAULT).replace('\\', '/')


def walk_files():
    for r, ds, fs in os.walk(VAULT):
        ds[:] = [d for d in ds if d not in SKIP_DIRS]
        for f in fs:
            yield os.path.join(r, f)


def read(p):
    try:
        with open(p, 'rb') as fh:
            b = fh.read()
        return b, b.decode('utf-8-sig', errors='replace')
    except Exception:
        return b'', ''


def strip_code(t):
    t = re.sub(r'```.*?```', '', t, flags=re.S)
    t = re.sub(r'~~~.*?~~~', '', t, flags=re.S)
    t = re.sub(r'`[^`\n]*`', '', t)
    return t


HASH_LIMIT = 50 * 1024 * 1024  # files up to 50 MB are also compared by content (sha256); larger files by size only


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def raw_state():
    now = {}
    for r, ds, fs in os.walk(os.path.join(VAULT, 'raw')):
        for f in fs:
            if f == '.gitkeep':
                continue
            p = os.path.join(r, f)
            try:
                st = os.stat(p)
                now[rel(p)] = [st.st_size, int(st.st_mtime), sha(p) if st.st_size <= HASH_LIMIT else '']
            except OSError:
                pass
    return now


def snapshot():
    out = raw_state()
    with open(MANIFEST, 'w', encoding='utf-8') as fh:
        json.dump({'date': datetime.datetime.now().isoformat(timespec='seconds'), 'files': out}, fh)
    print('raw/ snapshot saved:', len(out), 'files ->', rel(MANIFEST))


def main():
    if '--snapshot' in sys.argv:
        snapshot()
        return 0
    files = list(walk_files())
    md = [p for p in files if p.lower().endswith('.md')]
    relset = {rel(p) for p in files}
    low_md = {rel(p)[:-3].lower(): rel(p) for p in md}
    by_name = collections.defaultdict(list)
    for p in md:
        by_name[os.path.splitext(os.path.basename(p))[0].lower()].append(rel(p))

    def resolve(t):
        t = t.split('|')[0].split('#')[0].strip().rstrip('\\').replace('\\', '/').strip()
        if not t or '...' in t or t.lower() in ('link', 'wikilink'):
            return 'IGNORE'
        tl = t.lower()
        tl2 = tl[:-3] if tl.endswith('.md') else tl
        if tl2 in low_md:
            return low_md[tl2]
        for k, v in low_md.items():
            if k.endswith('/' + tl2):
                return v
        if tl2.split('/')[-1] in by_name:
            return by_name[tl2.split('/')[-1]][0]
        for r in relset:
            if r.lower() == tl or r.lower().endswith('/' + tl):
                return r
        return None

    out = collections.defaultdict(list)
    inbound = collections.Counter()
    unverified = {}
    for p in md:
        b, t = read(p)
        rp = rel(p)
        if len(b) == 0 or rp.startswith('outputs/vault-doctor/'):
            continue
        body = strip_code(t)
        for m in re.finditer(r'\[\[([^\]]+)\]\]', body):
            tg = resolve(m.group(1))
            if tg == 'IGNORE':
                continue
            if tg is None:
                out['broken_link'].append((rp, m.group(1).split('|')[0].rstrip('\\')))
            else:
                inbound[tg] += 1
        if b.startswith(b'\xef\xbb\xbf'):
            out['bom'].append(rp)
        if re.search('Ã[ -¿]|Ä[°-¿\u009f]|Å[\u009f\u009e]', t):
            out['mojibake'].append(rp)
        n = t.count('[UNVERIFIED]')
        if n:
            unverified[rp] = n
        if not rp.startswith('raw/'):
            fut = set()
            for m in re.finditer(r'(?m)^(?:updated|date):\s*(\d{4}-\d{2}-\d{2})|^- (\d{4}-\d{2}-\d{2})\b', t):
                d = m.group(1) or m.group(2)
                if d > TODAY:
                    fut.add(d)
            if fut:
                out['future_date'].append(rp + ' (' + ', '.join(sorted(fut)) + ')')
        if rp.startswith('wiki/') and rp not in INDEX_NAMES:
            if not t.lstrip('﻿').startswith('---'):
                out['no_frontmatter'].append(rp)
            elif not re.search(r'^type:', t[:1500], re.M):
                out['no_type'].append(rp)
        if rp.startswith('conversations/') and not re.search(r'^privacy:', t[:1500], re.M):
            out['no_privacy'].append(rp)
        if rp.startswith('wiki/decisions/'):
            head = t[:1200]
            for field in ('date', 'scope', 'status'):
                if not re.search('^' + field + ':', head, re.M):
                    out['decision_field_missing'].append(rp + ' (' + field + ')')
    for p in files:
        rp = rel(p)
        try:
            sz = os.path.getsize(p)
        except OSError:
            continue
        if sz == 0 and not p.endswith('.gitkeep'):
            out['empty_file'].append(rp)
        if '/' not in rp and rp not in ROOT_ALLOWED:
            out['root_stranger'].append(rp)
        if p.lower().endswith('.canvas'):
            try:
                c = json.loads(open(p, encoding='utf-8').read())
                folder = os.path.dirname(rp)
                for nd in c.get('nodes', []):
                    if nd.get('type') == 'file':
                        f = nd.get('file', '')
                        if f not in relset and (folder + '/' + f) not in relset:
                            out['canvas_target_missing'].append(rp + ' -> ' + f)
            except Exception as e:
                out['canvas_target_missing'].append(rp + ' (unreadable: ' + str(e)[:40] + ')')
    idx = next((p for p in md if rel(p) == 'wiki/INDEX.md'), None)
    idx_targets = set()
    if idx:
        for m in re.finditer(r'\[\[([^\]]+)\]\]', strip_code(read(idx)[1])):
            tg = resolve(m.group(1))
            if tg and tg != 'IGNORE':
                idx_targets.add(tg)
    for p in md:
        rp = rel(p)
        if rp.startswith('wiki/') and rp not in INDEX_NAMES:
            if rp not in idx_targets:
                out['not_in_index'].append(rp)
            if inbound[rp] == 0:
                out['orphan'].append(rp)
    ap = os.path.join(VAULT, 'AGENTS.md')
    if os.path.exists(ap):
        n_lines = len(read(ap)[1].splitlines())
        if n_lines > 200:
            out['agents_long'].append('AGENTS.md has ' + str(n_lines) + ' lines (limit 200; move detail to wiki/rules/)')
    sl = os.path.join(VAULT, 'skills', 'Skill-list.md')
    if os.path.exists(sl):
        sl_text = read(sl)[1]
        sk_root = os.path.join(VAULT, 'skills')
        for dp, dn, fn in os.walk(sk_root):
            if any(f.lower() == 'skill.md' for f in fn):
                r_ = os.path.relpath(dp, sk_root).replace(os.sep, '/')
                if r_ != '.' and r_ not in sl_text:
                    out['skill_not_listed'].append('skills/' + r_)
        for ln in sl_text.splitlines():
            m = re.match(r'^\|\s*`([\w-]+)/`', ln)  # only the first column of the table rows
            if m and not os.path.isdir(os.path.join(sk_root, m.group(1))):
                out['skill_folder_missing'].append('skills/' + m.group(1))
    logp = os.path.join(VAULT, 'wiki', 'log.md')
    if os.path.exists(logp):
        bad = 0
        for ln in read(logp)[1].splitlines():
            s = ln.strip()
            if s and not s.startswith('#') and not s.startswith('>') and not re.match(r'^- \d{4}-\d{2}-\d{2}', s):
                bad += 1
        if bad:
            out['log_format'].append('log.md: ' + str(bad) + ' lines do not start with "- YYYY-MM-DD"')
    for n, l in by_name.items():
        if len(l) > 1 and n not in ('index', 'log', 'skill', 'readme'):
            out['duplicate_name'].append(n + ': ' + ', '.join(l))
    if os.path.exists(MANIFEST):
        old = json.load(open(MANIFEST, encoding='utf-8'))
        od = old.get('files', {})
        now = raw_state()
        for k, v in od.items():
            if k not in now:
                out['raw_deleted'].append(k)
            elif now[k][0] != v[0]:
                out['raw_changed'].append(k + ' (size ' + str(v[0]) + ' -> ' + str(now[k][0]) + ')')
            elif len(v) > 2 and v[2] and now[k][2] and v[2] != now[k][2]:
                out['raw_changed'].append(k + ' (same size, content changed)')
        raw_info = 'raw snapshot dated ' + old.get('date', '?')
    else:
        raw_info = 'no raw/ snapshot yet (run with --snapshot once)'

    sections = [
        ('broken_link', 'Broken wikilink', 'ERROR'),
        ('empty_file', 'Empty (0 byte) file', 'ERROR'),
        ('raw_deleted', 'File DELETED in raw/ (raw must never change)', 'ERROR'),
        ('raw_changed', 'File CHANGED in raw/ (size, or content for files up to 50 MB; raw must never change)', 'ERROR'),
        ('canvas_target_missing', 'Canvas points to a missing note (makes empty nodes)', 'ERROR'),
        ('future_date', 'Future-dated entry (later than the computer clock)', 'ERROR'),
        ('root_stranger', 'Unexpected file in the vault root', 'WARNING'),
        ('bom', 'File starts with a BOM', 'WARNING'),
        ('mojibake', 'Broken-character trace (mojibake)', 'WARNING'),
        ('no_privacy', 'Imported chat note without a privacy: field', 'WARNING'),
        ('no_frontmatter', 'Wiki page without frontmatter', 'WARNING'),
        ('no_type', 'Wiki page without type:', 'WARNING'),
        ('decision_field_missing', 'Decision page missing a field', 'WARNING'),
        ('log_format', 'log.md format', 'WARNING'),
        ('skill_not_listed', 'Skill folder missing from Skill-list.md', 'WARNING'),
        ('skill_folder_missing', 'Skill-list.md names a folder that does not exist', 'WARNING'),
        ('agents_long', 'AGENTS.md is over 200 lines', 'WARNING'),
        ('not_in_index', 'Wiki page missing from INDEX.md', 'INFO'),
        ('orphan', 'Orphan wiki page (no page links to it)', 'INFO'),
        ('duplicate_name', 'Same page name in different folders', 'INFO'),
    ]
    ts = datetime.datetime.now()
    L = ['# Vault doctor report', '',
         '- Date: ' + ts.strftime('%Y-%m-%d %H:%M'),
         '- Scanned: ' + str(len(md)) + ' notes (.md), ' + str(len(files)) + ' files',
         '- ' + raw_info, '', '## Summary', '| Check | Level | Findings |', '|---|---|---|']
    counts = {}
    for k, title, lvl in sections:
        n = len(out.get(k, []))
        counts[k] = n
        L.append('| ' + title + ' | ' + lvl + ' | ' + ('0 (ok)' if n == 0 else '**' + str(n) + '**') + ' |')
    L.append('')
    for k, title, lvl in sections:
        items = out.get(k, [])
        if not items:
            continue
        L.append('## ' + title + ' (' + str(len(items)) + ')')
        if k == 'broken_link':
            g = collections.defaultdict(list)
            for p, t in items:
                g[p].append(t)
            for p, ts_ in sorted(g.items(), key=lambda x: -len(x[1]))[:40]:
                L.append('- `' + p + '`: ' + ', '.join('`[[' + x + ']]`' for x in sorted(set(ts_))[:6]))
        else:
            for i in items[:60]:
                L.append('- ' + i)
            if len(items) > 60:
                L.append('- ... (' + str(len(items) - 60) + ' more)')
        L.append('')
    if unverified:
        L.append('## [UNVERIFIED] density (top 10 pages)')
        for p, n in sorted(unverified.items(), key=lambda x: -x[1])[:10]:
            L.append('- `' + p + '`: ' + str(n))
        L.append('')
    L.append('> This report only informs. Fixes are made one by one, with the owner approval.')
    od = os.path.join(VAULT, 'outputs', 'vault-doctor')
    os.makedirs(od, exist_ok=True)
    rp = os.path.join(od, 'vault-doctor-report.md')
    with open(rp, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(L) + '\n')
    err = sum(counts[k] for k, _, l in sections if l == 'ERROR')
    warn = sum(counts[k] for k, _, l in sections if l == 'WARNING')
    info = sum(counts[k] for k, _, l in sections if l == 'INFO')
    print('VAULT DOCTOR: ERROR', err, '| WARNING', warn, '| INFO', info)
    for k, title, lvl in sections:
        if counts[k] and not QUIET:
            print('  [' + lvl + '] ' + title + ': ' + str(counts[k]))
    print('Report:', rel(rp))
    return 1 if err else 0


if __name__ == '__main__':
    sys.exit(main())
