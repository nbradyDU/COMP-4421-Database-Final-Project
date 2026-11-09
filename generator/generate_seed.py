"""Generate, validate and export fictional community data as TSV for MySQL import"""

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timedelta
from pathlib import Path
import statistics

from build_data import generate
from community_data import COLUMNS, DEFAULT_SEED, END, ORGANIZATIONS, START
from validate_data import validate


def mysql_field(value):
    """Encode unquoted MySQL fields, escaping literal backslashes."""
    if value is None:
        return r'\N'
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    return (str(value).replace('\\', '\\\\').replace('\0', r'\0')
            .replace('\t', r'\t').replace('\n', r'\n').replace('\r', r'\r')
            .replace('\x1a', r'\Z'))


def export(data, output):
    """Write headerless UTF-8 TSV with LF and MySQL backslash escapes."""
    output.mkdir(parents=True, exist_ok=True)
    for table, columns in COLUMNS.items():
        path = output / f'{table}.tsv'
        with path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.writer(handle, delimiter='\t', lineterminator='\n',
                                quoting=csv.QUOTE_NONE, quotechar=None)
            writer.writerows([mysql_field(row[col]) for col in columns]
                             for row in data[table])


def summarize(data):
    """Print measured engagement; return analytical values for tests."""
    findings = {}
    events = {e['event_id']: e for e in data['event']}
    rsvps = {(r['event_id'], r['organization_membership_id']): r
             for r in data['event_rsvp']}
    by_event = Counter(r['event_id'] for r in data['event_attendance']
                       if r['attendance_status'] == 'attended')
    print('Table counts: ' + ', '.join(
        f'{t}={len(rows)}' for t, rows in data.items()))
    member_counts = Counter(m['organization_id']
                            for m in data['organization_membership'])
    group_counts = Counter(g['organization_id']
                           for g in data['organization_group'])
    for org_id, config in enumerate(ORGANIZATIONS, 1):
        org_events = [e for e in data['event']
                      if e['organization_id'] == org_id]
        reservations = [r for r in data['event_rsvp']
                        if r['organization_id'] == org_id]
        attendance = [a for a in data['event_attendance']
                      if a['organization_id'] == org_id
                      and a['attendance_status'] == 'attended']
        visits = Counter(a['organization_membership_id'] for a in attendance)
        walkins = sum((a['event_id'], a['organization_membership_id'])
                      not in rsvps
                      for a in attendance)
        print(f"{config['name']}: memberships={member_counts[org_id]}, "
              f'groups={group_counts[org_id]}, '
              f'events={len(org_events)}, RSVPs={len(reservations)}, '
              f'attended={len(attendance)}, walk-ins={walkins}, '
              f'unique attendees={len(visits)}, repeat attendees='
              f'{sum(n >= 2 for n in visits.values())}')

        def mean_attendance(predicate):
            return statistics.mean(by_event[e['event_id']] for e in org_events
                                   if predicate(e))

        findings[org_id] = {}
        if org_id in (1, 5):
            public = mean_attendance(
                lambda e: e['visibility'] == 'organization')
            group = mean_attendance(lambda e: e['visibility'] == 'group_only')
            findings[org_id].update(public=public, group=group)
            print(f'  Mean attendance: organization-wide={public:.1f}, '
                  f'group-only={group:.1f}')
        if org_id == 2:
            open_events = {e['event_id'] for e in org_events
                           if e['visibility'] == 'organization'}
            confirmed = {(r['event_id'], r['organization_membership_id'])
                         for r in reservations if r['event_id'] in open_events
                         and r['rsvp_status'] == 'attending'}
            arrived = sum((a['event_id'], a['organization_membership_id'])
                          in confirmed
                          for a in attendance)
            rate = arrived / len(confirmed)
            findings[org_id]['turnout'] = rate
            print(f'  Open-game attending-RSVP turnout={rate:.1%}; '
                  'unrecorded outcomes remain unknown')
        if org_id in (3, 4):
            months = (5, 6, 7, 8, 9) if org_id == 3 else (2, 5, 8, 10)
            peak = mean_attendance(lambda e: e['visibility'] == 'organization'
                                   and e['start_at'].month in months)
            other = mean_attendance(lambda e: e['visibility'] == 'organization'
                                    and e['start_at'].month not in months)
            findings[org_id].update(peak=peak, other=other)
            print(f'  Mean outdoor/seasonal attendance: peak={peak:.1f}, '
                  f'other months={other:.1f}')
        if org_id == 5:
            intro_first = {}
            advanced = defaultdict(list)
            for row in attendance:
                event = events[row['event_id']]
                mid = row['organization_membership_id']
                if event['visibility'] == 'organization':
                    intro_first[mid] = min(
                        intro_first.get(mid, END), event['start_at'])
                else:
                    advanced[mid].append(event['start_at'])
            # Exclude late cohorts with less than 90 days of follow-up.
            cohort = {mid: date for mid, date in intro_first.items()
                      if date <= END - timedelta(days=90)}
            continued = sum(any(date < later <= date + timedelta(days=90)
                                for later in advanced[mid])
                            for mid, date in cohort.items())
            rate = continued / len(cohort)
            findings[org_id]['continuation'] = rate
            print(f'  Intro-to-advanced within 90 days='
                  f'{continued}/{len(cohort)} '
                  f'({rate:.1%}); only cohorts with full follow-up')
    outcomes = Counter(a['attendance_status']
                       for a in data['event_attendance'])
    # Build once rather than treating missing records as absences.
    recorded = {(a['event_id'], a['organization_membership_id'])
                for a in data['event_attendance']}
    unknown = sum(key not in recorded for key in rsvps)
    print(f'Confirmed outcomes={dict(outcomes)}; '
          f'RSVPs without outcome={unknown}')
    return findings


def main():
    """Generate locally, validate before export, and print evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=DEFAULT_SEED)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    output = args.output_dir or Path(__file__).resolve().parent / 'output'
    data = generate(args.seed)
    validate(data)
    summarize(data)
    export(data, output)
    print(f'Validated and wrote eight TSV files to {output}')
    print('TSV generation validated locally; '
          'MySQL import verification pending.')


if __name__ == '__main__':
    main()
