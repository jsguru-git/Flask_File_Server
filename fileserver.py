"""
A Flask file server.
"""
import logging
import time
import os

import requests
from flask import Flask, request, send_from_directory, render_template

LOCALHOST = '127.0.0.1'

logger = logging.getLogger(__name__)


def RunFileServer(fileServerDir, fileServerPort):
    """
    Run a Flask file server on the given port.
    """
    app = Flask(__name__, instance_path=fileServerDir)

    @app.route('/', methods=['GET'])
    def Home():  # pylint: disable=unused-variable
        
        fileArr = []
        for root, dirs, files in os.walk(fileServerDir):
            for fileName in files:
                fileArr.append(root.replace(fileServerDir, "") + "\\" + fileName)
        return render_template("home.html", files=fileArr)

    @app.route('/fileserver-is-ready', methods=['GET'])
    def FileServerIsReady():  # pylint: disable=unused-variable
        """
        Used to test if file server has started.
        """
        return "The fileserver is ready."

    @app.route('/<path:filename>', methods=['GET'])
    def ServeFile(filename):  # pylint: disable=unused-variable
        """
        Serves up a file from fileServerDir.
        """
        return send_from_directory(fileServerDir, filename.strip('/'))

    app.run(host=LOCALHOST, port=fileServerPort)


def WaitForFileServerToStart(port):
    url = 'http://%s:%s/fileserver-is-ready' % (LOCALHOST, port)
    attempts = 0
    while True:
        try:
            attempts += 1
            requests.get(url, timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.25)
            if attempts > 10:
                logger.warning("WaitForFileServerToStart: timeout")
                return

if __name__ == "__main__":
    dir_path = os.getcwd()
    storage_path = dir_path
    RunFileServer(storage_path, 8000)
