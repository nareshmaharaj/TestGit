from flask import Flask, render_template
import MySQLdb as mdb
import json
from datetime import datetime
import time
from flask import request
import logging
 
app = Flask(__name__)

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('latency_report.log')
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

def connect_db():
    try:
        connection = mdb.connect('localhost', 'edge', 'edge123!', 'edgegateway')
        return connection
    except Exception as err:
        logger.error("connect_db : ERROR :", exc_info=True)

@app.route("/index")
def index_page():
    return render_template('index.html')

@app.route("/surge", methods=['GET'])
def surge_data():
    try:
        displayPage = str(request.values.get('displayPage'))
        start_time = str(request.values.get('start_time'))
        end_time = str(request.values.get('end_time'))
        livestarttime = str(request.values.get('livestarttime'))
        livechart = 0
        con = connect_db()
        cursor = con.cursor()
        query = ""
        if displayPage == "1": # Last 30 mins
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM surge su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 30 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        elif displayPage == "2": # Last 1 hour
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM surge su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 60 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        elif displayPage == "3": # Last 6 hours
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM surge su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 360 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        elif displayPage == "4":  # Last 1 day
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM surge su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 1440 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        elif displayPage == "5":  # Last 30 days
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM surge su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 43200 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        else:
            if displayPage == "6" and livestarttime != "":
                query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM surge su WHERE " \
                " su.tstamp >=unix_timestamp('"+livestarttime+"') " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
                livechart = 1
            elif start_time != "" and end_time != "":
                query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM surge su WHERE " \
                " su.tstamp >=unix_timestamp('"+start_time+"') " \
                " AND su.tstamp <= unix_timestamp('"+end_time+"') "
            else:
                query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM surge su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 30 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        logger.info(query)
        datelist = []
        scorelist = []
        d1list = []
        d2list = []
        d3list = []
        d4list = []
        d5list = []
        faultlist = []
        if query != "":
            cursor.execute(query)
            records = cursor.fetchall()
            for row in records:
                datelist.append(float(row[0]))
                scorelist.append(float(row[6]))
                d1list.append(float(row[1]))
                d2list.append(float(row[2]))
                d3list.append(float(row[3]))
                d4list.append(float(row[4]))
                d5list.append(float(row[5]))
                faultlist.append(int(row[7]))
        html_page = 'surge.html'
        if livechart == 1:
            html_page = 'surge_live.html'
        return render_template(html_page,datelist=datelist,scorelist=scorelist, d1list=d1list, d2list=d2list,
                           d3list=d3list, d4list=d4list, d5list=d5list, faultlist=faultlist)
    except Exception as err:
        logger.error("surge_data : ERROR :", exc_info=True)


@app.route("/electrical", methods=['GET'])
def electrical_data():
    try:
        displayPage = str(request.values.get('displayPage'))
        start_time = str(request.values.get('start_time'))
        end_time = str(request.values.get('end_time'))
        livestarttime = str(request.values.get('livestarttime'))
        livechart = 0
        con = connect_db()
        cursor = con.cursor()
        query = "";
        if displayPage == "1":  # Last 30 mins
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.score, " \
                " su.fault FROM electrical su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 30 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        elif displayPage == "2":
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.score, " \
                " su.fault FROM electrical su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 60 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        elif displayPage == "3":
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.score, " \
                " su.fault FROM electrical su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 360 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        elif displayPage == "4":
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.score, " \
                " su.fault FROM electrical su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 1440 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        elif displayPage == "5":
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.score, " \
                " su.fault FROM electrical su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 43200 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        else:
            if displayPage == "6" and livestarttime != "":
                query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.score, " \
                " su.fault FROM electrical su WHERE " \
                " su.tstamp >=unix_timestamp('"+livestarttime+"') " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
                livechart = 1
            elif start_time != "" and end_time != "":
                query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.score, " \
                " su.fault FROM electrical su WHERE " \
                " su.tstamp >=unix_timestamp('"+start_time+"') " \
                " AND su.tstamp <= unix_timestamp('"+end_time+"') "
            else:
                query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.score, " \
                " su.fault FROM electrical su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 30 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        logger.info(query)
        datelist = []
        scorelist = []
        d1list = []
        d2list = []
        d3list = []
        d4list = []
        faultlist = []
        if query != "":
            cursor.execute(query)
            records = cursor.fetchall()
            for row in records:
                datelist.append(float(row[0]))
                scorelist.append(float(row[5]))
                d1list.append(float(row[1]))
                d2list.append(float(row[2]))
                d3list.append(float(row[3]))
                d4list.append(float(row[4]))
                faultlist.append(int(row[6]))
        html_page = 'electrical.html'
        if livechart == 1:
            html_page = 'electrical_live.html'
        return render_template(html_page,datelist=datelist,scorelist=scorelist, d1list=d1list, d2list=d2list,
                           d3list=d3list, d4list=d4list, faultlist=faultlist)
    except Exception as err:
        logger.error("electrical_data : ERROR :", exc_info=True)

