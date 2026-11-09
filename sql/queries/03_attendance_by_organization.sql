-- Query 3: Which communities get people to show up?

SELECT
    o.name AS organization,
    COUNT(DISTINCT e.event_id) AS total_events,
    SUM(
        CASE
            WHEN a.attendance_status = 'attended' THEN 1
            ELSE 0
        END
    ) AS total_check_ins,
    COUNT(DISTINCT
        CASE
            WHEN a.attendance_status = 'attended'
            THEN a.organization_membership_id
        END
    ) AS unique_attendees
FROM organization o
JOIN event e
    ON o.organization_id = e.organization_id
LEFT JOIN event_attendance a
    ON e.event_id = a.event_id
    AND e.organization_id = a.organization_id
WHERE e.start_at >= '2026-01-01'
  AND e.start_at < '2026-11-01'
GROUP BY o.organization_id, o.name
ORDER BY total_check_ins DESC;