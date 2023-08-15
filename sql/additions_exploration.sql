/* Database  */
SELECT table_catalog, table_schema, table_name,
	CASE table_name
		WHEN 'nodes' THEN (SELECT COUNT(*) FROM nodes)
		WHEN 'nodes_tags' THEN (SELECT COUNT(*) FROM nodes_tags)
		WHEN 'ways' THEN (SELECT COUNT(*) FROM ways)
		WHEN 'ways_nodes' THEN (SELECT COUNT(*) FROM ways_nodes)
		WHEN 'ways_tags' THEN (SELECT COUNT(*) FROM ways_tags)
	END AS record_count
FROM information_schema.tables AS tables
WHERE tables.table_catalog = 'osm'
  AND tables.table_schema = 'public'

/* Top Ten Cities and Towns by Population */
SELECT MAX(CASE key WHEN 'name' THEN value END) town
	,MAX(CASE key WHEN 'population' THEN 
		 (STRING_TO_ARRAY(value, ';'))[1] END)::INT population
FROM nodes_tags
GROUP BY id
HAVING MAX(CASE key WHEN 'name' THEN value END) IS NOT NULL
   AND MAX(CASE key WHEN 'population' THEN value END) IS NOT NULL
ORDER BY population DESC LIMIT 10;

/* Top Ten Largest Churches */
SELECT MAX(CASE key WHEN 'name' THEN value END) name,
	COUNT(DISTINCT ways_nodes.node_id) node_count
FROM ways_nodes
JOIN ways_tags ON ways_nodes.id = ways_tags.id
GROUP BY ways_nodes.id
HAVING MAX(CASE key WHEN 'name' THEN value END) IS NOT NULL
   AND MAX(CASE key WHEN 'amenity' THEN value END) = 'place_of_worship'
ORDER BY node_count DESC LIMIT 10;

/* Top Ten most frequent fast-food restaurants */
SELECT name, COUNT(DISTINCT id) way_count
FROM (
	SELECT ways_nodes.id, 
		MAX(CASE key WHEN 'name' THEN value END) name
	FROM ways_nodes
	JOIN ways_tags ON ways_nodes.id = ways_tags.id
	GROUP BY ways_nodes.id
	HAVING MAX(CASE key WHEN 'name' THEN value END) IS NOT NULL
	   AND MAX(CASE key WHEN 'amenity' THEN value END) = 'fast_food'
) base
GROUP BY name
ORDER BY way_count DESC LIMIT 10;
