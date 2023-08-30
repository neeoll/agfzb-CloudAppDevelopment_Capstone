import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    print("GET from {}".format(url))
    try:
        if api_key:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except requests.exceptions.RequestException as e:
        print("Network exception occurred:", e)
        return None

    status_code = response.status_code
    print("With status {}".format(status_code))
    
    json_data = None
    if response.content:
        json_data = json.loads(response.content)
    
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        requests.post(url, params=kwargs, json=json_payload)
    except requests.exceptions.RequestException as e:
        print("Network exception occurred:", e)
        return {"error": "Network exception"}



# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result['dealerships']["rows"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(
                address=dealer_doc["address"], 
                city=dealer_doc["city"], 
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"], 
                lat=dealer_doc["lat"], 
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"], 
                state=dealer_doc["state"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        reviews = json_result["reviews"]
        for review in reviews:
            review_obj = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                review=review["review"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment=analyze_text_with_watson_nlu(review["review"]),
                id=review["id"]
            )
            results.append(review_obj)
    return results
            

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_text_with_watson_nlu(text):
    try:
        headers = { "Content-Type": "application/json" }
        data = {
            "text": text,
            "features": { "sentiment": {} }
        }

        response = requests.post(
            "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/b7725bcb-3690-4e71-ad16-52f1fd9f53b6" + "/v1/analyze?version=2019-07-12",
            headers=headers,
            json=data,
            auth=(f"apikey", "w8nZAv0WMpjUbQ7Dx-qXYLgdnikLsNhySiXfck2o3IKP")
        )

        response_json = response.json()
        return response_json['sentiment']['document']['label']

    except requests.exceptions.RequestException as e:
        print("Network exception occurred:", e)
        return {"error": "Network exception"}
