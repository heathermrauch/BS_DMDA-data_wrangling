#-------##-------##-------##-------##-------##-------##-------##-------#
#                             node_tags.py                             #
#-------##-------##-------##-------##-------##-------##-------##-------#


import xml.etree.cElementTree as ET

from helpers import print_results, summarize_results


KZOO_CITIES = ['Augusta', 'Climax', 'Fulton', 'Galesburg','Kalamazoo',
               'Kalamazoo Township', 'Nazareth', 'Parchment', 'Portage', 
               'Richland', 'Richland Township', 'Schoolcraft', 'Scotts', 
               'Vicksburg']


def audit_node_tags(filename: str):
    ''' Audits each field to be placed in the node_tags sql table

    Required Parameters:
    filename (required): string representing xml file to be audited
    '''
    result_dict = {}
    cities = set()
    
    # Loop through all start tags and build dict structure
    for event, element in ET.iterparse(filename, events=('start',)):

        # Identify node elements
        if element.tag == 'node':
            
            # Loop through nested tag elements
            for tag in element.findall('tag'):
                key = tag.attrib['k']
                value = tag.attrib['v']

                # Build result_dict
                if key not in result_dict.keys():
                    result_dict[key] = {'n': 1, 'values': {value: 1}}
                elif value not in result_dict[key]['values'].keys():
                    result_dict[key]['n'] += 1
                    result_dict[key]['values'][value] = 1
                else:
                    result_dict[key]['n'] += 1
                    result_dict[key]['values'][value] +=1

                # Audit addr:city attributes
                if key =='addr:city':
                    if value not in KZOO_CITIES: 
                        cities.add(value)

    return result_dict, cities
                

if __name__ == '__main__':
    filename = 'map.osm'
    result_dict, cities = audit_node_tags(filename)
    print_results(result_dict, cities=cities)
    print_results(result_dict, filename='node_tag_audit.txt',
                  cities=cities)