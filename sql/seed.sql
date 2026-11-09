-- CEPD: run each numbered LOAD statement individually against EMPTY tables.

USE cepd_db;
SET SESSION time_zone = '+00:00';

-- 1. Import platform_user; inspect the result and warnings before continuing.
LOAD DATA LOCAL INFILE 'generator/output/platform_user.tsv'
INTO TABLE platform_user
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n'
(user_id, username, email, platform_status, created_at);
SHOW WARNINGS;
SELECT COUNT(*) AS imported_platform_user_rows FROM platform_user;

-- 2. Import organization; inspect the result and warnings before continuing.
LOAD DATA LOCAL INFILE 'generator/output/organization.tsv'
INTO TABLE organization
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n'
(organization_id, name, description, status, created_at);
SHOW WARNINGS;
SELECT COUNT(*) AS imported_organization_rows FROM organization;

-- 3. Import organization_membership; inspect the result and warnings before continuing.
LOAD DATA LOCAL INFILE 'generator/output/organization_membership.tsv'
INTO TABLE organization_membership
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n'
(organization_membership_id, user_id, organization_id, display_name, membership_status, joined_at);
SHOW WARNINGS;
SELECT COUNT(*) AS imported_organization_membership_rows FROM organization_membership;

-- 4. Import organization_group; inspect the result and warnings before continuing.
LOAD DATA LOCAL INFILE 'generator/output/organization_group.tsv'
INTO TABLE organization_group
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n'
(group_id, organization_id, name, description, visibility, status);
SHOW WARNINGS;
SELECT COUNT(*) AS imported_organization_group_rows FROM organization_group;

-- 5. Import group_membership; inspect the result and warnings before continuing.
LOAD DATA LOCAL INFILE 'generator/output/group_membership.tsv'
INTO TABLE group_membership
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n'
(group_membership_id, organization_id, group_id, organization_membership_id, role, membership_status, joined_at);
SHOW WARNINGS;
SELECT COUNT(*) AS imported_group_membership_rows FROM group_membership;

-- 6. Import event; inspect the result and warnings before continuing.
LOAD DATA LOCAL INFILE 'generator/output/event.tsv'
INTO TABLE event
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n'
(event_id, organization_id, group_id, title, description, start_at, end_at, delivery_mode, capacity, visibility, status);
SHOW WARNINGS;
SELECT COUNT(*) AS imported_event_rows FROM event;

-- 7. Import event_rsvp; inspect the result and warnings before continuing.
LOAD DATA LOCAL INFILE 'generator/output/event_rsvp.tsv'
INTO TABLE event_rsvp
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n'
(rsvp_id, organization_id, event_id, organization_membership_id, rsvp_status, rsvp_at);
SHOW WARNINGS;
SELECT COUNT(*) AS imported_event_rsvp_rows FROM event_rsvp;

-- 8. Import event_attendance; inspect the result and warnings before continuing.
LOAD DATA LOCAL INFILE 'generator/output/event_attendance.tsv'
INTO TABLE event_attendance
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n'
(attendance_id, organization_id, event_id, organization_membership_id, attendance_status, checked_in_at);
SHOW WARNINGS;
SELECT COUNT(*) AS imported_event_attendance_rows FROM event_attendance;
