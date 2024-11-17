import pm4py
import pandas as pd
import numpy as np
import editdistance
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


def import_xes(file_path, print_info=False):
    event_log = pm4py.read_xes(file_path)
    start_activities = pm4py.get_start_activities(event_log)
    end_activities = pm4py.get_end_activities(event_log)
    if print_info:
        print("Start activities: {}\nEnd activities: {}".format(
            start_activities, end_activities))

    # convert all activity codes to strings
    event_log['Activity code'] = event_log['Activity code'].astype(str)

    return event_log


def prefix_extraction(trace, max_len=None, steps=1):
    if max_len == None:
        max_len = len(trace)
    prefixes = [trace[:i]
                for i in range(1, len(trace) + 1, steps)
                if i <= max_len]
    return prefixes


def get_similarity(running_trace, traces, similarity=True):
    '''
    Calculate edit distances between running trace and all traces in the log.
    Convert to similarity score if similarity=True.
    '''
    # convert running trace to list if it is a series
    if isinstance(running_trace, pd.Series):
        running_trace = running_trace.iloc[0]
    
    # calculate edit distances
    str_edit_dist = []
    for case, activities in traces.items():
        distance = editdistance.eval(running_trace, activities)
        if similarity:
            similarity_score = 1 - distance / \
                max(len(running_trace), len(activities))
            str_edit_dist.append((case, similarity_score))
        else:
            str_edit_dist.append((case, distance))
    return dict(str_edit_dist)


def train_model(X_cols, event_log, similar_traces_list, lf_map):
    # Get last event for each trace in similar_traces_list (training set)
    X_train = event_log.groupby('case:concept:name')[X_cols]\
                       .last().loc[similar_traces_list]

    # Fill missing values and convert to string
    X_train = X_train.fillna('Missing', axis=1)
    for col in X_cols:
        X_train[col] = X_train[col].astype(str)

    # Convert to categorical (use a dictionary of LabelEncoders for each column)
    le_dict = {col: LabelEncoder() for col in X_cols}

    # Fit each encoder on the training data and transform the training data
    for col in X_cols:
        X_train[col] = le_dict[col].fit_transform(X_train[col])

    # Convert X and y to arrays
    X_train = X_train.to_numpy()
    y_train = np.array([lf_map[trace]
                       for trace in similar_traces_list]).astype(int)

    # Train decision tree model
    clf = DecisionTreeClassifier(max_depth=3, random_state=0)
    clf.fit(X_train, y_train)

    return clf, le_dict


def predict_label(X_cols, event_log, running_trace, clf, le_dict):
    # Prepare the test data (running_trace)
    X_test = event_log.groupby('case:concept:name')[X_cols]\
                      .last().loc[running_trace.index]

    # Fill missing values and convert to string
    X_test = X_test.fillna('Missing', axis=1)
    for col in X_cols:
        X_test[col] = X_test[col].astype(str)

    # Use the same label encoders to transform the test data
    for col in X_cols:
        try:
            X_test[col] = le_dict[col].transform(X_test[col])
        except ValueError:  # Raised if there's an unknown category
            # Check if 'Missing' is in the classes; if not, return 1, 0
            if 'Missing' not in le_dict[col].classes_:
                # Get the most common class from the root node of the decision tree
                most_common_class = clf.classes_[np.argmax(clf.tree_.value[0])]
                return most_common_class, 0
            # Transform with 'Missing' value if available
            X_test[col] = le_dict[col].transform(['Missing'])[0]

    # Convert X_test to a numpy array
    X_test = X_test.to_numpy()

    # Predict label for the running trace
    y_pred = int(clf.predict(X_test))
    try:
        y_pred_proba = clf.predict_proba(X_test)[0][y_pred]
    except:
        # if there is only one class in training data, set probability to 1
        y_pred_proba = 1

    return y_pred, y_pred_proba
