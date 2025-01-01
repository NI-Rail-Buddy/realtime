import requests

base_url = "http://opendata.translinkniplanner.co.uk/Ext_API/"

def time_sanitation(time_in):
    time_out = time_in[11:16]
    return time_out

def get_station_id(api_station_id):
    check = get_train_departures(api_station_id)
    locations_list = check["locations"]
    for x in locations_list:
       station_id = x["id"]
       return station_id

def get_destination_name(station_id):
    departures_info = get_train_departures(station_id)
    if departures_info:
        locations_list = departures_info["locations"]
        for x in locations_list:
            station_code = x["id"]
            return station_code

def get_train_departures(name_dm):
    url = f"{base_url}XML_DM_REQUEST?ext_macro=dm&type_dm=any&name_dm={name_dm}&useRealtime=1&excludedMeans=5&limit=10"
    response = requests.get(url, headers={"X-API-TOKEN": "6u83f0xduscmvpnp"})

    if response.status_code == 200:
        departures_data = response.json()
        return departures_data
    else:
        print(f"Failed to retrieve data {response.status_code}")

def main(secondList):
    location = "10000015"

    departures_info = get_train_departures(location)

    if departures_info:
        locations_list = departures_info["locations"]
        train_dep_list = departures_info["stopEvents"]
        for x in train_dep_list:
            f_dest_name = get_destination_name(x["transportation"]["destination"]["id"])
            try:
                if x["departureTimeEstimated"] == x["departureTimePlanned"]:
                    status = "On Time"
                else:
                    status = time_sanitation(x["departureTimeEstimated"])

                #print(x["transportation"]["properties"]["trainNumber"], get_station_id(x["transportation"]["origin"]["id"]), f_dest_name, x["location"]["properties"]["platform"], time_sanitation(x["departureTimePlanned"]), status)
                dataList = [x["transportation"]["properties"]["trainNumber"], get_station_id(x["transportation"]["origin"]["id"]), f_dest_name, x["location"]["properties"]["platform"], time_sanitation(x["departureTimePlanned"]), status]
                secondList.append(dataList)
            except:
                #print(x["transportation"]["properties"]["trainNumber"], get_station_id(x["transportation"]["origin"]["id"]), f_dest_name, x["location"]["properties"]["platform"], time_sanitation(x["departureTimePlanned"]), "status")
                dataList = [x["transportation"]["properties"]["trainNumber"], get_station_id(x["transportation"]["origin"]["id"]), f_dest_name, x["location"]["properties"]["platform"], time_sanitation(x["departureTimePlanned"]), "No Report"]
                secondList.append(dataList)

# departuresData = []
# departures = main(departuresData)
# print(departuresData)
