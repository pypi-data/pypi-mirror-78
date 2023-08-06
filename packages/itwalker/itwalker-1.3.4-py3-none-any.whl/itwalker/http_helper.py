import requests, urllib.parse, urllib3, json


class HttpHelper:
    def getRemoteToFile(self, file_url):
        http = urllib3.PoolManager()
        r = http.request('GET', file_url)
        if r.status == 200:
            return r.data
        else:
            return None

    def httpGet(self, url, headers, param):
        req_data = urllib.parse.urlencode(param)
        http = urllib3.PoolManager()
        return http.request('GET', url + "?" + req_data, headers=headers)

    def httpPost(self, url, url_param, headers, param):
        if url_param:
            url_data = urllib.parse.urlencode(url_param)
            url = url + "?" + url_data
        http = urllib3.PoolManager()
        return http.request('POST', url, body=json.dumps(param, ensure_ascii=False).encode('utf-8'),
                            headers=headers)

    def httpPostStream(self, url, url_param, headers, stream):
        if url_param:
            url_data = urllib.parse.urlencode(url_param)
            url = url + "?" + url_data
        return requests.post(url, headers=headers, files=stream)
