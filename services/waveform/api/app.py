#!/usr/bin/env python

import logging
import os
import tempfile
import shutil
import time
import audiowaveform
import uuid

from decouple import config
from flask import (
    Flask,
    request,
    make_response,
    jsonify,
    send_from_directory,
    url_for,
    redirect,
)
from flask.logging import default_handler


__version__ = "0.0.2"


JSON_NUM_SAMPLES = config("JSON_NUM_SAMPLES", default=1000, cast=int)
JSON_NUM_STEPS = config("JSON_NUM_STEPS", default=100, cast=int)

PNG_WIDTH = config("PNG_WIDTH", default=1800, cast=int)
PNG_HEIGHT = config("PNG_HEIGHT", default=301, cast=int)
PNG_FG = config("PNG_FG", default="ffffff00", cast=str)
PNG_BG = config("PNG_BG", default="ffffff", cast=str)

DATA_DIRECTORY = config("DATA_DIRECTORY", default=tempfile.mkdtemp())

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

for logger in (app.logger, logging.getLogger("audiowaveform")):
    logger.addHandler(default_handler)


"""
curl \
  -F "file=@/Users/ohrstrom/Desktop/megasna.mp3" \
  http://10.35.30.122:2001/processed/200
"""


def cleanup_data_directory(directory=DATA_DIRECTORY):
    app.logger.debug("cleanup data directory: %s", directory)
    time_in_secs = time.time() - 60
    for root, _dirs, files in os.walk(directory, topdown=False):
        for _file in files:
            full_path = os.path.join(root, _file)
            stat = os.stat(full_path)
            if stat.st_mtime <= time_in_secs:
                app.logger.info("unlink old file: %s", full_path)
                os.unlink(full_path)


@app.route("/")
def index():
    return jsonify(
        {
            "version": f"{__version__}",
            "routes": [
                {
                    "route": "/png(/<int:width(1800)>)(/<int:height(300)>)",
                    "methods": ["POST"],
                    "description": "generates audiowaveform as PNG image",
                },
                {
                    "route": f"/json(/<int:samples({JSON_NUM_SAMPLES})>)(/<int:steps({JSON_NUM_STEPS})>)",
                    "methods": ["POST"],
                    "description": "generates processed waveform data as JSON",
                },
            ],
        }
    )


@app.route("/upload")
def upload():
    # just for minimal testing/ demonstration
    return f"""
        <!doctype html>
        <title>Upload</title>
        <h1>Upload Audiofile</h1>
        <h2>Generate JSON</h2>
        <p>defaults to {JSON_NUM_SAMPLES} samples, {JSON_NUM_STEPS} steps</p>
        <form method=post enctype=multipart/form-data action=/json/{JSON_NUM_SAMPLES}>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        <h2>Generate PNG</h2>
        <p>defaults to {PNG_WIDTH}x{PNG_HEIGHT}px</p>
        <form method=post enctype=multipart/form-data action=/png/{PNG_WIDTH}/{PNG_HEIGHT}>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
    """


@app.route("/json", methods=["POST"], endpoint="json")
@app.route("/json/<int:num_samples>", methods=["POST"], endpoint="json")
@app.route("/json/<int:num_samples>/<int:num_steps>", methods=["POST"], endpoint="json")
def process_as_json(**kwargs):

    # access uploaded file
    file = request.files["file"]
    _, ext = os.path.splitext(file.filename)

    # create temp directory for processing & save uploaded file
    path = tempfile.mkstemp(suffix=ext)[1]
    file.save(path)

    # run waveform data generation
    try:
        app.logger.debug("generate waveform data for: %s", path)
        _waveform = audiowaveform.waveform_as_json(path)
    except audiowaveform.AudioWaveformException as e:
        app.logger.warning("error generating waveform data for: %s - %s", path, e)
        return make_response(jsonify({"errors": [str(e)]}), 400)
    finally:
        os.unlink(path)

    num_samples = kwargs.get("num_samples", JSON_NUM_SAMPLES)
    num_steps = kwargs.get("num_steps", JSON_NUM_STEPS)
    try:
        app.logger.debug("processing waveform data for: %s", path)
        _waveform = audiowaveform.process_waveform_data(
            _waveform, num_samples, num_steps
        )
        return jsonify({"data": _waveform})
    except audiowaveform.AudioWaveformException as e:
        app.logger.warning("error processing waveform data for: %s - %s", path, e)
        return make_response(jsonify({"errors": [str(e)]}), 400)


@app.route("/png", methods=["POST"], endpoint="png")
@app.route("/png/<int:width>", methods=["POST"], endpoint="png")
@app.route("/png/<int:width>/<int:height>", methods=["POST"], endpoint="png")
def process_as_png(**kwargs):

    # clean up old files
    cleanup_data_directory()

    # access uploaded file
    file = request.files["file"]
    _, ext = os.path.splitext(file.filename)

    # create temp directory for processing & save uploaded file
    path = tempfile.mkstemp(suffix=ext)[1]
    file.save(path)

    width = kwargs.get("width", PNG_WIDTH)
    height = kwargs.get("height", PNG_HEIGHT)
    fg = PNG_FG
    bg = PNG_BG

    # run waveform image generation
    try:
        app.logger.debug("generate waveform data for: %s", path)
        png_temp_path = audiowaveform.waveform_as_png(
            path, width=width, height=height, fg=fg, bg=bg, delete_after_processing=True
        )

        png_filename = f"{uuid.uuid1()}.png"

        png_path = os.path.join(DATA_DIRECTORY, png_filename)

        shutil.move(png_temp_path, png_path)

        return redirect(url_for("download_file", filename=png_filename))

        # return make_response(jsonify({'png_path': png_path, 'location': location, 'kwargs': kwargs}), 201)

    except audiowaveform.AudioWaveformException as e:
        app.logger.warning("error generating waveform data for: %s - %s", path, e)
        return make_response(jsonify({"errors": [str(e)]}), 400)


@app.route("/data/<path:filename>", methods=["GET"])
def download_file(filename):
    app.logger.info("serving %s from %s", filename, DATA_DIRECTORY)

    return send_from_directory(directory=DATA_DIRECTORY, filename=filename)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
