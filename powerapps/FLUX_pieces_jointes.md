# Pièces jointes : le flux Power Automate `AjoutPJ_CODECOH`

## Pourquoi un flux ?
Power Apps ne sait pas envoyer de fichiers à SharePoint avec `Patch` depuis l'écran multi-échantillons (erreur « Table (Attachment) »).
La méthode fiable est donc la suivante :
1. L'app crée les échantillons dans `X_Portail_CODECOH`, comme aujourd'hui.
2. Pour chaque échantillon créé et chaque fichier déposé dans la zone 📎, l'app appelle un petit flux.
3. Le flux ajoute le fichier en pièce jointe de l'élément SharePoint.

Durée de mise en place : environ 10 minutes.

---

## Étape 1 : créer le flux
1. Allez sur **https://make.powerautomate.com**, environnement **Servier Monde – PROD** (le même que l'app).
2. Cliquez sur **+ Créer**, puis **Flux de cloud instantané**.
3. Nom du flux : **`AjoutPJ_CODECOH`** (exactement ce nom).
4. Déclencheur : **Power Apps (V2)**. Cliquez sur **Créer**.

## Étape 2 : déclarer les 2 entrées du déclencheur
Ouvrez le déclencheur **Power Apps (V2)**, puis cliquez sur **+ Ajouter une entrée** deux fois, **dans cet ordre** :

| Ordre | Type | Nom |
|---|---|---|
| 1 | **Nombre** | `ID` |
| 2 | **Fichier** | `Fichier` |

## Étape 3 : ajouter l'action SharePoint
1. Cliquez sur **+ Nouvelle étape**, cherchez **SharePoint** et choisissez **Ajouter une pièce jointe**.
2. Remplissez les champs :

| Champ | Valeur |
|---|---|
| Adresse du site | `https://serviergroup.sharepoint.com/sites/ABC-ANIMALSBIOLOGICSCOMPLIANCE` |
| Nom de la liste | `X_Portail_CODECOH` |
| Id | contenu dynamique **ID** (du déclencheur) |
| Nom du fichier | onglet **Expression** : `triggerBody()?['file']?['name']` |
| Contenu du fichier | contenu dynamique **Fichier** (du déclencheur) |

3. Cliquez sur **Enregistrer**.

## Étape 4 : relier le flux à l'app
1. Dans Power Apps Studio, cliquez sur l'icône **Power Automate** dans la barre de gauche (ou **Action → Power Automate**).
2. **+ Ajouter un flux**, puis choisissez **`AjoutPJ_CODECOH`**.

## Étape 5 : mettre à jour le bouton Envoyer
Remplacez **OnSelect** de `nd_btnEnvoyer` par le contenu de `yaml/controles_seuls/2_bouton_Envoyer_OnSelect_FR.txt`.
Ce fichier est écrit avec les `;`, prêt à coller dans la barre de formule.
Vous pouvez aussi recoller tout l'écran avec `2_ScrNouvelleDemande_controles.pa.yaml` (clic droit sur l'écran → **Coller le code**).

La formule :
- crée les échantillons (sans pièce jointe) ;
- puis, pour chaque échantillon créé et chaque fichier de la zone 📎, appelle `AjoutPJ_CODECOH.Run(ID ; fichier)`.

## Étape 6 : tester
1. **F5**, 2 échantillons et 1 fichier, puis **Envoyer**.
2. Vous voyez « Ajout des pièces jointes… », puis « … déclaré(s) avec succès ».
3. Dans SharePoint, chaque ligne doit afficher le fichier en pièce jointe. Ajoutez la colonne 📎 à l'affichage pour la voir.
4. Dans Power Automate, l'**historique d'exécution** du flux montre une exécution par fichier et par échantillon, avec l'erreur éventuelle.

## Dépannage
| Symptôme | Solution |
|---|---|
| `AjoutPJ_CODECOH` souligné en rouge dans la formule | Le flux n'est pas encore ajouté à l'app (étape 4), ou son nom est différent |
| Erreur sur `.Run(` (« nombre d'arguments ») | Les entrées du déclencheur ne sont pas dans l'ordre **Nombre** puis **Fichier** (étape 2). Corrigez, enregistrez, puis dans Studio retirez et rajoutez le flux |
| Le flux échoue sur « Nom du fichier » | Vérifiez l'expression `triggerBody()?['file']?['name']`. Si votre entrée Fichier s'appelle autrement dans le corps du déclencheur, ouvrez une exécution et regardez la sortie du déclencheur pour voir la clé exacte |
| Pièces jointes refusées | Activez les pièces jointes sur la liste (Paramètres de la liste → Paramètres avancés) |
