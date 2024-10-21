def label_function_1(activities):
    '''
    rule:
    either the diagnostic test for the tumor marker CA-19.9
    or for the tumor marker ca-125 has to be performed.

    case is deviant if rule is violated
    '''
    activity1 = 'ca-19.9 tumormarker'
    activity2 = 'ca-125 mbv meia'
    
    deviant = True
    if activity1 in activities or activity2 in activities:
        deviant = False
    return deviant

def label_function_2(activities):
    '''
    rule:
    every time the diagnostic test for the CEA tumor marker is performed, 
    then the eia test for the squamous cell cancer has also to be performed eventually.

    case is deviant if rule is violated
    '''
    activity1 = 'cea - tumormarker mbv meia'
    activity2 = 'squamous cell carcinoma mbv eia'

    deviant = True
    if activity1 not in activities:
        deviant = False
    else:
        if activity2 in activities:
            if activities.index(activity2) > activities.index(activity1):
                deviant = False
    return deviant

def label_function_3(activities):
    '''
    rule:
    no histological examination can be performed until
    the eia test for the squamous cell cancer is performed

    case is deviant if rule is violated
    '''
    activity1 = 'histologisch onderzoek - biopten nno'
    activity2 = 'squamous cell carcinoma mbv eia'

    deviant = True
    if activity1 in activities:
        if activity2 in activities:
            if activities.index(activity1) > activities.index(activity2):
                deviant = False
    else:
        if activity2 in activities:
            deviant = False

    return deviant


def label_function_4(activities):
    '''
    rule:
    the resection for the histological examination has to be performed eventually

    case is deviant if rule is violated
    '''
    activity1 = 'histologisch onderzoek - grote resectiep'

    deviant = True
    if activity1 in activities:
        deviant = False
    
    return deviant

def get_lf_map(event_log, lf):
    activity_traces = event_log.groupby('case:concept:name')['concept:name'].apply(list)
    lf_map = activity_traces.apply(lf)
    return lf_map

def label_event_log(event_log, lf, column_name='deviant'):
    lf_map = get_lf_map(event_log, lf)
    event_log[column_name] = event_log['case:concept:name'].map(lf_map)
    return event_log