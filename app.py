import streamlit as st
import time
import requests
from council_logic import run_council

# 1. Configuration de la page
st.set_page_config(page_title="LLM Council Local", layout="wide")

# 2. Gestion du Thème
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'


def set_theme():
    if st.session_state.theme == 'Dark':
        st.markdown("""
            <style>
            .stApp { background-color: #0E1117; color: white; }
            .stMarkdown, .stSubheader { color: #E0E0E0; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp { background-color: #FFFFFF; color: black; }
            .stMarkdown, .stSubheader { color: #31333F; }
            </style>
        """, unsafe_allow_html=True)


# 3. Sidebar avec Health Check et Sélecteur de Thème
with st.sidebar:
    st.header("Paramètres & Statut")

    # Toggle Thème
    st.session_state.theme = st.selectbox("Apparence", ["Dark", "Light"])
    set_theme()

    st.markdown("---")

    try:
        res = requests.get("http://localhost:11434/", timeout=5)
        if res.status_code == 200:
            st.success("Ollama : Connecté ✅")
        else:
            st.warning("Ollama : Statut instable ⚠️")
    except:
        st.error("Ollama : Déconnecté ❌")

    st.info("**Membres du Conseil :**\n- Llama 3.2 (1b)\n- Phi 4 Mini\n- Chairman: Llama 3.1 (8b)")

# 4. Interface Principale
st.title(" Conseil Local des LLM")
st.markdown("*Système collaboratif multi-IA distribué*")

query = st.text_input("Posez votre question au conseil :", placeholder="Ex: Quel est l'avenir de l'IA locale ?")

if st.button("Lancer la délibération") and query:
    start_time = time.time()

    with st.status("Travail du conseil en cours...", expanded=True) as status:
        st.write("Étape 1 : Récolte des opinions (Stage 1)...")
        responses, reviews, final_ans = run_council(query)

        st.write("Étape 2 : Revue par les pairs (Stage 2)...")
        time.sleep(1)  # Petit délai pour l'effet visuel

        st.write("Étape 3 : Synthèse finale du Président (Stage 3)...")
        status.update(label="Délibération terminée !", state="complete")

    # 5. Affichage par onglets (Requirement)
    tab1, tab2, tab3 = st.tabs(["Opinions Initiales", "Critiques", "Synthèse Finale"])

    with tab1:
        st.subheader("Réponses brutes des conseillers")
        cols = st.columns(len(responses))
        for i, (model, text) in enumerate(responses.items()):
            with cols[i]:
                st.markdown(f"**Modèle : `{model}`**")
                st.info(text)

    with tab2:
        st.subheader("Analyse croisée des modèles")
        for critique in reviews.split("Critique de "):
            if critique.strip():
                parts = critique.split(":", 1)
                model_name = parts[0].strip()
                content = parts[1].strip() if len(parts) > 1 else ""


                cleaned_content = content.lstrip("1b:").lstrip("mini:").strip()

                with st.expander(f"Analyse faite par {model_name}"):
                    st.write(cleaned_content)

    with tab3:
        st.header(" Résultat Final du Président")
        st.success(final_ans)

        # Statistiques de performance (Bonus)
        duration = round(time.time() - start_time, 2)
        st.markdown(f"**Temps de traitement :** `{duration}s` | ** Mode :** `Local Inference`")