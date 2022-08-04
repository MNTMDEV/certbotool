import json


class UserConfig():
    @staticmethod
    def parse(filepath):
        f = None
        try:
            f = open(filepath)
            jsonstr = f.read()
            data = json.loads(jsonstr)
            return data
        except Exception as e:
            pass
        finally:
            if f!=None:
                f.close()
        return None

    @staticmethod
    def write(filepath, json):
        pass
