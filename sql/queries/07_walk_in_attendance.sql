-- Query 7: How many people attend without an RSVP?

SELECT
    o.name AS organization,
    COUNT(*) AS total_check_ins,
    SUM(
        CASE
            WHEN NOT EXISTS (
                SELECT 1
                FROM event_rsvp r
                WHERE r.event_id = a.event_id
                  AND r.organization_id = a.organization_id
                  AND r.organization_membership_id =
                      a.organization_membership_id
            )
            THEN 1
            ELSE 0
        END
    ) AS walk_in_check_ins,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN NOT EXISTS (
                    SELECT 1
                    FROM event_rsvp r
                    WHERE r.event_id = a.event_id
                      AND r.organization_id = a.organization_id
                      AND r.organization_membership_id =
                          a.organization_membership_id
                )
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        1
    ) AS walk_in_pct
FROM event_attendance a
JOIN event e
    ON a.event_id = e.event_id
    AND a.organization_id = e.organization_id
JOIN organization o
    ON e.organization_id = o.organization_id
WHERE a.attendance_status = 'attended'
  AND e.start_at >= '2026-01-01'
  AND e.start_at < '2026-11-01'
GROUP BY o.organization_id, o.name
ORDER BY walk_in_pct DESC;
