-- Query 8: Do group-only RSVPs and check-ins have matching group memberships?

SELECT
    (
        SELECT COUNT(*)
        FROM event_rsvp r
        JOIN event e
            ON r.event_id = e.event_id
            AND r.organization_id = e.organization_id
        WHERE e.visibility = 'group_only'
          AND NOT EXISTS (
              SELECT 1
              FROM group_membership gm
              WHERE gm.group_id = e.group_id
                AND gm.organization_id = e.organization_id
                AND gm.organization_membership_id =
                    r.organization_membership_id
          )
    ) AS invalid_group_rsvps,
    (
        SELECT COUNT(*)
        FROM event_attendance a
        JOIN event e
            ON a.event_id = e.event_id
            AND a.organization_id = e.organization_id
        WHERE e.visibility = 'group_only'
          AND a.attendance_status = 'attended'
          AND NOT EXISTS (
              SELECT 1
              FROM group_membership gm
              WHERE gm.group_id = e.group_id
                AND gm.organization_id = e.organization_id
                AND gm.organization_membership_id =
                    a.organization_membership_id
          )
    ) AS invalid_group_check_ins;
