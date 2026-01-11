import requests
import datetime

# Configuration (Inchangée)
COUNCIL_MEMBERS = ["llama3.2:1b", "phi4-mini"]
CHAIRMAN_MODEL = "llama3.1:8b"
OLLAMA_URL = "http://localhost:11434/api/generate"


def log_terminal(message):
    """Affiche un message horodaté dans la console PyCharm"""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [LLM_COUNCIL] {message}")


def ask_llm(model, prompt):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        log_terminal(f"Appel du modèle : {model}...")
        response = requests.post(OLLAMA_URL, json=payload, timeout=None)
        log_terminal(f"Réponse reçue de {model} ✅")
        return response.json().get("response", "Erreur : Réponse vide")
    except Exception as e:
        log_terminal(f"❌ Erreur sur {model} : {e}")
        return f"Erreur de connexion : {e}"


def run_council(user_query):
    log_terminal("--- DÉBUT DE LA DÉLIBÉRATION ---")

    # STAGE 1 : Opinions
    log_terminal("Étape 1 : Collecte des avis initiaux...")
    responses = {}
    for model in COUNCIL_MEMBERS:
        responses[model] = ask_llm(model, user_query)

    # STAGE 2 : Review (Anonymisée)
    log_terminal("Étape 2 : Lancement des critiques croisées...")
    reviews = ""
    for model in COUNCIL_MEMBERS:
        other_resp = "\n".join([f"- {v}" for k, v in responses.items() if k != model])
        review_prompt = f"En tant qu'expert, analyse ces réponses à la question '{user_query}' et donne une critique constructive :\n{other_resp}"
        review_text = ask_llm(model, review_prompt)
        reviews += f"Critique de {model}:\n{review_text}\n\n"

    # STAGE 3 : Chairman
    log_terminal("Étape 3 : Synthèse finale par le Chairman...")
    context = f"Question: {user_query}\n\n"
    for m, r in responses.items():
        context += f"Réponse de {m}: {r}\n\n"
    context += f"Critiques du conseil:\n{reviews}"

    chairman_prompt = f"Synthétise ces travaux en une réponse finale structurée et donne une note globale :\n{context}"
    final_answer = ask_llm(CHAIRMAN_MODEL, chairman_prompt)

    log_terminal("--- FIN DU PROCESSUS ---")
    return responses, reviews, final_answer