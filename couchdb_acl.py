import httplib
import json
from base64 import b64encode
from base64 import b64decode

user_creation_url_template = '/_users/org.couchdb.user:%s'

def provision_couchdb_user(username, password, role):
    connection = httplib.HTTPConnection('localhost', 5984)

    server_admin_auth = b64encode("rahul" + ":" + "rahul1982").decode("ascii")
    print server_admin_auth
    http_header = dict()
    http_header['Authorization'] = 'Basic %s' % server_admin_auth
    http_header ['Accept'] = 'application/json'
    print 'http_header: ', http_header

    user_creation_url = user_creation_url_template % username

    print 'user_creation_url:', user_creation_url

    print 'http_header:', http_header

    #create user for couch db instance
    try:
        print 'GET PROCESS'
        connection.request('GET', user_creation_url, headers=http_header)
        gethttpresponse = connection.getresponse()
        json_get_response = gethttpresponse.read()
        print 'gethttpresponse:', json_get_response

        response_load = json.loads(json_get_response)
        connection.close()

        user_creation_json = dict()
        user_creation_json['name'] = username
        user_creation_json['password'] = password
        user_creation_json['type'] = 'user'

        user_creation_json['roles'] = []
        user_creation_json['roles'].append(role)
        user_creation_json['roles'].append('testdb_member1')

        tmp_dict = dict()
        tmp_dict['roles'] = [role]
        tmp_dict['roles'].append('testdb_member1')

        # if tmp_dict['roles'] not in user_creation_json['roles']:
        #     print 'tmp not present', tmp_dict['roles'], user_creation_json['roles']
        #     shared_items = set(tmp_dict['roles']).intersection(user_creation_json['roles'])
        #     print 'len(shared_items): ', shared_items
        #     user_creation_json['roles'].append(role)

        print 'gethttpresponse: ', type(gethttpresponse.status), ' ', type(httplib.NOT_FOUND)
        if gethttpresponse.status != httplib.NOT_FOUND:
            print 'response_load', response_load
            print 'response_load[_rev]: ', response_load['_rev']
            # user_creation_json = user_creation_json_template % (username, password, role)
            user_creation_json['_rev'] = response_load['_rev']
            #print 'name: ', user_creation_json['name']
            print 'user_creation_json:', json.dumps(user_creation_json)

        print 'PUT PROCESS'
        connection.request('PUT', user_creation_url, headers=http_header, body=json.dumps(user_creation_json))
        httpresponse = connection.getresponse()
        print 'httpresponse: ', httpresponse.status
        connection.close()
    except Exception as e:
        print '--- exception --- :', e
        return 1
    return 0

security_json_template = '{"admins":{"names":[],"roles":[]},"members":{"names":[],"roles":["%s"]}}'
security_json_template1 = '{}'
security_url = '/%s/_security'

def provision_couchdb_security(database_name, role):
    connection = httplib.HTTPConnection('localhost', 5984)

    server_admin_auth = b64encode("rahul" + ":" + "rahul1982").decode("ascii")
    print server_admin_auth
    http_header = dict()
    http_header['Authorization'] = 'Basic %s' % server_admin_auth
    http_header ['Accept'] = 'application/json'
    print 'http_header: ', http_header

    try:
        print 'GET PROCESS'
        connection.request('GET', security_url % database_name, headers=http_header)
        gethttpresponse = connection.getresponse()
        json_get_response = gethttpresponse.read()
        print 'gethttpresponse:', json_get_response

        response_load = json.loads(json_get_response)
        connection.close()

        # if tmp_dict['roles'] not in user_creation_json['roles']:
        #     print 'tmp not present', tmp_dict['roles'], user_creation_json['roles']
        #     shared_items = set(tmp_dict['roles']).intersection(user_creation_json['roles'])
        #     print 'len(shared_items): ', shared_items
        #     user_creation_json['roles'].append(role)

        print 'gethttpresponse: '
        if gethttpresponse.status == httplib.OK and 'admins' in json_get_response:
            print 'PUT PROCESS', security_json_template % role
            connection.request('PUT', security_url % database_name,
                               headers=http_header, body=security_json_template % role)
            httpresponse = connection.getresponse()
            print 'httpresponse: ', httpresponse.status
            connection.close()
    except:
        print '--- exception --- :'
        return 1
    return 0

