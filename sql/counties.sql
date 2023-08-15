/* View unexpected counties */
SELECT DISTINCT tags.value
FROM (SELECT * FROM nodes_tags
	  UNION
	  SELECT * FROM ways_tags) AS tags
WHERE tags.key IN ('county', 'County', 'county_name')
  AND tags.value NOT ILIKE '%kalamazoo%'
ORDER BY value;

/* Correct unexpected counties */
UPDATE nodes_tags SET value = 'Kalamazoo'
WHERE key IN ('county', 'County', 'county_name')
  AND value ILIKE '%kalamazoo%';
UPDATE ways_tags SET value = 'Kalamazoo'
WHERE key IN ('county', 'County', 'county_name')
  AND value ILIKE '%kalamazoo%';
DELETE FROM nodes_tags
WHERE key IN ('county', 'County', 'county_name')
  AND value != 'Kalamazoo';
DELETE FROM ways_tags
WHERE key IN ('county', 'County', 'county_name')
  AND value != 'Kalamazoo';