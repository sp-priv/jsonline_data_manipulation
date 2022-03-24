# run  pip3 install -r requirements.txt --user
import jsonlines
import datetime
import os


def get_hits_and_visits():
    location = os.path.realpath(os.getcwd())
    file_name_input = input('Please provide file name (PLEASE NOTE: Unzipped file should be placed in '
                            f'"{os.path.realpath(os.path.join(os.getcwd()))}" directory) \n')
    file_path = os.path.join(location, file_name_input)
    hits_json = jsonlines.open(os.path.join(location, 'hits.json'), mode='w')
    visits_json = jsonlines.open(os.path.join(location, 'visits.json'), mode='w')

    with jsonlines.open(file_path) as f_ga:
        for line in f_ga.iter():
            # first iterate through hits withing json line to get information about hits and load it to hits.json
            for j, _ in enumerate(line["hits"]):
                one_hit = {}
                one_hit["hit_number"] = line["hits"][j]["hitNumber"]
                one_hit["hit_type"] = line["hits"][j]["type"]
                # hits_ in milliseconds so divided by 1000 ( visitStartTime in seconds according to GA documentation)
                one_hit["hit_timestamp"] = datetime.datetime.fromtimestamp(
                    int(line["visitStartTime"]) + int(line["hits"][j]["time"]) / 1000).isoformat(' ', 'milliseconds')
                one_hit["page_path"] = line["hits"][j]["page"]["pagePath"]
                one_hit["page_title"] = line["hits"][j]["page"]["pageTitle"]
                one_hit["hostname"] = line["hits"][j]["page"]["hostname"]
                one_hit["visit_id"] = line["visitId"]
                one_hit["full_visitor_id"] = line["fullVisitorId"]
                hits_json.write(one_hit)
            # while iterating through json lines (i.e GA visits) get information about visit and load it to vists.json
            visit = {}
            visit["full_visitor_id"] = line["fullVisitorId"]
            visit["visit_id"] = line["visitId"]
            visit["visit_number"] = line["visitNumber"]
            visit["visit_start_time"] = datetime.datetime.fromtimestamp(int(line["visitStartTime"])).isoformat(
                ' ', 'seconds')
            visit["browser"] = line["device"]["browser"]
            visit["country"] = line["geoNetwork"]["country"]
            visits_json.write(visit)

    hits_json.close()
    print(f'Finished loading hits to {os.path.realpath(os.path.join(os.getcwd()))}/output/hits.json')

    visits_json.close()
    print(f'Finished loading visits to {os.path.realpath(os.path.join(os.getcwd()))}/output/visits.json')


if __name__ == '__main__':
    try:
        get_hits_and_visits()
    except Exception as e:
        print(f'Unable to retrieve hits / visits. Following error has occcured: \n {e}')
