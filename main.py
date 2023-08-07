import requests
import datetime
import pandas as pd
import json
import time
from retry import retry
from loguru import logger


datetime_at_start = datetime.datetime.now().strftime("%Y-%m-%d %H%M")


def set_up_session():
    session = requests.Session()
    session.headers.update({
        'x-api-key': 'sh428739766321522266746152871799'})
    return session


def make_post_request(session, url, payload):
    r = session.post(url, payload)
    return r.json()


def make_post_payload(outbound_origin, outbound_dest, outbound_year, outbound_mo, outbound_day,
                      inbound_origin, inbound_dest, inbound_year, inbound_mo, inbound_day,
                      adults):
    post_payload = ({
        "query": {
            "market": "UK",
            "locale": "en-GB",
            "currency": "GBP",
            "queryLegs": [
                {
                    "originPlaceId": {
                        "iata": outbound_origin
                    },
                    "destinationPlaceId": {
                        "iata": outbound_dest
                    },
                    "date": {
                        "year": outbound_year,
                        "month": outbound_mo,
                        "day": outbound_day
                    }
                },
                {
                    "originPlaceId": {
                        "iata": inbound_origin
                    },
                    "destinationPlaceId": {
                        "iata": inbound_dest
                    },
                    "date": {
                        "year": inbound_year,
                        "month": inbound_mo,
                        "day": inbound_day
                    }
                }
            ],
            "cabinClass": "CABIN_CLASS_ECONOMY",
            "adults": str(adults),
            "includedCarriersIds": [],
            "excludedCarriersIds": [],
            "includedAgentsIds": [],
            "excludedAgentsIds": []
        }
    })
    return json.dumps(post_payload)


create_url = "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create"
poll_url = "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/poll/"

# session = set_up_session()
# payload = make_post_payload("LHR", "ATQ",
#                             "2023", "10", "24",
#                             "ATQ", "LHR", "2023", "11", "7")
#
# response = make_post_request(session, create_url, payload)
#
# session_token = response['sessionToken']
#
# url_session_token = poll_url + session_token
# r = session.post(url_session_token).json()

# _normalized = pd.json_normalize(final_content_results, max_level=2)

# data = d['hits']['hits']
# dict_flattened = (flatten(record, '.') for record in data)
# df = pd.DataFrame(dict_flattened)


# content = response['content']['results']['itineraries']

# unpacked = pd.json_normalize(response['content']['results'])

# dic_flattened = [flatten(d) for d in final_content_results]
# df = pd.DataFrame(flatten(final_content_results))

MAX_DURATION = 1200  # minutes
MAX_STOPS = 1  # per leg


# itineraries = r['content']['results']['itineraries']
# min_price = int(itineraries[list(itineraries)[0]]["pricingOptions"][0]["price"]["amount"])
# chosen_key = list(itineraries)[0]
# chosen_durations = []
# chosen_stops = []
# for key in list(itineraries):
#     price = int(itineraries[key]["pricingOptions"][0]["price"]["amount"])
#     # print(price)
#     if price < min_price:
#         legs = itineraries[key]['legIds']
#         durations = []
#         stops = []
#         for leg in legs:
#             durations.append(r['content']['results']['legs'][leg]['durationInMinutes'])
#             stops.append(r['content']['results']['legs'][leg]['stopCount'])
#         if max(durations) > MAX_DURATION or max(stops) > MAX_STOPS:
#             continue
#         min_price = price
#         chosen_key = key
#         chosen_durations = durations
#         chosen_stops = stops
#
# print(min_price)


# itineraries = r['content']['results']['itineraries']
# legs = r['content']['results']['legs']
# carriers = r['content']['results']['carriers']
# agents = r['content']['results']['agents']
# price = []
# duration_there = []
# duration_back = []
# stops_there = []
# n_stops_there = []
# stops_back = []
# n_stops_back = []
# airline_there = []
# airline_back = []
# agency = []
# for key in list(itineraries):
#     price.append(int(itineraries[key]["pricingOptions"][0]["price"]["amount"]))
#     there, back = itineraries[key]['legIds']
#     duration_there.append(legs[there]['durationInMinutes'])
#     duration_back.append(legs[back]['durationInMinutes'])
#     # stops_there.append(legs[there][''])
#     n_stops_there.append(legs[there]['stopCount'])
#     # stops_back.append(legs[back][''])
#     n_stops_back.append(legs[back]['stopCount'])
#     airlineID1 = legs[there]['operatingCarrierIds'][0]
#     airlineID2 = legs[there]['operatingCarrierIds'][-1]
#     airline_there.append(carriers[airlineID1]['name'])
#     airline_back.append(carriers[airlineID2]['name'])
#     agentID = itineraries[key]["pricingOptions"][0]['agentIds'][0]
#     agency.append(agents[agentID])

# df = pd.DataFrame({price,
#                     duration_there,
#                     duration_back,
#                     stops_there,
#                     n_stops_there,
#                     stops_back,
#                     n_stops_back,
#                     airline_there,
#                     airline_back,
#                     agency})


