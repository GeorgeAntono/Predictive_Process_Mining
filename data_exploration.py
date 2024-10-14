import pm4py

def import_xes(file_path):
    event_log = pm4py.read_xes(file_path)
    start_activities = pm4py.get_start_activities(event_log)
    end_activities = pm4py.get_end_activities(event_log)
    print("Start activities: {}\nEnd activities: {}".format(start_activities, end_activities))
    return event_log



if __name__ == "__main__":

    event_log = import_xes("data/Hospital_log.xes.gz")
    event_log.head(20).to_html('logs.html')