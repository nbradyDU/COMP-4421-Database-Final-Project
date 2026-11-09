-- Query 6: Is low RSVP follow-through widespread?

WITH event_follow_through AS (
    SELECT
        e.organization_id,
        e.event_id,
        COUNT(*) AS attending_rsvps,
        SUM(
            CASE
                WHEN a.attendance_status = 'attended' THEN 1
                ELSE 0
            END
        ) AS checked_in
    FROM event e
    JOIN event_rsvp r
        ON e.event_id = r.event_id
        AND e.organization_id = r.organization_id
    LEFT JOIN event_attendance a
        ON r.event_id = a.event_id
        AND r.organization_id = a.organization_id
        AND r.organization_membership_id =
            a.organization_membership_id
    WHERE r.rsvp_status = 'attending'
      AND e.start_at >= '2026-01-01'
      AND e.start_at < '2026-11-01'
    GROUP BY e.organization_id, e.event_id
    HAVING COUNT(*) >= 20
)
SELECT
    o.name AS organization,
    COUNT(*) AS qualifying_events,
    SUM(
        CASE
            WHEN f.checked_in * 2 < f.attending_rsvps
            THEN 1
            ELSE 0
        END
    ) AS events_below_50_pct,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN f.checked_in * 2 < f.attending_rsvps
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        1
    ) AS pct_events_below_50
FROM event_follow_through f
JOIN organization o
    ON f.organization_id = o.organization_id
GROUP BY o.organization_id, o.name
ORDER BY pct_events_below_50 DESC;
