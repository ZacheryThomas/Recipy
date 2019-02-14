"This is the rest server for the master unit"
import json
import os.path
from queue import Queue
from flask import Flask, request
import requests
import _thread
from filter_detect.data_types.DetectionEvent import DetectionEvent
from locator.data_types.Location import Location
from state_storage.impl.Database import Database

class MasterREST():
    def __init__(self, units, dbDir='state_storage/impl/data.db'):
        self.detectionEventQueue = Queue()    
        self.units = units
        topDir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        self.dbDir = (os.path.join(topDir, dbDir))
        self.app = self.create_app()

        # TODO: ip and port should probably be constructor parameters

        @self.app.route('/')
        def all_events_html():
            db = Database(self.app.config['dbDir'])
            events = db.return_all_events()
            events.reverse()
            html = "<html><head> <meta http-equiv=\"refresh\" content=\"30\"> </head>"
            html += "<body><font size = \"6\"><b> Elephant Detections</b> <br>"
            for e in events:
                s = e.pretty_string() + "<br>"
                html += s
            html += "</font></body></html>"
            return (html)

        @self.app.route('/1.0/events')
        def events_json():
            try:
                #TODO accept fields for time ranges or maybe for last 10 eg or something
                db = Database(self.app.config['dbDir'])
                events = db.return_all_events()
                events.reverse()
                eventsJSON = [event.json() for event in events]
                eventsJSON = json.dumps({'events' : eventsJSON})
                #print(eventsJSON)
                return(eventsJSON)

            except Exception as e:
                print(e)
                raise

        @self.app.route('/hello', methods=['POST'])
        def add_unit():
            try:
                ip = request.remote_addr

                eastOffset = float(request.values.get('eastOffset'))
                northOffset = float(request.values.get('northOffset'))
                unitName = request.values.get('unitName')
                location = Location(northOffset,eastOffset)

                units = self.app.config['units']
                units.update_unit(unitName,ip,location)

                return ('we gucci')

            except Exception as e:
                print(e)
                raise

        @self.app.route('/detectionEvent', methods=['POST'])
        def on_detection_event():
            try:
                detectionEvent = DetectionEvent(jsonStr = request.data.decode())

                if detectionEvent.originator not in self.app.config['units'].unitNames:
                    #get info from unrecognized unit
                    ip = request.remote_addr
                    r = requests.post('http://'+ip+':5001/whoAreYou')
                    print("Master asking for info from" + ip)

                self.app.config['detectionEventQueue'].put(detectionEvent)
                return('good boy')
            except Exception as e:
                print(e)
                pass

        @self.app.route('/howAreYou')
        def health_check():
            health = "I'm fine!"
            return (health)


        @self.app.route('/terminate', methods=['POST'])
        def shut_it_down():
            func = request.environ.get('werkzeug.server.shutdown')
            func()

    def start(self):
        _thread.start_new_thread(self.app.run , ('0.0.0.0',5000))

    def terminate(self):
        r = requests.post('http://0.0.0.0:5000/terminate')

    def create_app(self):
        app = Flask(__name__)
        app.config['units'] = self.units
        app.config['detectionEventQueue'] = self.detectionEventQueue
        app.config['dbDir'] = self.dbDir
        return app