@app.route("/dleakage", methods=['GET'])
def dleakage_data():
    try:
        displayPage = str(request.values.get('displayPage'))
        start_time = str(request.values.get('start_time'))
        end_time = str(request.values.get('end_time'))
        livestarttime = str(request.values.get('livestarttime'))
        livechart = 0
        con = connect_db()
        cursor = con.cursor()
        query = "";
        if displayPage == "1":  # Last 30 mins
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM dleakage su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 30 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        elif displayPage == "2":
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM dleakage su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 60 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        elif displayPage == "3":
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM dleakage su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 360 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        elif displayPage == "4":
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM dleakage su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 1440 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        elif displayPage == "5":
            query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                " su.fault FROM dleakage su WHERE " \
                " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 43200 MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) "
        else:
            if displayPage == "6" and livestarttime != "":
                query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                    " su.fault FROM dleakage su WHERE " \
                    " su.tstamp >=unix_timestamp('"+livestarttime+"') " \
                    " AND su.tstamp <= unix_timestamp(NOW()) "
                livechart = 1
            elif start_time != "" and end_time != "":
                query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                    " su.fault FROM dleakage su WHERE " \
                    " su.tstamp >=unix_timestamp('"+start_time+"') " \
                    " AND su.tstamp <= unix_timestamp('"+end_time+"') "
            else:
                query = "select 1000*su.tstamp, su.d1, su.d2, su.d3, su.d4, su.d5, su.score, " \
                    " su.fault FROM dleakage su " \
                    " su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL 30 MINUTE)) " \
                    " AND su.tstamp <= unix_timestamp(NOW()) "
        logger.info(query)
        datelist = []
        scorelist = []
        d1list = []
        d2list = []
        d3list = []
        d4list = []
        d5list = []
        faultlist = []
        if query != "":
            cursor.execute(query)
            records = cursor.fetchall()
            for row in records:
                datelist.append(float(row[0]))
                scorelist.append(float(row[6]))
                d1list.append(float(row[1]))
                d2list.append(float(row[2]))
                d3list.append(float(row[3]))
                d4list.append(float(row[4]))
                d5list.append(float(row[5]))
                faultlist.append(int(row[7]))
        html_page = 'dleakage.html'
        if livechart == 1:
            html_page = 'dleakage_live.html'
        return render_template(html_page,datelist=datelist,scorelist=scorelist, d1list=d1list, d2list=d2list,
                           d3list=d3list, d4list=d4list, d5list=d5list, faultlist=faultlist)
    except Exception as err:
        logger.error("dleakage_data : ERROR :", exc_info=True)

