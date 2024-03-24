import json
from pathlib import Path

import os

JSON_EXT='.json'


class CreateMLWriter:
    def __init__(self, folder_name, filename, img_size, shapes, output_file, database_src='Unknown',
                 local_img_path=None):
        self.folder_name = folder_name
        self.filename = filename
        self.database_src = database_src
        self.img_size = img_size
        self.box_list = []
        self.local_img_path = local_img_path
        self.shapes = shapes
        self.output_file = output_file

    def write(self):
        if os.path.isfile(self.output_file):
            with open(self.output_file, "r") as file:
                input_data = file.read()
                output_dict = json.loads(input_data)
        else:
            output_dict = []

        for shape in self.shapes:
            points = shape["points"]

            x1 =