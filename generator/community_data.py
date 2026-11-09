"""Fictional community activities, identity pools and output contract."""

from datetime import datetime


START = datetime(2025, 5, 1)
END = datetime(2026, 11, 1)  # Exclusive; includes all of October 31.
DEFAULT_SEED = 20260501
COLUMNS = {
    'platform_user': ('user_id', 'username', 'email', 'platform_status',
                      'created_at'),
    'organization': ('organization_id', 'name', 'description', 'status',
                     'created_at'),
    'organization_membership': (
        'organization_membership_id', 'user_id', 'organization_id',
        'display_name', 'membership_status', 'joined_at'),
    'organization_group': ('group_id', 'organization_id', 'name',
                           'description', 'visibility', 'status'),
    'group_membership': (
        'group_membership_id', 'organization_id', 'group_id',
        'organization_membership_id', 'role', 'membership_status',
        'joined_at'),
    'event': ('event_id', 'organization_id', 'group_id', 'title',
              'description',
              'start_at', 'end_at', 'delivery_mode', 'capacity', 'visibility',
              'status'),
    'event_rsvp': ('rsvp_id', 'organization_id', 'event_id',
                   'organization_membership_id', 'rsvp_status', 'rsvp_at'),
    'event_attendance': ('attendance_id', 'organization_id', 'event_id',
                         'organization_membership_id', 'attendance_status',
                         'checked_in_at'),
}
# Names are mixed independently of organizations and engagement. Repeated full
# names are allowed; platform handles and test emails remain unique.
FIRST_NAMES = (
    'Amira Ben Carmen Daniel Elena Felix Grace Hugo Iris Jonah Kai Leila Maya '
    'Nico Owen Priya Quinn Rosa Samira Theo Uma Victor Wren Yasmin Zoe Adrian '
    'Bea Caleb Dalia Ellis Farah Gavin Hana Isaac Jade Kiran Lena Mateo Nadia '
    'Oliver Petra Rafael Sienna Tobias Vera Wesley Avery Casey Devon Emery '
    'Finley Jordan Morgan Parker Riley Rowan Sage Taylor Cameron Drew Robin '
    'Sasha Alex Jamie Noa Remy Abigail Adam Aisha Akira Alan Alessia Alice '
    'Alina Alonzo Ana Anika Annabel Arjun Arthur Asher Astrid Amina Audrey '
    'August Bao Beatrice Bianca Blake Brianna Bruno Callum Celia Charlie '
    'Chloe Clara Colin Dahlia Dante Darius David Delia Diana Dominic Eden '
    'Edgar Eduardo Elias Elliot Emilia Eric Esme Ethan Eva Evelyn Ezra '
    'Fatima Flora Frances Gabriel Gemma George Greta Hannah Harper Hassan '
    'Hazel Helena Henry Idris Imani Ines Ingrid Isabel Ivan Jacob James '
    'Jasper Jean Jesse Joel Joseph Joy Julia Julian Jun June Karim Keiko '
    'Kennedy Kenji Kiara Lara Layla Leon Liam Lila Lily Logan Lucia Luis '
    'Luka Lydia Maeve Malik Mara Marcus Mariam Marisol Mason Max Mei Micah '
    'Mila Miriam Naomi Nasir Nathan Nell Nina Noel Nora Omar Oscar Pablo '
    'Paola Patrick Paul Phoebe Ravi Renata Rhea Ricardo Rina River Ronan '
    'Ruby Ryan Sabrina Sadie Salma Samuel Sara Serena Shiloh Simon Sofia '
    'Soren Stella Sylvia Talia Tessa Thomas Tori Tristan Valeria Vanessa '
    'Viola Vivian Wallace Xander Yara Yusuf Zain Zoya'
).split()
LAST_NAMES = (
    'Adams Baker Bennett Brooks Campbell Carter Chen Clarke Cole Collins '
    'Cooper Cruz Davis Diaz Edwards Ellis Evans Flores Ford Foster Garcia '
    'Gomez Gray Green Griffin Hall Harris Hayes Hill Howard Hughes James '
    'Jensen Jones Kelly Kim King Lane Lee Lewis Lin Lopez Martin Mason '
    'Miller Mitchell Moore Morgan Morris Murphy Nelson Nguyen Ortiz Park '
    'Patel Perez Perry Price Quinn Ramirez Reed Reyes Rivera Ross Ruiz '
    'Scott Shaw Singh Smith Stone Sullivan Taylor Thomas Torres Tran Turner '
    'Walker Ward Watson White Williams Wilson Wood Wright Young Abbott Ahmed '
    'Allen Alvarez Andersen Armstrong Arnold Bailey Banks Barrett Barton '
    'Becker Bell Benson Bishop Blair Bowman Boyd Bradley Brennan Briggs '
    'Brown Bryant Burke Burns Burton Butler Caldwell Carlson Carr Carroll '
    'Castillo Chapman Chavez Choi Coleman Cook Costa Crawford Cunningham '
    'Daniels Dawson Delgado Dennis Douglas Dunn Elliott Erickson Estrada '
    'Ferguson Fernandez Fisher Fleming Flynn Fowler Fox Francis Franklin '
    'Freeman Gallagher Gardner Gilbert Gill Gordon Graham Grant Guerrero '
    'Gutierrez Hamilton Hansen Hardy Hart Hawkins Henderson Henry Herrera '
    'Hicks Hoffman Holland Holmes Hopkins Horton Hudson Hunter Ibrahim '
    'Jacobs Jefferson Jiang Johnston Jordan Kaur Keller Kennedy Khan Klein '
    'Knight Kumar Lambert Larson Lawrence Lawson Leach Leonard Li Long '
    'Lowe Lucas Lynch Mahmoud Manning Marshall Matthews Maxwell Medina '
    'Mendez Meyer Miles Mills Molina Monroe Montgomery Morales Munoz Nash '
    'Neal Newman Nichols Nolan Olsen Ortega Osborne Owens Palmer Pearson '
    'Pena Perkins Peters Pierce Porter Powell Pratt Preston Rahman Ramos '
    'Ray Rhodes Rice Richards Richardson Riley Robertson Robinson Rocha '
    'Rogers Romero Rose Russell Salazar Sanchez Sanders Santos Schmidt Shah '
    'Shelton Silva Simmons Simpson Spencer Steele Stephens Stevens Stewart '
    'Stokes Sutton Tan Tate Terry Thompson Todd Tucker Valdez Vargas '
    'Vasquez Vega Wagner Wallace Walters Warren Watkins Watts Weaver Webb '
    'Weber Wells West Wheeler Whitaker Wilkins Wong Wu Yang Yates Zhang'
).split() + [
    "O'Neill", "O'Brien", 'Al-Hassan', 'De la Cruz', 'van Dijk', (
        'van der Meer'
    ),
    'Reed-Walker', 'Garcia-Lopez', 'Bell-Ross', 'Da Silva', 'St. Clair',
]
HANDLE_WORDS = (
    'quiet bright copper silver amber mossy nimble sunny lunar wandering '
    'gentle hidden curious brisk calm wild little distant clever velvet '
    'misty lucky patient vivid golden coastal alpine mellow early swift'
).split()
HANDLE_NOUNS = (
    'cedar orbit willow otter fern comet maple raven river pebble fox '
    'sparrow compass meadow cloud lantern badger juniper brook heron '
    'harbor acorn trail finch grove kite sprout elm lark cove'
).split()

