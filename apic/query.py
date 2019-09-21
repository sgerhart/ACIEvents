from __future__ import absolute_import, division, print_function
from builtins import *


import requests


# Generic requests for REST Gets (ACICSP is read only to ACI)
def json_get(url, auth_token):

    try:

        response = requests.get(url, cookies=auth_token, verify=False)

        # response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        print("http error: ", e)

    except requests.exceptions.ConnectionError as e:

        print("There is a connection issue: ", e)


# Refresh APICs Token
def refresh_apic(apic_ip,auth_token):

    apic_url = 'https://' + apic_ip + '/api/aaaRefresh.json'

    refreshed_auth = json_get(apic_url,auth_token)

    for r in refreshed_auth['imdata']:

        token = str(r['aaaLogin']['attributes']['token'])

        return {'APIC-Cookie': token}


# Build subscriptions for WebSocket
def build_subscription(url, auth_token):

    sub_ids = []

    # vpcif_subscr_url = url + 'class/vpcIf.json?subscription=yes'
    # dom_subscr_url = url + 'class/fvRsDomAtt.json?subscription=yes'
    # fvAEPg_url = url + 'class/fvAEPg.json?subscription=yes'

    lnode_subscr_url = url + 'class/fabricLooseNode.json?subscription=yes'
    rvRsPath_url = url + 'class/fvRsPathAtt.json?subscription=yes'
    tagInst_url = url + 'class/tagInst.json?subscription=yes'

    # url_subscr = {rvRsPath_url, lnode_subscr_url, dom_subscr_url, fvAEPg_url, tagInst_url}
    url_subscr = {rvRsPath_url, lnode_subscr_url, tagInst_url}

    for u in url_subscr:

        sub_info = json_get(u, auth_token)

        sub_ids.append(str(sub_info['subscriptionId']))

    return sub_ids


# Refresh subscriptions
def refresh_subscription(apic_ip, ids,auth_token):

    for i in ids:

        url = 'https://' + apic_ip + '/api/subscriptionRefresh.json?id=' + i

        # print(url)

        json_get(url, auth_token)


