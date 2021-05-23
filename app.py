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
   for i in launch_sites.l:
      pom = launch_sites.l.get(i)
      list.get('jumpPoints').append({i: {'lon': pom.get('lon'), 'lan': pom.get('lan')}})
   return json.dumps(list)

#returns json of data for given name + coordinats
@app.route('/data',methods=['GET', 'POST'])
def getData():
   name = request.args["name"]
   atributes = launch_sites.l.get(name)
   x = atributes.get('lon')
   y = atributes.get('lat')
   ok = atributes.get('ok')
   t = start(name, x, y, ok)
   jumpPoint = {
      "WindSpeed": t.getWindSpeed, #double
      "WindBust": t.getWindBust(), #double
      "WindDirection": t.getWindDirection(), #chat or str
      "Temperature": t.getTemperature(), #double
      "TimeAndDate": t.getTimeAndDate(), #date
      "isWindGood": t.isWindGood() #T/F
   }
   return json.dumps(jumpPoint)


#run() - runs the application on the local development server.
#app.run([host, port, debug, options])
# host - Hostname to listen on. Defaults to 127.0.0.1 (localhost).
#        Set to ‘0.0.0.0’ to have server available externally
# port - defaults to 5000
if __name__ == '__main__':
   app.run()





