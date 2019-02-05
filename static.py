from flask import *
import json
import matplotlib.pyplot as plt

labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

f, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
f.savefig("foo.pdf", bbox_inches='tight')

with open("MOCK_DATA.json", "r") as read_file:
    data = json.load(read_file)
    for person in data:
        if person["id"]==10:
             print(person["email"])


app = Flask(__name__)
def results():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    zone = req.get('queryResult').get('parameters').get('bank_name')
    cost = {'Federal Bank':'6.85%', 'Allahabad Bank':'6.75%'}
    speech = "The interest rate of " + zone + " is " + str(cost[zone])
    return {'fulfillmentText': speech}

@app.route('/static_res', methods=['POST'])

def static_res():
    return make_response(jsonify(results()))

if __name__ == '__main__':
    app.run()