import requests
import yaml
import os
import pandas as pd
import numpy as np
import json as json
from askdata.askdata_client import Agent
import uuid
from datetime import datetime

root_dir = os.path.abspath(os.path.dirname(__file__))
# retrieving base url
yaml_path = os.path.join(root_dir, '../askdata/askdata_config/base_url.yaml')
with open(yaml_path, 'r') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    url_list = yaml.load(file, Loader=yaml.FullLoader)


class Entity:
    def __init__(self, Agent):
        self._agentId = Agent._agentId
        self._domain = Agent._domain
        self.username = Agent.username
        self._language = Agent._language
        self._token = Agent._token
        self._env = Agent._env
        self.regex_list = []


        self._headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self._token
        }

        if self._env == 'dev':
            self.base_url_entity = url_list['BASE_URL_MANGER_DEV']
        if self._env == 'qa':
            self.base_url_entity = url_list['BASE_URL_MANGER_QA']
        if self._env == 'prod':
            self.base_url_entity = url_list['BASE_URL_MANGER_PROD']

    def load_entities(self):
        # https://smartmanager.askdata.com/types/GROUPAMA_QA/entity/menu

        # to test
        authentication_url = self.base_url_entity + '/types/' + self._domain + '/entity/menu'
        r = requests.get(url=authentication_url, headers=self._headers, verify=False)
        r.raise_for_status()
        df_entities = pd.DataFrame(r.json())
        return df_entities

    def load_entity_values(self, entity_code):
        #https://smartmanager.askdata.com//data/GROUPAMA_QA/entity/AGENZIA?_page=0&_limit=50&filter=%257B%257D
        # to test
        authentication_url = self.base_url_entity + '//data/' + self._domain + '/entity/' + entity_code
        r = requests.get(url=authentication_url, headers=self._headers, verify=False)
        r.raise_for_status()
        df_values = pd.DataFrame(r.json())
        return df_values

    def save_entity(self):
        pass

    def save_entityvalues(self):
        pass

    def syn_modifier(self,regex):
        #self.regex_list.append()
        pass

    def push_synonyms(self):
        #https://smartmanager.askdata.com/data/GROUPAMA_QA/entity/AGENZIA
        pass
