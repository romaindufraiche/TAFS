# Portail CODECOH (app « ABC ») : refonte charte Servier et déclaration multi-échantillons

Source : l'export Power Apps du dossier Drive `transfert` (package `.zip` décompressé : `manifest.json` + `N11f08592-…-document.msapp`).
Sources de données (inchangées) : liste SharePoint `X_Portail_CODECOH` du site *ABC-ANIMALSBIOLOGICSCOMPLIANCE*.

## Ce qui change

| Écran | Avant | Après |
|---|---|---|
| **Accueil** | 3 boutons (Nouvelle demande, Mes demandes, Administration), fond bleu | **3 tuiles** : *Bibliothèque des échantillons*, *Nouvelle demande*, *Mes demandes*. Plus d'administration |
| **Nouvelle demande** | Formulaire pour **1 seul** échantillon | **Plusieurs échantillons à la fois** : une ligne par échantillon (*Titre* = nom, *Ref commerciale*, *Type de substance*, *Tissue source*, *Pathologie*, *Coordonnées fournisseur*), avec les boutons *Dupliquer* et *Supprimer*. *Nom demandeur* et *Date enregistrement demande* sont **automatiques**. **Envoyer** crée les lignes puis ouvre la page *Pièces jointes* |
| **Pièces jointes** (nouveau) | – | Liste des échantillons créés et formulaire SharePoint pour joindre les fichiers de chacun (sans Power Automate) |
| **Bibliothèque des échantillons** (nouveau) | – | Tous les échantillons déjà déclarés (tous demandeurs), triés par nom, avec une barre de recherche (nom ou référence). Si l'échantillon est introuvable, un bouton envoie vers *Nouvelle demande* avec le nom pré-rempli |
| **Mes demandes** | Liste simple | Mes échantillons : nom, référence, type, pathologie, date d'enregistrement et demandeur, avec une recherche par nom |
| **Administration** | Écran `ScrAdmin` | **Supprimé** |
| **Détail demande** | Formulaire | Fiche en lecture seule : toutes les colonnes et les pièces jointes, qu'on peut ouvrir d'un clic |

> 🆕 **Repartir d'une application vide** : suivez [`TUTO_nouveau_projet.md`](TUTO_nouveau_projet.md).

### Charte graphique appliquée
Les couleurs sont reprises du thème du site servier.com.

| Rôle | Couleur | Power Fx |
|---|---|---|
| Couleur principale (titres, tuiles) | Indigo Servier `#24226A` | `RGBA(36, 34, 106, 1)` |
| Accent / action principale | Corail `#D44233` | `RGBA(212, 66, 51, 1)` |
| Survol / texte secondaire | Indigo 500 `#7088B6` | `RGBA(112, 136, 182, 1)` |
| Bordures | Indigo 200 `#D4DEF2` | `RGBA(212, 222, 242, 1)` |
| Fond d'écran | Indigo 50 `#EBEBF9` | `RGBA(235, 235, 249, 1)` |
| Succès (n° CODECOH attribué) | Vert `#3F7E12` | `RGBA(63, 126, 18, 1)` |
| Police | Arial | `Font.Arial` |

> Si votre service communication vous a fourni une charte officielle (codes couleurs exacts, police), il suffit de modifier les constantes en haut de `tools/generate_yaml.py` puis de relancer `python3 tools/generate_yaml.py`.

Un aperçu est disponible dans `maquette/` (fichiers `1_accueil.png`, `2_nouvelle_demande.png`, `3_mes_demandes.png`).

## Fichiers

```
powerapps/
├── yaml/
│   ├── 1_ScrAccueil.pa.yaml            ← écran complet (à coller)
│   ├── 2_ScrNouvelleDemande.pa.yaml
│   ├── 3_ScrMesDemandes.pa.yaml
│   ├── 4_ScrDetailDemande.pa.yaml
│   └── controles_seuls/                ← solution de repli : contrôles seuls + propriétés de l'écran
├── maquette/                           ← aperçu visuel
├── logo ABC.png                        ← logo à charger dans Médias
└── TUTO_nouveau_projet.md              ← tutoriel pas à pas depuis une app vide
```

---

## Comment remettre ça dans Power Apps (≈ 15 min)

Le code est au format **YAML Power Apps**. C'est le format que Power Apps Studio utilise pour « Copier le code » et « Coller le code ». Rien n'est à installer.

