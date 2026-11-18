# Tutoriel : créer le Portail CODECOH à partir d'une application vide

Durée : 20 à 30 minutes. Aucune installation n'est nécessaire, tout se fait dans le navigateur (Edge ou Chrome récent).

## Ce dont vous avez besoin

| Élément | Où le trouver |
|---|---|
| Les 4 fichiers de contrôles | `yaml/controles_seuls/1_…` à `4_…_controles.pa.yaml` |
| Les propriétés des écrans | `yaml/controles_seuls/…_proprietes_ecran.txt` |
| Le logo | `logo ABC.png` (**gardez exactement ce nom de fichier**) |
| Un accès en modification à la liste SharePoint `x_Demandes CODECOH` | site *ABC-ANIMALSBIOLOGICSCOMPLIANCE* |

Résultat final : 4 écrans.

```
ScrAccueil  ──►  ScrNouvelleDemande  (déclarer plusieurs échantillons)
     └────────►  ScrMesDemandes  ──►  ScrDetailDemande
```

> ⚠️ Les noms (écrans, source de données, image) doivent être recopiés **exactement**, accents et majuscules compris : les formules les utilisent.

---

## Étape 1 : créer l'application vide
1. Allez sur **https://make.powerapps.com**.
2. En haut à droite, choisissez l'environnement **Servier Monde – PROD**.
3. Cliquez sur **+ Créer**, puis **Application vide**, puis **Application canevas vide** → **Créer**.
4. Nom : `Portail CODECOH`. Format : **Tablette**. Cliquez sur **Créer**.
5. Studio s'ouvre avec un écran `Screen1`.

## Étape 2 : connecter la liste SharePoint
1. Dans la barre de gauche, cliquez sur l'icône **Données** (le cylindre), puis **+ Ajouter des données**.
2. Cherchez **SharePoint** et sélectionnez votre connexion (ou créez-la avec **Connexion directe**).
3. Collez l'adresse du site :
   `https://serviergroup.sharepoint.com/sites/ABC-ANIMALSBIOLOGICSCOMPLIANCE`
4. Cochez la liste **`x_Demandes CODECOH`**, puis **Connecter**.
5. Vérifiez que le panneau Données affiche bien `x_Demandes CODECOH`.

