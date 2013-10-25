import httplib2, json

class DataQuery:

  def __init__(self, host = 'dbmaster.autodns.kserver.biz', port = 5984, database = 'locationmaps', username = 'luzifer', password = ''):
    self.baseurl = 'http://%s:%d/%s/_design/locations/_view/get_for_user_with_location' % (host, port, database)
    self.requester = httplib2.Http('.cache')
    self.requester.add_credentials(username, password)

  def get_data_since(self, account = 'knut', starttime = 0):
    '''
      URL http://dbmaster.autodns.kserver.biz:5984/locationmaps/_design/locations/_view/get_for_user_with_location?startkey=[%22knut%22,1290254183]
    '''
    fullurl = '%s?startkey=[%%22%s%%22,%d]' % (self.baseurl, account, starttime)
    resp, content = self.requester.request(fullurl, 'GET')

    data = json.loads(content)
    return self._simplify_data(data)

  def _simplify_data(self, data):
    out = {}

    for ds in data['rows']:
      out[ds['key'][1]] = ds['value']

    return out
    

