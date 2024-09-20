import cv2
import numpy as np
import os
import streamlit as st

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
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matchList = []
    finalVal = -1
    
    for des in desList:
        if len(des) == 0:  # Ignorer les images sans descripteurs
            matchList.append(0)
            continue

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

def matching_page():
    st.title("Détection et Reconnaissance de Cathéters")
    st.write("Cette application utilise OpenCV pour détecter et reconnaître des cathéters à partir d'une vidéo en direct.")

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