@app.route("/surgesinglechart", methods=['GET'])
def singlechart():
    try:
        displaychart = str(request.values.get('displaychart'))
        start_time = str(request.values.get('start_time'))
        end_time = str(request.values.get('end_time'))
        livestarttime = str(request.values.get('livestarttime'))
        displayPage = str(request.values.get('displayPage'))
        livechart = 0
        con = connect_db()
        cursor = con.cursor()
        query = "";
        is_fault_data = 0;
        dispinterval = 0
        if displayPage == "1":
            dispinterval = 30;
        elif displayPage == "2":
            dispinterval = 60
        elif displayPage == "3":
            dispinterval = 360
        elif displayPage == "4":
            dispinterval = 1440
        elif displayPage == "5":
            dispinterval = 43200

        if displaychart == "d1":
            displaylabelheader = "Surge ActPressureDiffTankIn Latency Chart"
            displaylabel = "ActPressureDiffTankIn"
        elif displaychart == "d2":
            displaylabelheader = "Surge ActPressureDiffTankOut Latency Chart"
            displaylabel = "ActPressureDiffTankOut"
        elif displaychart == "d3":
            displaylabelheader = "Surge ActPressureDiffOrifice1 Latency Chart"
            displaylabel = "ActPressureDiffOrifice1"
        elif displaychart == "d4":
            displaylabelheader = "Surge ActPressureDiffOrifice2 Latency Chart"
            displaylabel = "ActPressureDiffOrifice2"
        elif displaychart == "d5":
            displaylabelheader = "Surge CompressorSpeed Latency Chart"
            displaylabel = "CompressorSpeed"
        elif displaychart == "score":
            displaylabelheader = "Surge Score Latency Chart"
            displaylabel = "Score"
        elif displaychart == "fault":
            displaylabelheader = "Surge Fault Latency Chart"
            displaylabel = "Fault"
        if dispinterval > 0:
            if displaychart == "d1":
                query = "select 1000*su.tstamp, su.d1 FROM surge su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "d2":
                query = "select 1000*su.tstamp, su.d2 FROM surge su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "d3":
                query = "select 1000*su.tstamp, su.d3 FROM surge su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "d4":
                query = "select 1000*su.tstamp, su.d4 FROM surge su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "d5":
                query = "select 1000*su.tstamp, su.d5 FROM surge su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "score":
                query = "select 1000*s.tstamp, s.score FROM surge s WHERE " \
                    " s.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                    " AND s.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "fault":
                query = "select 1000*s.tstamp, s.fault FROM surge s WHERE " \
                    " s.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                    " AND s.tstamp <= unix_timestamp(NOW()) " % dispinterval
                is_fault_data = 1
        else:
            if displayPage == "6" and livestarttime != "":
                if displaychart == "d1":
                    query = "select 1000*su.tstamp, su.d1 FROM surge su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "d2":
                    query = "select 1000*su.tstamp, su.d2 FROM surge su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "d3":
                    query = "select 1000*su.tstamp, su.d3 FROM surge su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "d4":
                    query = "select 1000*su.tstamp, su.d4 FROM surge su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "d5":
                    query = "select 1000*su.tstamp, su.d5 FROM surge su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "score":
                    query = "select 1000*s.tstamp, s.score FROM surge s WHERE " \
                        " s.tstamp >=unix_timestamp('" + livestarttime + "') AND s.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "fault":
                    query = "select 1000*s.tstamp, s.fault FROM surge s WHERE " \
                    " s.tstamp >=unix_timestamp('"+livestarttime+"') " \
                    " AND s.tstamp <= unix_timestamp(NOW()) "
                    is_fault_data = 1
                livechart = 1
            elif start_time != "" and end_time != "":
                if displaychart == "d1":
                    query = "select 1000*su.tstamp, su.d1 FROM surge su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "d2":
                    query = "select 1000*su.tstamp, su.d2 FROM surge su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "d3":
                    query = "select 1000*su.tstamp, su.d3 FROM surge su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "d4":
                    query = "select 1000*su.tstamp, su.d4 FROM surge su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "d5":
                    query = "select 1000*su.tstamp, su.d5 FROM surge su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "score":
                    query = "select 1000*s.tstamp, s.score FROM surge s WHERE " \
                        " s.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND s.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "fault":
                    query = "select 1000*s.tstamp, s.fault FROM surge s WHERE " \
                        " s.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND s.tstamp <= unix_timestamp('" + end_time + "') "
                    is_fault_data = 1
        logger.info(query)
        datelist = []
        datalist = []
        if query != "":
            cursor.execute(query)
            records = cursor.fetchall()
            for row in records:
                datelist.append(float(row[0]))
                if is_fault_data == 0:
                    datalist.append(float(row[1]))
                else:
                    datalist.append(int(row[1]))
        html_page = 'surge_single_chart.html'
        if livechart == 1:
            html_page = 'surge_single_chart_live.html'
        return render_template(html_page,datelist=datelist,datalist=datalist,displaylabelheader=displaylabelheader,
                           displaylabel=displaylabel)
    except Exception as err:
        logger.error("singlechart : ERROR :", exc_info=True)

