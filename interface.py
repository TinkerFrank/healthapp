"""Interface for health_app"""
# imports
import pickle
import logging
import pandas as pd
import sys

with open("state.bin", "rb") as f:
    reg = pickle.load(f)


def inputDigit(message, acceptableRange):
    inputStr = str()
    withinRange = False
    numberOfTries = 3
    i = 0

    while not (inputStr.isdigit() and withinRange) and i < numberOfTries:
        try:
            inputStr = input(message)

            if inputStr.isdigit():
                inputNum = float(inputStr)

                if inputNum in acceptableRange:
                    return inputNum
                else:
                    print('not in range:', acceptableRange)
            else:
                print('only whole numbers accepted')
            i += 1
        except:
            print("\nToo many tries, restart program to try again.")
        #trying to not show the error WIP

# range = min - 2*std and max + 2*std
genetic = float(inputDigit('Vul de genetische leeftijd in:', range(55, 110)))
length = float(inputDigit('Vul de lengte in centimeters in:', range(0, 220)))
mass = float(inputDigit(
    "Vul het lichaamsgewicht in hele kilo's in: ", range(0, 200)))
alcohol = float(inputDigit(
    "Vul het aantal glazen, alcohol per dag in: ", range(0, 10)))
sugar = float(inputDigit(
    "Vul het aantal suikerklontjes per dag in:", range(0, 15)))
smoking = float(inputDigit(
    "Vul het aantal sigaretten per dag in:", range(0, 36)))
exercise = float(inputDigit(
    "Vul het aantal uren beweging per dag in:", range(0, 7)))
divider = pow(length/100, 2) if length > 0 else None
bmi = round(mass/divider)
logging.debug(f'bmi: {bmi}')

data = {'genetic': genetic, 'length': [length], 'mass': [mass],
        'alcohol': [alcohol], 'sugar': [sugar],
        'smoking': [smoking], 'exercise': [exercise], 'bmi': [bmi]}

df = pd.DataFrame.from_dict(data)

lifespan_predict = reg.predict(df.values)
df['predict'] = lifespan_predict
print('lifespan_prediction:', lifespan_predict)
print(df.head())
