import streamlit as st

# Dictionnaire contenant les descriptions des cathéters, sans le cathéter Foley
catheters = {
    "midline": "Un cathéter à mi-chemin est inséré dans une veine périphérique, généralement dans le bras, avec l'extrémité positionnée à un point intermédiaire, entre une veine périphérique et une veine centrale. Il est utilisé pour l'administration de médicaments et de fluides sur une période modérée (1 à 4 semaines).",
    "hub": "Le terme 'Hub' fait référence à l'embout ou à la connexion d'un cathéter qui permet d'attacher des seringues ou des tubes de perfusion. Les cathéters Hub sont souvent des cathéters veineux centraux (CVC) utilisés pour l'accès veineux à long terme, notamment pour l'administration de médicaments, la nutrition parentérale, ou la prise de sang.",
    "hickman": "Un cathéter veineux central implanté chirurgicalement, souvent utilisé pour l'administration de médicaments ou la chimiothérapie sur une longue durée. Il possède plusieurs voies qui permettent des infusions multiples ou la prise de sang simultanée.",
    "port-a-cath": "Un cathéter veineux central avec un port implanté sous la peau. Il est utilisé pour l'accès veineux à long terme, comme la chimiothérapie ou les perfusions régulières, et est moins visible et plus confortable pour les patients car le port est entièrement sous la peau."
}

def chatbot_page():
    st.title("Chatbot Médical - Questions/Réponses sur les Cathéters")

    # Fonction pour afficher la réponse basée sur la question de l'utilisateur
    def chatbot_response(user_input):
        user_input = user_input.lower()
        if "midline" in user_input:
            return catheters["midline"]
        elif "hub" in user_input:
            return catheters["hub"]
        elif "hickman" in user_input:
            return catheters["hickman"]
        elif "port" in user_input or "port-à-cath" in user_input:
            return catheters["port-a-cath"]
        else:
            return "Désolé, je n'ai pas d'information sur ce type de cathéter. Veuillez essayer avec un autre terme."

    # Saisie de l'utilisateur
    st.write("Posez votre question sur les cathéters, par exemple: 'Qu'est-ce qu'un cathéter Midline?'")

    user_question = st.text_input("Votre question:")

    # Afficher la réponse du chatbot
    if user_question:
        response = chatbot_response(user_question)
        st.write("**Réponse du Chatbot:**")
        st.write(response)