@app.route("/electricalsinglechart", methods=['GET'])
def electricalsinglechart():
    try:
        displaychart = str(request.values.get('displaychart'))
        start_time = str(request.values.get('start_time'))
        end_time = str(request.values.get('end_time'))
        livestarttime = str(request.values.get('livestarttime'))
        displayPage = str(request.values.get('displayPage'))
        livechart = 0
        con = connect_db()
        cursor = con.cursor()
        query = "";
        is_fault_data = 0;
        dispinterval = 0
        if displayPage == "1":
            dispinterval = 30;
        elif displayPage == "2":
            dispinterval = 60
        elif displayPage == "3":
            dispinterval = 360
        elif displayPage == "4":
            dispinterval = 1440
        elif displayPage == "5":
            dispinterval = 43200

        if displaychart == "d1":
            displaylabelheader = "Electrical ActVoltageDCLinkCompressorTop Latency Chart"
            displaylabel = "ActVoltageDCLinkCompressorTop"
        elif displaychart == "d2":
            displaylabelheader = "Electrical ActVoltageINUOutputCompressorTop Latency Chart"
            displaylabel = "ActVoltageINUOutputCompressorTop"
        elif displaychart == "d3":
            displaylabelheader = "Electrical ActCurrentCompressorTop Latency Chart"
            displaylabel = "ActCurrentCompressorTop"
        elif displaychart == "d4":
            displaylabelheader = "Electrical ActCurrentCompressorBottom Latency Chart"
            displaylabel = "ActCurrentCompressorBottom"
        elif displaychart == "score":
            displaylabelheader = "Electrical Score Latency Chart"
            displaylabel = "Score"
        elif displaychart == "fault":
            displaylabelheader = "Electrical Fault Latency Chart"
            displaylabel = "Fault"

        if dispinterval > 0:
            if displaychart == "d1":
                query = "select 1000*su.tstamp, su.d1 FROM electrical su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                    " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "d2":
                query = "select 1000*su.tstamp, su.d2 FROM electrical su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "d3":
                query = "select 1000*su.tstamp, su.d3 FROM electrical su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "d4":
                query = "select 1000*su.tstamp, su.d4 FROM electrical su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "score":
                query = "select 1000*s.tstamp, s.score FROM electrical s WHERE " \
                    " s.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                    " AND s.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "fault":
                query = "select 1000*s.tstamp, s.fault FROM electrical s WHERE " \
                    " s.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                    " AND s.tstamp <= unix_timestamp(NOW()) " % dispinterval
                is_fault_data = 1
        else:
            if displayPage == "6" and livestarttime != "":
                if displaychart == "d1":
                    query = "select 1000*su.tstamp, su.d1 FROM electrical su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "d2":
                    query = "select 1000*su.tstamp, su.d2 FROM electrical su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "d3":
                    query = "select 1000*su.tstamp, su.d3 FROM electrical su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "d4":
                    query = "select 1000*su.tstamp, su.d4 FROM electrical su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "score":
                    query = "select 1000*s.tstamp, s.score FROM electrical s WHERE " \
                        " s.tstamp >=unix_timestamp('" + livestarttime + "') AND s.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "fault":
                    query = "select 1000*s.tstamp, s.fault FROM electrical s WHERE " \
                    " s.tstamp >=unix_timestamp('"+livestarttime+"') " \
                    " AND s.tstamp <= unix_timestamp(NOW()) "
                    is_fault_data = 1
                livechart = 1
            elif start_time != "" and end_time != "":
                if displaychart == "d1":
                    query = "select 1000*su.tstamp, su.d1 FROM electrical su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "d2":
                    query = "select 1000*su.tstamp, su.d2 FROM electrical su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "d3":
                    query = "select 1000*su.tstamp, su.d3 FROM electrical su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "d4":
                    query = "select 1000*su.tstamp, su.d4 FROM electrical su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "score":
                    query = "select 1000*s.tstamp, s.score FROM electrical s WHERE " \
                        " s.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND s.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "fault":
                    query = "select 1000*s.tstamp, s.fault FROM electrical s WHERE " \
                        " s.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND s.tstamp <= unix_timestamp('" + end_time + "') "
                    is_fault_data = 1
        logger.info(query)
        datelist = []
        datalist = []
        if query != "":
            cursor.execute(query)
            records = cursor.fetchall()
            for row in records:
                datelist.append(float(row[0]))
                if is_fault_data == 0:
                    datalist.append(float(row[1]))
                else:
                    datalist.append(int(row[1]))

        html_page = 'electrical_single_chart.html'
        if livechart == 1:
            html_page = 'electrical_single_chart_live.html'
        return render_template(html_page,datelist=datelist,datalist=datalist,displaylabelheader=displaylabelheader,
                           displaylabel=displaylabel)
    except Exception as err:
        logger.error("electricalsinglechart : ERROR :", exc_info=True)

