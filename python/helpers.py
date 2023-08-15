#-------##-------##-------##-------##-------##-------##-------##-------#
#                              helpers.py                              #
#-------##-------##-------##-------##-------##-------##-------##-------#


import datetime, pprint, xml.etree.cElementTree as ET


def audit_lat_lon(value:str, bounds:list):
    val = float(value)
    if val < float(bounds[0]) or val > float(bounds[-1]):
        return val


def audit_timestamp(value:str):
    try:
        timestamp = datetime.datetime.strptime(value,
                                               '%Y-%m-%dT%H:%M:%SZ')
        return timestamp
    except:
        return None


def summarize_results(result_dict:dict, name:str, n:int=10):
    ''' Summarizes all elements of a dictionary if its length is n
    or less. Counts the top n elements of the dictionary if its length
    is more than n. By default, n is 10.

    Parameters:
    result_dict (required): a dictionary of keys and counts to be
        printed
    name (required): a string representing the name to be used when
        referencing data
    n (default=10): an integer representing the threshold to use when
        printing the top n
    '''
    out = '\n'
    length = len(result_dict)
    if length < n: 
        n = length
    result_list = sorted(result_dict.items(), key=lambda x: x[1],
                         reverse=True)
    out += f'\nUnique {name}: {length}' 
    out += f'\nTop {n} {name}:'
    i = 0
    for item in result_list:
        if i >= n: 
            break
        out += f'\n\t{item[0]}: n={item[1]}'
        i += 1
    return out


def print_results(data:dict, filename:str=None, lat_bounds:list=None, lats_oob:list=None, lon_bounds:list=None, lons_oob:list=None, ts_list:list=None, ts_errors:list=None, cities:set=None, counties:set=None):
    out =    '#================#'
    out += '\n# Audit Findings #'
    out += '\n#================#'

    top_data = {key: value['n'] 
                    for key, value in data.items() 
                        if value['n']}
    out += summarize_results(top_data, 'attributes')
    
    sub_data = {k: v for k, v in top_data.items() if v > 400} 
    for key, value in sub_data.items():
        out += summarize_results(data[key]['values'], f'{key} values')
    
    if lat_bounds:
        out += '\n\nLatitude Bounds: {} to {}'.format(lat_bounds[0],
                                                      lat_bounds[-1])
    if lats_oob:
        out += '\nNumber of out-of-bounds values: ' + str(len(lats_oob))
        out += '\n\tMin out-of-bounds: ' + str(min(lats_oob))
        out += '\n\tMax out-of-bounds: ' + str(max(lats_oob))
    if lon_bounds:
        out += '\n\nLongitude Bounds: {} to {}'.format(lon_bounds[0],
                                                       lon_bounds[-1])
    if lons_oob:
        out += '\nNumber of out-of-bounds values: ' + str(len(lons_oob))
        out += '\n\tMin out-of-bounds: ' + str(min(lons_oob))
        out += '\n\tMax out-of-bounds: ' + str(max(lons_oob))
    if ts_errors and ts_list:
        out += '\n\nTimestamp Conversion Errors: ' + str(len(ts_errors))
        out += '\n\tFirst timestamp: ' + str(min(ts_list))
        out += '\n\tLast timestamp: ' + str(max(ts_list))
    elif not(ts_errors) and ts_list:
        out += '\n\nTimestamp Conversion Errors: 0'
        out += '\n\tFirst timestamp: ' + str(min(ts_list))
        out += '\n\tLast timestamp: ' + str(max(ts_list))
    if cities: 
        out += '\n\nCities not within Kalamazoo County'
        out += '\n' + pprint.pformat(cities)
    if counties:
        out += '\n\nCounties not equal to Kalamazoo'
        out += '\n' + pprint.pformat(counties)

    if filename:
        with open(filename, mode='w') as f:
            f.writelines(out)
    else:
        print(out)