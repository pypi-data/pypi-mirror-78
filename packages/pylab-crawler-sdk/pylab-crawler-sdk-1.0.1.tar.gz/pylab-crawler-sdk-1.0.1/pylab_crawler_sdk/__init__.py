import requests

BASE_URL = 'https://crawler.pylab.co'


class Session(object):
    def __init__(self, key):
        self.key = key

    def add_log(self, task_id, content):
        """로그를 기록합니다"""
        if not task_id:
            return
        try:
            res = requests.post(f'{BASE_URL}/sdk/task-logs/?key={self.key}', data={
                'task': task_id,
                'content': content
            })
            res.raise_for_status()
        except:
            pass

    def is_running(self, task_id):
        if not task_id:
            return True
        try:
            res = requests.get(f'{BASE_URL}/sdk/task-terminations/?key={self.key}&task={task_id}')
            res.raise_for_status()
        except:
            return True
        json = res.json()
        return len(json) == 0
