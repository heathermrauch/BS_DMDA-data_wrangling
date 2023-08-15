/* Find unexpected cities */
SELECT tags.value, COUNT(*)
FROM (SELECT * FROM nodes_tags
	  UNION
	  SELECT * FROM ways_tags) AS tags
WHERE tags.key = 'city'
  AND tags.value NOT IN ('Augusta', 'Brady Township', 'Climax', 'Fulton', 'Galesburg',
						 'Kalamazoo', 'Kalamazoo Township', 'Nazareth', 'Parchment',
						 'Portage', 'Richland', 'Richland Township', 'Schoolcraft',
						 'Scotts', 'Vicksburg')
GROUP BY tags.type, tags.key, tags.value
ORDER BY count DESC;

/* Correct unexpected cities */
UPDATE nodes_tags SET value = 'Kalamazoo'
WHERE key = 'city' AND value IN ('Kalamaazo', 'kalamazoo');
UPDATE nodes_tags SET value = 'Scotts'
WHERE key = 'city'AND value = 'scotts';
UPDATE ways_tags SET value = 'Kalamazoo'
WHERE key = 'city' AND value IN ('Kalamaazo', 'kalamazoo');
UPDATE ways_tags SET value = 'Scotts'
WHERE key = 'city' AND value = 'scotts';
DELETE FROM nodes_tags WHERE key = 'city'
AND value NOT IN ('Augusta', 'Brady Township', 'Climax', 'Fulton', 'Galesburg',
				  'Kalamazoo', 'Kalamazoo Township', 'Nazareth', 'Parchment',
				  'Portage', 'Richland', 'Richland Township', 'Schoolcraft',
				  'Scotts', 'Vicksburg');
DELETE FROM ways_tags WHERE key = 'city'
AND value NOT IN ('Augusta', 'Brady Township', 'Climax', 'Fulton', 'Galesburg',
				  'Kalamazoo', 'Kalamazoo Township', 'Nazareth', 'Parchment',
				  'Portage', 'Richland', 'Richland Township', 'Schoolcraft',
				  'Scotts', 'Vicksburg');
