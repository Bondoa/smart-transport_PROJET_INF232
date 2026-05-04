document.getElementById("form").addEventListener("submit", async function(e){
    e.preventDefault(); // ⚠️ empêche le rechargement

    const data = {
        nom: document.getElementById("nom").value,
        depart: document.getElementById("depart").value,
        arrivee: document.getElementById("arrivee").value,
        moyen: document.getElementById("moyen").value,
        temps: parseFloat(document.getElementById("temps").value),
        cout: parseFloat(document.getElementById("cout").value),
        satisfaction: parseInt(document.getElementById("satisfaction").value)
    };

    const res = await fetch("/submit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();

    alert(result.message); // ✅ message du serveur
});


// 🔥 2. AFFICHER LES STATISTIQUES
async function loadStats(){
    const res = await fetch("/stats");
    const data = await res.json();

    document.getElementById("stats").innerHTML =
        "<b>Coût moyen :</b> " + data.cout_moyen + " FCFA<br>" +
        "<b>Temps moyen :</b> " + data.temps_moyen + " minutes<br>" +
        "<b>Satisfaction :</b> " + data.satisfaction_moyenne;

    const ctx = document.getElementById('chart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                { label: 'Coût', data: data.couts },
                { label: 'Temps', data: data.temps },
                { label: 'Satisfaction', data: data.satisfactions }
            ]
        }
    });
}


// 🔥 3. PRÉDICTION DU COÛT
async function predict(){
    const temps = document.getElementById("temps_prediction").value;

    if(!temps){
        alert("❌ Entrer un temps !");
        return;
    }

    try {
        const res = await fetch(`/predict?temps=${temps}`);
        const data = await res.json();

        console.log("Réponse backend :", data); // 🔍 DEBUG

        if(data.message){
            document.getElementById("resultat_prediction").innerHTML = data.message;
        } else if(data.cout_estime !== undefined){
            document.getElementById("resultat_prediction").innerHTML =
                "💰 Coût estimé : " + data.cout_estime + " FCFA";
        } else {
            document.getElementById("resultat_prediction").innerHTML =
                "❌ Erreur de prédiction";
        }

    } catch (error) {
        console.error(error);
        alert("Erreur serveur ❌");
    }
}
async function classify(){
    const temps = document.getElementById("temps_class").value;
    const cout = document.getElementById("cout_class").value;
    const moyen = document.getElementById("moyen_class").value;

    if(!temps || !cout){
        alert("❌ Remplir tous les champs !");
        return;
    }

    try {
        const res = await fetch(`/classify?temps=${temps}&cout=${cout}&moyen=${moyen}`);

        if(!res.ok){
            throw new Error("Erreur serveur");
        }

        const data = await res.json();

        document.getElementById("resultat_classification").innerHTML =
            data.message ? data.message :
            "⭐ Satisfaction prédite : " + data.satisfaction_predite;

    } catch (error) {
        console.error(error);
        alert("Erreur classification ❌");
    }
}
