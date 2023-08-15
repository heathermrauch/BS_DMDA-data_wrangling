#-------##-------##-------##-------##-------##-------##-------##-------#
#                               nodes.py                               #
#-------##-------##-------##-------##-------##-------##-------##-------#


import xml.etree.cElementTree as ET

from helpers import (audit_lat_lon, audit_timestamp, 
                     summarize_results, print_results)


def audit_nodes(filename: str):
    ''' Audits each field to be placed in the nodes sql table

    Parameters:
    filename (required): string representing xml file to be audited
    '''
    result_dict = {}
    lats_oob = []
    lons_oob = []
    ts_list = []
    ts_errors = []

    # Loop through all start tags and build dict structure
    for event, element in ET.iterparse(filename, events=('start',)):

        # Store lat and lon bounds
        if element.tag == 'bounds':
            lat_bounds = [element.attrib['minlat'], 
                          element.attrib['maxlat']]
            lon_bounds = [element.attrib['minlon'], 
                          element.attrib['maxlon']]

        # Identify node elements
        if element.tag == 'node':

            # Loop through node attributes
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

                # Audit lat attributes
                if key == 'lat':
                    oob_lat = audit_lat_lon(element.attrib.get(key),
                                            lat_bounds)
                    if oob_lat: lats_oob.append(oob_lat)

                # Audit lon attributes
                elif key == 'lon':
                    oob_lon = audit_lat_lon(element.attrib.get(key),
                                            lon_bounds)
                    if oob_lon: lons_oob.append(oob_lon)

                # Audit timestamp attributes
                elif key == 'timestamp':
                    timestamp = audit_timestamp(element.attrib.get(key))
                    if timestamp:
                        ts_list.append(timestamp)
                    else:
                        ts_errors.append(element.attrib.get(key))

    return (lat_bounds, lats_oob, lon_bounds, lons_oob, ts_errors,
            ts_list, result_dict)


if __name__ == "__main__":
    filename = 'map.osm'
    lat_bounds, lats_oob, lon_bounds, lons_oob, ts_errors, ts_list, \
        result_dict = audit_nodes(filename)
    print_results(result_dict,
                  lat_bounds=lat_bounds, lats_oob=lats_oob,
                  lon_bounds=lon_bounds, lons_oob=lons_oob,
                  ts_errors=ts_errors, ts_list=ts_list)
    print_results(result_dict, filename='output/node_audit.txt',
                  lat_bounds=lat_bounds, lats_oob=lats_oob,
                  lon_bounds=lon_bounds, lons_oob=lons_oob,
                  ts_errors=ts_errors, ts_list=ts_list)