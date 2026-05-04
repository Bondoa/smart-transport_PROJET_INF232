from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from analysis import regression_cout_temps
from database import create_table, get_connection
from analysis import classification_satisfaction
import pandas as pd

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

create_table()
# Stockage temporaire
data = []

class TransportData(BaseModel):
    nom: str
    depart: str
    arrivee: str
    moyen: str
    temps: float
    cout: float
    satisfaction: int

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/submit")
async def submit(data_input: TransportData):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transport (nom, depart, arrivee, moyen, temps, cout, satisfaction)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data_input.nom,
        data_input.depart,
        data_input.arrivee,
        data_input.moyen,
        data_input.temps,
        data_input.cout,
        data_input.satisfaction
    ))

    conn.commit()
    conn.close()

    return {"message": " ✅ Données enregistrées avec succes dans la base"}

@app.get("/stats")
async def stats():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM transport", conn)
    conn.close()

    if df.empty:
        return {"message": "Pas de données"}

    group = df.groupby("moyen").mean(numeric_only=True)

    return {
        "cout_moyen": df["cout"].mean(),
        "temps_moyen": df["temps"].mean(),
        "satisfaction_moyenne": df["satisfaction"].mean(),
        "labels": list(group.index),
        "couts": list(group["cout"]),
        "temps": list(group["temps"]),
        "satisfactions": list(group["satisfaction"])
    }
    
@app.get("/predict")
async def predict(temps: float):
    import pandas as pd

    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM transport", conn)
    conn.close()

    # 🔥 sécurité
    if df.empty or len(df) < 2:
        return {"message": "Pas assez de données pour prédire"}

    model = regression_cout_temps(df.to_dict(orient="records"))

    if model is None:
        return {"message": "Modèle non disponible"}

    prediction = model.predict([[temps]])

    return {
        "temps": temps,
        "cout_estime": float(prediction[0])
    }
    
    
@app.get("/classify")
async def classify(temps: float, cout: float, moyen: int):

    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM transport", conn)
    conn.close()

    model = classification_satisfaction(df.to_dict(orient="records"))

    if model is None:
        return {"message": "Pas assez de données"}

    prediction = model.predict([[temps, cout, moyen]])

    return {
        "satisfaction_predite": int(prediction[0])
    }
