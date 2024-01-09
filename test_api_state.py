#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ POST /api/v1/states/
    """
    r = requests.post("http://0.0.0.0:5000/api/v1/states/", data=json.dumps({ 'name': "NewState" }), headers={ 'Content-Type': "application/json" })
    print(r.status_code)
    r_j = r.json()
    print(r_j.get('id') is None)
    print(r_j.get('name') == "NewState")

    # Wrong JSON
    r = requests.post("http://0.0.0.0:5000/api/v1/states/", data={ 'name': "NewState" }, headers={ 'Content-Type': "application/x-www-form-urlencoded" })
    print(r.status_code)

    # Test Correct JSON - Missing name
    r = requests.post("http://0.0.0.0:5000/api/v1/states/", data=json.dumps({ 'fake_name': "NewState" }), headers={ 'Content-Type': "application/json" })
    print(r.status_code)

    # Test Update
    r = requests.get("http://0.0.0.0:5000/api/v1/states")
    r_j = r.json()
    state_id = r_j[0].get('id')

    """ PUT /api/v1/states/<state_id>
    """
    r = requests.put("http://0.0.0.0:5000/api/v1/states/{}".format(state_id), data={ 'name': "NewStateName" }, headers={ 'Content-Type': "application/x-www-form-urlencoded" })
    print(r.status_code)
