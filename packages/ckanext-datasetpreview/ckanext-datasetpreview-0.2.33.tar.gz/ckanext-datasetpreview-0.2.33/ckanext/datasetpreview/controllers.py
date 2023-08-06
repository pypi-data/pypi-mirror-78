import urllib
import ckan.plugins as p
from ckan.plugins.toolkit import config
import ckan.lib.helpers as h, json
from ckan.lib.base import BaseController, c, \
                          request, response, abort, redirect


import logging
log = logging.getLogger(__name__)

class ViewController(BaseController):

    def chart(self):
        
        params_to_forward = {}
        
        for key, value in request.params.iteritems():
            params_to_forward[key] = value

        params_to_forward['lala'] = 'lala'

        return p.toolkit.render('dataset-preview/chart.html')
