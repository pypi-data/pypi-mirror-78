import json
import os

from common.exceptions import TemplateException

basename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resources/templates'))


class Template(object):
    # noinspection PyShadowingNames
    def __init__(self, basename: str):
        self.__basename: str = basename

    def load_template(self, name: str) -> dict:
        try:
            with open('{}/{}.json'.format(self.__basename, name)) as json_file:
                return json.load(json_file)
        except FileNotFoundError as e:
            raise e
        except Exception:
            raise TemplateException(message='exception in template {}'.format(name),
                                    template_name=name)

    def load_template_with_args(self, name: str, args: dict) -> dict:
        try:
            with open('{}/{}.json'.format(self.__basename, name), 'r') as file:
                template = file.read()
            # noinspection StrFormat
            filed = template.format(**args)
            return json.loads(filed)
        except FileNotFoundError as e:
            raise e
        except Exception:
            raise TemplateException(message='exception in template {}'.format(name),
                                    template_name=name)
