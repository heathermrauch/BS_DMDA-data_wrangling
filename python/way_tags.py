#-------##-------##-------##-------##-------##-------##-------##-------#
#                             way_tags.py                             #
#-------##-------##-------##-------##-------##-------##-------##-------#


import xml.etree.cElementTree as ET
import node_tags

def audit_way_tags(filename:str):
    result_dict = {}
    counties = set()

    # Loop through all start tags and build dict structure
    for event, element in ET.iterparse(filename, events=('start',)):

        # Identify way elements
        if element.tag == 'way':

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
                    result_dict[key]['values'][value] += 1

                # Audit tiger:county tags
                if key == 'tiger:county':
                    if value != 'Kalamazoo, MI':
                        counties.add(value)

    return result_dict, counties


if __name__ == '__main__':
    filename = 'map.osm'
    result_dict, counties = audit_way_tags(filename)
    node_tags.print_results(result_dict, counties=counties)
    node_tags.print_results(result_dict, filename='output/way_tag_audit.txt', counties=counties)