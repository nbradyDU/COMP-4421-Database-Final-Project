-- Query 5: Which events have the weakest RSVP follow-through?

SELECT
    o.name AS organization,
    e.event_id,
    e.title,
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
FROM event e
JOIN organization o
    ON e.organization_id = o.organization_id
JOIN event_rsvp r
    ON e.event_id = r.event_id
    AND e.organization_id = r.organization_id
LEFT JOIN event_attendance a
    ON r.event_id = a.event_id
    AND r.organization_id = a.organization_id
    AND r.organization_membership_id = a.organization_membership_id
WHERE r.rsvp_status = 'attending'
  AND e.start_at >= '2026-01-01'
  AND e.start_at < '2026-11-01'
GROUP BY o.name, e.event_id, e.title
HAVING COUNT(*) >= 20
ORDER BY check_in_rate_pct ASC
LIMIT 10;