validate_doc_update = '''
{
  "validate_doc_update": "function(newDoc, oldDoc, userCtx, secObj) {if (userCtx.roles.indexOf('_admin') == -1) { throw({forbidden: 'user does not have write access'});}}"
}
'''



def provision_role_to_rouser (database_name):
    connection = httplib.HTTPConnection('localhost', 5984)

    server_admin_auth = b64encode("rahul" + ":" + "rahul1982").decode("ascii")
    print server_admin_auth
    http_header = dict()
    http_header['Authorization'] = 'Basic %s' % server_admin_auth
    http_header ['Accept'] = 'application/json'
    print 'http_header: ', http_header

    try:
        print 'GET PROCESS'
        connection.request('GET', '/%s/_design/CLSNetReadAccess' % database_name, headers=http_header)
        gethttpresponse = connection.getresponse()
        json_get_response = gethttpresponse.read()
        print 'gethttpresponse:', json_get_response

        response_load = json.loads(json_get_response)
        connection.close()

        print 'gethttpresponse: '
        if gethttpresponse.status == httplib.NOT_FOUND:
            print 'PUT PROCESS'
            connection.request('PUT', '/%s/_design/CLSNetReadAccess' % database_name,
                               headers=http_header, body=validate_doc_update)
            httpresponse = connection.getresponse()
            print 'httpresponse: ', httpresponse.status
            connection.close()
    except:
        print '--- exception --- :'
        return 1
    return 0



def couchdb_acl_setup():
    provision_couchdb_user('rouser5', 'password', 'testdb_member2')
    provision_couchdb_security('testdb', 'testdb_member2')
    provision_role_to_rouser ('testdb')


def fabric_ca_server_csr_signing():
    c = httplib.HTTPConnection("localhost", 7054)
    userAndPass = b64encode("admin" + ":" + "adminpw").decode("ascii")
    print userAndPass
    headers = dict()
    headers = { 'Authorization' : 'Basic %s' % userAndPass }

    json_body = dict
    csr_content = '''
    -----BEGIN CERTIFICATE REQUEST-----
    MIIBSTCB8AIBADBdMQswCQYDVQQGEwJVUzEXMBUGA1UECBMOTm9ydGggQ2Fyb2xp
    bmExFDASBgNVBAoTC0h5cGVybGVkZ2VyMQ8wDQYDVQQLEwZGYWJyaWMxDjAMBgNV
    BAMTBWFkbWluMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEv3dodjmcdgoJhboa
    j5aEcn52fdwmpvDW55gTmnYjt0rMnmSnF6Hf2S1o7f3TawzgBy1xX5f63fXQRshP
    De8Xg6AxMC8GCSqGSIb3DQEJDjEiMCAwHgYDVR0RBBcwFYITcmFodWwtSW5zcGly
    b24tMzQ0MjAKBggqhkjOPQQDAgNIADBFAiEA80QH+1Tx8RleaeoRfj/ysK0dEWrc
    LI+ekiycJKI9h5MCIFiJQ/gbL/cTJZCceddpt2fcRP1adnFuYyoEKe/U9o2E
    -----END CERTIFICATE REQUEST-----
    '''
    json_body = {'certificate_request': csr_content}
    body = json.dumps(json_body)
    print body
    #c.request('GET', '/', body, headers=headers)
    c.request('POST', '/enroll', body=body, headers=headers)
    res = c.getresponse()

    data = res.read()
    print res.reason, res.status
    print res.getheaders()
    json_data = json.loads(data)
    print json_data

    print 'Certificate Data: ', json_data['result']['Cert']
    print b64decode(json_data['result']['Cert'])


couchdb_acl_setup()