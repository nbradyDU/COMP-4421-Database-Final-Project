"""Essential schema and participation checks, without database access."""

from collections import Counter
from datetime import datetime

from community_data import COLUMNS, END, ORGANIZATIONS, START


def require(condition, message):
    """Raise a useful validation error even when Python runs with -O."""
    if not condition:
        raise ValueError(message)


def validate(data):
    """Check keys, composite references, current eligibility and chronology."""
    indexes = {}
    for table, columns in COLUMNS.items():
        rows = data[table]
        require(all(set(row) == set(columns) for row in rows),
                f'{table}: column mismatch')
        indexes[table] = {row[columns[0]]: row for row in rows}
        require(len(indexes[table]) == len(rows), f'{table}: duplicate ID')
        require(all(isinstance(key, int) and key > 0
                    for key in indexes[table]), f'{table}: invalid ID')
    unique_keys = {
        'platform_user': [('username',), ('email',)],
        'organization': [('name',)],
        'organization_membership': [('user_id', 'organization_id')],
        'organization_group': [('organization_id', 'name')],
        'group_membership': [('group_id', 'organization_membership_id')],
        'event_rsvp': [('event_id', 'organization_membership_id')],
        'event_attendance': [('event_id', 'organization_membership_id')],
    }
    for table, keys in unique_keys.items():
        for key in keys:
            values = [tuple(row[col] for col in key) for row in data[table]]
            require(len(set(values)) == len(values),
                    f'{table}: duplicate {key}')
    enums = {
        'platform_status': {'active', 'inactive', 'suspended'},
        'membership_status': {'active', 'inactive', 'suspended'},
        'status': {'active', 'inactive', 'archived'},
        'role': {'member', 'admin', 'owner'},
        'delivery_mode': {'online', 'offline'},
        'rsvp_status': {'attending', 'maybe', 'cancelled'},
        'attendance_status': {'attended', 'absent'},
    }
    nullable = {('organization', 'description'),
                ('organization_group', 'description'), ('event', 'group_id'),
                ('event', 'description'), ('event', 'capacity'),
                ('event_attendance', 'checked_in_at')}
    limits = {'username': 50, 'email': 254, 'display_name': 100, 'title': 255}
    for table, rows in data.items():
        for row in rows:
            for col, value in row.items():
                require(value is not None or (table, col) in nullable,
                        f'{table}: unexpected NULL {col}')
                if col in enums:
                    require(value in enums[col], f'{table}: invalid {col}')
                if col in limits:
                    require(isinstance(value, str) and
                            0 < len(value) <= limits[col],
                            f'{table}: invalid length {col}')
                if col == 'name':
                    limit = 100 if table == 'organization_group' else 255
                    require(0 < len(value) <= limit, f'{table}: invalid name')
                if isinstance(value, datetime):
                    require(START <= value < END,
                            f'{table}: date outside window')
            if 'organization_id' in row and table != 'organization':
                require(row['organization_id'] in indexes['organization'],
                        f'{table}: missing organization')
    users = indexes['platform_user']
    members = indexes['organization_membership']
    groups = indexes['organization_group']
    events = indexes['event']
    links = {}
    for member in members.values():
        require(member['user_id'] in users, 'membership: missing user')
        require(users[member['user_id']]['created_at'] <= member['joined_at'],
                'membership: joined before platform registration')
        organization = indexes['organization'][member['organization_id']]
        require(organization['created_at'] <= member['joined_at'],
                'membership: joined before organization')
    for group in groups.values():
        require(group['visibility'] in ('public', 'private'),
                'group: visibility')
    for link in data['group_membership']:
        group = groups.get(link['group_id'])
        member = members.get(link['organization_membership_id'])
        require(group is not None and member is not None,
                'group: missing reference')
        require(group['organization_id'] == member['organization_id']
                == link['organization_id'], 'group: organization mismatch')
        require(member['joined_at'] <= link['joined_at'],
                'group: joined too early')
        links[link['group_id'], link['organization_membership_id']] = link
    for group_id in groups:
        leaders = [link for link in data['group_membership']
                   if link['group_id'] == group_id
                   and link['role'] in ('owner', 'admin')]
        require(sum(link['role'] == 'owner' for link in leaders) == 1,
                'group: expected one owner')
        require(1 <= sum(link['role'] == 'admin' for link in leaders) <= 2,
                'group: expected one or two admins')
        for link in leaders:
            member = members[link['organization_membership_id']]
            require(link['membership_status'] == 'active'
                    and member['membership_status'] == 'active'
                    and users[member['user_id']]['platform_status']
                    == 'active',
                    'group: inactive leader')
    for event in events.values():
        require(event['start_at'] < event['end_at'], 'event: invalid times')
        require(event['status'] == 'archived',
                'event: completed historical events must be archived')
        require(event['capacity'] is None or (
            isinstance(event['capacity'], int) and event['capacity'] > 0),
            'event: invalid capacity')
        require(event['visibility'] in ('organization', 'group_only'),
                'event: invalid visibility')
        group = groups.get(event['group_id'])
        require(event['group_id'] is None or (group is not None and
                group['organization_id'] == event['organization_id']),
                'event: invalid hosting group')
        require(event['visibility'] != 'group_only' or group is not None,
                'event: group-only without group')
    rsvps = {(r['event_id'], r['organization_membership_id']): r
             for r in data['event_rsvp']}
    for table in ('event_rsvp', 'event_attendance'):
        for row in data[table]:
            event = events.get(row['event_id'])
            member = members.get(row['organization_membership_id'])
            require(event is not None and member is not None,
                    f'{table}: missing reference')
            require(event['organization_id'] == member['organization_id']
                    == row['organization_id'],
                    f'{table}: organization mismatch')
            require(member['membership_status'] == 'active' and
                    users[member['user_id']]['platform_status'] == 'active',
                    f'{table}: inactive participant')
            available = member['joined_at']
            if event['visibility'] == 'group_only':
                link = links.get((event['group_id'],
                                  member['organization_membership_id']))
                require(link is not None and
                        link['membership_status'] == 'active',
                        f'{table}: ineligible group participant')
                available = max(available, link['joined_at'])
            require(available <= event['start_at'],
                    f'{table}: event before join')
            if table == 'event_rsvp':
                require(available <= row['rsvp_at'] < event['start_at'],
                        'RSVP: invalid timeline')
            else:
                rsvp = rsvps.get((row['event_id'],
                                  row['organization_membership_id']))
                attended = row['attendance_status'] == 'attended'
                checkin = row['checked_in_at']
                require((attended and checkin is not None and
                         event['start_at'] <= checkin <= event['end_at']) or
                        (not attended and checkin is None),
                        'attendance: check-in')
                require(rsvp is None or rsvp['rsvp_status'] != 'cancelled',
                        'attendance: cancelled RSVP')
                if not attended:
                    require(rsvp is not None and
                            rsvp['rsvp_status'] == 'attending',
                            'absence: no confirmed reservation')
    require(len(data['organization']) == 5, 'Expected five organizations')
    counts = Counter(m['organization_id'] for m in members.values())
    expected = [config['population'] for config in ORGANIZATIONS]
    require([counts[i] for i in range(1, 6)] == expected,
            'Unexpected membership distribution')
