
import subprocess

class Request:
    def __init__(self, url="", headers={}, body={}):
        self.__headers = headers
        self.__body = body
        self.__url = url

    def getUrl(self):
        return self.__url

    def getHeaders(self):
        return self.__headers

    def geyBody(self):
        return self.__body

    def __getHeadersRequest(self):
        result = []
        for key in self.__headers:
            result.append("-H")
            result.append("'{}: {}'".format(key, self.__headers[key]))
        return result

    def __getBodyRequest(self):
        result = "'{}'".format(str(self.__body).replace("'", '"'))
        return result

    def GET(self):
        try:
            curl = ["curl", "-XGET"] + self.__getHeadersRequest() + [self.__url]
            result = subprocess.check_output(' '.join(curl), shell=True, stderr=subprocess.STDOUT)
        except:
            result = None
        return result

    def POST(self):
        try:
            curl = ["curl", "-XPOST", "-d", self.__getBodyRequest()] + self.__getHeadersRequest() + [self.__url]
            result = subprocess.check_output(' '.join(curl), shell=True, stderr=subprocess.STDOUT)
        except:
            result = None
        return result

    def PUT(self):
        try:
            curl = ["curl", "-XPUT", "-d", self.__getBodyRequest()] + self.__getHeadersRequest() + [self.__url]
            result = subprocess.check_output(' '.join(curl), shell=True, stderr=subprocess.STDOUT)
        except:
            result = None
        return result

    def DELETE(self):
        try:
            curl = ["curl", "-XDELETE"] + self.__getHeadersRequest() + [self.__url]
            result = subprocess.check_output(' '.join(curl), shell=True, stderr=subprocess.STDOUT)
        except:
            result = None
        return result
