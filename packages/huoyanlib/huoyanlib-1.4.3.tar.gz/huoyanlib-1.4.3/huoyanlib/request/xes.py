import json
import requests


class Like:
    def __init__(self, work_id):
        pid = str(work_id)
        self.url = "http://code.xueersi.com/api/compilers/" + str(pid) + "?id=" + str(pid)
        headers = {'Content-Type': 'application/json'}
        r = requests.get(self.url, headers=headers)
        self.response = json.loads(r.text)
        self.like = self.response['data']['likes']

    def check_is_like(self):
        import time
        while True:
            time.sleep(5)
            like = self.response['data']['likes']
            if like - self.like >= 1:
                return True
            else:
                return False


class Xes(Like):
    def __init__(self, work_id):
        self.picture_url = "https://livefile.xesimg.com/programme/assets/7ddec8b247e63d9971addecd8b752b3d.jpg"
        super().__init__(work_id)

    def get_name(self):
        return self.response['data']['name']

    def get_description(self):
        if self.response['data']['description'] == '':
            return None
        else:
            return self.response['data']['description']

    def get_likes(self):
        return self.response['data']['likes']

    def get_unlikes(self):
        return self.response['data']['unlikes']

    def get_favorites(self):
        return self.response['data']['favorites']

    def get_adapt_numbers(self):
        return self.response['data']['source_code_views']

    def download_icon(self):
        import os
        os.makedirs('./', exist_ok=True)
        from urllib.request import urlretrieve
        urlretrieve(self.picture_url, './icon.jpg')
        os.system('icon.jpg')
        return "下载完成"

    def get_author_name(self):
        return self.response['data']['username']

    def get_author_id(self):
        return self.response['data']['user_id']

    def get_work_tags(self):
        tags = self.response['data']['tags']
        list_of_tags = tags.split()
        return list_of_tags

    def get_hot(self):
        return self.response['data']['popular_score']

    def get_views(self):
        return self.response['data']['views']

    def get_first_published_time(self):
        return self.response['data']['published_at']

    def get_latest_modified_time(self):
        return self.response['data']['modified_at']

    def get_latest_updated_time(self):
        return self.response['data']['updated_at']

    def get_created_time(self):
        return self.response['data']['created_at']

    def is_hidden_code(self):
        if self.response['data']['hidden_code'] == 2:
            return False
        else:
            return True