@app.route("/dleakagesinglechart", methods=['GET'])
def dleakagesinglechart():
    try:
        displaychart = str(request.values.get('displaychart'))
        start_time = str(request.values.get('start_time'))
        end_time = str(request.values.get('end_time'))
        livestarttime = str(request.values.get('livestarttime'))
        displayPage = str(request.values.get('displayPage'))
        livechart = 0
        con = connect_db()
        cursor = con.cursor()
        query = "";
        is_fault_data = 0;
        dispinterval = 0
        if displayPage == "1":
            dispinterval = 30;
        elif displayPage == "2":
            dispinterval = 60
        elif displayPage == "3":
            dispinterval = 360
        elif displayPage == "4":
            dispinterval = 1440
        elif displayPage == "5":
            dispinterval = 43200
        if displaychart == "d1":
            displaylabelheader = "Dleakage ActSpeedCompressorTop Latency Chart"
            displaylabel = "ActSpeedCompressorTop"
        elif displaychart == "d2":
            displaylabelheader = "Dleakage ActPositionValveInlet Latency Chart"
            displaylabel = "ActPositionValveInlet"
        elif displaychart == "d3":
            displaylabelheader = "Dleakage ActPositionValveOutlet Latency Chart"
            displaylabel = "ActPositionValveOutlet"
        elif displaychart == "d4":
            displaylabelheader = "Dleakage ActPressureAbsoluteTankOut Latency Chart"
            displaylabel = "ActPressureAbsoluteTankOut"
        elif displaychart == "d5":
            displaylabelheader = "Dleakage ActPressureDiffTankIn Latency Chart"
            displaylabel = "ActPressureDiffTankIn"
        elif displaychart == "score":
            displaylabelheader = "Dleakage Score Latency Chart"
            displaylabel = "Score"
        elif displaychart == "fault":
            displaylabelheader = "Dleakage Fault Latency Chart"
            displaylabel = "Fault"

        if dispinterval > 0:
            if displaychart == "d1":
                query = "select 1000*su.tstamp, su.d1 FROM dleakage su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "d2":
                query = "select 1000*su.tstamp, su.d2 FROM dleakage su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "d3":
                query = "select 1000*su.tstamp, su.d3 FROM dleakage su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "d4":
                query = "select 1000*su.tstamp, su.d4 FROM dleakage su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "d5":
                query = "select 1000*su.tstamp, su.d5 FROM dleakage su WHERE su.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                " AND su.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "score":
                query = "select 1000*s.tstamp, s.score FROM dleakage s WHERE " \
                    " s.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                    " AND s.tstamp <= unix_timestamp(NOW()) " % dispinterval
            elif displaychart == "fault":
                query = "select 1000*s.tstamp, s.fault FROM dleakage s WHERE " \
                    " s.tstamp >=unix_timestamp(DATE_SUB(NOW(), INTERVAL %s MINUTE)) " \
                    " AND s.tstamp <= unix_timestamp(NOW()) " % dispinterval
                is_fault_data = 1
        else:
            if displayPage == "6" and livestarttime != "":
                if displaychart == "d1":
                    query = "select 1000*su.tstamp, su.d1 FROM dleakage su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "d2":
                    query = "select 1000*su.tstamp, su.d2 FROM dleakage su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "d3":
                    query = "select 1000*su.tstamp, su.d3 FROM dleakage su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "d4":
                    query = "select 1000*su.tstamp, su.d4 FROM dleakage su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "d5":
                    query = "select 1000*su.tstamp, su.d5 FROM dleakage su WHERE " \
                        " su.tstamp >=unix_timestamp('" + livestarttime + "') AND su.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "score":
                    query = "select 1000*s.tstamp, s.score FROM dleakage s WHERE " \
                        " s.tstamp >=unix_timestamp('" + livestarttime + "') AND s.tstamp <= unix_timestamp(NOW()) "
                elif displaychart == "fault":
                    query = "select 1000*s.tstamp, s.fault FROM dleakage s WHERE " \
                    " s.tstamp >=unix_timestamp('"+livestarttime+"') " \
                    " AND s.tstamp <= unix_timestamp(NOW()) "
                    is_fault_data = 1
                livechart = 1
            elif start_time != "" and end_time != "":
                if displaychart == "d1":
                    query = "select 1000*su.tstamp, su.d1 FROM dleakage su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "d2":
                    query = "select 1000*su.tstamp, su.d2 FROM dleakage su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "d3":
                    query = "select 1000*su.tstamp, su.d3 FROM dleakage su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "d4":
                    query = "select 1000*su.tstamp, su.d4 FROM dleakage su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "d5":
                    query = "select 1000*su.tstamp, su.d5 FROM dleakage su WHERE " \
                        " su.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND su.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "score":
                    query = "select 1000*s.tstamp, s.score FROM dleakage s WHERE " \
                        " s.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND s.tstamp <= unix_timestamp('" + end_time + "') "
                elif displaychart == "fault":
                    query = "select 1000*s.tstamp, s.fault FROM dleakage s WHERE " \
                        " s.tstamp >=unix_timestamp('" + start_time + "') " \
                        " AND s.tstamp <= unix_timestamp('" + end_time + "') "
                    is_fault_data = 1
        logger.info(query)
        datelist = []
        datalist = []
        if query != "":
            cursor.execute(query)
            records = cursor.fetchall()
            for row in records:
                datelist.append(float(row[0]))
                if is_fault_data == 0:
                    datalist.append(float(row[1]))
                else:
                    datalist.append(int(row[1]))

        html_page = 'dleakage_single_chart.html'
        if livechart == 1:
            html_page = 'dleakage_single_chart_live.html'
        return render_template(html_page,datelist=datelist,datalist=datalist,displaylabelheader=displaylabelheader,
                           displaylabel=displaylabel)
    except Exception as err:
        logger.error("dleakagesinglechart : ERROR :", exc_info=True)

