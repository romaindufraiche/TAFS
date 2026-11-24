# Tutoriel : créer le Portail CODECOH à partir d'une application vide

Durée : 20 à 30 minutes. Aucune installation n'est nécessaire, tout se fait dans le navigateur (Edge ou Chrome récent).

## Ce dont vous avez besoin

| Élément | Où le trouver |
|---|---|
| Les 6 fichiers de contrôles | `yaml/controles_seuls/1_…` à `6_…_controles.pa.yaml` |
| Les propriétés des écrans | `yaml/controles_seuls/…_proprietes_ecran.txt` |
| Le logo | `logo ABC.png` (**gardez exactement ce nom de fichier**) |
| Un accès en modification à la liste SharePoint `X_Portail_CODECOH` | site *ABC-ANIMALSBIOLOGICSCOMPLIANCE* |

Résultat final : 6 écrans.

```
ScrAccueil ─┬─►  ScrBibliotheque  ──(échantillon trouvé)──►  ScrDetailDemande
            │          └──(introuvable)──►  ScrNouvelleDemande
            ├─►  ScrNouvelleDemande  ──(Envoyer)──►  ScrPiecesJointes  ──►  ScrMesDemandes
            └─►  ScrMesDemandes  ──►  ScrDetailDemande  ──(📎)──►  ScrPiecesJointes
```

> ⚠️ Les noms (écrans, source de données, image) doivent être recopiés **exactement**, accents et majuscules compris : les formules les utilisent.

---

## Étape 0 : préparer la liste SharePoint `X_Portail_CODECOH`

### Colonnes attendues par l'app

