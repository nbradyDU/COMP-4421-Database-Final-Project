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