# Each activity is a (title, description) pair. Shared parameters stay small:
# frequency, public/group interest and public/group RSVP turnout.
# Each community has one special gathering from its second May onward.
ORGANIZATIONS = (
    {
        'name': 'Ethical Non-Monogamy Community', 'population': 6000,
        'description': (
            'Fictional community for education and social activities.'
        ),
        'interval': 7, 'interest': (95, 32), 'turnout': (.74, .85),
        'events': (
            ('Community Welcome Meetup',
             'Meet members and explore upcoming activities.'),
            ('Neighborhood Picnic and Conversation',
             'Bring a picnic and join small conversation tables.'),
            ('Community Cafe: Meet Your Neighbors',
             'Share introductions over refreshments.'),
            ('Member-Led Skill Swap',
             'Members demonstrate useful everyday skills.'),
            ('New Member Orientation',
             'Learn how groups work and meet volunteer hosts.'),
            ('Community Potluck',
             'Share a meal and help plan future gatherings.'),
            ('Creative Afternoon Exchange',
             'Try short craft activities led by members.'),
            ('Community Walk and Talk',
             'Take a relaxed neighborhood walk with fellow members.'),
        ),
        'special': ('Community Connections Showcase', (
            'Celebrate a year of activities with member-led demonstrations.'
        )),
        'groups': (
            ('Discussion Circle', (
                ('Conversation Cafe: Making Time for Community',
                 'Discuss ways to fit community activities into busy '
                 'schedules.'),
                ('Discussion Circle: Listening Practice',
                 'Practice listening through short paired conversations.'),
                ('Discussion Circle: Shared Expectations',
                 'Discuss expectations for welcoming group activities.'))),
            ('Book Club', (
                ('Book Club: Reader Picks and Tea',
                 'Compare member-selected readings over tea.'),
                ('Book Club: Essay Exchange',
                 'Share short essays and discuss their themes.'),
                ('Book Club: Reading List Workshop',
                 'Build the next reading list together.'))),
            ('Social Activities', (
                ('Social Club: Picnic and Lawn Games',
                 'Share picnic food and try casual lawn games.'),
                ('Social Club: Board Games and Potluck',
                 'Learn a board game over shared snacks.'),
                ('Social Club: Local Arts Walk',
                 'Explore a local arts route together.'))),
            ('Peer Learning', (
                ('Peer Learning: Welcoming New Members',
                 'Practice introductions and welcoming routines.'),
                ('Peer Learning: Planning an Activity',
                 'Work through a small activity plan in teams.'),
                ('Peer Learning: Facilitation Practice',
                 'Try short meeting facilitation exercises.'))),
            ('Volunteer Planning', (
                ('Volunteer Huddle: Welcome Table',
                 'Prepare signs and supplies for the welcome table.'),
                ('Volunteer Huddle: Calendar Review',
                 'Review dates, venues and volunteer availability.'),
                ('Volunteer Huddle: Activity Debrief',
                 'Review recent gatherings and select practical '
                 'improvements.'))),
        ),
    },
    {
        'name': 'Gaming Community', 'population': 9000,
        'description': (
            'Fictional gaming community with varied formats and schedules.'
        ),
        'interval': 5, 'interest': (180, 30), 'turnout': (.43, .77),
        'events': (
            ('Open Game Social: Bring a Favorite',
             'Teach a favorite game at an open community table.'),
            ('New Players Welcome Table',
             'Learn beginner-friendly games with volunteer guides.'),
            ('Community Co-op Challenge',
             'Form small teams for a cooperative game challenge.'),
            ('Board Game Exchange',
             'Swap games and try short demonstrations.'),
            ('Casual Tournament Meetup',
             'Play short friendly rounds with flexible pairings.'),
            ('Puzzle and Party Game Social',
             'Rotate through quick puzzles and party games.'),
            ('Learn-to-Play Workshop',
             'Practice the rules of a member-selected game.'),
            ('Community Game Demo Fair',
             'Try short demos and compare favorite game mechanics.'),
        ),
        'special': ('Community Gaming Showcase', (
            'Play member-created games and celebrate community projects.'
        )),
        'groups': (
            ('Tabletop Games', (
                ('Tabletop Club: Teach a New Game',
                 'Practice teaching rules at small tables.'),
                ('Tabletop Club: Cooperative Puzzle Session',
                 'Work together through a tabletop puzzle.'),
                ('Tabletop Club: Two-Player Favorites',
                 'Compare short two-player games.'))),
            ('Cooperative Games', (
                ('Co-op Crew: New Campaign Kickoff',
                 'Choose roles and begin a cooperative campaign.'),
                ('Co-op Crew: Save-Game Meetup',
                 'Continue an existing campaign from its last checkpoint.'),
                ('Co-op Crew: Team Challenge',
                 'Try a short challenge with rotating team roles.'))),
            ('Strategy Games', (
                ('Strategy Table: Short-Game Ladder',
                 'Play short strategy matches with rotating opponents.'),
                ('Strategy Table: Replay and Learn',
                 'Review a match and compare alternative moves.'),
                ('Strategy Table: Opening Moves Clinic',
                 'Practice opening moves in a selected strategy game.'))),
            ('Game Design', (
                ('Design Lab: Paper Prototype Playtest',
                 'Playtest paper prototypes and record feedback.'),
                ('Design Lab: Feedback Roundtable',
                 'Discuss usability and balance in member prototypes.'),
                ('Design Lab: Rulebook Clinic',
                 'Edit draft rulebooks after a guided playthrough.'))),
            ('Tournament Planning', (
                ('Tournament Crew: Bracket Rehearsal',
                 'Test brackets using sample match results.'),
                ('Tournament Crew: Rules and Schedule Clinic',
                 'Review event rules and estimate round timings.'),
                ('Tournament Crew: Host Practice',
                 'Rehearse check-in and match announcements.'))),
        ),
    },
    {
        'name': 'Rollerblading Community', 'population': 4000,
        'description': (
            'Fictional community for skating practice and shared outings.'
        ),
        'interval': 9, 'interest': (90, 24), 'turnout': (.78, .82),
        'events': (
            ('River Loop Community Skate',
             'Follow a shared route with several pace groups.'),
            ('Park Paths: Easy-Pace Roll',
             'Practice steady pacing on a short park loop.'),
            ('Neighborhood Wheels Meetup',
             'Meet fellow skaters for a relaxed community outing.'),
            ('Trailside Social',
             'Combine a short trail skate with a social break.'),
            ('New Skaters Welcome Roll',
             'Join a short route with beginner-friendly pacing.'),
            ('Community Route Sampler',
             'Compare two short routes and share observations.'),
            ('Greenway Group Outing',
             'Explore a greenway route with volunteer leads.'),
            ('Seasonal Trail Meetup',
             'Review current trail conditions before a group roll.'),
        ),
        'special': ('Community Wheels Celebration', (
            'Celebrate a year of skating with a shared route and picnic.'
        )),
        'groups': (
            ('Trail Skating', (
                ('Trail Crew: Route Notes and Pace Planning',
                 'Compare route notes and plan pace groups.'),
                ('Trail Crew: Short Loop Practice',
                 'Practice consistent pacing on a short loop.'),
                ('Trail Crew: Group Signals Practice',
                 'Rehearse simple group signals on a familiar route.'))),
            ('Beginner Practice', (
                ('Beginner Circle: Stops and Turns',
                 'Practice basic stops and turns at a comfortable pace.'),
                ('Beginner Circle: Balance Practice',
                 'Work through low-speed balance exercises.'),
                ('Beginner Circle: First Short Route',
                 'Try a short route with experienced volunteers.'))),
            ('Indoor Skills', (
                ('Indoor Skills: Footwork Fundamentals',
                 'Practice basic footwork in an indoor space.'),
                ('Indoor Skills: Low-Speed Agility',
                 'Work through low-speed agility stations indoors.'),
                ('Indoor Skills: Cornering Practice',
                 'Practice controlled turns on a marked indoor circuit.'))),
            ('Route Planning', (
                ('Route Team: Map the Next Skate',
                 'Compare maps and select the next community route.'),
                ('Route Team: Trail Conditions Roundtable',
                 'Review reported surfaces and route access.'),
                ('Route Team: Rest Stop Planning',
                 'Identify rest points and alternative route segments.'))),
            ('Volunteer Planning', (
                ('Skate Volunteers: Welcome Desk Briefing',
                 'Prepare route notes and check-in materials.'),
                ('Skate Volunteers: Equipment Swap Planning',
                 'Organize tables and labels for an equipment swap.'),
                ('Skate Volunteers: Outing Debrief',
                 'Review the last outing and update volunteer assignments.'))),
        ),
    },
    {
        'name': 'Pagan / Nontraditional Religion Community', (
            'population'
        ): 6500,
        'description': (
            'Fictional community for learning, seasonal gatherings and '
            'service.'
        ),
        'interval': 10, 'interest': (100, 30), 'turnout': (.80, .83),
        'events': (
            ('Community Gathering: Seasonal Potluck',
             'Share seasonal dishes and conversation at a community table.'),
            ('Seasonal Arts and Story Exchange',
             'Share art and stories connected with the changing season.'),
            ('Community Garden Gathering',
             'Exchange gardening notes and plan shared garden activities.'),
            ('Seasonal Community Cafe',
             'Meet members over refreshments and seasonal discussion '
             'prompts.'),
            ('New Members Welcome Gathering',
             'Meet hosts and learn about study, craft and service groups.'),
            ('Community Craft Exchange',
             'Share handmade items and demonstrate simple techniques.'),
            ('Seasonal Reading Meetup',
             'Discuss member-selected readings about seasonal traditions.'),
            ('Volunteer Opportunities Open House',
             'Learn about local service projects and volunteer tasks.'),
        ),
        'special': ('Community Arts and Learning Showcase', (
            'Share a year of craft projects, reading discoveries and service '
            'work.'
        )),
        'groups': (
            ('Seasonal Gatherings', (
                ('Seasonal Circle: Shared Table Planning',
                 'Plan food, seating and activities for the next gathering.'),
                ('Seasonal Circle: Stories and Tea',
                 'Share member-selected seasonal stories over tea.'),
                ('Seasonal Circle: Gathering Debrief',
                 'Discuss recent gatherings and collect ideas for the next '
                 'season.'))),
            ('Study Circle', (
                ('Study Circle: Member-Selected Readings',
                 'Discuss readings chosen by circle members.'),
                ('Study Circle: Questions and Conversation',
                 'Explore questions raised by the current readings.'),
                ('Study Circle: Source Comparison',
                 'Compare how selected sources describe a common topic.'))),
            ('Arts and Crafts', (
                ('Craft Circle: Nature Journaling',
                 'Make journal pages using observation and sketching.'),
                ('Craft Circle: Shared Materials Workshop',
                 'Try craft techniques using shared materials.'),
                ('Craft Circle: Project Exchange',
                 'Show unfinished projects and exchange practical '
                 'suggestions.'))),
            ('Community Service', (
                ('Service Circle: Neighborhood Care Planning',
                 'Choose tasks for a neighborhood service activity.'),
                ('Service Circle: Community Garden Check-In',
                 'Review garden tasks and organize shared supplies.'),
                ('Service Circle: Supply Sorting Session',
                 'Sort donated supplies for an agreed community project.'))),
            ('Volunteer Planning', (
                ('Gathering Volunteers: Welcome Table',
                 'Prepare welcome materials and host assignments.'),
                ('Gathering Volunteers: Venue and Supplies',
                 'Review venue arrangements and supply lists.'),
                ('Gathering Volunteers: Calendar Clinic',
                 'Coordinate the next study, craft and service dates.'))),
        ),
    },
    {
        'name': 'Front Range Open Source & Technology Collective',
        'population': 4500,
        'description': (
            'Fictional collective for technical learning and community '
            'projects.'
        ),
        'interval': 7, 'interest': (110, 24), 'turnout': (.84, .79),
        'events': (
            ('Intro Workshop: Your First Git Commit',
             'Create a small repository and practice committing a change.'),
            ('Intro Workshop: Python for Everyday Tasks',
             'Write a short Python script for a simple everyday task.'),
            ('Intro Workshop: A Friendly Tour of Linux',
             'Explore files, commands and basic Linux tools.'),
            ('Intro Workshop: Explore a Public Dataset',
             'Practice reading and summarizing a provided sample dataset.'),
            ('Intro Workshop: AI Evaluation Basics',
             'Compare model predictions with a small labeled example.'),
            ('Intro Workshop: Build a Home Lab Plan',
             'Sketch a small home lab and discuss equipment choices.'),
            ('Intro Workshop: Accessible Documents',
             'Practice clear formatting and accessibility checks.'),
            ('Intro Workshop: Your First Issue Report',
             'Write a reproducible issue report for a sample project.'),
        ),
        'special': ('Intro Technology Taster Fair', (
            'Try short beginner activities led by each technical group.'
        )),
        'groups': (
            ('Open-Source Development', (
                ('Project Lab: Review a First Pull Request',
                 'Review a small contribution and practice useful feedback.'),
                ('Project Lab: Issue Triage and Release Notes',
                 'Sort project issues and draft concise release notes.'),
                ('Project Lab: Maintainer Pairing',
                 'Pair on a small maintenance task in a sample repository.'))),
            ('AI & Data Science', (
                ('Data Lab: Evaluate a Small Classifier',
                 'Compare classifier errors using a labeled sample.'),
                ('Data Lab: Reproduce a Notebook Result',
                 'Rerun a notebook and compare its documented outputs.'),
                ('Data Lab: Data Quality Clinic',
                 'Inspect missing values and inconsistent labels in sample '
                 'data.'))),
            ('Computer Hardware & Homelabs', (
                ('Homelab Bench: Network Diagnostics',
                 'Trace connections and interpret basic network diagnostics.'),
                ('Homelab Bench: Storage and Backup Practice',
                 'Practice a backup and restore using sample files.'),
                ('Homelab Bench: Service Monitoring',
                 'Compare logs and simple checks for a local lab service.'))),
            ('Digital Literacy & Mentorship', (
                ('Mentor Studio: Accessible Tutorials',
                 'Test a tutorial for clear steps and accessible formatting.'),
                ('Mentor Studio: Refine a Learning Guide',
                 'Revise a learning guide after peer feedback.'),
                ('Mentor Studio: Practice a Help Session',
                 'Rehearse explaining a small technical task to a new '
                 'learner.'))),
            ('Community Technology Projects', (
                ('Community Build: Library Tool Sprint',
                 'Work on small tasks for a fictional library tool.'),
                ('Community Build: Demo and Feedback',
                 'Demonstrate recent project changes and collect feedback.'),
                ('Community Build: Project Planning Table',
                 'Choose a small project milestone and divide the tasks.'))),
        ),
    },
)
