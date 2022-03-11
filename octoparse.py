import os
import requests
import csv

import util



def log_in(base_url, username, password): 	
        """login and get a access token
        
        Arguments:
                base_url {string} -- authrization base url(currently same with api)
                username {[type]} -- your username
                password {[type]} -- your password
        
        Returns:
                json -- token entity include expiration and refresh token info like:
                        {
                                "access_token": "ABCD1234",      # Access permission
                                "token_type": "bearer",		 # Token type
                                "expires_in": 86399,		 # Access Token Expiration time (in seconds)(It is recommended to use the same token repeatedly within this time frame.) 
                                "refresh_token": "refresh_token" # To refresh Access Token
                        }
        """
        print('Get token:')
        content = 'username={0}&password={1}&grant_type=password'.format(username, password)
        token_entity = requests.post(base_url + 'token', data = content).json()

        if 'access_token' in token_entity:
                print(token_entity)
                return token_entity
        else:
                print(token_entity['error_description'])
                os._exit(-2)


def start_task(base_url, token, task_id):
        """Start Running Task
        
        Arguments:
                base_url {string} -- base url of the api
                token {string} -- token string from a valid token entity
                task_id {string} -- task id of a task from our platform
        
        Returns:
                string -- remind message(include error if exists)
        """
        print('StartTask:')
        url = 'api/task/startTask?taskId=' + task_id
        response = util.request_t_post(base_url, url, token)
        print(response['error_Description'])
        return response

def get_tasks_status(base_url, token, task_id_List):
        """This returns status of multiple tasks.
        
        Arguments:
                base_url {string} -- base url of the api
                token {string} -- token string from a valid token entity
                task_id {string list} -- task id(s) of one or more task(s) from our platform
        
        Returns:
                list -- status list of given task(s)
        """
        print('TaskStatus:')
        url = 'api/task/getTaskStatusByIdList'
        content = { "taskIdList": task_id_List }
        response = util.request_t_post(base_url, url, token, content)
        task_status_list = []
        if 'error' in response:
                if response['error'] == 'success':
                        task_status_list = response['data']
                        for ts in task_status_list:
                                print('%s\t%s\t%s'%(ts['taskId'], ts['taskName'], ts['status']))
                else:
                        print(response['error_Description'])
        else:
                print(response)

        return task_status_list

def stop_task(base_url, token, task_id):
        """Stop Running Task
        
        Arguments:
                base_url {string} -- base url of the api
                token {string} -- token string from a valid token entity
                task_id {string} -- task id of a task from our platform

        Returns:
                string -- remind message(include error if exists)
        """
        print('StopTask:')
        url = 'api/task/stopTask?taskId=' + task_id
        response = util.request_t_post(base_url, url, token)
        print(response['error_Description'])
        return response;

def get_data_by_offset(base_url, token, task_id, offset=0, size=10):
        """Get task data by data offset

        To get data, parameters such as offset, size and task ID are all required in the request. 
        Offset should default to 0 (offset=0), and size∈[1,1000] for making the initial request. 
        The offset returned (could be any value greater than 0) should be used for making the next request. 
        For example, if a task has 1000 data rows, using parameter: offset = 0, size = 100 will return 
        the first 100 rows of data and the offset X (X can be any random number greater than or equal to 100). 
        When making the second request, user should use the offset returned from the first request, offset = X, size = 100 
        to get the next 100 rows of data (row 101 to 200) as well as the new offset to use for the request follows.
        
        Arguments:
                base_url {string} -- base url of the api
                token {string} -- token string from a valid token entity
                task_id {string} -- task id of a task from our platform
        
        Keyword Arguments:
                offset {int} -- an offset from last data request, should remains 0 if is the first request (default: {0})
                size {int} -- data row size for the request (default: {10})
        
        Returns:
                json -- task dataList and relevant information:
                         {
                                "data": {
                                "offset": 4,
                                "total": 100000,
                                "restTotal": 99996,
                                "dataList": [
                                {
                                        "state": "Texas",
                                        "city": "Plano"
                                },
                                {
                                        "state": "Texas",
                                        "city": "Houston"
                                },
                                ...
                                ]
                                },
                                "error": "success",
                                "error_Description": "Action Success"
                        }
        """
        print('GetTaskDataByOffset:')
        url = 'api/allData/getDataOfTaskByOffset?taskId=%s&offset=%s&size=%s'%(task_id, offset, size)
        task_data_result = util.request_t_get(base_url, url, token)
        # util.show_task_data(task_data_result)
        return task_data_result

def remove_task_data(base_url, token, task_id):
        """Clear data of a task
        
        Arguments:
                base_url {string} -- base url of the api
                token {string} -- token string from a valid token entity
                task_id {string} -- task id of a task from our platform
        
        Returns:
                string -- remind message(include error if exists)
        """
        print('RemoveTaskData:')
        url = 'api/task/removeDataByTaskId?taskId=' + task_id
        response = util.request_t_post(base_url, url, token)
        print(response['error_Description'])
        return response



# base_url = 'http://advancedapi.octoparse.com/'
base_url = 'http://dataapi.octoparse.com/'
user_name = 'tranceyos3077'
password = 'ZUA6ewu5y'

token_entity = log_in(base_url, user_name, password)
token = token_entity['access_token']

task_id = '7692cb69-8caa-b03f-1d87-c871ac608049'
# start_task(base_url, token, task_id)

# get_tasks_status(base_url, token, task_id)

# stop_task(base_url, token, task_id)


# Get result from Octoparse
result_data_size = get_data_by_offset(base_url, token, task_id)['data']['total']
result_data =  get_data_by_offset(base_url, token, task_id, size=result_data_size)['data']['dataList']
print(result_data)
print(result_data_size)
field_names = ['Page_URL', 'business_address']
csv_merchant_Octo_PATH = './csv_merchant_octo'
Path = './csv_merchant_octo'
file_name = 'NAMES'

# Save result as csv file
with open(Path+'/'+file_name+'.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    writer.writeheader()
    writer.writerows(result_data)

# Delete data in the task
remove_task_data(base_url, token, task_id)


csv_from_zon_processed_PATH='./csv_from_zon_processed'

csv_files_merchant_OCTO = glob.glob(csv_merchant_Octo_PATH + "/*.csv")

for file in csv_files_merchant_OCTO:

    base_file_name = os.path.basename(file)
    print(base_file_name)
    file_name = os.path.splitext(base_file_name)[0]
    file_name = file_name[:-14]
    
    print("Processing & Merging: "+ file_name.title())





