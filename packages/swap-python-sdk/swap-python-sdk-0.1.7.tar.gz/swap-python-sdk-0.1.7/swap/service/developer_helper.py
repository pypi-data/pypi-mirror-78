import os
import warnings
import requests
import json

def check_environment_variables():
    try:
        key_exists = os.path.exists(os.getcwd() + '/auth/service_account_key.json')
    except:
        raise Exception("You need a Google Cloud service account key to use the SWAP sample app, and this should be saved in the 'auth' folder with the name 'service_account_key.json'")

    if "SWAP_API_TOKEN" not in os.environ:
        raise Exception("Your SWAP_API_TOKEN environment hasn't been set, this is required for using a SWAP service")

    if "COGNITE_API_KEY" not in os.environ:
        exception_message = "The environment variable COGNITE_API_KEY needs to be set before using the sample app."
        exception_message += "\n On a Windows system you can do this with the following command:"
        exception_message += "\n    set COGNITE_API_KEY=REPLACE_WITH_YOUR_COGNITE_API_KEY"
        exception_message += "\n On a Unix based system you can do this with the following command:"
        exception_message += "\n    export COGNITE_API_KEY=REPLACE_WITH_YOUR_COGNITE_API_KEY"
        print(exception_message)

def check_latest_version_of_sdk():
    print("Checking you have the latest version of the SDK... ", end = '')
    remote_sdk_info = requests.get("https://pypi.python.org/pypi/swap-python-sdk/json")
    remote_sdk_info_json = json.loads(remote_sdk_info.text)
    remote_sdk_version = remote_sdk_info_json['info']['version']

    from subprocess import call
    f = open("sdk_version.txt", "w+")
    if os.name == 'nt':
        call('pipenv run pip show swap-python-sdk | findstr Version', shell=True, stdout=f)
    else:
        call('pipenv run pip show swap-python-sdk | grep Version', shell=True, stdout=f)
    f.close()
    f = open("sdk_version.txt", "r")
    local_sdk_version = f.read().replace('\n','').replace('Version: ','')
    f.close()

    if remote_sdk_version == local_sdk_version:
        print("Your sdk version is up to date")
    else:
        print("\nIt looks like you are using an older version of the SDK")
        print(f"  Your version: {local_sdk_version}")
        print(f"  Latest pypi version: {remote_sdk_version}")
        print("To update the sdk, please run the following command: ")
        print("pipenv run pip install --upgrade swap-python-sdk")
