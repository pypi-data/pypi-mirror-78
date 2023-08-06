
from eurekaClientShare.constant.format import FORMAT
import json

class Instance:
    def __init__(self, info):
        self.__format = FORMAT
        self.__state = "STARTING"
        self.__set(info)

    def __set(self, info):
        self.__format["instance"]["hostName"] = info['HOSTINSTANCE']
        self.__format["instance"]["app"] = info['SERVICENAME']
        self.__format["instance"]["instanceId"] = "{}:{}:{}".format(info['HOSTINSTANCE'], info['SERVICENAME'], info['PORTINSTANCE'])
        self.__format["instance"]["vipAddress"] = "{}{}:{}".format(info['PROTOCOL'], info['HOSTINSTANCE'], info['PORTINSTANCE'])
        self.__format["instance"]["secureVipAddress"] = self.__format["instance"]["vipAddress"]
        self.__format["instance"]["ipAddr"] = self.__format["instance"]["vipAddress"]
        self.__format["instance"]["status"] = self.__state
        self.__format["instance"]["port"] = {"$": info['PORTINSTANCE'], "@enabled": "true"}
        self.__format["instance"]["securePort"] = {"$": info['PORTINSTANCE'], "@enabled": "true"}
        self.__format["instance"]["healthCheckUrl"] = "{}{}:{}/healthcheck".format(info['PROTOCOL'], info['HOSTINSTANCE'], info['PORTINSTANCE'])
        self.__format["instance"]["statusPageUrl"] = "{}{}:{}/status".format(info['PROTOCOL'], info['HOSTINSTANCE'], info['PORTINSTANCE'])
        self.__format["instance"]["homePageUrl"] = "{}{}:{}".format(info['PROTOCOL'], info['HOSTINSTANCE'], info['PORTINSTANCE'])
        self.__format["instance"]["dataCenterInfo"] = {
			"@class": "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo",
			"name": "MyOwn"
		}

    def setState(self, state, info):
        self.__state = state
        self.__set(info)
        return self

    def getStatus(self):
        return self.__state

    def getAppName(self):
        return self.__format["instance"]["app"]

    def getInstanceId(self):
        return self.__format["instance"]["instanceId"]

    def getDict(self):
        return self.__format

    def getString(self):
        return str(self.__format).replace("'", '"')

    def getJson(self):
        result = str(self.__format).replace("'", '"')
        return json.dumps(result)
