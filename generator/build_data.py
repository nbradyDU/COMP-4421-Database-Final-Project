"""Build fictional populations and coherent community activity history."""

from datetime import timedelta
import random

from community_data import (COLUMNS, DEFAULT_SEED, END, FIRST_NAMES,
                            HANDLE_NOUNS, HANDLE_WORDS, LAST_NAMES,
                            ORGANIZATIONS, START)


def add_row(data, table, **values):
    """Append a record with an explicit, sequential table-local identifier."""
    row = {COLUMNS[table][0]: len(data[table]) + 1, **values}
    data[table].append(row)
    return row


def make_username(first, last, used, rng):
    """Choose a natural handle with seeded suffixes for collisions."""
    first = first.lower()
    last = last.lower().replace(' ', '').replace("'", '').replace('.', '')
    creative = rng.choice(HANDLE_WORDS) + rng.choice(('', '.', '_'))
    creative += rng.choice(HANDLE_NOUNS)
    base = rng.choice((f'{first}.{last}', f'{first[0]}{last}',
                       f'{first}_{last[0]}', f'{last}.{first}',
                       f'{first}-{last}',
                       f'{first}{last[0]}{rng.randrange(10, 100)}',
                       creative, creative))[:45]
    username = base
    while username in used:
        username = f'{base}{rng.randrange(10, 10000)}'
    used.add(username)
    return username


def assign_group_roles(data):
    """Give each group its earliest eligible owner and up to two admins."""
    users = {u['user_id']: u for u in data['platform_user']}
    members = {m['organization_membership_id']: m
               for m in data['organization_membership']}
    for group in data['organization_group']:
        eligible = []
        for link in data['group_membership']:
            member = members[link['organization_membership_id']]
            if (link['group_id'] == group['group_id']
                    and link['membership_status'] == 'active'
                    and member['membership_status'] == 'active'
                    and users[member['user_id']]['platform_status']
                    == 'active'):
                eligible.append(link)
        eligible.sort(key=lambda link: (link['joined_at'],
                                       link['group_membership_id']))
        for index, link in enumerate(eligible[:3]):
            link['role'] = 'owner' if index == 0 else 'admin'


def build_population(data, config, org_id, rng,
                     display_names, usernames):
    """Create groups and memberships, allowing shared platform identities."""
    population = config['population']
    groups = []
    for index, (group_name, _) in enumerate(config['groups']):
        group = add_row(
            data, 'organization_group', organization_id=org_id,
            name=group_name, description=f'Fictional {group_name} group.',
            visibility='private' if index >= 3 else 'public',
            status='active')
        groups.append(group)
    # Reuse 8% of identities from earlier organizations.
    previous_users = list(data['platform_user'])
    shared = (rng.sample(previous_users, int(population * .08))
              if org_id > 1 else [])
    members = []
    group_links = {}
    engagement = {}
    for index in range(population):
        # Some joins favor the early history; most favor later recruitment.
        # Both draws cover the whole window, avoiding a founding-date spike.
        last_day = (END - START).days - 1
        peak_day = 0 if rng.random() < .22 else last_day
        days = int(rng.triangular(0, last_day, peak_day))
        joined = START + timedelta(days=days, hours=rng.randrange(12))
        if index < len(shared):
            user = shared[index]
            joined = max(joined, user['created_at'])
        else:
            user_id = len(data['platform_user']) + 1
            first = rng.choice(FIRST_NAMES)
            last = rng.choice(LAST_NAMES)
            display_name = f'{first} {last}'
            if rng.random() < .15:
                middle = rng.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                display_name = f'{first} {middle}. {last}'
            display_names[user_id] = display_name
            username = make_username(first, last, usernames, rng)
            user = add_row(
                data, 'platform_user', username=username,
                email=f'{username}@example.test',
                platform_status=rng.choices(
                    ('active', 'inactive', 'suspended'), (97, 2, 1))[0],
                created_at=joined)
        member = add_row(
            data, 'organization_membership', user_id=user['user_id'],
            organization_id=org_id,
            display_name=display_names[user['user_id']],
            membership_status=rng.choices(
                ('active', 'inactive', 'suspended'), (94, 5, 1))[0],
            joined_at=joined)
        members.append(member)
        member_id = member['organization_membership_id']
        engagement[member_id] = rng.choices(
            (0, .3, 1, 3), (42, 30, 22, 6))[0]
        group_count = rng.choices((0, 1, 2, 3), (15, 45, 30, 10))[0]
        for group in rng.sample(groups, group_count):
            group_joined = joined + timedelta(days=rng.randrange(22))
            if group_joined >= END:
                continue
            link = add_row(
                data, 'group_membership', organization_id=org_id,
                group_id=group['group_id'],
                organization_membership_id=member_id,
                role='member',
                membership_status=rng.choices(
                    ('active', 'inactive', 'suspended'), (96, 3, 1))[0],
                joined_at=group_joined)
            group_links[group['group_id'], member_id] = link
    return groups, members, group_links, engagement


