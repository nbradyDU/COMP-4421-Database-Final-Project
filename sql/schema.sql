/*
  Community Event and Participation Database (CEPD) schema.

*/

CREATE DATABASE IF NOT EXISTS cepd_db;

USE cepd_db;

-- 1. People with a single identity across the platform.
CREATE TABLE platform_user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(254) NOT NULL UNIQUE,
    platform_status ENUM('active', 'inactive', 'suspended')
        NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
); 

-- 2. Communities that contain members, groups, and events.
CREATE TABLE organization (
    organization_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT NULL,
    status ENUM('active', 'inactive', 'archived')
        NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
); 

-- 3. Resolves the many-to-many user/organization relationship.
CREATE TABLE organization_membership (
    organization_membership_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    organization_id INT NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    membership_status ENUM('active', 'inactive', 'suspended')
        NOT NULL DEFAULT 'active',
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uq_om_user_org (user_id, organization_id),
    -- Supporting key for organization-matching composite foreign keys.
    UNIQUE KEY uq_om_id_org (organization_membership_id, organization_id),

    CONSTRAINT fk_om_user FOREIGN KEY (user_id)
        REFERENCES platform_user(user_id),
    CONSTRAINT fk_om_org FOREIGN KEY (organization_id)
        REFERENCES organization(organization_id)
); 

-- 4. Group belongs directly to one organization.
CREATE TABLE organization_group (
    group_id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NULL,
    visibility ENUM('public', 'private') NOT NULL DEFAULT 'public',
    status ENUM('active', 'inactive', 'archived')
        NOT NULL DEFAULT 'active',

    UNIQUE KEY uq_group_org_name (organization_id, name),
    UNIQUE KEY uq_group_id_org (group_id, organization_id),

    CONSTRAINT fk_group_org FOREIGN KEY (organization_id)
        REFERENCES organization(organization_id)
); 

-- 5. Resolves the many-to-many org-membership/group relationship.
CREATE TABLE group_membership (
    group_membership_id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    group_id INT NOT NULL,
    organization_membership_id INT NOT NULL,
    role ENUM('member', 'admin', 'owner') NOT NULL DEFAULT 'member',
    membership_status ENUM('active', 'inactive', 'suspended')
        NOT NULL DEFAULT 'active',
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uq_gm_group_member (group_id, organization_membership_id),

    CONSTRAINT fk_gm_group_org FOREIGN KEY (group_id, organization_id)
        REFERENCES organization_group(group_id, organization_id),
    CONSTRAINT fk_gm_member_org FOREIGN KEY
        (organization_membership_id, organization_id)
        REFERENCES organization_membership
        (organization_membership_id, organization_id)
);

-- 6. Events can be hosted directly by an org or created by one of its groups.
CREATE TABLE event (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    group_id INT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    start_at DATETIME NOT NULL,
    end_at DATETIME NOT NULL,
    delivery_mode ENUM('online', 'offline') NOT NULL DEFAULT 'online',
    capacity INT NULL,
    visibility ENUM('organization', 'group_only')
        NOT NULL DEFAULT 'organization',
    status ENUM('active', 'inactive', 'archived')
        NOT NULL DEFAULT 'active',

    UNIQUE KEY uq_event_id_org (event_id, organization_id),

    CONSTRAINT fk_event_org FOREIGN KEY (organization_id)
        REFERENCES organization(organization_id),
    CONSTRAINT fk_event_group_org FOREIGN KEY (group_id, organization_id)
        REFERENCES organization_group(group_id, organization_id),

    CONSTRAINT ck_event_times CHECK (end_at > start_at),
    CONSTRAINT ck_event_capacity CHECK (capacity IS NULL OR capacity > 0),
    CONSTRAINT ck_event_group_only CHECK (
        visibility <> 'group_only' OR group_id IS NOT NULL
    )
);

-- 7. Intention to attend. One RSVP per org member per event.
CREATE TABLE event_rsvp (
    rsvp_id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    event_id INT NOT NULL,
    organization_membership_id INT NOT NULL,
    rsvp_status ENUM('attending', 'maybe', 'cancelled')
        NOT NULL DEFAULT 'attending',
    rsvp_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uq_rsvp_event_member (event_id, organization_membership_id),

    CONSTRAINT fk_rsvp_event_org FOREIGN KEY (event_id, organization_id)
        REFERENCES event(event_id, organization_id),
    CONSTRAINT fk_rsvp_member_org FOREIGN KEY
        (organization_membership_id, organization_id)
        REFERENCES organization_membership
        (organization_membership_id, organization_id)
);

-- 8. Confirmed attendance outcomes. An RSVP is NOT required for walk-ins.
CREATE TABLE event_attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    organization_id INT NOT NULL,
    event_id INT NOT NULL,
    organization_membership_id INT NOT NULL,
    attendance_status ENUM('attended', 'absent') NOT NULL,
    checked_in_at TIMESTAMP NULL DEFAULT NULL,

    UNIQUE KEY uq_att_event_member (event_id, organization_membership_id),

    CONSTRAINT fk_att_event_org FOREIGN KEY (event_id, organization_id)
        REFERENCES event(event_id, organization_id),
    CONSTRAINT fk_att_member_org FOREIGN KEY
        (organization_membership_id, organization_id)
        REFERENCES organization_membership
        (organization_membership_id, organization_id),

    -- No row means unknown; explicit 'absent' means confirmed absence.
    CONSTRAINT ck_att_checkin CHECK (
        (attendance_status = 'attended' AND checked_in_at IS NOT NULL)
        OR
        (attendance_status = 'absent' AND checked_in_at IS NULL)
    )
); 

SHOW TABLES;