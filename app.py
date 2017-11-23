from flask import Flask, render_template, redirect, request as flask_request
import socket
import sys
import os
import psutil
import logging

app = Flask(__name__)

logger = logging.getLogger(__name__)
appLogsHandler = logging.FileHandler('logs/app.log')
appLogsFormatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
appLogsHandler.setFormatter(appLogsFormatter)
logger.addHandler(appLogsHandler)
logger.setLevel(logging.ERROR)

accessLogger = logging.getLogger('werkzeug')
accessLogsHandler = logging.FileHandler('logs/access.log')
accessLogsFormatter = logging.Formatter('%(levelname)s: %(message)s' )
accessLogsHandler.setFormatter(accessLogsFormatter)
accessLogger.addHandler(accessLogsHandler)
accessLogger.setLevel(logging.INFO)

@app.route('/gethostdetails')
def gethostdetail():
    logger.info(' /gethostdetails ')
    details = {}
    details['Host Name']=socket.gethostname()
    details['Host IP']=socket.gethostbyname(socket.gethostname())
    details['Python Version']=sys.version
    logger.debug(details)
    return render_template('hostdetails.html', details=details)


@app.route('/cpu')
def add():
    logger.info(' /cpu ')
    data = {}
    virtual_mem = list(psutil.virtual_memory())
    data['cpu']=psutil.cpu_percent()
    data['vm_total']= round(virtual_mem[0] / (1024*1024),2)
    data['vm_available']= round(virtual_mem[1] / (1024*1024),2)
    data['vm_perc_free']= virtual_mem[2]
    logger.debug(data)
    return render_template('cpu.html', data=data)


@app.errorhandler(404)
def page_not_found(e):
    logger.error(' Bad URL, redirecting to /gethostdetails ')
    return redirect("/gethostdetails")

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
