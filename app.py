import json
import start
import launch_sites

from flask import Flask
from flask import request

app = Flask(__name__)

#returns json of names + coordinats
@app.route('/list')
def getList():
   list = {'jumpPoints':[]}
   for i in l:
      pom = l.get(i)
      list.get('jumpPoints').append({i: {'lon': pom.get('lon'), 'lan': pom.get('lan')}})
   return json.dumps(list)

#returns json of data for given name + coordinats
@app.route('/data',methods=['GET', 'POST'])
def getData():
   name = request.args["name"]
   x = request.args["x"]
   y = request.args["y"]
   t = start(name,x,y) ### un l se more al v uno start dodat al pa v konstruktor, ker 'ok' wind thing??
   jumpPoint = {
      "WindSpeed": t.getWindSpeed(),
      "WindBust": t.getWindBust(),
      "WindDirection": t.getWindDirection(),
      "Temperature": t.getTemperature(),
      "TimeAndDate": t.getTimeAndDate(),
      "isWindGood": t.isWindGood()
   }
   return json.dumps(jumpPoint)


#run() - runs the application on the local development server.
#app.run([host, port, debug, options])
# host - Hostname to listen on. Defaults to 127.0.0.1 (localhost).
#        Set to ‘0.0.0.0’ to have server available externally
# port - defaults to 5000
if __name__ == '__main__':
   app.run()