# def make_df(r):
#     itineraries = r['content']['results']['itineraries']
#     legs = r['content']['results']['legs']
#     carriers = r['content']['results']['carriers']
#     agents = r['content']['results']['agents']
#     price = []
#     duration_there = []
#     duration_back = []
#     stops_there = []
#     n_stops_there = []
#     stops_back = []
#     n_stops_back = []
#     airline_there = []
#     airline_back = []
#     agency = []
#     for key in list(itineraries):
#         price.append(int(itineraries[key]["pricingOptions"][0]["price"]["amount"]))
#         there, back = itineraries[key]['legIds']
#         duration_there.append(legs[there]['durationInMinutes'])
#         duration_back.append(legs[back]['durationInMinutes'])
#         # stops_there.append(legs[there][''])
#         n_stops_there.append(legs[there]['stopCount'])
#         # stops_back.append(legs[back][''])
#         n_stops_back.append(legs[back]['stopCount'])
#         airlineID1 = legs[there]['operatingCarrierIds'][0]
#         airlineID2 = legs[there]['operatingCarrierIds'][-1]
#         airline_there.append(carriers[airlineID1]['name'])
#         airline_back.append(carriers[airlineID2]['name'])
#         agentID = itineraries[key]["pricingOptions"][0]['agentIds'][0]
#         agency.append(agents[agentID])
#     df =


@retry(KeyError, tries=10, delay=5, backoff=2)
def get_session_token(session, payload):
    logger.info("get session token")
    response = make_post_request(session, create_url, payload)
    session_token = response['sessionToken']
    return session_token


@retry(KeyError, tries=10, delay=5, backoff=2)
def get_results(session, url_session_token):
    logger.info("get results")
    r = session.post(url_session_token).json()
    results = r['content']['results']
    return results


datetime_of_scrape = []
start_date = []
end_date = []
length_of_stay = []
itinerary = []
price = []
duration_there = []
duration_back = []
stops_there = []
n_stops_there = []
stops_back = []
n_stops_back = []
origin_airport = []
destination_airport = []
airline_there = []
airline_back = []
agency = []

earliest_start = "2023-09-01"
latest_start = "2024-05-01"

days_lb = 10
days_ub = 16

n_adults = 5

origins = ["LHR", "LGW"]
destinations = ["ATQ", "DEL"]

airport_combos = []
for o in origins:
    for d in destinations:
        airport_combos.append((o, d))

session = set_up_session()
date_range = pd.date_range(start=earliest_start, end=latest_start)
i = 1
requests = len(date_range) * (days_ub - days_lb) * len(airport_combos)
for start in date_range:
    for days in range(days_lb, days_ub):
        end = start + datetime.timedelta(days=days)
        for origin, destination in airport_combos:
            logger.info(f"request {i}/{requests}\tstart: {str(start)}\tend: {str(end)}\t{origin} to {destination}")
            payload = make_post_payload(origin, destination, start.year, start.month, start.day,
                                        destination, origin, end.year, end.month, end.day,
                                        adults=n_adults)
            session_token = get_session_token(session, payload)
            url_session_token = poll_url + session_token
            results = get_results(session, url_session_token)
            for key in list(results["itineraries"]):
                datetime_of_scrape.append(datetime_at_start)
                start_date.append(start)
                end_date.append(end)
                length_of_stay.append(days)
                itinerary.append(key)
                price.append(int(results["itineraries"][key]["pricingOptions"][0]["price"]["amount"]) / (1000 * n_adults))
                there, back = results["itineraries"][key]['legIds']
                duration_there.append(results["legs"][there]['durationInMinutes'] / 60)
                duration_back.append(results["legs"][back]['durationInMinutes'] / 60)
                # stops_there.append(legs[there][''])
                n_stops_there.append(results["legs"][there]['stopCount'])
                # stops_back.append(legs[back][''])
                n_stops_back.append(results["legs"][back]['stopCount'])
                origin_airport.append(origin)
                destination_airport.append(destination)
                airlineID1 = results["legs"][there]['operatingCarrierIds'][0]
                airlineID2 = results["legs"][there]['operatingCarrierIds'][-1]
                airline_there.append(results["carriers"][airlineID1]['name'])
                airline_back.append(results["carriers"][airlineID2]['name'])
                agentID = results["itineraries"][key]["pricingOptions"][0]['agentIds'][0]
                agency.append(results["agents"][agentID]["name"])
            i += 1

df = pd.DataFrame({"datetime_of_scrape": datetime_of_scrape,
                   "start_date": start_date,
                   "end_date": end_date,
                   "length_of_stay": length_of_stay,
                   "itinerary": itinerary,
                   "price": price,
                   "duration_there": duration_there,
                   "duration_back": duration_back,
                   "total_duration": [sum(x) for x in zip(duration_there, duration_back)],
                   "n_stops_there": n_stops_there,
                   "n_stops_back": n_stops_back,
                   "total_stops": [sum(x) for x in zip(n_stops_there, n_stops_back)],
                   "origin_airport": origin_airport,
                   "destination_airport": destination_airport,
                   "airline_there": airline_there,
                   "airline_back": airline_back,
                   "agency": agency})


df_processed = df.loc[df.groupby(["start_date",
                                  "end_date",
                                  "length_of_stay",
                                  "n_stops_there",
                                  "n_stops_back",
                                  "duration_there",
                                  "duration_back"]).price.idxmin()]


logger.info("writing to disk")
df.to_csv("data.csv")
df_processed.to_csv(f"{datetime_at_start}_flight_prices.csv")