## Étape 3 : ajouter le logo
1. Dans la barre de gauche, cliquez sur **Médias** (l'icône image), puis **+ Charger**.
2. Choisissez le fichier **`logo ABC.png`**.
3. Le média doit apparaître sous le nom **`logo ABC`**.

## Étape 4 : créer les 4 écrans vides (avant de coller quoi que ce soit)
Les écrans se renvoient les uns vers les autres. Il faut donc qu'ils existent tous avant de coller le code.

1. Dans l'arborescence (à gauche), double-cliquez sur `Screen1` et renommez-le **`ScrAccueil`**.
2. Cliquez sur **+ Nouvel écran**, puis **Vide**. Renommez le nouvel écran **`ScrNouvelleDemande`**.
3. Recommencez pour créer **`ScrMesDemandes`**.
4. Recommencez pour créer **`ScrDetailDemande`**.

L'ordre dans l'arborescence doit être : `ScrAccueil` en premier, c'est l'écran de démarrage.

## Étape 5 : coller les contrôles (respectez l'ordre 1 → 4)
Pour **chaque** écran :

1. Ouvrez le fichier correspondant avec le Bloc-notes (ou un autre éditeur de texte) :

   | Écran | Fichier |
   |---|---|
   | `ScrAccueil` | `1_ScrAccueil_controles.pa.yaml` |
   | `ScrNouvelleDemande` | `2_ScrNouvelleDemande_controles.pa.yaml` |
   | `ScrMesDemandes` | `3_ScrMesDemandes_controles.pa.yaml` |
   | `ScrDetailDemande` | `4_ScrDetailDemande_controles.pa.yaml` |

2. Faites **Ctrl+A**, puis **Ctrl+C**.
3. Dans Studio, faites un **clic droit sur le nom de l'écran** dans l'arborescence, puis **Coller le code**.
   Autre méthode : sélectionnez l'écran et faites **Ctrl+V**.
4. Les contrôles apparaissent dans l'écran (en-tête, boutons, galerie…).

> Collez `ScrMesDemandes` **avant** `ScrDetailDemande`, car le détail utilise la galerie `Gallery1` de *Mes demandes*.

## Étape 6 : régler les propriétés des écrans
Pour chaque écran, ouvrez le fichier `…_proprietes_ecran.txt` correspondant. Ensuite :

1. Sélectionnez l'écran dans l'arborescence.
2. Dans la liste déroulante des propriétés (en haut à gauche, à côté de *fx*), choisissez la propriété indiquée, par exemple **Fill**.
3. Collez la formule dans la barre de formule.

| Écran | Propriétés à régler |
|---|---|
| Tous | `Fill`, `LoadingSpinnerColor` |
| `ScrNouvelleDemande` | **`OnVisible`** en plus. **Indispensable** : c'est cette propriété qui prépare le tableau des échantillons |

## Étape 7 : tester
1. Sélectionnez `ScrAccueil` et appuyez sur **F5** (ou cliquez sur ▶ en haut à droite).
2. Cliquez sur **Nouvelle demande** :
   - saisissez 2 ou 3 échantillons (bouton **+ Ajouter un échantillon** ou icône **Dupliquer**) ;
   - cliquez sur **Envoyer N demande(s)**.
3. Vous arrivez sur **Mes demandes** et les échantillons y apparaissent. Cliquez sur une ligne pour voir le **détail**.
4. Vérifiez dans la liste SharePoint qu'il y a **une ligne par échantillon**.

## Étape 8 : enregistrer, publier, partager
1. **Fichier → Enregistrer**, puis **Publier → Publier cette version**.
2. **Partager** : ajoutez les utilisateurs.
   Ils doivent aussi avoir le droit **Modification** sur la liste SharePoint `x_Demandes CODECOH`, sinon ils ne pourront pas envoyer de demande.

---

## Dépannage

| Symptôme | Cause probable / solution |
|---|---|
| Croix rouges sur de nombreuses formules | Un nom ne correspond pas. Vérifiez les noms des 4 écrans, de la source `x_Demandes CODECOH` et du média `logo ABC` |
| Erreur sur `Navigate(ScrDetailDemande…)` ou `Gallery1` | `ScrDetailDemande` n'existe pas encore, ou la galerie a été renommée `Gallery1_1` : renommez-la `Gallery1` |
| Erreur sur une colonne | Les formules utilisent les noms de colonnes **exactement** comme dans SharePoint : `Nom/type échantillon`, `Référence commerciale`, `Tissue Source`, `Pathologie`, `Demandeur`, `Commentaires`, `Numéro CODECOH`, `N° d'autorisation` et les dates de la déclaration. Si une colonne est renommée, il faut corriger la formule (le vérificateur d'application indique où). Panneau Données → `…` → **Actualiser** après toute modification de la liste |
| L'envoi échoue avec « champ obligatoire » | Une colonne que l'app ne remplit pas (*Numéro CODECOH*, *Coordonnées fournisseur*, *N° d'autorisation*, dates) est obligatoire dans SharePoint. Allez dans Paramètres de la liste → la colonne → *Exiger que cette colonne contienne des informations* = **Non** |
| Le tableau des échantillons est vide (aucune ligne) | La propriété `OnVisible` de `ScrNouvelleDemande` n'a pas été collée (étape 6) |
| Le menu « Coller le code » n'apparaît pas | Rechargez Studio sur Edge ou Chrome à jour, puis essayez **Ctrl+V** sur l'écran sélectionné |
| Erreur de type sur *Pathologie* | L'app la saisit en texte libre. Si la colonne est de type *Choix* dans SharePoint, dites-le-moi pour la transformer en liste déroulante |
