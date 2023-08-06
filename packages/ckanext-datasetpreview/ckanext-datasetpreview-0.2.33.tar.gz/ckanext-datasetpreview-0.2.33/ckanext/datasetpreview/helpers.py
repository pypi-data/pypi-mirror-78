import hashlib
import json
import logging
import os
import random
import requests
from pylons import config
from messytables import CSVTableSet, type_guess, \
  types_processor, headers_guess, headers_processor, \
  offset_processor
from messytables.types import IntegerType, DecimalType, StringType


log = logging.getLogger(__name__)


def package_preview(pkg_dict):

    draw = config.get('ckanext.datasetpreview.draw', 'ALL')

    if draw is ['NO', 'none', 'false']:
        return False
    
    base = {
            'name': unicode(pkg_dict['name']).encode("utf-8"),
            'height': config.get('ckanext.datasetpreview.chart_height', '300'),
            'chart_title': '',  # we already have the title in the list
            'chart_type': random.choice(['Bar', 'Bar', 'Bar', 'Column', 'Column', 'Pie']),
            'chart_color': random.choice(['#303030', '#707070', '#AABBCC']),
            'url': 'csv_resource',  # lazy URL, use the first available CSV resource. Could use the resource['name'] instead
            'fields': '[0, 1]',  # lazy selector, just the first two columns
            }
    
    existing_config = False  
    # sample config: {"chart_type": "Bar", "chart_color": "#FF00AA"}
    for extra in pkg_dict['extras']:
        if extra['key'] == 'dataset_preview':
            existing_config = json.loads(extra['value'])

    if draw != 'ALL' and not existing_config:
        return False

    if existing_config:
        base.update(existing_config)

    return json.dumps(base)


def get_preview_chart_data(pkg_dict):
    """
    Check if this dataset use preview and in this case return data to preview
    """
    dp = package_preview(pkg_dict)
    if not dp:
        log.debug('No dataset preview for {}'.format(pkg_dict['name']))
        return False
    log.info('Dataset preview found for{}: {}'.format(pkg_dict['name'], dp))
    
    cfg = json.loads(dp)
    
    data = {unicode(k).encode("utf-8"): unicode(v).encode("utf-8") for k, v in cfg.iteritems()}
    # some fields requires to be dumped
    data['fields'] = json.loads(data['fields'])
    
    if data['url'].lower().startswith('http'):
        pass
    else:
        data_found = False
        if data['url'] == 'csv_resource':  
            for resource in pkg_dict['resources']:
                if resource['format'].lower() == 'csv':
                    data_found = True
                    data['url'] = unicode(resource['url']).encode("utf-8")
        else: # could by a resource name
            for resource in pkg_dict['resources']:
                if resource['name'] == data['url']:
                    data_found = True
                    data['url'] = unicode(resource['url']).encode("utf-8")
        
        if not data_found:
            return False

    headers, datos = csv_as_data(data['url'], data['fields'])
    if datos is None:  # something failed
        return None
    data['data'] = datos
    data['headers'] = headers

    return data

def csv_as_data(url, fields):

    path = csv_url_to_path(url)
    if path is None:
        log.error('Error saving URL {}'.format(url))
        return None, None
    fh = open(path, 'rb')
    # Load a file object:
    table_set = CSVTableSet(fh)
    # A table set is a collection of tables:
    row_set = table_set.tables[0]
    # guess header names and the offset of the header:
    offset, headers = headers_guess(row_set.sample)
    row_set.register_processor(headers_processor(headers))
    log.info('DatasetPreview CSV headers {}'.format(headers))
    
    # add one to begin with content, not the header:
    row_set.register_processor(offset_processor(offset + 1))

    # guess column types:
    types = type_guess(row_set.sample, strict=True)
    log.info('DatasetPreview CSV types {}'.format(types))
    
    final_headers = []
    c = 0
    numeric_used_fields = []
    for header in headers:
        # if fields is like [0, 1] check for "c"
        # if fields is like ["field1", "field2"] check the header name
        h = unicode(header).encode("utf-8")
        if c in fields or h in fields:
            if type(types[c]) == IntegerType:
                final_headers.append([h, 'number'])
            elif type(types[c]) == DecimalType:
                final_headers.append([h, 'number'])
            else:
                final_headers.append([h, 'string'])
            numeric_used_fields.append(c)
        c+= 1
    
    # and tell the row set to apply these types to
    # each row when traversing the iterator:
    row_set.register_processor(types_processor(types))
    log.info('Rowset {}'.format(row_set))

    data = []
    # now run some operation on the data:
    for row in row_set:
        line = []
        c = 0
        for val in row:
            # if fields is like [0, 1] check for "c"
            # if fields is like ["field1", "field2"] check the header name
            if c in numeric_used_fields:
                if type(val.type) == StringType:
                    v = unicode(val.value).encode("utf-8")
                elif type(val.type) == DecimalType:
                    v = float(val.value)
                elif type(val.type) == IntegerType:
                    v = val.value
                line.append(v)
            c += 1
        data.append(line)
    
    return final_headers, data


def csv_url_to_path(url):
    """ Define a unique path for this URL and save the data in there
        Return the path"""

    path = get_cache_path(url)
    if not os.path.isfile(path):
        # if it fails could be None
        return save_cache(url, path)
    
    return path


def get_cache_path(url):
    """ get cache path from URL """
    cache_folder = config['ckanext.datasetpreview.cache_path']
    name = hashlib.sha1(url).hexdigest()
    path = os.path.join(cache_folder, '{}.csv'.format(name))
    log.info('DataPreview cache path {}'.format(path))
    return path


def save_cache(url, path):
    """ save online CSV locally """
    try:
        response = requests.get(url, allow_redirects=True)
    except Exception as e:
        log.error('Error getting URL {}: {}'.format(url, str(e)))
        return None
    # ensure content is CSV
    log.debug('DatasetPreview status response URL {}: {}'.format(url, response.status_code))
    if response.status_code == 404:
        log.error('DatasetPreview CSV not found in URL {}'.format(url))
        # raise Exception('DatasetPreview Unexpected status {}: {}'.format(url, response.status_code))
        return None
    elif response.text.startswith('<!DOCTYPE html>'):
        # raise Exception('DatasetPreview Unexpected response {}'.format(response.text))
        log.error('DatasetPreview CSV is not CSV {}'.format(url))
        return None
    f = open(path, 'wb')
    f.write(response.content)
    f.close()
    log.info('DataPreview cache saved {}'.format(path))
    
    return path