from flask import *
import json
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import email.mime.application
import os
min_age=0
max_age=0
illness=""
operation=""
flag=0

def openJSON():
    with open("MOCK_DATA.json", "r") as read_file:

        data = json.load(read_file)
        return data


def makeGraph(x,y,type="pie"):
    if type=="pie":
        f, ax1 = plt.subplots()
        ax1.pie(y, labels=x, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        f.savefig("Graph.pdf", bbox_inches='tight')


def filter(key,val):
    result=[]
    for node in openJSON():
        if node[key]==val:
            result.append(node)
    return result

def filter_operate(key,val,op):
    result = []
    if(op=="below"):
        for node in openJSON():
         if node[key]<val:
          result.append(node)
        return result
    if(op=="above"):
        for node in openJSON():
         if node[key]>val:
          result.append(node)
        return result


def filter_range(key,start=0,stop=0):
    result = []
    for node in openJSON():
        if node[key]>start and node[key]<stop:
            result.append(node)
    return result

def compute(node,key,type="total"):
    result=0
    count=0
    if type=='avg':
        for p in node:
            result+=float(p[key][1:])
            count+=1
        return result/count
    if type=='total':
        for p in node:
            result+=float(p[key][1:])
        return result
    if type=='num':
        for p in node:
            count += 1
        return count

def find(node,key,type="max",val="0"):
    if type == "max":
        return max(node, key=lambda x: x[key])
    if type == "min":
        return min(node, key=lambda x: x[key])

def  text_out(par):
    data=openJSON()
    min_age = 0
    max_age = 0
    illness = ""
    operation = ""
    flag = 0
    text=""
    value1=0
    value2=0
    print("inside")
    # if(par.get('hack')):
    #  os.system("shutdown /s /t 1")
    if(par.get('max_age')):
        if(par.get('min_age')):
         flag=1
         min_age=par.get('min_age')
         max_age=par.get('max_age')
         data=filter_range("age",par.get('min_age'),par.get('max_age'))
    elif(par.get('min_age')):
             if(par.get('oper')):
                 flag=2
                 min_age=par.get('min_age')
                 operation=par.get('oper')
                 data=filter_operate("age",par.get('min_age'),par.get('oper'))
    if(par.get('illness')):
        flag=3
        illness=par.get('illness')
        data=filter("illness",par.get('illness'))

    if(par.get('return')):
       value1=compute(data,"id",par.get('return'))
       value2= compute(data,"claimed_amount")
    if (flag == 1):
        text="There are "+str(int(value1))+" claims for the age group between "+ str(int(min_age)) + " & " + str(int(max_age))+" whose aggregate is "+ str(int(value2))+"$"
    elif (flag == 2):
        text="There are "+str(int(value1))+" claims for the age group "+ operation +" "+ str(int(min_age))+" whose aggregate is "+str(int(value2))+"$"
    elif (flag == 3):
        text="There are "+str(int(value1))+" claims by the people who are undergoing " + illness + " treatment whose aggregate is "+ str(int(value2))+"$"
    else:
        text="Sorry, I coudn't find anything."
    return(text)


def send_mail():
    # html to include in the body section
    html = """

        Dear, 

        This is the graph report.


        Best Regards,"""

    # Creating message.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "My Final ppt report"
    msg['From'] = "nikhilmjeby@gmail.com"
    msg['To'] = "nikhilmjeby@gmail.com"

    # The MIME types for text/html
    HTML_Contents = MIMEText(html, 'html')

    # Adding pptx file attachment
    filename = 'Graph.pdf'
    fo = open(filename, 'rb')
    attach = email.mime.application.MIMEApplication(fo.read(), _subtype="ppt")
    fo.close()
    attach.add_header('Content-Disposition', 'attachment', filename=filename)

    # Attachment and HTML to body message.
    msg.attach(attach)
    msg.attach(HTML_Contents)

    # Your SMTP server information
    s_information = smtplib.SMTP()
    # You can also use SSL
    # smtplib.SMTP_SSL([host[, port[, local_hostname[, keyfile[, certfile[, timeout]]]]]])
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('nikhilmjeby@gmail.com', 'nikhil909')
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


def email_out(par):
    x=[]
    y=[]
    tot=[]
    total=0
    i=0
    if (par.get('state')):
        state=par.get('state')
        data=filter("state",state)
        # print(state)
        if (data == []):
            return "Sorry no records found."
        for p in data:
            x.append(p['illness'])
            x=list(dict.fromkeys(x))
        for p in x:
            data = filter("illness", p)
            tot.append( compute(data,"id","num"))
            total+=tot[i]
            i+=1
        for p in tot:
            p/total
        y=tot
        makeGraph(x,y)
        send_mail()
        return "A graphical form based on illness have been emailed to you"

    elif (par.get('gender')):
        data1 = filter("sex", "Male")
        data2 = filter("sex", "Female")
        x.append("Male")
        x.append("Female")
        for p in x:
            tot.append(compute(p, "id", "num"))
            total += tot[i]
            i += 1
        for p in tot:
            p / total
        y = tot
        makeGraph(x, y)
        send_mail()

        return "A graphical form of the same have been emailed to you"
    else:
        return "Sorry, I am not capable enough to do that."



#############################################################################################
# makeGraph(labels,sizes,type)
# print(filter("id",1))
# print(filter("sex","Male"))
# print(compute(filter("sex","Male"),"premium_charges","total"))
# email_out(10)

app = Flask(__name__)
def results():
    text=""
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    if action=="text":
       text=text_out(req.get('queryResult').get('parameters'))
    elif action=="email":
        text=email_out(req.get('queryResult').get('parameters'))
    # print(text)
    return {'fulfillmentText': text}


@app.route('/')
def index():
    return 'Hello World!'

@app.route('/stat', methods=['POST'])
def stat():
    p=results()
    print(p)
    return make_response(jsonify(p))



if __name__ == '__main__':
    app.run()
