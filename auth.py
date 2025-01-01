from flask import Blueprint, render_template
import time
#import YS_return_departure_data
import requests

auth = Blueprint('auth', __name__)


def refreshResults():
    curr_time = time.strftime("%H:%M", time.localtime())

    middleWebsite = ""
    topWebsite = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="20">
        <meta name="keywords" content="York Street Train Station, York Street, Real Time Train Departures">
        <meta name="description" content="Real Time Train Departures from York Street Train Station">
        <meta name="author" content="Connor Graham">
        <title>York Street Trains</title>
        <!-- <link rel="stylesheet" href="departure_screen_styles.css"> -->
        <style>body{color:#fff;background-color:#000;font-family:Arial,Helvetica,sans-serif;font-size:18pt;margin:0;padding:0}.scrollbar_hide{overflow-y:hidden!important}div.control_panel{align:center;width:100%;margin-bottom:2px;color:#bfbfbf;font-size:10pt}a:link,a:visited{color:#0ff;text-decoration:none}div.control_panel a,div.control_panel a:visited{color:#bfbfbf}div.wrapper_cp{border:1px dotted red}div.wrapper{margin:0;padding:0;width:100%;overflow:hidden}div.heading{min-height:42px;color:#fff;background-color:#002ba4;padding:5px 4px 6px;font-size:28pt;font-weight:400}div.interleave{color:#ff0;background-color:#002ba4;padding:0 4px;font-size:22pt;font-weight:400;width:100%;max-height:101px;overflow:hidden}div.departures{float:left;text-align:left}div.departures span.station{color:#fff}div.last_updated{float:right;text-align:right;font-size:20pt;color:#bfbfbf}div.last_updated_sn{float:right;text-align:right;font-size:20pt;color:#bfbfbf;position:relative;top:5px}div.last_updated span.update_time,div.last_updated_sn span.update_time{color:#fff}div.contents{clear:both;overflow:hidden}div.contents_sn{clear:both;overflow:hidden;height:598px}div.contents_sn_noheader{clear:both;overflow:hidden;height:604px}div.interleave_sn{height:112px;color:#000;font-weight:700;background-color:#bfbfbf;border-top:1px solid #fff;padding:5px 4px}div.interleave_sn_scrollable{height:112px;line-height:28px;font-size:18pt;overflow:hidden}table{font-family:Arial;width:100%;border-collapse:collapse;table-layout:fixed;margin-top:0}tr.header{font-size:26pt;height:40px;margin:0}tr.header_small{font-size:26pt}table th{border-collapse:collapse;color:#fff;background-color:#002ba4;padding:4px;border-bottom:1px solid #fff;text-align:left;font-weight:400;font-size:17pt}th.code{width:70px}th.dest,th.orig{width:140px}th.plat{width:45px}th.incident{width:25px}th.arr{width:120px}th.expa{width:140px}th.dep{width:120px}th.expd{width:140px}table td{text-align:left;padding-top:2px;padding-left:4px;padding-right:4px;font-size:20pt;vertical-align:top}td.no_trains{font-size:34pt;padding:52px}td.dest,td.orig{color:#ff0}td.plat{text-align:center}td.plat span.chg{font-weight:700;color:#000;background-color:#fff;margin:0;padding:0 10px}td.cancelled span{font-weight:700;color:#000;background-color:#fff;margin:0;padding:0 5px}div.comment,td.more_info{font-size:18pt}div.TrainIncident{font-size:11pt!important;font-style:normal;line-height:normal;font-weight:400;font-variant:normal;text-transform:none;color:#ff0}div.overwrite_sn{border-top:1px solid #fff;padding:19px 20px;text-align:center}div.overwrite_sn_pg{border-top:1px solid #fff;text-align:right}div.overwrite_sn_scrollable{border-top:1px solid #fff;padding:19px 20px;height:675px;font-size:30pt;overflow:hidden;text-align:center}div.overwrite_sn_paged{border-top:1px solid #fff;text-align:center;height:638px;overflow:hidden}a,a.control{color:#ff0;text-decoration:none;font-weight:400}a:hover{color:#ff0;text-decoration:underline;font-weight:400}td.CallingAt{font-size:11pt!important;font-style:normal;line-height:normal;font-weight:400;font-variant:normal;text-transform:none;color:#fff}table.hidden{position:relative;background-color:transparent;padding:0;visibility:visible}table.CallingPoints{background-color:#000;color:#00f}thead.HeadingsClass{font-size:18pt;font-style:normal;line-height:normal;font-weight:400;font-variant:normal;text-transform:none;color:#0ff}.TriangleColumn{width:80px}.TriangleColour{color:#ff0;font-size:18pt}.AlignCenter{text-align:center}.WhiteSpace{white-space:pre-line;margin:0}.CallingPatt{display:block;width:33%;float:left}.fa-warning{font-size:25px;text-align:center;color:#ff0}.operatorTypeGW{background-color:#0a493e!important}</style>
    </head>
    <body>
        <div class="wrapper">
            <div class="heading">
                <div class="departures"><span class="station">York Street</span> Arrivals & Departures</div>
                <div class="last_updated"> Last Updated: <span class="update_time">'''
    secondTopWebsite = '''</span></div>
                <div class="interleave" id="special_notice">Customer Support mode</div>
            </div>
            <div class="contents">
                <table>
                    <tbody>
                        <tr class="header_small">
                            <th class="code">Code</th>
                            <th class="orig">From</th>
                            <th class="dest">To</th>
                            <th class="plat">Plat</th>
                            <!-- <th class="plat">Length</th> -->
                            <th class="incident"></th>
                            <th class="arr">Scheduled <br>Arrival</th>
                            <th class="expa">Expected <br>Arrival</th>
                            <th class="dep">Scheduled <br>Departure</th>
                            <th class="expd">Expected <br>Departure</th>
                        </tr>'''

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
        url = f"{base_url}XML_DM_REQUEST?ext_macro=dm&type_dm=any&name_dm={name_dm}&useRealtime=1&excludedMeans=5&limit=5"
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

    departuresData = []
    departures = main(departuresData)
    #print(departuresData)

    for x in range(len(departuresData)):
        middleWebsite = middleWebsite + f'''                    <tr id="{departuresData[x][0]}">
                            <td class="code">B000</td>
                            <td class="orig">{departuresData[x][1]}</td>
                            <td class="dest">{departuresData[x][2]}</td>
                            <!-- <td class="plat"><span class="chg">{departuresData[x][3]}</span></td> -->
                            <td class="plat">{departuresData[x][3]}</td>
                            <td></td>
                            <td class="arr"></td>
                            <!-- <td class="exp cancelled"><span>Cancelled</span></td> -->
                            <td class="exp"><span></span></td>
                            <td class="dep">{departuresData[x][4]}</td>
                            <td class="exp"><span>{departuresData[x][5]}</span></td>
                        </tr>
                        <tr>
                            <td class="indent" id="indent0"></td>
                            <td class="more_info" colspan="7">
                                <!-- <div>
                                    <span class="lr_header">Last report: </span>
                                    <span class="lr_text">No report</span>
                                </div> -->
                            </td>
                        </tr>
                        <tr>
                            <td></td>
                            <td colspan="8"></td>
                        </tr>'''
    bottomWebsite = '''                    <!-- <tr>
                            <td class="no_trains" colspan="9">There is currently no train information available.</td>
                        </tr> -->
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>'''

    return topWebsite+str(curr_time)+secondTopWebsite+middleWebsite+bottomWebsite

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return "<p>Logout</p>"

@auth.route("/ys")
def ys_csm():
    return refreshResults()

