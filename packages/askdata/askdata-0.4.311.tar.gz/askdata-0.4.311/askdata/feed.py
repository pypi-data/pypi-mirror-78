import requests
import yaml
import os
import pandas as pd
import numpy as np
import json as json
import uuid
from datetime import datetime
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_LOG_FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] - %(asctime)s --> %(message)s"
g_logger = logging.getLogger()
logging.basicConfig(format=_LOG_FORMAT)
g_logger.setLevel(logging.INFO)

root_dir = os.path.abspath(os.path.dirname(__file__))
# retrieving base url
yaml_path = os.path.join(root_dir, '../askdata/askdata_config/base_url.yaml')
with open(yaml_path, 'r') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    url_list = yaml.load(file, Loader=yaml.FullLoader)



class InsightFeed():
    """this class is used for push a message into feed fo the specific agent
    For select the specific component type to add at the InsightFeed, choose between this values:
     {
            1: table,
            2: comparison,
            3: text,
            4: item,
            5: rank,
            6: cta
        }
    """
    def __init__(self, Agent, stream="main"):
        self.agentId = Agent.agentId
        self.workspaceId = Agent.workspaceId
        self.username = Agent.username
        self.language = Agent.language
        self.token = Agent.token
        self.stream = stream
        self.insight_id = "$" + self.agentId + "$custom$" + str(uuid.uuid1())
        self.id = str(uuid.uuid1())

        #"action": "smartfeed://card/" + self.insight_id, "action_label": "Details",
        self.feed_dict = { "agentId":self.agentId,"language":self.language,"stream":self.stream,"users":[self.username],
            "messages":[{"insightId": self.insight_id, "topics": [],
                        "attachment":{
                            "id": self.agentId + self.id,
                            "body": [],
                            "footer": {"bookmark": {"count": 0, "isBookmarked": False}, "interaction": 0,
                                       "url": "smartfeed://card/" + self.insight_id
                        },
                        "header": {"icon": "https://s3.eu-central-1.amazonaws.com/innaas.smartfeed/icons/bridgestone/Graphite/Main/icon-chart-segmented@2x.png",
                                   "notification": 0, "timestamp": round(datetime.now().timestamp()), "title": "Details"
                        }
                        },
                        "time": round(datetime.now().timestamp())
                        }
                        ]
                    }


    def __str__(self):
        return '{}'.format(self.agentId)

    def add_component(self, df, component_type, var_perc=True):

        def table(df):
            component_table = {"component_type": "table", "details": {"columns": [], "rows": []}}
            component_table["details"]["columns"] = list(df.columns)[:3]
            for i in df.index:
                row = list(df.iloc[i, :3])
                component_table["details"]["rows"].append(row)
            return component_table

        def comparison(df,var_perc=True):
            component_comparison = {"component_type": "comparison", "details": {"item_a": {"label": "", "value": "",
                                                                                           "format": "string",
                                                                                           "unit": "EUR",
                                                                                           "markup": "",
                                                                                           "description": ""},
                                                                                "item_b": {"label": "", "value": "",
                                                                                           "format": "string",
                                                                                           "unit": "EUR","markup": "",
                                                                                           "description": ""}}}
            if(list(df.shape).__len__()) == 1:
                component_comparison["details"]["item_a"]["label"] = list(df.index)[0]
                component_comparison["details"]["item_a"]["value"] = df[0]
                component_comparison["details"]["item_b"]["label"] = list(df.index)[1]
                component_comparison["details"]["item_b"]["value"] = df[1]
                if(var_perc == True):
                    #aggiungere il formato dovunque - terminare
                    component_comparison["details"]["item_a"]["value"] = (df[1]-df[0])/df[0]
                pass
            else:
                pass
            return component_comparison

        def text(text):
            component_text = {"component_type": "text", "details": {"text": str(text)}}
            return component_text
        def item(df):
            pass
        def rank(df):
            pass

        def cta(df):
            component_cta = {"component_type": "cta", "details": {"link": "", "label": ""}}
            if(list(df.shape).__len__()) == 1:
                component_cta["details"]["link"] = df[0]
                component_cta["details"]["label"] = df[1]
            else:
                component_cta["details"]["link"] = df.iloc[0, 0]
                component_cta["details"]["label"] = df.iloc[0, 1]
            return component_cta

        switcher = {
            1: table,
            2: comparison,
            3: text,
            4: item,
            5: rank,
            6: cta
        }
        # Get the function from switcher dictionary
        func = switcher.get(component_type, lambda: "Invalid Component Type")
        # Execute the function
        #body = self.feed_dict["messages"][0]["attachment"]["body"]
        self.feed_dict["messages"][0]["attachment"]["body"].append(func(df))
        return self.feed_dict["messages"][0]["attachment"]["body"]

    def get_components(self):
        print(self.self.feed_dict["messages"][0]["attachment"]["body"])
        return self.feed_dict["messages"][0]["attachment"]["body"]

    def del_component(self,component_number):
        pass

    def refactor_header(self, icon, title, action_flag=False, action_label='', action=''):
        if action_flag == True:
            self.feed_dict["messages"][0]["attachment"]["header"]["action"] = action
            self.feed_dict["messages"][0]["attachment"]["header"]["action_label"] = action_label
        self.feed_dict["messages"][0]["attachment"]["header"]["icon"] = icon
        self.feed_dict["messages"][0]["attachment"]["header"]["title"] = title
    def push_insight(self):
        pass

    # curl - X
    # DELETE \
    #         'https://smartfeed.askdata.com/messages/{{messageId}}' \
    #         - H
    # 'Authorization: Bearer d1dee093-1c6b-4356-8b36-20e949d60850' \
    # - H
    # 'Postman-Token: 562dac10-d8ab-4ec5-b36f-c8a7d2cfd2d0' \
    # - H
    # 'cache-control: no-cache'

class FeedCard():

    def __init__(self, Agent , empty=True):
        self.agentId = Agent.agentId
        self.workspaceId = Agent.workspaceId
        self.username = Agent.username
        self.language = Agent.language
        self.token = Agent.token
        self.env = Agent.env

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer" + " " + self.token
        }

        if self.env == 'dev':
            self.base_url_feedcard = url_list['BASE_URL_FEED_DEV']
        if self.env == 'qa':
            self.base_url_feedcard = url_list['BASE_URL_FEED_QA']
        if self.env == 'prod':
            self.base_url_feedcard = url_list['BASE_URL_FEED_PROD']

    def delete_card(self,messageid):

        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        authentication_url = self.base_url_feedcard + '/messages/' + messageid
        r = s.delete(url=authentication_url, headers=self.headers)
        r.raise_for_status()

        logging.INFO('--------- ---------  --------')
        logging.INFO(f'--- DELETED ---------> messageId: {messageid}')

