import streamlit as st
import cv2
import numpy as np
import os

# Configuration de l'ORB avec plus de caractéristiques détectées
orb = cv2.ORB_create(nfeatures=3000)

# Chemin vers le dossier contenant les images des cathéters
path = 'C:/Users/user/Desktop/staage/train'
images = []
classNames = []

# Chargement des images et des noms de classes
myList = os.listdir(path)
for cl in myList:
    imgCur = cv2.imread(f'{path}/{cl}', 0)
    if imgCur is not None:
        images.append(imgCur)
        classNames.append(os.path.splitext(cl)[0])
    else:
        st.write(f"Erreur de chargement de l'image: {cl}")

# Fonction pour trouver les descripteurs de toutes les images
def findDes(images):
    desList = []
    for img in images:
        kp, des = orb.detectAndCompute(img, None)
        if des is not None:
            desList.append(des)
        else:
            desList.append([])  # Ajouter une liste vide si aucun descripteur n'est trouvé
    return desList

# Fonction améliorée pour identifier l'image à partir des descripteurs
def findID(img, desList, thres=15):
    kp2, des2 = orb.detectAndCompute(img, None)
    
    if des2 is None:  # Si aucun descripteur n'est trouvé, renvoyer -1
        return -1

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matchList = []
    finalVal = -1
    
    for des in desList:
        if len(des) == 0:  # Ignorer les images sans descripteurs
            matchList.append(0)
            continue

        # Assurez-vous que les descripteurs sont du même type
        if des.dtype != des2.dtype:
            des2 = des2.astype(des.dtype)

        matches = bf.match(des, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        good_matches = [m for m in matches if m.distance < 50]  # Utilisation d'un seuil plus strict pour la distance
        matchList.append(len(good_matches))
    
    if len(matchList) != 0:
        if max(matchList) > thres:
            finalVal = matchList.index(max(matchList))
    
    return finalVal

# Initialisation des descripteurs
desList = findDes(images)

# Titre et logo
st.sidebar.image("logo.jpeg", width=200)  # Remplacez par le chemin de votre logo
st.sidebar.title("Navigation")

# Navigation entre les pages
page = st.sidebar.selectbox("Navigateur", ["Accueil", "Matching", "Chatbot"])

if page == "Accueil":
    st.header("Page d'Accueil")
    st.write("Bienvenue dans l'application de détection et reconnaissance des cathéters.")
    st.write("Voici quatre images représentatives :")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image('Midline-Catheter.jpg', caption='Midline-Catheter', width=150)
    with col2:
        st.image('cathater hub.jpeg', caption='Hub-Catheter', width=150)
    with col3:
        st.image('hickman.jpeg', caption='Hickman-Catheter', width=150)
    with col4:
        st.image('portacath.jpg', caption='Portacath-Catheter', width=150)

elif page == "Matching":
    st.header("Matching d'Images")
    st.write("Cette section utilise OpenCV pour détecter et reconnaître des cathéters à partir d'une vidéo en direct.")
    
    start_video = st.button("Démarrer la Capture Vidéo")

    if start_video:
        # Utilisation de la caméra
        cap = cv2.VideoCapture(0)
        
        stframe = st.empty()  # Placeholder pour les images de la vidéo

        while cap.isOpened():
            success, img2 = cap.read()
            if not success:
                st.write("Impossible d'accéder à la caméra.")
                break
            
            imgOriginal = img2.copy()
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            id = findID(img2, desList)
            
            if id != -1:
                cv2.putText(imgOriginal, classNames[id], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(imgOriginal, "Inconnu", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            
            # Conversion pour l'affichage Streamlit
            imgOriginal = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2RGB)
            stframe.image(imgOriginal, channels="RGB")
        
        cap.release()
        cv2.destroyAllWindows()

elif page == "Chatbot":
    st.header("Chatbot Médical - Questions/Réponses sur les Cathéters")
    
    catheters = {
        "midline": "Un cathéter à mi-chemin est inséré dans une veine périphérique, généralement dans le bras, avec l'extrémité positionnée à un point intermédiaire, entre une veine périphérique et une veine centrale. Il est utilisé pour l'administration de médicaments et de fluides sur une période modérée (1 à 4 semaines).",
        "hub": "Le terme 'Hub' fait référence à l'embout ou à la connexion d'un cathéter qui permet d'attacher des seringues ou des tubes de perfusion. Les cathéters Hub sont souvent des cathéters veineux centraux (CVC) utilisés pour l'accès veineux à long terme, notamment pour l'administration de médicaments, la nutrition parentérale, ou la prise de sang.",
        "hickman": "Un cathéter veineux central implanté chirurgicalement, souvent utilisé pour l'administration de médicaments ou la chimiothérapie sur une longue durée. Il possède plusieurs voies qui permettent des infusions multiples ou la prise de sang simultanée.",
        "port-a-cath": "Un cathéter veineux central avec un port implanté sous la peau. Il est utilisé pour l'accès veineux à long terme, comme la chimiothérapie ou les perfusions régulières, et est moins visible et plus confortable pour les patients car le port est entièrement sous la peau."
    }

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
