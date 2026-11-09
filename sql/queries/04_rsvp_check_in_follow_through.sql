-- Query 4: Do people who RSVP actually attend?

SELECT
    o.name AS organization,
    COUNT(*) AS attending_rsvps,
    SUM(
        CASE
            WHEN a.attendance_status = 'attended' THEN 1
            ELSE 0
        END
    ) AS checked_in,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN a.attendance_status = 'attended' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        1
    ) AS check_in_rate_pct
FROM event_rsvp r
JOIN event e
    ON r.event_id = e.event_id
    AND r.organization_id = e.organization_id
JOIN organization o
    ON e.organization_id = o.organization_id
LEFT JOIN event_attendance a
    ON r.event_id = a.event_id
    AND r.organization_id = a.organization_id
    AND r.organization_membership_id = a.organization_membership_id
WHERE r.rsvp_status = 'attending'
  AND e.start_at >= '2026-01-01'
  AND e.start_at < '2026-11-01'
GROUP BY o.organization_id, o.name
ORDER BY check_in_rate_pct DESC;