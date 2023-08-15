#-------##-------##-------##-------##-------##-------##-------##-------#
#                             load_sql.py                              #
#-------##-------##-------##-------##-------##-------##-------##-------#


import datetime, pandas as pd, psycopg2, re
import xml.etree.cElementTree as ET
from io import StringIO


NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 
               'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']
COLON = re.compile(r'^([a-z]|[A-Z]|_)+:([a-z]|[A-Z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>\'"\?%#$@\t\r\n]')
param_dic = {
    'host': 'localhost',
    'database': 'osm',
    'port': 5433,
    'user': 'project_user',
    'password': 'Passw0rd'
}


def parse_osm(filename:str, node_fields:list=NODE_FIELDS, way_fields:list=WAY_FIELDS, default_tag_type:str='regular', colon=COLON, problemchars=PROBLEMCHARS):
    nodes = []
    node_tags = []
    ways = []
    way_tags = []
    way_nodes = []

    for event, element in ET.iterparse(filename, events=('start',)):

        if element.tag == 'node':
            node = {}
            for field in node_fields:
                node[field] = element.attrib.get(field)
            nodes.append(node)

            for tag in element.findall('tag'):
                key = tag.attrib.get('k')
                value = re.sub(problemchars, ' ', tag.attrib.get('v'))
                node_tag = {}
                node_tag['id'] = node.get('id')
                if colon.search(key):
                    node_tag['key'] = key.split(':', 1)[1]
                    node_tag['value'] = value
                    node_tag['type'] = key.split(':', 1)[0]
                else:
                    node_tag['key'] = key
                    node_tag['value'] = value
                    node_tag['type'] = default_tag_type
                node_tags.append(node_tag)

        elif element.tag == 'way':
            way = {}
            for field in way_fields:
                way[field] = element.attrib.get(field)
            ways.append(way)

            for tag in element.findall('tag'):
                key = tag.attrib.get('k')
                value = re.sub(problemchars, ' ', tag.attrib.get('v'))
                way_tag = {}
                way_tag['id'] = way.get('id')
                if colon.search(key):
                    way_tag['key'] = key.split(':', 1)[1]
                    way_tag['value'] = value
                    way_tag['type'] = key.split(':', 1)[0]
                else:
                    way_tag['key'] = key
                    way_tag['value'] = value
                    way_tag['type'] = default_tag_type
                way_tags.append(way_tag)

            i = 0
            for node in element.findall('nd'):
                way_node = {
                    'id': way.get('id'),
                    'node_id': node.attrib.get('ref'),
                    'position': i
                }
                way_nodes.append(way_node)
                i += 1

    return nodes, node_tags, ways, way_tags, way_nodes


def connect(params_dic:dict=param_dic):
    ''' Connect to the PostgreSQL database server '''
    conn = None
    try:
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn


def copy_from_stringio(conn, df:pd.DataFrame, table:str):
    ''' Save a dataframe in memory and copy to PostgreSQL '''
    # Save dataframe to in memory buffer
    buffer = StringIO()
    df.to_csv(buffer, header=False, index=False, sep='\t',
              line_terminator='\n')
    buffer.seek(0)

    cursor = conn.cursor()
    try:
        cursor.copy_from(buffer, table, sep='\t')
        conn.commit()
        print(f'Inserted {len(df)} records into {table}')
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Error: {error}')
        conn.rollback()
        cursor.close()
    finally:
        cursor.close()


if __name__ == '__main__':
    
    # Parse osm file into dicts
    filename = 'map.osm'
    nodes, node_tags, ways, way_tags, way_nodes = parse_osm(filename)
    
    # Load dicts into DataFrames
    df_nodes = pd.DataFrame.from_dict(nodes)
    df_node_tags = pd.DataFrame.from_dict(node_tags)
    df_ways = pd.DataFrame.from_dict(ways)
    df_way_tags = pd.DataFrame.from_dict(way_tags)
    df_way_nodes = pd.DataFrame.from_dict(way_nodes)

    # Handle timestamp fields
    df_nodes['timestamp'] = df_nodes['timestamp'].apply(
        lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z')
    )
    df_ways['timestamp'] = df_ways['timestamp'].apply(
        lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z')
    )

    # Load data to PostgreSQL
    with connect(param_dic) as conn:
        copy_from_stringio(conn, df_nodes, 'nodes')
        copy_from_stringio(conn, df_node_tags, 'nodes_tags')
        copy_from_stringio(conn, df_ways, 'ways')
        copy_from_stringio(conn, df_way_tags, 'ways_tags')
        copy_from_stringio(conn, df_way_nodes, 'ways_nodes')