@app.route("/index2")
def index2():
    return render_template('index2.html')

@app.route("/chart", methods=['POST'])
def chart():
    displayPage = str(request.values.get('selDisp'))
    start_time = str(request.values.get('start_time'))
    end_time = str(request.values.get('end_time'))
    livestarttime = str(request.values.get('livestarttime'))
    surgechk = str(request.values.get('chksurge'))
    electricalchk = str(request.values.get('chkelectrical'))
    dleakagechk = str(request.values.get('chkdleakage'))

    return render_template('chart.html', displayPage=displayPage, surgechk=surgechk, electricalchk=electricalchk,
                           dleakagechk=dleakagechk, start_time=start_time, end_time=end_time,
                           livestarttime=livestarttime)

@app.route("/chart", methods=['GET'])
def display():
    displayPage = str(request.values.get('displayPage'))
    surgechk = str(request.values.get('surgechk'))
    electricalchk = str(request.values.get('electricalchk'))
    dleakagechk = str(request.values.get('dleakagechk'))
    return render_template('chart.html', displayPage=displayPage, surgechk=surgechk, electricalchk=electricalchk,
                           dleakagechk=dleakagechk)


@app.route("/date")
def datepage():
    return render_template('datepage.html')

if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0', port=5000, passthrough_errors=True, threaded=True)

