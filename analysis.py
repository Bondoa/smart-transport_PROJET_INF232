from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

def regression_cout_temps(data):
    df = pd.DataFrame(data)

    if len(df) < 2:
        return None

    X = df[["temps"]]
    y = df["cout"]

    model = LinearRegression()
    model.fit(X, y)

    return model


def classification_satisfaction(data):
    df = pd.DataFrame(data)

    if len(df) < 5:
        return None

    df["moyen"] = df["moyen"].astype("category").cat.codes

    X = df[["temps", "cout", "moyen"]]
    y = df["satisfaction"]

    model = DecisionTreeClassifier()
    model.fit(X, y)

    return model
