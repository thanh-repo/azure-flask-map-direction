# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 09:02:46 2022.

@author: ThanhOffice
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

import requests
import logging

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, supports_credentials=True)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

logging.basicConfig(handlers=[logging.FileHandler(
    filename='app.log',
    encoding='utf-8', mode='a+')],
    format="%(asctime)s |:| LINE NO.: %(lineno)d: %(message)s",
    datefmt="%F %A %T",
    level=logging.ERROR)

def get_duration(origin, dest):
    """Get driving direction by opensource project-osrm.org.

    Args
    ----------
        origin (array[long, lat]): DESCRIPTION.
        dest (array[long, lat]): DESCRIPTION.

    Returns
    -------
        float: Duration in minutes.

    """
    url = f"http://router.project-osrm.org/route/v1/driving/"\
        f"{origin[0]},{origin[1]};{dest[0]},{dest[1]}?overview=false"
    try:
        result = requests.get(url=url)
        result_json = result.json()
        if result_json["code"] == "Ok":
            routes = result_json["routes"]
            if len(routes) > 0:
                return float(routes[0]["duration"])/60
    except Exception as ex:
        print(ex)
        logging.error(ex)
        logging.error(url)
    return None


def search_lon_lat(address):
    """Get longitude and latitude from address.

    Args
    -------
        address (TYPE): DESCRIPTION.

    Returns
    -------
        TYPE: DESCRIPTION.
        TYPE: DESCRIPTION.

    """
    url = f"https://nominatim.openstreetmap.org/search.php?"\
        f"street={address['street']}&"\
        f"city={address['city']}&"\
        f"county={address['county']}&"\
        f"state={address['state']}&"\
        f"country={address['country']}&"\
        f"postalcode={address['postalcode']}&"\
        f"format=jsonv2"
    try:
        result = requests.get(url=url)
        result_json = result.json()
        if len(result_json) > 0:
            return result_json[0]["lon"], result_json[0]["lat"]
    except Exception as ex:
        print(ex)
        logging.error(ex)
        logging.error(url)
    raise ValueError("Address not found")


def check_para(data, parameters):
    """Check requirement parameter.

    Args:
    -------
        data (TYPE): DESCRIPTION.
        parameters (list): Parameter required.

    Returns
    -------
        para (TYPE): DESCRIPTION.

    """
    for para in parameters:
        if para not in data.keys():
            return para
    return None


@app.route("/service", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def service():
    """Call test services.

    Returns
    -------
        TYPE: DESCRIPTION.

    """
    return jsonify({"service": "Ok"})


@app.route("/getnear", methods=["GET", "POST"])
def getnear():
    """Call test services.

    Returns
    -------
        TYPE: DESCRIPTION.
        EP: Error Parameter
        EL: Error Location
        ED: Error Direction
        EP000: Parameter not found, (parameter)
        EL000: Location not found, (location)
        ED000: Direction to clinic 1, 2 not found
        ED001: Direction to clinic 1 not found
        ED002: Direction to clinic 2 not found

    """
    require = ["clinic1", "clinic2", "client"]
    require_sub = ["street", "city", "county",
                   "state", "postalcode", "country"]
    data = request.get_json()
    para_out = check_para(data, require)
    if para_out is not None:
        return jsonify({"error": f"EP000 '{para_out}'.",
                        "nearest": "",
                        "direction": ""})
    lat_long = data.copy()
    for item in data.keys():
        try:
            para_out = check_para(data[item], require_sub)
            if para_out is not None:
                return jsonify({"service": f"EP000 '{para_out}'",
                                "nearest": "",
                                "direction": ""})
            lat_long_rs = search_lon_lat(data[item])
        except ValueError:
            return jsonify({"service": f"EL000 {item}",
                            "nearest": "",
                            "direction": ""})
        lat_long[item] = [lat_long_rs[0], lat_long_rs[1]]
    duration1 = get_duration(lat_long["client"], lat_long["clinic1"])
    duration2 = get_duration(lat_long["client"], lat_long["clinic2"])
    # AI technology, If else until die :))
    if duration1 is None and duration2 is None:
        return jsonify({"service": "ED000 Clinic 1, 2 not found",
                        "nearest": "",
                        "direction": ""})
    elif duration1 is None and duration2 is not None:
        url_direction = "https://www.google.com/maps/dir/?api=1&"\
            f"origin={lat_long['client'][1]},{lat_long['client'][0]}&"\
            f"destination={lat_long['clinic2'][1]},{lat_long['clinic2'][0]}"
        return jsonify({"service": "ED001 Clinic 1 not found",
                        "nearest": "clinic2",
                        "direction": url_direction})
    elif duration1 is not None and duration2 is None:
        url_direction = "https://www.google.com/maps/dir/?api=1&"\
            f"origin={lat_long['client'][1]},{lat_long['client'][0]}&"\
            f"destination={lat_long['clinic1'][1]},{lat_long['clinic1'][0]}"
        return jsonify({"service": "ED002 Clinic 2 not found",
                        "nearest": "clinic1",
                        "direction": url_direction})
    elif duration1 - duration2 > 30.0:
        url_direction = "https://www.google.com/maps/dir/?api=1&"\
            f"origin={lat_long['client'][1]},{lat_long['client'][0]}&"\
            f"destination={lat_long['clinic2'][1]},{lat_long['clinic2'][0]}"
        return jsonify({"service": "Ok",
                        "nearest": "clinic2",
                        "direction": url_direction})
    else:
        url_direction = "https://www.google.com/maps/dir/?api=1&"\
            f"origin={lat_long['client'][1]},{lat_long['client'][0]}&"\
            f"destination={lat_long['clinic1'][1]},{lat_long['clinic1'][0]}"
        return jsonify({"service": "Ok",
                        "nearest": "clinic1",
                        "direction": url_direction})


if __name__ == '__main__':
   app.run()