import os.path
from os import path

import json
import time
import requests
from requests.exceptions import HTTPError
import pandas as pd

import aimlflow.utils as utils

# Swami
#BASE_URL = 'https://xh6svzuqii.execute-api.us-east-1.amazonaws.com/Navigator'
# Dev
BASE_URL = 'https://ygermtztdb.execute-api.us-east-1.amazonaws.com/Navigator'


class AiService:
    _access_token = None
    _id_token = None
    _service_name = None
    _service_id = None
    _data_source_id = None
    _fe_id = None
    _train_id = None
    _dep_id = None
    _username = None
    _password = None


    def __init__(self):
        pass


    def _construct_header(self):
        if not self._id_token:
            return None

        header = {
            'Authorization': 'Bearer ' + self._id_token
        }
        return header


    def _check_authentication(self):
        if not self._id_token:
            print('Not Authenticated! To use APIs, first authenticate using aiservice.auth()')
            return False
        return True


    def get_user_info(self):
        url = BASE_URL + '/get-user-info'
        try:
            params = {'AccessToken':  self._access_token}
            response = requests.get(url, params=params)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            print(f'User Info fetch failed!')  # Python 3.6
        except Exception as e:
            print('Unable to get user info!')
        return None


    def auth(self, username, password):
        result = False
        try:
            url = BASE_URL + '/get-token'
            params = {'username': username, 'password': password}
            response = requests.post(url, json=params)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()

            try:
                response_json = response.json()
            except Exception as e:
                print('User Authentication failed!')
                return False

            self._id_token = response_json['AuthenticationResult']['IdToken']
            self._access_token = response_json['AuthenticationResult']['AccessToken']

            if utils.check_email(username):
                response = self.get_user_info()
                if not response:
                    utils.color_print('Unable to get user information for authentication!' \
                        'Please contact support@pyxeda.ai for assistance.', 'RED')
                    return False
                self._username = response['Username']
            else:
                self._username = username
            self._password = password
            utils.color_print('Successful Authenication!', 'GREEN')
            result = True

        except HTTPError as http_err:
            utils.color_print(f'User Authentication failed!', 'RED')  # Python 3.6
        except Exception as e:
            print('unable to authenticate the user! Error: ', str(e))
        return result


    def createService(self, name):
        is_auth = self._check_authentication()
        if not is_auth:
            return False

        response = False
        try:
            url = BASE_URL + '/aiservice'
            params = {'name': name}
            response = requests.post(url, headers=self._construct_header(), json=params)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()

            try:
                response_json = response.json()
            except Exception as e:
                utils.color_print('AI Service creation failed!. Service already exists with the same name', 'RED')
                return None

            # print('Json: ', response_json)
            #TODO: Check for success
            self._service_name = name
            self._service_id = response_json['ser_id']
            return self._service_id
        except HTTPError as http_err:
            print('AI Service Creation failed!')
        except Exception as e:
            print('Unable to create an AI Service! Error: ', str(e))
        return None


    def getService(self, name):
        is_auth = self._check_authentication()
        if not is_auth:
            return None

        response = False
        try:
            url = BASE_URL + '/aiservice'
            params = {'name': name}
            response = requests.get(url, headers=self._construct_header(), params=params)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
            try:
                response_json = response.json()
            except Exception as e:
                print('Service with the name was not present!')
                return None

            self._service_name = name
            ids = list(response_json.keys())
            self._service_id = ids[0]
            return self._service_id
        except HTTPError as http_err:
            print('AI Service get failed!')
        except Exception as e:
            print('Unable to get the AI Service!')
        return None

    def _split_big_url(self, upload_url):
        print(upload_url)
        url, rest = str.split(upload_url, '?', 1)
        print(url, rest)
        params = str.split(rest, '&')
        all_params = {}
        for param in params:
            key, value = str.split(param, '=')
            all_params[key] = value
        return url, all_params


    def _importData(self, params):
        response = None
        try:
            url = BASE_URL + '/aiservice/datasets'
            response = requests.post(url, headers=self._construct_header(), json=params)
            response.raise_for_status()

            response_json = response.json()
            if 'result' in response_json and response_json['result'] == 'success':
                self._data_source_id = response_json['data_id']
                utils.color_print('Successfully Uploaded dataset!', 'GREEN')
                response = response_json
        except Exception as e:
            utils.color_print('Unable to upload dataset! Error: '.format(str(e)), 'RED')
            response = None
        return response

    def uploadData(self, params=None):
        is_auth = self._check_authentication()
        if not is_auth:
            return None

        response = None
        try:
            file_name = None
            if params:
                if 'fileName' in params:
                    file_name = params['fileName']
                if 'cloud' in params:
                    cloud = params['cloud']
                    if cloud != 'AWS':
                        utils.color_print('{} is not yet supported!'.format(cloud), 'RED')
                        return None
                else:
                    cloud = 'AWS'
                if cloud == 'AWS':
                    url = BASE_URL + '/storage/s3/uploadLink'
                if not 'raw_data' in params and 'localFile' in params and not params['localFile']:
                    print('raw_data or params[\"localFile\"] is required to uploadData')
                    return None

            # TODO: handle linked accounts
            upload_params = {
                'bucket': self._username,
                'key': params['fileName'],
                'method': 'PUT',
                'contentType': 'text/csv',
            }
            response = requests.post(url, headers=self._construct_header(), params=upload_params)
            response.raise_for_status()

            response_json = response.json()
            upload_url = response_json['url']

            headers = {'Content-Type': 'text/csv'}
            if 'rawData' in params and params['rawData']:
                fileobj = params['rawData']
            else:
                fileobj = open(params['localFile'], 'rb')

            # Upload the file to the cloud location
            response = requests.put(upload_url, headers=headers, data=fileobj)
            response.raise_for_status()

            # Import the data and get a data id
            import_params = {
                'serviceName': self._service_name,
                'location': {'bucket': self._username, 'key': params['fileName']},
                'dataType': 'csv',
                'cloud': 'AWS',
                'source': 's3',
            }
            response = self._importData(import_params)
            if not response:
                utils.color_print('Unable to import the uploaded dataset!', 'RED')
                return None

        except Exception as e:
            print('Unable to upload data! Error: ', str(e))
        return response


    def uploadLocalData(self, params):
        if not 'localFile' in params or not params['localFile']:
            utils.color_print('Need the complete path of the file in params[\"localFile\"]!', 'RED')
            return None
        if not path.exists(params['localFile']):
            utils.color_print('LocalFile {} does not exist!'.format(params['localFile']), 'RED')
            return None
        # check to see if you have a local file params and its a valid file
        return self.uploadData(params)

    def uploadRawData(self, params):
        if not 'rawData' in params or not params['rawData']:
            utils.color_print('Need the raw data in bytes in params[\"rawData\"]!', 'RED')
            return None
        if not isinstance(params['rawData'], bytes):
            utils.color_print('Raw data of the file should be in bytes!')
            return None
        return self.uploadData(params)


    def uploadJSONData(self, params):
        if not 'jsonData' in params or not params['jsonData']:
            utils.color_print('Need the data as a json string in params[\"jsonData\"]!', 'RED')
            return None
        try:
            tmp_json = json.loads(params['jsonData'])
            del tmp_json
        except Exception as e:
            utils.color_print('Need the data to be a valid json string in params[\"jsonData\"]!', 'RED')
        try:
            read_file = pd.read_json(params['jsonData'])
            csv_string = read_file.to_csv(index=False)
            csv_bytes = csv_string.encode()
            del params['jsonData']
            params['rawData'] = csv_bytes
            return self.uploadRawData(params)
        except Exception as e:
            utils.color_print('Unable to upload jsonData!', 'RED')
            return None

    #TODO: Add a parameter to decide on the wait time
    def getFEStatus(self, fe_id=None, blocking=False, wait_time=None):
        is_auth = self._check_authentication()
        if not is_auth:
            return None

        response = None
        if not fe_id:
            #get the latest FE id
            fe_id = self._fe_id
        # Check again to see if the fe id has been set
        if not fe_id:
            return response
        if not wait_time:
            # Wait 30 seconds between status checks
            wait_time = 30
        url = BASE_URL + '/aiservice/feature-engineering'
        params = {
            'reportId': fe_id
        }
        while True:
            try:
                response = requests.get(url, headers=self._construct_header(), params=params)
                # check the response
                response_json = response.json()
                # print(response_json)
                status = response_json[fe_id]['status']
                # print('Status: ', status)
                if status in ['ready', 'failed']:
                    if status == 'ready':
                        utils.color_print('FE successfully completed!', 'GREEN')
                    else:
                        utils.color_print('FE failed!', 'RED')
                    return utils.expand_all_response(response_json[fe_id])
                if not blocking:
                    utils.color_print('FE in progress...', 'BLACK')
                    response = utils.expand_all_response(response_json[fe_id])
                    break
                time.sleep(wait_time)
            except Exception as e:
                print('Unable to get the FE status for {} Error: {}'.format(fe_id, str(e)))
                response = None
                break
        return response


    def launchFE(self, params):
        is_auth = self._check_authentication()
        if not is_auth:
            return None

        response = None
        column = None
        wait_time=None
        # serviceId, dataSourceId, column, problemType, data_type
        try:
            url = BASE_URL + '/aiservice/feature-engineering'
            if 'column' in params and params['column']:
                column = params['column']
            if 'dataSourceId' in params and params['dataSourceId']:
                data_source_id = params['dataSourceId']
            else:
                data_source_id = self._data_source_id
            if 'waitTime' in params and params['waitTime'] and isinstance(params['waitTime'], int):
                wait_time = params['waitTime']
            if not column:
                print('Unable to run FE! Column (params[\"column\"] was not provided!')
                return response
            if not data_source_id:
                print('Unable to run FE! Datasource (param[\"dataSourceId\"] was not provided!')
                return response

            params = {
                'serviceId': self._service_id,
                'dataSourceId': data_source_id,
                'problemType': 'auto',
                'data_type': 'csv',
                'column': column
            }
            response = requests.post(url, headers=self._construct_header(), json=params)
            response.raise_for_status()

            # print('URL response 1: ', response.json())
            response_json = response.json()

            #todo Check the status of FE operation
            fe_ids = list(response_json.keys())
            self._fe_id = fe_ids[0]
            time.sleep(2)
            response = self.getFEStatus(self._fe_id, blocking=True, wait_time=wait_time)
        except Exception as e:
            print('Unable to launch FE! Error: ', str(e))
        return response


    def getDeploymentStatus(self, dep_id=None, blocking=False, wait_time=None):
        is_auth = self._check_authentication()
        if not is_auth:
            return None

        response = None
        if not dep_id:
            #get the latest FE id
            dep_id = self._dep_id
        # Check again to see if the fe id has been set
        if not dep_id:
            return response
        if not wait_time:
            wait_time = 30

        url = BASE_URL + '/deployment'
        params = {
            'deploymentId': dep_id
        }
        while True:
            try:
                response = requests.get(url, headers=self._construct_header(), params=params)
                # check the response
                response.raise_for_status()

                response_json = response.json()
                # print(response_json)
                status = response_json[dep_id]['status']
                # print('Status: ', status)
                if status in ['Completed', 'ready', 'Failed']:
                    return response_json[dep_id]
                if not blocking:
                    response = response_json[dep_id]
                    break
                time.sleep(wait_time)
            except Exception as e:
                print('Unable to get the Deployment status for {} Error: {}'.format(dep_id, str(e)))
                response = None
                break
        return response



    def getTrainingStatus(self, train_id, blocking=False, wait_time=None):
        is_auth = self._check_authentication()
        if not is_auth:
            return None

        response = None
        if not train_id:
            train_id = self._train_id
        if not train_id:
            return response
        if not wait_time:
            wait_time = 30

        try:
            url = BASE_URL + '/trainexperiment'
            params = {
                'experimentId': train_id,
                'serviceId': self._service_id
            }
            while True:
                response = requests.get(url, headers=self._construct_header(), params=params)
                # print(response)
                response_json = response.json()
                # print(response_json)
                status = response_json[train_id]['status']
                if status in ['Completed', 'Failed']:
                    if status == 'Failed':
                        utils.color_print('Training job failed!', 'RED')
                        return utils.expand_all_response(response_json[train_id])
                    else:
                        if response_json[train_id]['launch_mode'] == 'automatic':
                            # Deployment id is not populated immediately so sleep and try it again
                            dep_id = response_json[train_id]['dep_id']
                            if not dep_id:
                                time.sleep(60)
                                response = requests.get(url, headers=self._construct_header(), params=params)
                                response_json = response.json()
                            # find the status of the deployment
                            dep_id = response_json[train_id]['dep_id']
                            dep_response = self.getDeploymentStatus(dep_id, blocking=True, wait_time=wait_time)
                            # print('Deployment response: ', dep_response)
                            if dep_response and dep_response['status'] in ['Completed', 'ready']:
                                utils.color_print('Training successfully completed!', 'GREEN')

                            return utils.expand_all_response(response_json[train_id])
                        else:
                            utils.color_print('Training job successfully completed', 'GREEN')
                            return utils.expand_all_response(response_json[train_id])
                time.sleep(wait_time)
                if not blocking:
                    utils.color_print('Training in progress...', 'BLACK')
                    response = response_json
                    break
        except Exception as e:
            print('Unable to get the training status for {} Error: {}'.format(train_id, str(e)))
        return response



    def launchTrain(self, params):
        is_auth = self._check_authentication()
        if not is_auth:
            return None

        response = None
        # serviceId, dataSourceId, column, problemType, data_type
        try:
            column = None
            url = BASE_URL + '/train'
            if 'fe_id' in params and params['fe_id']:
                fe_id = params['fe_id']
            else:
                fe_id = self._fe_id
            if 'launchMode' in params:
                launch_mode = params['launchMode']
            else:
                launch_mode = 'automatic'
            if 'engine' in params:
                engine = params['engine']
            else:
                engine = 'aws-sklearn-serverless'
            if engine not in ['aws-sklearn-serverless', 'aws-sagemaker']:
                print('Please provide a valid ML (aws-sklearn-serverless/aws-sagemaker) engine!')
                return None
            if 'waitTime' in params and params['waitTime'] and isinstance(params['waitTime'], int):
                wait_time = params['waitTime']

            if not fe_id:
                print('Unable to Train! Feature engineering id (params[\"fe_id\"]) was not provided!')
                return response

            params = {
                'serviceId': self._service_id,
                'reportId': fe_id,
                'launchMode': launch_mode,
                'mode': engine
            }
            response = requests.post(url, headers=self._construct_header(), json=params)
            # print('URL response: ', response.json())
            response_json = response.json()

            #todo Check the status of FE operation
            train_id = response_json['exp_id']
            self._train_id = train_id
            time.sleep(2)
            response = self.getTrainingStatus(train_id, blocking=True, wait_time=wait_time)
            # print(response)

        except Exception as e:
            print('Unable to launch Train! Error: ', str(e))
        return response


    def getServiceDetails(self, service_name=None):
        is_auth = self._check_authentication()
        if not is_auth:
            return None

        if not service_name:
            service_name = self._service_name
        if not service_name:
            return None
        try:
            url = BASE_URL + '/aiservice'
            params = {'name': service_name}
            response = requests.get(url, headers=self._construct_header(), params=params)
            response.raise_for_status()

            # print('Response: ', response)
            response_json = response.json()
            # print('Json: ', response_json)
            ids = list(response_json.keys())
            service_id = ids[0]
            return response_json[service_id]
        except Exception as e:
            print('Unable to fetch the service details! Error: ', str(e))
            return None

    def getEndpointURL(self, service_name=None):
        is_auth = self._check_authentication()
        if not is_auth:
            return None

        response = None
        try:
            response = self.getServiceDetails(service_name)
            if not response:
                utils.color_print('Unable to fetch service details! Please check the service name.', 'RED')
            endpoint_url = response['url']
            if not endpoint_url:
                utils.color_print('Endpoint URL is not yet available for this Ai Service!', 'BLACK')
            return endpoint_url
        except Exception as e:
            print('Unable to get the endpoint details! Error:', str(e))
            return None