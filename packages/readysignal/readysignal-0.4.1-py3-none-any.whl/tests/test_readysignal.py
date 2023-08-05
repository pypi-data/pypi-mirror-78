from tests.credentials import creds
from readysignal import connect_to_readysignal, list_signals, get_signal_details
from readysignal import get_signal, get_signal_pandas, signal_to_csv
import pandas as pd


def test_connect_to_readysignal():
    """
    tests the API connection to Ready Signal

    :return: API connection or error
    """
    access_token = creds['access_token']
    rs = connect_to_readysignal(access_token)

    assert rs.ok


def test_list_signals():
    """
    tests an API call to get list of all signals a user owns

    :return: list of signal ids, or error
    """
    access_token = creds['access_token']
    signals = list_signals(access_token)

    assert isinstance(signals, dict)
    assert 'data' in signals.keys()

    return signals


def test_get_signal_details():
    access_token = creds['access_token']
    signal_id = creds['signal_id']
    signal_details = get_signal_details(access_token, signal_id)

    assert isinstance(signal_details, dict)
    assert 'data' in signal_details.keys()

    return signal_details


def test_get_signal():
    access_token = creds['access_token']
    signal_id = creds['signal_id']
    signal = get_signal(access_token, signal_id)

    assert isinstance(signal, dict)
    assert 'data' in signal.keys()

    return signal


def test_get_signal_pandas():
    access_token = creds['access_token']
    signal_id = creds['signal_id']
    signal = get_signal_pandas(access_token, signal_id)

    assert isinstance(signal, type(pd.DataFrame()))
    assert 'start' in signal.columns

    return signal


def test_signal_to_csv():
    access_token = creds['access_token']
    signal_id = creds['signal_id']
    file_name = 'test1.csv'
    signal_to_csv(access_token, signal_id, file_name)

    return file_name


test_connect_to_readysignal()
test_list_signals()
test_get_signal_details()
test_get_signal()
print(test_get_signal_pandas())
test_signal_to_csv()
