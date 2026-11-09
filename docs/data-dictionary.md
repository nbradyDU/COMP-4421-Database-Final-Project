# Data Dictionary

**PK** = Primary key  
**FK** = Foreign key  
**UQ** = Unique key  

`NULL` means the field is optional. Other fields are required unless a default value is supplied.

## `platform_user` — One platform identity per person

| Column | Type | NULL? | Description |
|---|---|---|---|
| `user_id` | INT | No | PK; automatically assigned user ID |
| `username` | VARCHAR(50) | No | UQ; platform username |
| `email` | VARCHAR(254) | No | UQ; email address |
| `platform_status` | ENUM | No | `active`, `inactive`, `suspended`; default `active` |
| `created_at` | TIMESTAMP | No | Creation time; defaults to current timestamp |

## `organization` — A community or organization

| Column | Type | NULL? | Description |
|---|---|---|---|
| `organization_id` | INT | No | PK; automatically assigned organization ID |
| `name` | VARCHAR(255) | No | UQ; organization name |
| `description` | TEXT | Yes | Optional description |
| `status` | ENUM | No | `active`, `inactive`, `archived`; default `active` |
| `created_at` | TIMESTAMP | No | Creation time; defaults to current timestamp |

## `organization_membership` — A user belongs to an organization

| Column | Type | NULL? | Description |
|---|---|---|---|
| `organization_membership_id` | INT | No | PK; membership ID |
| `user_id` | INT | No | FK → `platform_user.user_id` |
| `organization_id` | INT | No | FK → `organization.organization_id` |
| `display_name` | VARCHAR(100) | No | Name shown within this organization |
| `membership_status` | ENUM | No | `active`, `inactive`, `suspended`; default `active` |
| `joined_at` | TIMESTAMP | No | Join timestamp; defaults to current timestamp |

**Keys:**
- UQ(`user_id`, `organization_id`)
- Supporting UQ(`organization_membership_id`, `organization_id`)

## `organization_group` — A group within an organization

| Column | Type | NULL? | Description |
|---|---|---|---|
| `group_id` | INT | No | PK; group ID |
| `organization_id` | INT | No | FK → `organization.organization_id` |
| `name` | VARCHAR(100) | No | Group name; unique within its organization |
| `description` | TEXT | Yes | Optional description |
| `visibility` | ENUM | No | `public`, `private`; default `public` |
| `status` | ENUM | No | `active`, `inactive`, `archived`; default `active` |

**Keys:**
- UQ(`organization_id`, `name`)
- Supporting UQ(`group_id`, `organization_id`)

## `group_membership` — An organization member joins a group

| Column | Type | NULL? | Description |
|---|---|---|---|
| `group_membership_id` | INT | No | PK; group membership ID |
| `organization_id` | INT | No | Organization ID used for composite FK validation |
| `group_id` | INT | No | FK pair with `organization_id` → `organization_group` |
| `organization_membership_id` | INT | No | FK pair with `organization_id` → `organization_membership` |
| `role` | ENUM | No | `member`, `admin`, `owner`; default `member` |
| `membership_status` | ENUM | No | `active`, `inactive`, `suspended`; default `active` |
| `joined_at` | TIMESTAMP | No | Join timestamp; defaults to current timestamp |

**Keys:**
- UQ(`group_id`, `organization_membership_id`)
- Composite FKs ensure groups and members belong to the same organization.

## `event` — An organization or group-created event

| Column | Type | NULL? | Description |
|---|---|---|---|
| `event_id` | INT | No | PK; event ID |
| `organization_id` | INT | No | FK → `organization.organization_id` |
| `group_id` | INT | Yes | Optional FK pair with `organization_id` → `organization_group` |
| `title` | VARCHAR(255) | No | Event title |
| `description` | TEXT | Yes | Optional description |
| `start_at` | DATETIME | No | Scheduled start |
| `end_at` | DATETIME | No | Scheduled end; must be after start |
| `delivery_mode` | ENUM | No | `online`, `offline`; default `online` |
| `capacity` | INT | Yes | Optional positive capacity; informational only |
| `visibility` | ENUM | No | `organization`, `group_only`; default `organization` |
| `status` | ENUM | No | `active`, `inactive`, `archived`; default `active` |

**Keys:**
- Supporting UQ(`event_id`, `organization_id`)
- `group_only` events require a `group_id`.
- Organization-wide events created by groups appear under the organization name.

## `event_rsvp` — A member's response to an event

| Column | Type | NULL? | Description |
|---|---|---|---|
| `rsvp_id` | INT | No | PK; RSVP ID |
| `organization_id` | INT | No | Organization ID used for composite FK validation |
| `event_id` | INT | No | FK pair with `organization_id` → `event` |
| `organization_membership_id` | INT | No | FK pair with `organization_id` → `organization_membership` |
| `rsvp_status` | ENUM | No | `attending`, `maybe`, `cancelled`; default `attending` |
| `rsvp_at` | TIMESTAMP | No | RSVP timestamp; defaults to current timestamp |

**Keys:**
- UQ(`event_id`, `organization_membership_id`)
- Composite FKs ensure the event and membership belong to the same organization.

An RSVP records someone's intention to attend, not whether they actually attended.

## `event_attendance` — Recorded attendance, including walk-ins

| Column | Type | NULL? | Description |
|---|---|---|---|
| `attendance_id` | INT | No | PK; attendance ID |
| `organization_id` | INT | No | Organization ID used for composite FK validation |
| `event_id` | INT | No | FK pair with `organization_id` → `event` |
| `organization_membership_id` | INT | No | FK pair with `organization_id` → `organization_membership` |
| `attendance_status` | ENUM | No | `attended` or `absent`; no default |
| `checked_in_at` | TIMESTAMP | Yes | Required when `attended`; NULL when `absent` |

**Keys:**
- UQ(`event_id`, `organization_membership_id`)
- Composite FKs ensure the event and membership belong to the same organization.
- No FK to `event_rsvp`, allowing walk-in attendance.

A missing attendance record means attendance is unknown, not that the member was absent.

---

## Data Rules

The column tables identify primary keys, foreign keys, required fields, unique values, and defaults. The following rules describe how records must relate to one another.

| Area | Rules |
|---|---|
| Memberships | A user can have one membership per organization and one membership per group. |
| Organizations and groups | Composite foreign keys keep groups and their members associated with the correct organization. Group names must be unique within their organization. |
| Events | End times must be after start times. Capacity must be positive when provided. Group-only events require a group belonging to the same organization. |
| RSVPs | Each member can have one RSVP per event. The event and membership must belong to the same organization. |
| Attendance | Each member can have one attendance record per event. An `attended` record requires a check-in timestamp, while an `absent` record must not have one. Attendance does not require an RSVP. |

## Limitations

The current database does not enforce

- Event capacity limits.
- Active membership requirements when registering or attending.
- Authorization to participate in group-only events.
- Access restrictions based on visibility settings.

These require additional database or application-level controls.
