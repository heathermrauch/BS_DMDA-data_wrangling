/* Out of Bounds Coordinates */
SELECT tags.key, tags.value, COUNT(DISTINCT nodes.id) AS n
FROM nodes 
JOIN (SELECT nodes_tags.id AS node_id, nodes_tags.key, nodes_tags.value
	  FROM nodes_tags
	  UNION ALL
	  SELECT ways_nodes.node_id, ways_tags.key, ways_tags.value
	  FROM ways_tags
	  JOIN ways_nodes ON ways_tags.id = ways_nodes.id
) AS tags ON nodes.id = tags.node_id
WHERE (nodes.lat < 42.0697000 OR nodes.lat > 42.4224000 OR
	   nodes.lon < -85.7661000 OR nodes.lon > -85.2937000)
  AND (tags.key ILIKE '%county%' OR tags.key ILIKE '%city%')
GROUP BY tags.key, tags.value
ORDER BY value;

/* Out of Bounds Coordinates Labeled 'Kalamazoo' */
SELECT id, lat, lon, key, value
FROM nodes 
JOIN (SELECT nodes_tags.id AS node_id, nodes_tags.key, nodes_tags.value
	  FROM nodes_tags
	  UNION ALL
	  SELECT ways_nodes.node_id, ways_tags.key, ways_tags.value
	  FROM ways_tags
	  JOIN ways_nodes ON ways_tags.id = ways_nodes.id
) AS tags ON nodes.id = tags.node_id
WHERE (nodes.lat < 42.0697000 OR nodes.lat > 42.4224000 OR
	   nodes.lon < -85.7661000 OR nodes.lon > -85.2937000)
  AND (tags.key ILIKE '%county%' OR tags.key ILIKE '%city%')
  AND tags.value ILIKE '%kalamazoo%'
ORDER BY value;

/* Remove Out of Bounds Coordinates */
DELETE FROM ways_tags WHERE ways_tags.id IN (
	SELECT ways_nodes.id FROM ways_nodes WHERE ways_nodes.node_id IN (
		SELECT nodes.id FROM nodes
		WHERE (nodes.lat < 42.0697000 OR nodes.lat > 42.4224000 OR
			   nodes.lon < -85.7661000 OR nodes.lon > -85.2937000)
	)
);
DELETE FROM ways_nodes WHERE ways_nodes.node_id IN (
	SELECT nodes.id FROM nodes
	WHERE (nodes.lat < 42.0697000 OR nodes.lat > 42.4224000 OR
		   nodes.lon < -85.7661000 OR nodes.lon > -85.2937000)
);
DELETE FROM nodes_tags WHERE nodes_tags.id IN (
	SELECT nodes.id FROM nodes
	WHERE (nodes.lat < 42.0697000 OR nodes.lat > 42.4224000 OR
		   nodes.lon < -85.7661000 OR nodes.lon > -85.2937000)
);
DELETE FROM nodes 
	WHERE (nodes.lat < 42.0697000 OR nodes.lat > 42.4224000 OR
		   nodes.lon < -85.7661000 OR nodes.lon > -85.2937000);