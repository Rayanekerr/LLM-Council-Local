import streamlit as st
import time
import requests
from council_logic import run_council

st.set_page_config(page_title="LLM Council Local", layout="wide")

# Sidebar avec Health Check dynamique
with st.sidebar:
    st.header("Statut du Système")
    try:
        res = requests.get("http://localhost:11434/", timeout=5)
        if res.status_code == 200:
            st.success("Ollama : Connecté ✅")
        else:
            st.warning("Ollama : Statut instable ⚠️")
    except:
        st.error("Ollama : Déconnecté ❌")

    st.info("**Membres du Conseil :**\n- Llama 3.2 (1b)\n- Phi 4 Mini\n- Chairman: Llama 3.1 (8b)")

st.title("🏛️ Conseil Local des LLM")
query = st.text_input("Posez votre question au conseil :", placeholder="Ex: Quel est l'avenir de l'IA locale ?")

if st.button("Lancer la délibération ") and query:
    start_time = time.time()

    with st.status("Travail du conseil en cours...", expanded=True) as status:
        st.write("Étape 1 : Récolte des opinions...")
        responses, reviews, final_ans = run_council(query)
        st.write("Étape 2 : Analyse croisée terminée.")
        st.write("Étape 3 : Synthèse finale du Président...")
        status.update(label="Délibération terminée !", state="complete")

    # Affichage par onglets
    tab1, tab2, tab3 = st.tabs([" Opinions Initiales", " Critiques", " Synthèse Finale"])

    with tab1:
        cols = st.columns(len(responses))
        for i, (model, text) in enumerate(responses.items()):
            with cols[i]:
                st.subheader(f"Modèle : {model}")
                st.info(text)

    with tab2:
        st.subheader("Analyse détaillée par modèle")
        # On sépare les critiques pour l'affichage
        for critique in reviews.split("Critique de "):
            if critique.strip():
                parts = critique.split(":", 1)
                name = parts[0]
                content = parts[1] if len(parts) > 1 else ""
                with st.expander(f"Analyse de {name}"):
                    st.write(content)

    with tab3:
        st.header("Résultat Final du Président")
        st.success(final_ans)
        st.caption(f"Temps de traitement : {round(time.time() - start_time, 2)}s")