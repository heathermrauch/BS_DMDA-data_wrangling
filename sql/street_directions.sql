SELECT DISTINCT tags.value
FROM (SELECT * FROM nodes_tags
	  UNION
	  SELECT * FROM ways_tags) AS tags
WHERE tags.type = 'addr' AND tags.key = 'street'
/* compare the parsed value array to the array of expected values
   only return values that don't contain any exected values */
  AND NOT(string_to_array(tags.value, ' ') &&
		  ARRAY['North', 'South', 'East', 'West'])
  AND string_to_array(tags.value, ' ') && ARRAY['N', 'S', 'E', 'W'];

/* build the table of values to replace */
CREATE TABLE value_mapping (old_value text, new_value text);
INSERT INTO value_mapping VALUES
('N', 'North'), ('S', 'South'), ('E', 'East'), ('W', 'West');

/* perform the updates */
UPDATE nodes_tags
SET value = REPLACE(nodes_tags.value, value_mapping.old_value, value_mapping.new_value)
FROM value_mapping
WHERE value_mapping.old_value = ANY(string_to_array(nodes_tags.value, ' '))
  AND value_mapping.new_value != ANY(string_to_array(nodes_tags.value, ' '))
  AND nodes_tags.type = 'addr' AND nodes_tags.key = 'street';
UPDATE ways_tags
SET value = REPLACE(ways_tags.value, value_mapping.old_value, value_mapping.new_value)
FROM value_mapping
WHERE value_mapping.old_value = ANY(string_to_array(ways_tags.value, ' '))
  AND value_mapping.new_value != ANY(string_to_array(ways_tags.value, ' '))
  AND ways_tags.type = 'addr' AND ways_tags.key = 'street';
  
/* the value mapping table is no longer needed */
DROP TABLE value_mapping;