def add_participation(data, event, chosen, target, turnout, reconciled, rng):
    """Record RSVP intent, confirmed outcomes and walk-ins separately."""
    rsvp_count = min(target, len(chosen))
    for position, (_, mid, available) in enumerate(chosen):
        walk_in = position >= rsvp_count
        if walk_in:
            outcome = 'attended'
        else:
            rsvp_status = rng.choices(
                ('attending', 'maybe', 'cancelled'), (72, 18, 10))[0]
            earliest = max(available, event['start_at'] - timedelta(days=14))
            latest = event['start_at'] - timedelta(minutes=30)
            rsvp_at = earliest + timedelta(seconds=int(
                rng.random() * (latest - earliest).total_seconds()))
            add_row(data, 'event_rsvp',
                    organization_id=event['organization_id'],
                    event_id=event['event_id'],
                    organization_membership_id=mid,
                    rsvp_status=rsvp_status, rsvp_at=rsvp_at)
            chance = turnout if rsvp_status == 'attending' else .24
            if rsvp_status == 'cancelled':
                continue
            if rng.random() < chance:
                outcome = 'attended'
            elif rsvp_status == 'attending' and reconciled:
                # Only reconciled rosters establish confirmed absence.
                outcome = 'absent'
            else:
                continue
        add_row(
            data, 'event_attendance', organization_id=event['organization_id'],
            event_id=event['event_id'], organization_membership_id=mid,
            attendance_status=outcome,
            checked_in_at=(
                event['start_at'] + timedelta(minutes=rng.randrange(31))
                if outcome == 'attended' else None))


def build_events(data, config, org_id, groups, members, group_links,
                 engagement, rng):
    """Create a community calendar and select only eligible participants."""
    users = {u['user_id']: u for u in data['platform_user']}
    eligible = [m for m in members if m['membership_status'] == 'active'
                and users[m['user_id']]['platform_status'] == 'active']
    event_start = START + timedelta(
        days=7 + rng.randrange(7), hours=18)
    activities = {group['group_id']: choices
                  for group, (_, choices) in zip(groups, config['groups'])}
    previous_title = None
    special_used = False
    while event_start + timedelta(hours=3) < END:
        group_only = rng.random() < .45
        category = 1 if group_only else 0
        interest = config['interest'][category]
        turnout = config['turnout'][category]
        if group_only:
            host = rng.choice(groups)
        else:
            host = rng.choice(groups) if rng.random() < .4 else None
        choices = (activities[host['group_id']] if group_only
                   else config['events'])
        title, description = rng.choice(
            [activity for activity in choices
             if activity[0] != previous_title])
        if (not group_only and not special_used
                and event_start >= START.replace(year=2026)):
            title, description = config['special']
            special_used = True
        previous_title = title
        mode = 'offline'
        if org_id == 3:
            summer = event_start.month in (5, 6, 7, 8, 9)
            if group_only:
                interest *= .85 if summer else 1.2
            else:
                interest *= 1.6 if summer else .35
        if org_id == 4 and not group_only:
            interest *= 2.1 if event_start.month in (2, 5, 8, 10) else .7
        can_be_online = org_id in (2, 5) and not any(
            word in title for word in ('Exchange', 'Fair', 'Welcome Table'))
        if can_be_online and rng.random() < .35:
            mode = 'online'
        target = max(2, int(interest * rng.uniform(.7, 1.25)))
        turnout = min(.95, turnout * rng.uniform(.85, 1.1))
        reconciled = rng.random() < .35
        duration = rng.choice((90, 120, 150, 180))
        event = add_row(
            data, 'event', organization_id=org_id,
            group_id=host['group_id'] if host else None,
            title=title, description=description, start_at=event_start,
            end_at=event_start + timedelta(minutes=duration),
            delivery_mode=mode,
            capacity=None if rng.random() < .17 else max(
                10, int(target * rng.uniform(.9, 1.5))),
            visibility='group_only' if group_only else 'organization',
            status='archived')
        candidates = []
        for member in eligible:
            mid = member['organization_membership_id']
            available = member['joined_at']
            if group_only:
                link = group_links.get((host['group_id'], mid))
                if link is None or link['membership_status'] != 'active':
                    continue
                available = max(available, link['joined_at'])
            if available > event_start - timedelta(hours=1):
                continue
            weight = engagement[mid]
            if org_id == 5 and not group_only:
                age = (event_start - member['joined_at']).days
                weight *= 3 if age <= 90 else .08
            if weight > 0:
                # Higher rates give smaller waits, favoring regulars.
                # Each member appears once, so no duplicates are drawn.
                candidates.append(
                    (rng.expovariate(weight), mid, available))
        candidates.sort()
        walkin_count = rng.randint(0, max(1, target // 8))
        chosen = candidates[:target + walkin_count]
        add_participation(data, event, chosen, target, turnout,
                          reconciled, rng)
        event_start += timedelta(
            days=config['interval'] + rng.choice((-2, -1, 0, 0, 1, 2)))
        hours = (10, 14, 18) if event_start.weekday() >= 5 else (18, 19)
        event_start = event_start.replace(hour=rng.choice(hours))


def generate(seed=DEFAULT_SEED):
    """Build the complete dataset using a local RNG and fixed history."""
    rng = random.Random(seed)
    data = {table: [] for table in COLUMNS}
    display_names = {}
    usernames = set()
    for org_id, config in enumerate(ORGANIZATIONS, 1):
        add_row(data, 'organization', name=config['name'],
                description=config['description'], status='active',
                created_at=START)
        groups, members, links, engagement = build_population(
            data, config, org_id, rng, display_names, usernames)
        build_events(data, config, org_id, groups, members, links,
                     engagement, rng)
    assign_group_roles(data)
    return data
