
#TODO ADD SELL CAPABILITIES
#TODO ADD WAREHOUSE CHECK 
#CAPABILITIES
import time
import schedule
import actions
import datetime
import constants
import requests
import json
import sys
import os

DEBUG=0
FATAL=1
FLAGED=2
logger_= open("simlog","w+",buffering=1)
sheetIsOpen=False
creds=dict(email="",passwd="")


def get_buildings(session,headers):
    if logger_ != None:
        logger(DEBUG,"Fetching buildings")
        json_data=session.get("https://www.simcompanies.com/api/v2/players/me/buildings",headers=headers).json()
        
        # EXAMPLE DATA
        #[{"busy": {"canFetch": false, "duration": 170, "sales_order": {"kind": 4, 
        #"name": "Oranges", "image": "images/resources/oranges.png"}, "started": 
        #"2018-12-03T20:27:56.464459+00:00"}, "image": 
        #"images/landscape/grocery2-lvl2.png", "id": 199596, "size": 2, "name": "Grocery 
        #Store", "position": "1"}, {"image": "images/landscape/grocery2-lvl1.png", 
        #"position": "2", "size": 1, "name": "Grocery Store", "id": 206224}, {"image": 
        #"images/landscape/plantation-lvl1.png", "position": "3", "size": 2, "name": 
        #"Plantation", "id": 201202}, {"image": "images/landscape/plantation-lvl1.png", 
        #"position": "0", "size": 2, "name": "Plantation", "id": 199595}]

    return json_data

def cookie_fix(session,headers):
    session.get("https://www.simcompanies.com/landscape",headers=headers)#,headers=headers)
    return 0

