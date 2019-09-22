
import threading
import json
import ssl
import time
import websocket


from datetime import datetime

from apic.query import build_subscription, refresh_subscription, refresh_apic


ssl._create_default_https_context = ssl._create_unverified_context


# This class is used for refreshing the subscriptions
class worker(threading.Thread):

   def __init__(self, apic_ip, subscript_ids, token):

       threading.Thread.__init__(self)
       self.subids = subscript_ids
       self.token = token

   def run(self):

        refresh_subs(self.subids, self.token)


# This class is used for the getting the subscriptions - websocket
class listener(threading.Thread):

    # def __init__(self, apic_ip, cookie,uname, upwd):
    def __init__(self):

        threading.Thread.__init__(self)
        self.name = "Testing Listener"


    def run(self):

        # print "Starting " + self.name
        try:

            get_subscription()

        except Exception as e:

            print(e)


# Used to refresh the subscriptions - Called by the worker thread
# def refresh_subs(apic_ip, subids, token):
def refresh_subs(subids, token):

    global refreshed_token
    global refreshed

    new_token = ''

    min = 0

    while True:

        time.sleep(45)

        if refreshed_token == '':

            # print("Refreshing Subscriptions with Original Token")
            refresh_subscription(apicip, subids, token)

        else:

            # print("Refreshing Subscriptions with Refreshed_Token")
            refresh_subscription(apicip, subids, refreshed_token)

        if min == 10:

            refreshed = 1

            if new_token == '':

                new_token = refresh_apic(apicip,token)

                min = 0

                # clustermatrix(ucsname,ucspwd,new_token,apicip)

            else:

                new_token = refresh_apic(apicip, refreshed_token)

                min = 0

                # clustermatrix(ucsname, ucspwd, new_token, apicip)

        else:

            min += 1

        refreshed_token = new_token

        # print(refreshed_token)


# Opens up a websocket for subscription events (vpcIf, fabricLooseNode, fvRsDomAtt) This is called by the listener class
# def get_subscription(apic_ip, cookie, uname, upwd):
def get_subscription():

        url = 'wss://' + apicip + '/socket' + token['APIC-Cookie']

        # print('In get_subscription')

        try:

            ws = websocket.WebSocketApp(url,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
            # ws.on_open = on_open
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, ping_interval=70, ping_timeout=10)

        except websocket.WebSocketException as e:
            print ("WebSocketException: Failed to recreate connection to host, please ensure network connection to host: " + url)
            print(e)
        except websocket.WebSocketConnectionClosedException as e:
            print ("WebSocketConnectionClosedException:Failed to recreate connection to host, please ensure network connection to host: " +
                url)
            print(e)

        except websocket.WebSocketTimeoutException as e:
            print ("WebSocketTimeoutException: Failed to recreate connection to host, please ensure network connection to host: " +
                url)
            print(e)

        except Exception as e:
            print ("Exception: Failed to recreate connection to host, please ensure network connection to host: " + url)
            print(e)



def on_message(ws, message):

    # print('++++++ ' + message + ' +++++++')

    result = json.loads(message)

    for i in result['imdata']:

        # Triggered on then Physical Domain or VMM domain is added to
        # an EPG (Important when VMM integration is involved) - This is not used for CSPs currently
        if 'fvRsDomAtt' in i:

            s = 'vmmp-VMware'

            try:

                if str(i['fvRsDomAtt']['attributes']['status']) == 'deleted':

                    if refreshed_token == '':

                        print("Delete Event Detected")

                    else:

                        print("Delete Event Detected")

                elif str(i['fvRsDomAtt']['attributes']['tDn']).find(s) and str(
                        i['fvRsDomAtt']['attributes']['status']) == 'created':

                    if refreshed_token == '':

                        print("Create Event Detected")

                    else:

                        print("Create Event Detected")

            except Exception as e:

                # print(e)

                pass

        # Triggered on static path binding on EPG
        if 'fvRsPathAtt' in i:

            try:

                if str(i['fvRsPathAtt']['attributes']['status']) == 'created':

                    if refreshed_token == '':

                        print("Static Attach Event")

                        print(i)

                    else:

                        print("Static Attach Event")

                        print(i)


                elif str(i['fvRsPathAtt']['attributes']['status']) == 'deleted':

                    if refreshed_token == '':

                        print("Static Delete Event")

                        print(i)

                    else:

                        print("Static Delete Event")

                        print(i)

            except:

                pass


def on_error(ws, error):

    print('######' + error + '######')
    print(error)


def on_close(ws):

    print("### closed ###")


def start(apic_ip, cookie, apic_url):

    global apicip
    global token

    apicip = apic_ip
    token = cookie

    wss_listener = listener()

    wss_listener.start()

    print("Websocket Coming Up")

    # using sleep to make sure that the websocket
    # listener was active before making the subscriptions
    time.sleep(5)

    subscription_ids = (build_subscription(apic_url, cookie))

    # worker to refresh the subscription IDs every 45 seconds (60 default expire)
    subworker = worker(apic_ip, subscription_ids,cookie)

    subworker.start()

    time.sleep(60)


refreshed_token = ''

