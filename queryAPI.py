import requests
import math
import time
import datetime


def queryAPI(API_TOKEN, URL, PARAMS=''):
    header = {'Authorization': 'token {0}'.format(
        API_TOKEN), 'Accept': 'application/vnd.github.v3+json'}
    max_tries = 3
    next_page = ''
    while True:
        try:
            response = requests.get(
                url=URL, headers=header, params=PARAMS, timeout=10)
            remaining_requests = int(response.headers['x-ratelimit-remaining'])
            reset_time = datetime.datetime.fromtimestamp(
                int(response.headers['x-ratelimit-reset']))
            waiting_time = (reset_time-datetime.datetime.now()).total_seconds()

            if remaining_requests % 10 == 0:
                print("%d requests remaining, reset in %d minutes...user %s" %
                      (remaining_requests, math.ceil(waiting_time/60.0), URL))

            if remaining_requests == 0:
                print("Allowed requests depleted, waiting %d minutes and %d seconds before continuing..." % (
                    math.floor(waiting_time/60.0), waiting_time % 60))
                time.sleep(waiting_time)
                continue

            if response.status_code != 200:
                print("Error, waiting 10 seconds before retrying..." +
                      str(response.status_code))
                time.sleep(10)
                continue
            elif response.status_code == 200:
                try:
                    next_page = str(response.links['next']['url'])
                except:
                    next_page = ''

                response_json = response.json()
                response.close()
                break
        except requests.exceptions.RequestException as e:
            if max_tries > 0:
                max_tries = max_tries - 1
                print("Error traying: " + URL +
                      " waiting 10 seconds before retrying. Remaining tries " + str(max_tries))
            else:
                break
            #raise SystemExit(e)
            time.sleep(10)
            continue
        except Exception:
            print("Other Error, waiting 10 seconds before retrying..." +
                  str(response.status_code))
            time.sleep(10)
            continue
    return response_json, next_page
