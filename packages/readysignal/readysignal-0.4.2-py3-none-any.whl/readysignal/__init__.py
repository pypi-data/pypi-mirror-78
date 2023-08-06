import requests
import pandas as pd
import time


def connect_to_readysignal(access_token, signal_id=None, output=False):
    """
    creates connection to correct API URL to list signals, show signal
    details, and return complete signal data
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number, to show signal details
    or output full signal
    :param output: show signal data or not
    :return:
    """
    try:
        # show signal
        if signal_id and output:
            url = f'http://app.readysignal.com/api/signals/{str(signal_id)}/output'
            headers = {'Authorization': 'Bearer ' + str(access_token),
                       'Accept': 'application/json'}

            req = requests.get(url, headers=headers)

            if req.status_code != 200:
                print(
                    'Connection to Ready Signal failed. Check that your access token is up-to-date and signal ID is valid.')
                return

            resp = req.json()
            num_pages = resp['last_page']

            for page in range(2, num_pages + 1):
                next_page = requests.get(f'http://app.readysignal.com/api/signals/{str(signal_id)}/output',
                                         headers=headers,
                                         params={'page': page}).json()
                resp['data'] += next_page['data']
                time.sleep(1)

            return resp['data']

        # list signals
        elif not signal_id:
            url = 'http://app.readysignal.com/api/signals'

        # show signal details
        else:
            url = f'http://app.readysignal.com/api/signals/{str(signal_id)}'

        headers = {'Authorization': 'Bearer ' + str(access_token),
                   'Accept': 'application/json'}
        req = requests.get(url, headers=headers)

        return req.json()
    except Exception as e:
        print('Connection to Ready Signal failed. Error:', e)
        return


def list_signals(access_token):
    """
    lists all the signals associated with the user's access token
    :param access_token: user's unique access token
    :return: json of signals
    """
    conn = connect_to_readysignal(access_token)
    return conn


def get_signal_details(access_token, signal_id):
    """
    shows the details for a specific signal
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: json of signal details
    """
    conn = connect_to_readysignal(access_token, signal_id)
    return conn


def get_signal(access_token, signal_id):
    """
    returns a signal's data in json format
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: json of signal
    """
    conn = connect_to_readysignal(access_token, signal_id, output=True)
    return conn


def get_signal_pandas(access_token, signal_id):
    """
    returns a signal's data as a Pandas DataFrame
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: Pandas DataFrame of signal
    """
    conn = connect_to_readysignal(access_token, signal_id, output=True)
    return pd.DataFrame.from_dict(conn)


def signal_to_csv(access_token, signal_id, file_name):
    """
    returns a signal's data as a Pandas DataFrame
    :param file_name: name of file to write signal output to
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: Pandas DataFrame of signal
    """
    if '.' in file_name and '.csv' not in file_name:
        exit('Please enter a file name in the format: "signal" or "signal.csv"')
    elif '.' not in file_name:
        file_name += '.csv'

    output = get_signal_pandas(access_token, signal_id)
    output.to_csv(file_name, index=False)
