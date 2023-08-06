import json
from typing import Dict


class FileSystemConnector(object):
    def __init__(self, file_name=None):

        if not file_name:
            file_name = '/tmp/jocasta.json'

        self.file_name = file_name

    def send(self, data: Dict) -> bool:
        """
        Write data as JSON to file.
        """

        with open(self.file_name, 'w') as f:
            f.write(json.dumps(data))

        return True
