"""Interface for health_app"""
# imports
import pickle
import logging
import pandas as pd

with open("state.bin", "rb") as f:
    reg = pickle.load(f)


def inputDigit(message, acceptableRange):
    inputStr = str()
    withinRange = False
    numberOfTries = 3
    i = 0

    while not (inputStr.isdigit() and withinRange) and i < numberOfTries:
        inputStr = input(message)

        if inputStr.isdigit():
            inputNum = float(inputStr)

            if inputNum in acceptableRange:
                return inputNum

        i += 1

acceptableRange = range(18, 118)
age = int(inputDigit("Age: ", acceptableRange))
logging.debug(f"age : {age}")

genetic = float(inputDigit('Vul de genetische leeftijd in:', acceptableRange=()))
length = float(input('Vul de lengte in centimeters in: ')) 
mass = float(input ("Vul het lichaamsgewicht in hele kilo's in: "))
alcohol = float(input("Vul het aantal glazen alcohol per dag in: "))
sugar = float(input("Vul het aantal suikerklontjes per dag in: "))
smoking = float(input("Vul het aantal sigaretten per dag in: "))
exercise = float(input("Vul het aantal uren beweging per dag in: "))
divider = pow(length/100, 2) if length >0 else None
bmi = round(mass/divider)
logging.debug(f'bmi: {bmi}')

data = {'genetic': genetic, 'length':[length],'mass': [mass], 
                                 'alcohol': [alcohol], 'sugar': [sugar], 
                                 'smoking': [smoking], 'exercise': [exercise], 'bmi': [bmi]}

df = pd.DataFrame.from_dict(data)

lifespan_predict = reg.predict(df.values)
df['predict']=lifespan_predict
print('lifespan_prediction:',lifespan_predict)
print(df.head())