def email_simcompany_login():
    if logger_ != None:
        logger(DEBUG,"Loging in")
        session = requests.Session()
        URL="https://www.simcompanies.com/api/v2/auth/email/auth/"
        EMAIL=creds["email"]
        PASSWORD=creds["passwd"]

        session.get("https://www.simcompanies.com/signin/")#verify=False)
        csrftoken= session.cookies['csrftoken'].strip()

        login_data = json.dumps(dict(email=EMAIL,password=PASSWORD,timezone_offset=480))
        cookies=dict(csrftoken=csrftoken)

        # no need to ever change these headers
        headers={"X-CSRFToken":csrftoken, "Host":"www.simcompanies.com", \
                "Referer":"https://www.simcompanies.com/", \
                "Connection":"keep-alive", \
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101  \
                Firefox/64.0","Content-Type":"application/json;charset=utf-8"}
        session.post(URL,data=login_data,headers=headers)#verify=False)verify=False, proxies=dict(http="http://localhost:8080",https="https://localhost:8080"
        #liar 
        headers["X-CSRFToken"]=session.cookies['csrftoken']
        cookie_fix(session,headers)
    else:
        return -1
    return session,headers

def take_unfinished(buildingid):
    if logger_ != None:
        pass

    return JSONDATA

def get_resource(session, headers, rid):
    if logger_ != None:
        logger(DEBUG,"Fetching prices for id: " + str(rid))
        json_data = session.get("https://www.simcompanies.com/api/market/"+str(rid))
        cookie_fix(session,headers)
    return json_data

def take_average(session,headers,rid):
    if logger_ != None:
        logger(DEBUG,"Taking averages for resource: "+str(rid))
        resource=rid
        data=core.get_resource(session,headers,resource)
        sum_=0
        sumq=0
        for i in range(0,10):
           sum_+=data[i]['price']
           sumq+=data[i]['quantity']
        avg_p=sum_/10
        avg_q=sumq/10
    return avg_p,avg_q

def buy_resource(session, headers, quantity, quality, price ,rid): # api/v2/market-order/take  order : {"price":0.335,"quality":0,"quantity":1,"resource":2}
    if logger_ != None:
        logger(DEBUG,"Buying " + str(quantity) + " of " + str(rid) + " at price of " + str(price) + " and at quality " + str(quality))
        cookie_fix(session,headers)
        data = json.dumps(dict(resource=rid,quantity=quantity,quality=quality,price=price))
        json_data_msg = session.post("https://www.simcompanies.com/api/v2/market-order/take",headers=headers , data=data)

        cookie_fix(session,headers)
    
    return json_data_msg # {"price": 1, "message": "You have bought 1 Water for $1"}


def calculate_price(json_market_list,quantity,rid):
    if logger_ != None:
        logger(DEBUG,"Calculating market price for "+ str(rid))
        price = 0
        quantity=quantity
        leftover=0
        for i in json_market_list:
            leftover=quantity - i['quantity']
            if leftover >= 0:
                price += (quantity - leftover) * i['price']
                quantity = leftover
            else:
                price += quantity * i['price']
                break
        
    return price

def take_average(session,headers,rid):
    resource=rid
    data=get_resource(session,headers,resource)
    sum_=0
    sumq=0
    for i in range(0,11):
       sum_+=data[i]['price']
       sumq+=data[i]['quantity']

    total=sum_/10
    totalq=sumq/10
    return total,totalq



def produce(session,headers,bid, resource,quantity):
    logger(DEBUG,"producing: "+str(resource)+" at quantity " + str(quantity) + " at building "+str(bid))
    page=session.get("https://www.simcompanies.com/b/"+str(bid)+"/",headers=headers).text
    csrfmiddlewaretoken=""
    for i in page.splitlines():
        if "csrf" in i and "input" not in i:
            csrfmiddlewaretoken=i.split("'")[3]
            break # prevents setting again
    if csrfmiddlewaretoken != "":
        data_=dict(csrfmiddlewaretoken=csrfmiddlewaretoken,resource=resource,quantity=quantity)
        tmp = headers
        tmp["Content-Type"]="application/x-www-form-urlencoded"
        session.post("https://www.simcompanies.com/production-order/"+str(bid)+"/",headers=tmp,data=data_)
            #verify=False, proxies=dict(http="http://localhost:8080",https="https://localhost:8080"))
        cookie_fix(session,headers)
    else:
        return -1
    return 0
def sell(session,headers,bid,resource,quantity,price):
    logger(DEBUG,"Selling: " + str(resource) + " at quantity " + str(quantity) + " at building " +str(bid))
    page=session.get("https://www.simcompanies.com/b/"+str(bid)+"/",headers=headers).text
    for i in page.splitlines():
        if "csrf" in i and "input" not in i:
            csrfmiddlewaretoken=i.split("'")[3]
            break # prevents setting again
    if csrfmiddlewaretoken != "":
        data_=dict(csrfmiddlewaretoken=csrfmiddlewaretoken,resource=resource,quantity=quantity,price=price)
        tmp = headers
        tmp["Content-Type"]="application/x-www-form-urlencoded"
        session.post("https://www.simcompanies.com/sales-order/"+str(bid)+"/",headers=tmp,data=data_)
        cookie_fix(session,headers)
    return 0
def sell_market(session,headers,rid,price,qunatity): #THSI RID IS PRODUCED RANDOMLY CONSULT THE GET_WAREHOUSE DATA
    logger(DEBUG,"Selling to market resource " +str(rid) + " at price " + str(price) + " at quantity " +quantity) 
    page = session.get("https://www.simcompanies.com/warehouse/",headers=headers).text
    for i in page.splitlines():
        if "csrf" in i and "input" not in i:
            csrfmiddlewaretoken=i.split("'")[3]
            break # prevents setting again
    if csrfmiddlewaretoken != "":
        data_=dict(csrfmiddlewaretoken=csrfmiddlewaretoken,resourceId=rid,quantity=quantity,price=price)
        tmp = headers
        tmp["Content-Type"]="application/x-www-form-urlencoded"
        session.post("https://www.simcompanies.com/api/v2/market-order/",headers=tmp,data=data_)
        cookie_fix(session,headers)

def sell_contract(session,headers,rid,price,quantity,contractTo): #THSI RID IS PRODUCED RANDOMLY CONSULT THE GET_WAREHOUSE DATA
    logger(DEBUG,"Selling to contract resource " +str(rid) + " at price " + 
            str(price) + " at quantity " +quantity + " to " +contractTo) 
    page = session.get("https://www.simcompanies.com/warehouse/",headers=headers).text
    for i in page.splitlines():
        if "csrf" in i and "input" not in i:
            csrfmiddlewaretoken=i.split("'")[3]
            break # prevents setting again
    if csrfmiddlewaretoken != "":
        data_=dict(csrfmiddlewaretoken=csrfmiddlewaretoken,resourceId=rid,quantity=quantity,
                price=price,contractTo=contractTo.replace(" ","+")) # Be SURE TO CHECK THE PROPER CAPILIZATION
                                                                    # YOU DO THIS BY CHECKING CONTARCTS WHEN 
                                                                    # ENTERING THE COMPANY NAME
        tmp = headers
        tmp["Content-Type"]="application/x-www-form-urlencoded"
        session.post("https://www.simcompanies.com/api/v2/market-order/",headers=tmp,data=data_)
        cookie_fix(session,headers)


def get_warehouse(session,headers):
    logger(DEBUG,"Fetching resources at warehouse")
    # To View the json data reference 
    # just print it in a console or something
    json_data = session.get("https://www.simcompanies.com/api/resource",headers=headers).json()
    cookie_fix(session,headers)
    return json_data

############################TODO#################################
def op_sheet(path,context):
    if logger != None:
        pass
    
    return sheet

#writing to sheets will be handled by actions

def save(sheet,context):
    if logger != None:
        pass

    return 0
#################################################################

def logger(type_,message):
    end=""
    if type_ == DEBUG:
        prt1="[DEBUG " + str(datetime.datetime.now())+ "] "
    elif type_ == FATAL:
        prt1= "[FATAL "+ str(datetime.datetime.now())+ "] "
    elif type_ == FLAGED:
        prt1 = "[FLAGED "+ str(datetime.datetime.now())+ "] "
    else:
        return -1

    end = prt1 + message +"\n"
    logger_.write(end)
    logger_.flush()
    return 0 


# TODO ADD FUNCTION AVALIBILITY CHECKING AND 
# VERIFICATION OF EXISTENCE. IF FUNCTIONS IN
# ACTIONS.PY ARE IN CONFIG AND IF FUNCTIONS
# ARE AVALIBLE (EXIST) IN ACTIONS.PY
def triggers(functions):
    # configure file editing and parseing
    logger(DEBUG,"parsing function.config")
    tmp=open("function.config","r+",buffering=1)
    atmp=open("function.config","a",buffering=1)
    body=tmp.read()
    for j in functions: # add any new actions
        if j not in body:
            logger(DEBUG,"adding new function to config")
            atmp.write(j + " 0:00" + " no\n") # FUNC 0:00 yes/no
            atmp.flush()
            body+=j + " 0:00" + " no\n"

    for i in body.splitlines():
        for k in dir(actions):
            if k in i and "yes" in i:
                function=getattr(actions,i.split(" ")[0])
                solid_time=i.split(" ")[1]
                logger(DEBUG,"Set schedule for funciton")   #TODO FiX LOGGING
                schedule.every().day.at(solid_time).do(function)


def main():
    # parsing of possible actions
    logger_= open("simlog","w+",buffering=1)
    logger(DEBUG,"Opened Log")
    function_list=[]
    tmp=open("./actions.py","r")
    logger(DEBUG,"Parsing actions.py")
    body=tmp.read()
    tmp.close()
    body=body.split("\n")
    for i in body:
        if "def" in i:
            i=i.split("def")[1]
            i=i.split("(")[0]
            function_list.append(i.strip())
    
    triggers(function_list);

    while True:
        time.sleep(10)
        schedule.run_pending()


