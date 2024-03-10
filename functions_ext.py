import math
import numpy as np
import pandas as pd


def betae(a, teta2, b, teta3, c):
    H = np.sign(teta2) * a * math.sin(np.radians(teta2)) + b * math.sin(teta3)
    alpha = math.asin(H / c)
    beta = teta3 - alpha
    return beta


def tetae(teta, d, MM, MP, B):
    u = d + MM * math.cos(teta)
    v = MM * math.sin(teta)
    A = (B * B - MP * MP - u * u - v * v) / ((-2) * MP)
    A = -A / (math.sqrt(u * u + v * v))
    if abs(A) <= 1:
        if u > 0:
            phi = math.pi + math.atan(v / u) - math.acos(A)
        else:
            phi = math.atan(v / u) - math.acos(A)
    else:
        phi = 0
    if phi < 0:
        phi = 2 * math.pi + phi

    u = (-d + MP * math.cos(phi)) - (MM * math.cos(teta))
    v = (MP * math.sin(phi)) - (MM * math.sin(teta))

    if v > 0:
        teta = math.atan2(v, u)
    else:
        teta = 2 * math.pi + math.atan2(v, u)
    return teta


def saveListToExcel(listName, headerNames, path):
    try:
        ws_dict = pd.read_excel(path, sheet_name='Sheet1', usecols=headerNames)
    except FileNotFoundError:
        ws_dict = pd.DataFrame([], columns=headerNames)
    if len(listName) != len(headerNames):
        listName = np.zeros(len(headerNames))
    df = pd.DataFrame([listName], columns=headerNames)
    ws_dict = ws_dict.append(df, ignore_index=True)
    with pd.ExcelWriter(path) as writer:
        ws_dict.to_excel(writer)
        writer.save()


def isQuadrangle(a, b, c, d):
    return max(a, b, c, d) < a + b + c + d - max(a, b, c, d)


def optimizer(a, b, c, d, teta2start, teta2end):
    betaMax = 150.0
    betaMin = 180.0 - betaMax
    newConfiguration, omega, epsilon = [], [], []
    teta2prev, teta3prev = 0, 0
    i = 0
    omegaWorst = 0

    if not isQuadrangle(a, b, c, d):
        return newConfiguration, omega, epsilon

    teta3start = tetae(math.pi - np.radians(teta2start), d, a, c, b)
    step = 1 if teta2end > teta2start else -1

    for teta2 in np.arange(teta2start, teta2end + step, step):
        teta3 = tetae(math.pi - np.radians(teta2), d, a, c, b)
        beta = np.degrees(betae(a, teta2, b, teta3, c))
        angleOfA = teta2 - teta2start
        angleOfB = round(np.degrees(abs(teta3 - teta3start)), 1)
        newConfiguration = [a, b, c, d, angleOfA, angleOfB]
        if beta < betaMin or beta > betaMax:
            return newConfiguration, omega, epsilon
        if i > 0:
            omegaVar = (teta3 - teta3prev) / np.radians(teta2 - teta2prev)
            omega.append(omegaVar)
            omegaWorst = max(abs(omegaVar - 1), omegaWorst)
            if i > 1:
                epsilon.append((omega[-1] - omega[-2]) / np.radians(teta2 - teta2prev))
        teta2prev = teta2
        teta3prev = teta3
        i = i + 1
    return newConfiguration, omega, epsilon
