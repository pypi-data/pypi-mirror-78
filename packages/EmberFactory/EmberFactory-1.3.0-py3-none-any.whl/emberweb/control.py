# -*- coding: utf-8 -*-
"""
EmberFactory / control: links the web UI to the drawing code

Written as a flask Blueprint; if revising the app structure is desired, consider reading
https://stackoverflow.com/questions/24420857/what-are-flask-blueprints-exactly

Copyright (C) 2020  philippe.marbaix@uclouvain.be
"""

from flask import Blueprint
from flask import render_template
from flask import request, url_for, redirect
from flask import current_app, session
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
import sys
import uuid
from embermaker import helpers as hlp
from embermaker import makember as mke

bp = Blueprint("control", __name__)


@bp.route('/result', methods=['GET', 'POST'])
def result():
    # Avoid failure if this page is visited without providing data
    if request.method == 'GET':
        return redirect(url_for('index'))

    # Default message to be returned within the template
    message = {"error": "", "warning": "", "log": [], "outfile": None, "uncaught-err": False}

    # File upload and embermaker run
    # ------------------------------
    hlp.startlog()
    try:
        # Store user choice about deleting files:
        session['delfile'] = request.form.get('delfile') == 'on'
        # Get filename and check file
        fileitem = request.files['file']
        if not fileitem.filename:
            message["error"] = "No file provided or bad file."
            return render_template("emberweb/error.html", message=message)
        fnamesplit = os.path.splitext(os.path.basename(fileitem.filename))
        # Reject file if the extension does not suggest an Excel file
        # (wile devils can masquerade as angels, this protects against potential evils who look like evils)
        if fnamesplit[1] not in ['.xls', '.xlsx']:
            message["error"] = "Unexpected file extension."
            return render_template("emberweb/error.html", message=message)

        # Generate a file path name containing a unique ID
        # (so files are always stored under different names + users cannot get somone else's file):
        sesid = str(uuid.uuid1())
        fnamesplit = os.path.splitext(os.path.basename(fileitem.filename))
        fname = secure_filename(fnamesplit[0] + "_" + sesid + fnamesplit[1])
        infile = os.path.join(current_app.instance_path, 'in/', fname)
        # Upload file
        fileitem.save(infile)
        # Store file name in case we might have to delete it, especially after uncaught error
        session['infile'] = infile

        # Execution of makember (makemberout = [fname, error-message-if-any])
        makemberout = mke.makember(infile=infile, prefcsys=request.form['csys'])

        # Optionally delete file
        if session['delfile']:
            os.remove(infile)

        # An output file was generated (success!)
        if makemberout[0] is not None:
            # Provide a url for the download
            # makemberout[0] is the file's path on the server
            outfile = 'out/' + os.path.basename(makemberout[0])
            message["outfile"] = outfile  # inserts url for download
            # Report logged messages
            message["log"] = hlp.getlog("full")
            warnings = hlp.getlog("warning")
            if len(warnings) > 0:
                message["warning"] = warnings
            critical = hlp.getlog("critical")
            if len(critical) > 0:
                message["error"] = critical

        # No file was generated: a fatal error occurred:
        else:
            message["error"] = "Execution generated the following message, then failed: " + str(makemberout[1])
            return render_template("emberweb/error.html", message=message)

    # An error occurred, and we did not handle it in any way:
    except Exception as exc:
        message["error"] = "An error for which there is no handling has occurred. " \
                           "We apologize. The details provided below may help to understand the problem." \
                           "It might relate to an issue in your input file. We are interested in" \
                           "receiving this information to improve the Ember Factory (see contact at the bottom)."
        exc_tb = sys.exc_info()[2]
        while exc_tb.tb_next is not None:
            exc_tb = exc_tb.tb_next
        finame = exc_tb.tb_frame.f_globals['__name__']
        lineno = str(exc_tb.tb_frame.f_lineno)
        errtype = type(exc).__name__
        hlp.addlogfail("[" + finame + ":" + lineno + "]: " + errtype + " (" + str(exc) + ")")
        message["log"] = hlp.getlog("full")
        message["uncaught-err"] = True
        return render_template("emberweb/error.html", message=message)

    return render_template("emberweb/result.html", message=message)


# Enable downloading the obtained files:
@bp.route('/out/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    dloads = os.path.join(current_app.instance_path, "out/")
    response = send_from_directory(directory=dloads, filename=filename)
    if session['delfile']:
        os.remove(os.path.join(dloads, filename))
    return response


# Delete file on user request after an uncaught error
@bp.route('/delete-in', methods=['GET'])
def delete_in():
    dloads = os.path.join(current_app.instance_path, "in/")
    if session['infile']:
        try:
            os.remove(os.path.join(dloads, session['infile']))
            session['infile'] = None
            response = 'deleted'
        except IOError:
            response = 'failed'
    else:
        response = 'no file'
    return response
