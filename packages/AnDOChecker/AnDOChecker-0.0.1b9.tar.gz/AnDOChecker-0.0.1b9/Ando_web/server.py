# File: server.py
# Project: Ando_web
# File Created: Wednesday, 1st July 2020 4:10:50 pm
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Thursday, 2nd July 2020 1:35:59 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2020 MIT, Institue de neurosciences de la Timone


from flask import Flask, jsonify, render_template, request
import os
import ando.engine as a
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/_AnDOchecker', methods=["GET", "POST"])
def _AnDOchecker():
    """
    Take all the file selected and send it to the API via json : :
    [
    data : [
            'exp-Landing/sub-anye/180116_001_m_anye_land-001/Touch.txt',
            'exp-Landing/sub-enya/180116_001_m_enya_land-001/source/Touch.txt',
            'exp-Landing/sub-enya/180116_001_m_enya_land-001/Touch.txt',
            'exp-Landing/sub-enyo/180116_001_m_enyo_land-001/Touch.txt'
            ]
     ]

    Returns:
        [json]: return a json response with the feedback coresponding
         to the verbose mod of the AnDO Checker
        [
            "out" : [list] all error repported by the ando Checker function,
            "result": [bool] true: if an error occurred , false : if nothing
             is repported
        ]

    TODO: why not try to use jinja2 template .
    """

    if request.method == 'POST':
        data = request.json
        list_of_folders_names = list()
        list_of_path = list()
        for file in data:
            """
            Deleting files from path
            """
            list_of_path.append(os.path.dirname(file))

        for file in list_of_path:
            """
            Transform path to list of folders names :
            'exp-Landing/sub-enyo/180116_001_m_enyo_land-001/"
            to
            ['exp-Landing','sub-enyo','180116_001_m_enyo_land-001']
            """
            list_of_folders_names.append(file.split(os.sep))

        list_of_folders_names = a.parse_all_path(list_of_folders_names)
        for item in list_of_folders_names:
            result, feedback = (a.is_AnDO_verbose_Format(item))
        # print(out)
        return jsonify({
            "feedback": feedback,
            "result": result
         })


if __name__ == "__main__":
    app.run()
