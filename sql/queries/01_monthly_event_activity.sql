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
