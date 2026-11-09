-- Query 1: How has event activity changed over time?

SELECT
    DATE_FORMAT(start_at, '%Y-%m') AS event_month,
    COUNT(*) AS total_events,
    COUNT(DISTINCT organization_id) AS active_organizations
FROM event
WHERE start_at >= '2026-01-01'
  AND start_at < '2026-11-01'
GROUP BY DATE_FORMAT(start_at, '%Y-%m')
ORDER BY event_month;

-- Query 2: Which organizations host the most events?

SELECT
    o.name AS organization,
    COUNT(e.event_id) AS total_events
FROM organization o
JOIN event e
    ON o.organization_id = e.organization_id
WHERE e.start_at >= '2026-01-01'
  AND e.start_at < '2026-11-01'
GROUP BY o.organization_id, o.name
ORDER BY total_events DESC;

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
