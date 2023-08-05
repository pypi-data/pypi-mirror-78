import requests
import json
import pandas as pd
import numpy as np

class B2L:
    def __init__(self, token, mode = 0):
        self.token = token
        if mode == 1:
            self.base_path = 'http://host.docker.internal'
        elif mode == 2:
            self.base_path = 'http://localhost'
        else:
            self.base_path = 'https://brain2logic.com'

    def sourceList(self):
        headers = {'Authorization': 'Token ' + self.token}
        response = requests.get(self.base_path + '/source/', headers=headers)
        return response.json()
    
    def getSource(self, id):
        headers = {'Authorization': 'Token ' + self.token}
        response = requests.get(self.base_path + '/source/' + str(id) + '/', headers=headers)
        return response.json()

    def uploadSource(self, data, name, columns=None):
        if isinstance(data, pd.DataFrame):
            columns = (data.columns).tolist()
            data = (data.values).tolist()
        elif isinstance(data, np.ndarray):
            data = data.tolist()

        headers = {'Authorization': 'Token ' + self.token}
        response = requests.post(self.base_path + '/source/0/', {'data': json.dumps(data), 'columns': json.dumps(columns) if columns is not None else None, 'name': name}, headers=headers)
        return response.json()

    def updateSource(self, id, data, name, columns=None):
        if isinstance(data, pd.DataFrame):
            columns = (data.columns).tolist()
            data = (data.values).tolist()
        elif isinstance(data, np.ndarray):
            data = data.tolist()

        headers = {'Authorization': 'Token ' + self.token}
        response = requests.put(self.base_path + '/source/' + str(id) + '/', {'data': json.dumps(data), 'columns': json.dumps(columns) if columns is not None else None, 'name': name}, headers=headers)
        return response.json()

    def deleteSource(self, id):
        headers = {'Authorization': 'Token ' + self.token}
        response = requests.delete(self.base_path + '/source/' + str(id) + '/', headers=headers)
        return response.json()

    def getAnaplanData(self, workspaceID, modelID, exportName):
        headers = {'Authorization': 'Token ' + self.token}
        response = requests.post(self.base_path + '/anaplan/preview', {'workspaceID': workspaceID, 'modelID': modelID, 'exportName': exportName}, headers=headers)
        return response.json()

    def storyList(self):
        headers = {'Authorization': 'Token ' + self.token}
        response = requests.get(self.base_path + '/story/', headers=headers)
        return response.json()

    def getStory(self, id):
        headers = {'Authorization': 'Token ' + self.token}
        response = requests.get(self.base_path + '/story/' + str(id) + '/', headers=headers)
        return response.json()
    
    def getForecastImput(self):
        with open('forecast_input.json') as json_file:
            return json.load(json_file)

    def putForecastResult(self, df):
        data = {'columns': (df.columns).tolist(), 'values': (df.values).tolist()}
        with open('forecast_result.json', 'w') as outfile:
            json.dump(data, outfile)