### 0. Travailler sur une copie (recommandé)
1. Allez sur [make.powerapps.com](https://make.powerapps.com), environnement **Servier Monde – PROD**.
2. Dans **Applications**, cliquez sur `…` à côté de **ABC**, puis **Enregistrer sous** (ou **Exporter le package** pour garder une sauvegarde).
   Vous pouvez aussi faire **Fichier → Enregistrer sous** dans Studio.
3. Ouvrez la copie en **modification** (Studio).

### 1. Supprimer l'écran Administration
Dans l'arborescence (à gauche) : `ScrAdmin`, puis `…` → **Supprimer**.

### 2. Remplacer l'écran d'accueil
1. Supprimez `ScrAccueil` (ou renommez-le `ScrAccueil_old` pour le garder un moment).
2. Ouvrez `yaml/1_ScrAccueil.pa.yaml`, sélectionnez tout le texte et copiez-le (Ctrl+A, Ctrl+C).
3. Dans Studio, faites un clic droit sur l'arborescence des écrans (ou utilisez `…` sur un écran), puis choisissez **Coller** / **Coller le code**.
   L'écran `ScrAccueil` est recréé avec tous ses contrôles.
4. Glissez-le **en premier** dans la liste des écrans pour qu'il s'ouvre au démarrage.

> **Si « Coller » ne crée pas l'écran** (selon la version de Studio) :
> 1. Créez un écran **vide** (`+ Nouvel écran` → *Vide*) et nommez-le `ScrAccueil`.
> 2. Copiez `yaml/controles_seuls/1_ScrAccueil_controles.pa.yaml`, faites un clic droit sur l'écran puis **Coller le code**.
> 3. Recopiez les propriétés de l'écran (Fill, OnVisible…) depuis `…_proprietes_ecran.txt` dans la barre de formule.

### 3. Remplacer l'écran Nouvelle demande
Même procédure avec `2_ScrNouvelleDemande.pa.yaml` : supprimez l'ancien `ScrNouvelleDemande`, puis collez.
Pensez à copier aussi la propriété **OnVisible** de l'écran si vous passez par la solution de repli : c'est elle qui initialise le tableau des échantillons.

### 4. Remplacer l'écran Mes demandes
Supprimez l'ancien `ScrMesDemandes`, puis collez `3_ScrMesDemandes.pa.yaml`.
La galerie s'appelle toujours **`Gallery1`**, donc l'écran *Détail demande* (`Form2.Item = Gallery1.Selected`) continue de fonctionner.
Si Studio renomme la galerie `Gallery1_1` (parce qu'il restait une ancienne galerie), renommez-la `Gallery1`.

### 5. Écran Détail demande (couleurs uniquement)
Sélectionnez `ScrDetailDemande` puis :
- `Fill` → `RGBA(235, 235, 249, 1)`
- bouton *Menu* : `Fill` → `RGBA(36, 34, 106, 1)`
- le titre (`Label8`) : `Color` → `RGBA(36, 34, 106, 1)`

### 6. Tester puis publier
1. Appuyez sur **F5** (aperçu). Testez : Accueil → Nouvelle demande → ajoutez 2 ou 3 lignes (bouton *Ajouter*, icône *Dupliquer*) → **Envoyer**. Vous devez arriver sur *Mes demandes* avec les nouvelles lignes.
2. Vérifiez dans la liste SharePoint `X_Portail_CODECOH` qu'il y a bien **une ligne par échantillon**.
3. Si le **vérificateur d'application** (icône stéthoscope) ne signale aucune erreur : **Fichier → Enregistrer → Publier**.

---

## Fonctionnement de l'écran multi-échantillons (pour la maintenance)

- Les lignes du tableau sont stockées dans la collection locale `colEchantillons` (`Id, Nom, Ref, TypeSub, Source, Patho`). Elle est réinitialisée à chaque ouverture de l'écran (`OnVisible`).
- **Ajouter** fait un `Collect` d'une ligne vide. **Dupliquer** recopie la ligne en ajoutant « (copie) » au nom. **Supprimer** fait un `Remove`, et reste désactivé s'il ne reste qu'une ligne.
- **Envoyer** :
  1. vérifie que chaque ligne a un nom (sinon, la bordure passe en corail et un message s'affiche) ;
  2. fait `ForAll(nd_galEchantillons.AllItems, Patch('X_Portail_CODECOH', Defaults(...), {...}))`, c'est-à-dire une ligne SharePoint par échantillon, avec les informations communes recopiées sur chaque ligne ;
  3. colonnes remplies : *Nom échantillon*, *Référence commerciale*, *Type de substance*, *Tissue source*, *Pathologie* (texte libre), plus *Nom demandeur* = nom de l'utilisateur connecté et *Date enregistrement demande* = `Today()` ;
  4. affiche un message de succès, ou le message d'erreur SharePoint.

### Régénérer le YAML
```bash
python3 tools/generate_yaml.py
```
