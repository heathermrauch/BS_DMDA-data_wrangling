#-------##-------##-------##-------##-------##-------##-------##-------#
#                                ways.py                               #
#-------##-------##-------##-------##-------##-------##-------##-------#


import datetime, xml.etree.cElementTree as ET

import nodes

def audit_ways(filename:str):
    ''' Audits each field to be placed in the ways sql table

    Parameters:
    filename (required): string representing xml file to be audited
    '''
    result_dict = {}
    ts_list = []
    ts_errors = []

    # Loop through all start tags and build dict structure
    for event, element in ET.iterparse(filename, events=('start',)):

        # Identify way elements
        if element.tag == 'way':

            # Loop through way attributes
            for key, value in element.attrib.items():

                # Build result_dict
                if key not in result_dict.keys():
                    result_dict[key] = {'n': 1, 'values': {value: 1}}
                elif value not in result_dict[key]['values'].keys():
                    result_dict[key]['n'] += 1
                    result_dict[key]['values'][value] = 1
                else:
                    result_dict[key]['n'] += 1
                    result_dict[key]['values'][value] += 1

                # Audit timestamp attrib
                if key == 'timestamp':

                    # Check for actual date/time
                    try:
                        timestamp = datetime.datetime.strptime(element.attrib.get(key),
                                                               '%Y-%m-%dT%H:%M:%SZ')
                        ts_list.append(timestamp)
                    except:
                        ts_errors.append(element.attrib.get(key))

    return result_dict, ts_list, ts_errors

if __name__ == '__main__':
    filename = 'map.osm'
    result_dict, ts_list, ts_errors = audit_ways(filename)
    nodes.print_results(result_dict, ts_list=ts_list, ts_errors=ts_errors)
    nodes.print_results(result_dict, ts_list = ts_list, ts_errors = ts_errors,
                        filename='output/way_audit.txt')