| Colonne (nom exact) | Type SharePoint | Rempli par |
|---|---|---|
| Titre | Une seule ligne de texte (colonne par défaut, contient le **nom de l'échantillon**) | l'utilisateur (obligatoire) |
| Ref commerciale | Une seule ligne de texte | l'utilisateur |
| Type de substance | Une seule ligne de texte | l'utilisateur |
| Tissue source | Une seule ligne de texte | l'utilisateur |
| Pathologie | Une seule ligne de texte | l'utilisateur |
| Coordonnées fournisseur | Une seule ligne de texte | l'utilisateur |
| Nom demandeur | Une seule ligne de texte | automatique (nom de la personne connectée) |
| Date enregistrement demande | Une seule ligne de texte | automatique (date du jour, format jj/mm/aaaa) |
| *Pièces jointes* | intégrées à la liste, pas une colonne | l'utilisateur (zone 📎) |

### Créer une colonne sans piège (exemple : *Coordonnées fournisseur*)
1. Ouvrez la liste, puis cliquez sur **+ Ajouter une colonne** à droite des en-têtes.
2. Choisissez **Une seule ligne de texte**.
   Si les coordonnées sont longues (plus de 255 caractères), choisissez plutôt **Plusieurs lignes de texte**, en type **Texte brut**, et **sans** l'option *Ajouter à du texte existant* : Power Apps ne voit pas ce genre de colonne.
3. Nom : tapez d'abord un nom **sans accent ni espace**, par exemple `CoordFournisseur`, puis **Enregistrer**. SharePoint crée ainsi un nom technique propre.
4. Rouvrez l'en-tête de la colonne → **Paramètres de la colonne** → **Modifier**, et renommez-la exactement **`Coordonnées fournisseur`**. Vérifiez qu'il n'y a pas d'espace en trop, ni au milieu ni à la fin.
5. Laissez **Exiger que cette colonne contienne des informations = Non**.

### Activer les pièces jointes
Les pièces jointes ne sont pas une colonne : c'est une option de la liste, activée par défaut.
1. Cliquez sur ⚙️ (en haut à droite) → **Paramètres de la liste** → **Paramètres avancés**.
2. Vérifiez que **Pièces jointes à des éléments de la liste = Activé**, puis cliquez sur **OK**.

### Après toute modification de la liste
Dans Power Apps Studio, ouvrez le panneau **Données**, puis `…` à côté de `X_Portail_CODECOH` → **Actualiser**. Sans cela, Power Apps ne voit pas les nouvelles colonnes.

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
4. Cochez la liste **`X_Portail_CODECOH`**, puis **Connecter**.
5. Vérifiez que le panneau Données affiche bien `X_Portail_CODECOH`.

## Étape 3 : ajouter le logo
1. Dans la barre de gauche, cliquez sur **Médias** (l'icône image), puis **+ Charger**.
2. Choisissez le fichier **`logo ABC.png`**.
3. Le média doit apparaître sous le nom **`logo ABC`**.

## Étape 4 : créer les 6 écrans vides (avant de coller quoi que ce soit)
Les écrans se renvoient les uns vers les autres. Il faut donc qu'ils existent tous avant de coller le code.

1. Dans l'arborescence (à gauche), double-cliquez sur `Screen1` et renommez-le **`ScrAccueil`**.
2. Cliquez sur **+ Nouvel écran**, puis **Vide**. Renommez le nouvel écran **`ScrNouvelleDemande`**.
3. Recommencez pour créer **`ScrMesDemandes`**.
4. Recommencez pour créer **`ScrDetailDemande`**.
5. Recommencez pour créer **`ScrPiecesJointes`**.
6. Recommencez pour créer **`ScrBibliotheque`**.

L'ordre dans l'arborescence doit être : `ScrAccueil` en premier, c'est l'écran de démarrage.

## Étape 5 : coller les contrôles (respectez l'ordre 1 → 6)
Pour **chaque** écran :

1. Ouvrez le fichier correspondant avec le Bloc-notes (ou un autre éditeur de texte) :

   | Écran | Fichier |
   |---|---|
   | `ScrAccueil` | `1_ScrAccueil_controles.pa.yaml` |
   | `ScrNouvelleDemande` | `2_ScrNouvelleDemande_controles.pa.yaml` |
   | `ScrMesDemandes` | `3_ScrMesDemandes_controles.pa.yaml` |
   | `ScrDetailDemande` | `4_ScrDetailDemande_controles.pa.yaml` |
   | `ScrPiecesJointes` | `5_ScrPiecesJointes_controles.pa.yaml` |
   | `ScrBibliotheque` | `6_ScrBibliotheque_controles.pa.yaml` |

2. Faites **Ctrl+A**, puis **Ctrl+C**.
3. Dans Studio, faites un **clic droit sur le nom de l'écran** dans l'arborescence, puis **Coller le code**.
   Autre méthode : sélectionnez l'écran et faites **Ctrl+V**.
4. Les contrôles apparaissent dans l'écran (en-tête, boutons, galerie…).

> Les fichiers `…_proprietes_ecran.txt` sont écrits avec des `;` (syntaxe française de la barre de formule) : collez-les tels quels.

## Étape 6 : régler les propriétés des écrans
Pour chaque écran, ouvrez le fichier `…_proprietes_ecran.txt` correspondant. Ensuite :

1. Sélectionnez l'écran dans l'arborescence.
2. Dans la liste déroulante des propriétés (en haut à gauche, à côté de *fx*), choisissez la propriété indiquée, par exemple **Fill**.
3. Collez la formule dans la barre de formule.

| Écran | Propriétés à régler |
|---|---|
| Tous | `Fill`, `LoadingSpinnerColor` |
| `ScrNouvelleDemande` | **`OnVisible`** en plus. **Indispensable** : c'est cette propriété qui prépare le tableau des échantillons |
| `ScrPiecesJointes` | **`OnVisible`** en plus (réinitialise la liste des pièces jointes enregistrées) |

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
   Ils doivent aussi avoir le droit **Modification** sur la liste SharePoint `X_Portail_CODECOH`, sinon ils ne pourront pas envoyer de demande.

---

## Dépannage

| Symptôme | Cause probable / solution |
|---|---|
| Croix rouges sur de nombreuses formules | Un nom ne correspond pas. Vérifiez les noms des 6 écrans, de la source `X_Portail_CODECOH` et du média `logo ABC` |
| Erreur sur `Navigate(ScrDetailDemande…)` ou `varSel` | L'écran `ScrDetailDemande` n'existe pas encore ou a un autre nom. Le détail affiche l'échantillon choisi dans *Mes demandes* ou dans la *Bibliothèque* (variable `varSel`) |
| Erreur sur une colonne (« La colonne … n'existe pas ») | Le nom dans SharePoint diffère d'un caractère (espace en double, majuscule, accent). Le message propose le nom le plus proche : corrigez le nom de la colonne dans SharePoint, puis Données → `…` → **Actualiser**. Noms attendus : voir l'étape 0. Si renommer ne suffit pas, supprimez la colonne et recréez-la (étape 0) |
| L'envoi échoue avec « champ obligatoire » | Une colonne de la liste que l'app ne remplit pas (par ex. la colonne *Titre* masquée) est obligatoire. Paramètres de la liste → la colonne → *Exiger que cette colonne contienne des informations* = **Non** |
| Le tableau des échantillons est vide (aucune ligne) | La propriété `OnVisible` de `ScrNouvelleDemande` n'a pas été collée (étape 6) |
| Le menu « Coller le code » n'apparaît pas | Rechargez Studio sur Edge ou Chrome à jour, puis essayez **Ctrl+V** sur l'écran sélectionné |
| « Le type de cet argument … ne correspond pas » | Le type d'une colonne SharePoint ne correspond pas à ce que l'app envoie. Types attendus : toutes les colonnes = **Une seule ligne de texte** (voir l'étape 0) ; *Date enregistrement demande* = **Date et heure** |
| Pièces jointes non ajoutées | Après **Envoyer**, la page *Pièces jointes* s'ouvre : sélectionnez chaque échantillon, joignez ses fichiers, puis cliquez sur **Enregistrer les pièces jointes**. Pour un échantillon déjà déclaré, utilisez le bouton 📎 de la page *Détail* |
| Le formulaire de pièces jointes n'apparaît pas après le collage | Insérez un **Formulaire d'édition** (source `X_Portail_CODECOH`) contenant uniquement le champ *Pièces jointes* et nommez-le `pj_frmPJ`. Réglez **Item** = `LookUp(X_Portail_CODECOH; ID = pj_galEch.Selected.ID)` et **DefaultMode** = `FormMode.Edit`, et recopiez **OnSuccess** depuis le fichier `5_…` |
| La bibliothèque n'affiche pas tous les échantillons d'un autre demandeur | Les collaborateurs doivent avoir au moins le droit **Lecture** sur toute la liste `X_Portail_CODECOH` (et **Modification** pour déclarer) |
| La recherche ne trouve pas un échantillon | Elle cherche les noms ou références qui **commencent par** le texte saisi (ex. `HEK` trouve `HEK293`, mais `293` ne le trouve pas) |
