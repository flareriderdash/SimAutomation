import time
import json
import core
import constants
#mew

# THERE ARE ASSUMPTIONS MADE BY THIS FUNCTION
# THAT MAY NOT BE BENEFITAIAL IF ALLOWED TO 
# BE MADE UNNOTICED


#################### BEFORE RUNNING ##################
#
#   THESE FUNCTIONS WILL NOT RUN UNTIL THE ASSIGED TIME
#   THEREFORE:
#
# - ALWAYS CHECK YOUR VARIABLE NAMES
# - ALWAYS CHECK YOUR LOGIC
# - FILL IN ANY MISSING SEMICOLONS
# - ALWAYS CHECK FROR CORRECT CONTEXT (ex. core.logger not logger)
# - ALWAYS FAMILIARIZE YOURSELF THE JSON RESPONSE
# - ALWAYS CHECK YOUR PARAMETERS
#################### BEFORE RUNNING ##################

def oranges_produce():
    core.logger(core.DEBUG,"Running function oranges_produce")
    quantity=[3830,3829]
    session,headers=core.email_simcompany_login()

    # ALL NECESSARY FOR PRODUCTION
    total_quantity=0
    for q in quantity:
        total_quantity += q
    water_resource_data=core.get_resource(session,headers,constants.WATER)
    water_price=core.calculate_price(water_resource_data,(total_quantity*3),constants.WATER)
    seeds_resource_data=core.get_resource(session,headers,constants.SEEDS)
    seeds_price=core.calculate_price(seeds_resource_data,total_quantity,constants.SEEDS)
    core.buy_resource(session,headers,(total_quantity*3),0,water_price,constants.WATER)
    core.buy_resource(session,headers,total_quantity,0,seeds_price,constants.SEEDS)

    buildings=core.get_buildings(session,headers)
    if type(quantity) == list:
        for amount in quantity:
            for i in buildings:
                try:
                    tmp=i['busy']
                    continue
                except KeyError:
                    if i['name'] == "Plantation":
                        bid=i['id']
                        core.produce(session,headers,bid,constants.ORANGES,amount)


def oranges_sell():
    core.logger(core.DEBUG,"Running function oranges_sell")
    quantity=[5106,2553]
    price=4
    session,headers=core.email_simcompany_login()

    buildings=core.get_buildings(session,headers)
    for amount in quantity:
        for i in buildings:
            try:
                tmp=i['busy']
                continue
            except KeyError:
                if i['name'] == "Grocery Store":
                    bid=i['id']
                    core.sell(session,headers,bid,constants.ORANGES,amount,price)

def processor_produce():
    quantity=[220]
    core.logger(core.DEBUG,"Running processor produce")
    session,headers=core.email_simcompany_login()
    total_quantity=0
    for q in quantity:
        total_quantity +=q
    chem_data=core.get_resource(session,headers,constants.CHEMICALS)
    silicon_data=core.get_resource(session,headers,constants.SILICON)
    transport_data=core.get_resource(session,headers,constants.TRANSPORT)

    chem_price=core.calculate_price(chem_data,total_quantity,constants.CHEMICALS)
    silicon_price=core.calculate_price(silicon_data,(total_quantity*4),constants.SILICON)
    transport_price=core.calculate_price(transport_data,total_quantity,constants.TRANSPORT)

    core.buy_resource(session,headers,total_quantity,0,chem_price,constants.CHEMICALS)
    core.buy_resource(session,headers,(total_quantity*4),0,silicon_price,constants.SILICON)
    core.buy_resource(session,headers,total_quantity,0,transport_price,constants.TRANSPORT)

    buildings=core.get_buildings(session,headers)
    for amount in quantity:
        for i in buildings:
            try:
                tmp=i['busy']
                continue
            except KeyError:
                if i['name'] == "Electronics factory":
                    bid=i['id']
                    core.produce(session,headers,bid,constants.PROCESSORS,amount)
