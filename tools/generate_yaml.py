"""Génère les écrans Power Apps (format YAML « Coller le code ») aux couleurs Servier.

Usage : python3 tools/generate_yaml.py   -> écrit powerapps/yaml/*.pa.yaml
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "powerapps" / "yaml"

# --- Palette Servier (relevée sur servier.com, thème du site) -----------------
NAVY = "RGBA(36, 34, 106, 1)"        # #24226A  indigo-900 : couleur principale
INDIGO500 = "RGBA(112, 136, 182, 1)" # #7088B6  survol / textes secondaires
INDIGO200 = "RGBA(212, 222, 242, 1)" # #D4DEF2  bordures
INDIGO50 = "RGBA(235, 235, 249, 1)"  # #EBEBF9  fond de page
CORAL = "RGBA(212, 66, 51, 1)"       # #D44233  accent / action principale
CORAL_DARK = "RGBA(170, 50, 38, 1)"
CYAN = "RGBA(71, 191, 217, 1)"       # #47BFD9
GREEN = "RGBA(63, 126, 18, 1)"       # #3F7E12
TEXT = "RGBA(49, 49, 49, 1)"         # #313131
WHITE = "RGBA(255, 255, 255, 1)"
TRANSPARENT = "RGBA(0, 0, 0, 0)"
FONT = "Font.Arial"

HEADER_H = 88


def fmt(value, indent):
    """Formate une valeur de propriété (formule Power Fx)."""
    value = str(value)
    if "\n" in value or ":" in value or "#" in value:
        pad = " " * (indent + 2)
        lines = ("=" + value).split("\n")
        return "|-\n" + "\n".join(pad + l if l else "" for l in lines)
    return "=" + value


def ctrl(name, control, props, children=None, variant=None, layout=None, metadata=None):
    return {"name": name, "control": control, "props": props,
            "children": children or [], "variant": variant,
            "layout": layout, "metadata": metadata}


def render_ctrl(c, indent):
    sp = " " * indent
    out = [f"{sp}- {c['name']}:", f"{sp}    Control: {c['control']}"]
    if c["variant"]:
        out.append(f"{sp}    Variant: {c['variant']}")
    if c.get("layout"):
        out.append(f"{sp}    Layout: {c['layout']}")
    if c.get("metadata"):
        out.append(f"{sp}    MetadataKey: {c['metadata']}")
    out.append(f"{sp}    Properties:")
    for k in sorted(c["props"]):
        out.append(f"{sp}      {k}: {fmt(c['props'][k], indent + 6)}")
    if c["children"]:
        out.append(f"{sp}    Children:")
        for ch in c["children"]:
            out.extend(render_ctrl(ch, indent + 6))
    return out


SCREENS = {}


def render_screen(name, props, children):
    SCREENS[name] = (props, children)
    out = ["Screens:", f"  {name}:", "    Properties:"]
    for k in sorted(props):
        out.append(f"      {k}: {fmt(props[k], 6)}")
    out.append("    Children:")
    for c in children:
        out.extend(render_ctrl(c, 6))
    return "\n".join(out) + "\n"


# --- Briques réutilisables -----------------------------------------------------
def label(name, text, x, y, w, h, size=12, color=TEXT, bold=False, **extra):
    p = {"Text": text, "X": x, "Y": y, "Width": w, "Height": h, "Size": size,
         "Color": color, "Font": FONT,
         "FontWeight": "FontWeight.Bold" if bold else "FontWeight.Normal"}
    p.update(extra)
    return ctrl(name, "Label@2.5.1", p)


def rect(name, x, y, w, h, fill, **extra):
    p = {"X": x, "Y": y, "Width": w, "Height": h, "Fill": fill}
    p.update(extra)
    return ctrl(name, "Rectangle@2.3.0", p)


def button(name, text, x, y, w, h, onselect, primary=True, **extra):
    fill = CORAL if primary else WHITE
    color = WHITE if primary else NAVY
    p = {"Text": text, "X": x, "Y": y, "Width": w, "Height": h,
         "OnSelect": onselect, "Fill": fill, "Color": color,
         "HoverFill": CORAL_DARK if primary else INDIGO50,
         "HoverColor": color, "PressedFill": NAVY, "PressedColor": WHITE,
         "BorderColor": CORAL if primary else NAVY, "BorderThickness": 1,
         "HoverBorderColor": CORAL_DARK if primary else NAVY,
         "BorderStyle": "BorderStyle.Solid",
         "DisabledFill": INDIGO200, "DisabledColor": WHITE,
         "DisabledBorderColor": INDIGO200,
         "Font": FONT, "FontWeight": "FontWeight.Bold", "Size": 13,
         "RadiusTopLeft": 4, "RadiusTopRight": 4,
         "RadiusBottomLeft": 4, "RadiusBottomRight": 4}
    p.update(extra)
    return ctrl(name, "Classic/Button@2.2.0", p)


def text_input(name, default, x, y, w, h=36, hint="", onchange=None, **extra):
    p = {"Default": default, "X": x, "Y": y, "Width": w, "Height": h,
         "HintText": f'"{hint}"', "Font": FONT, "Size": 12, "Color": TEXT,
         "Fill": WHITE, "BorderColor": INDIGO200, "BorderThickness": 1,
         "HoverBorderColor": INDIGO500, "FocusedBorderColor": NAVY,
         "FocusedBorderThickness": 2, "AccessibleLabel": f'"{hint}"',
         "RadiusTopLeft": 4, "RadiusTopRight": 4,
         "RadiusBottomLeft": 4, "RadiusBottomRight": 4}
    if onchange:
        p["OnChange"] = onchange
    p.update(extra)
    return ctrl(name, "Classic/TextInput@2.3.2", p)


def icon(name, ico, x, y, size, color, onselect=None, tooltip="", **extra):
    p = {"Icon": ico, "X": x, "Y": y, "Width": size, "Height": size,
         "Color": color, "Tooltip": f'"{tooltip}"', "AccessibleLabel": "Self.Tooltip"}
    if onselect:
        p["OnSelect"] = onselect
    p.update(extra)
    return ctrl(name, "Classic/Icon@2.5.0", p)


def header(prefix, title, subtitle, back=True, back_to="ScrAccueil", back_text="←  Accueil",
           back_action=None):
    items = [
        rect(f"{prefix}_rectHeader", 0, 0, "Parent.Width", HEADER_H, WHITE),
        rect(f"{prefix}_rectAccent", 0, HEADER_H, "Parent.Width", 4, CORAL),
        ctrl(f"{prefix}_imgLogo", "Image@2.2.3", {
            "Image": "'logo ABC'", "X": 32, "Y": 12, "Width": 96, "Height": 64,
            "ImagePosition": "ImagePosition.Fit"}),
        label(f"{prefix}_lblTitre", title, 148, 14, 900, 36, size=20,
              color=NAVY, bold=True),
        label(f"{prefix}_lblSousTitre", subtitle, 148, 50, 900, 26, size=12,
              color=INDIGO500),
    ]
    if back:
        items.append(button(f"{prefix}_btnAccueil", f'"{back_text}"',
                            "Parent.Width - 212", 26, 180, 38,
                            back_action or f"Navigate({back_to}, ScreenTransition.UnCover)",
                            primary=False))
    return items


def card(name, x, y, w, h):
    return rect(name, x, y, w, h, WHITE, BorderColor=INDIGO200,
                BorderThickness=1, BorderStyle="BorderStyle.Solid")


# =============================================================================
# 1. Écran d'accueil : deux boutons, plus d'administration
# =============================================================================
def screen_accueil():
    tile_w, tile_h, gap = 380, 230, 40
    total = 3 * tile_w + 2 * gap
    x1 = f"(Parent.Width - {total}) / 2"
    x2 = f"{x1} + {tile_w + gap}"
    x3 = f"{x1} + {2 * (tile_w + gap)}"
    y = 250

    def tile(prefix, x, title, desc, ico, target):
        nav = f"Navigate({target}, ScreenTransition.Cover)"
        return [
            button(f"acc_btn{prefix}", f'"{title}"', x, y, tile_w, tile_h, nav,
                   primary=False, Fill=NAVY, Color=WHITE, HoverFill=INDIGO500,
                   HoverColor=WHITE, BorderColor=NAVY, HoverBorderColor=INDIGO500,
                   Size=22, VerticalAlign="VerticalAlign.Middle",
                   PaddingTop=40, RadiusTopLeft=8, RadiusTopRight=8,
                   RadiusBottomLeft=8, RadiusBottomRight=8),
            icon(f"acc_ico{prefix}", ico, f"{x} + {tile_w // 2 - 32}", y + 40, 64,
                 WHITE, onselect=nav, tooltip=title),
            rect(f"acc_rect{prefix}", f"{x} + {tile_w // 2 - 30}", y + tile_h - 28,
                 60, 4, CORAL),
            label(f"acc_lbl{prefix}Desc", f'"{desc}"', x, y + tile_h + 12, tile_w,
                  60, size=12, color=TEXT, Align="Align.Center"),
        ]

    children = header("acc", '"Portail CODECOH"',
                      "\"Gestion des demandes d'échantillons\"", back=False)
    children += [
        label("acc_lblBonjour", '"Bonjour " & User().FullName', x1, 140,
              total, 40, size=22, color=NAVY, bold=True),
        label("acc_lblIntro",
              '"Commencez par vérifier si l\'échantillon existe déjà dans la bibliothèque."',
              x1, 182, total, 30, size=13, color=INDIGO500),
    ]
    children += tile("Bibliotheque", x1, "Bibliothèque des échantillons",
                     "Rechercher si un échantillon est déjà déclaré",
                     "Icon.Search", "ScrBibliotheque")
    children += tile("Nouvelle", x2, "Nouvelle demande",
                     "Déclarer un ou plusieurs échantillons absents de la bibliothèque",
                     "Icon.Add", "ScrNouvelleDemande")
    children += tile("MesDemandes", x3, "Mes demandes",
                     "Suivre l'état de mes déclarations CODECOH",
                     "Icon.DetailList", "ScrMesDemandes")
    children.append(label("acc_lblPied", '"Servier – Animals & Biologics Compliance"',
                          0, "Parent.Height - 36", "Parent.Width", 28, size=10,
                          color=INDIGO500, Align="Align.Center"))
    return render_screen("ScrAccueil", {"Fill": INDIGO50,
                                        "LoadingSpinnerColor": NAVY}, children)


# =============================================================================
# Liste SharePoint « X_Portail_CODECOH » : noms des colonnes tels qu'affichés
# =============================================================================
DS = "'X_Portail_CODECOH'"
C_NOM = "Titre"                                 # texte (colonne Titre = nom de l'échantillon)
C_REF = "'Ref commerciale'"                    # texte
C_TYPE = "'Type de substance'"                  # texte
C_TISSU = "'Tissue source'"                     # texte
C_PATHO = "Pathologie"                          # texte
C_DEMANDEUR = "'Nom demandeur'"                 # texte -> rempli automatiquement
C_DATE = "'Date enregistrement demande'"        # texte -> rempli automatiquement (jj/mm/aaaa)
C_FOURN = "'Coordonnées fournisseur'"           # texte
C_PJ = "'Pièces jointes'"                       # pièces jointes de l'élément (lecture)

EMPTY_ROW = '{Id: varNextId, Nom: "", Ref: "", TypeSub: "", Source: "", Patho: "", Fourn: ""}'


def combo(name, column, key, x, y, w, sync_expr, label_txt):
    """Liste déroulante alimentée par les choix d'une colonne SharePoint Choix."""
    return ctrl(name, "Classic/ComboBox@2.4.0", {
        "Items": f"Choices([@{DS}].{column})",
        "DefaultSelectedItems": f"Filter(Choices([@{DS}].{column}), Value = ThisItem.{key})",
        "DisplayFields": '["Value"]', "SearchFields": '["Value"]',
        "SelectMultiple": "false", "IsSearchable": "true",
        "InputTextPlaceholder": '"Choisir…"',
        "OnChange": sync_expr,
        "X": x, "Y": y, "Width": w, "Height": 36,
        "Font": FONT, "Size": 12, "Color": TEXT, "Fill": WHITE,
        "BorderColor": INDIGO200, "HoverBorderColor": INDIGO500,
        "ChevronBackground": WHITE, "ChevronFill": NAVY,
        "ChevronHoverBackground": INDIGO50, "ChevronHoverFill": NAVY,
        "SelectionFill": NAVY, "SelectionColor": WHITE,
        "HoverFill": INDIGO50, "HoverColor": TEXT,
        "PressedFill": NAVY, "PressedColor": WHITE,
        "AccessibleLabel": f'"{label_txt}"'})


# =============================================================================
# 2. Nouvelle demande : déclaration de plusieurs échantillons
# =============================================================================
def screen_nouvelle():
    M = 32
    W = "Parent.Width - 64"
    p = "nd"

    def sync(field, expr):
        return (f"Patch(colEchantillons, LookUp(colEchantillons, Id = ThisItem.Id), "
                f"{{{field}: {expr}}})")

    # ---- Bandeau : demandeur et date remplis automatiquement --------------
    c1_y, c1_h = 108, 96
    children = header(p, '"Nouvelle demande"',
                      '"Ajoutez autant d\'échantillons que nécessaire, puis envoyez"')
    children += [
        card(f"{p}_cardAuto", M, c1_y, W, c1_h),
        icon(f"{p}_icoAuto", "Icon.Person", M + 24, c1_y + 18, 28, NAVY),
        label(f"{p}_lblAuto",
              '"Demandeur : " & User().FullName & "     ·     Date d\'enregistrement : " '
              '& Text(Today(), "dd/mm/yyyy")',
              M + 64, c1_y + 14, "Parent.Width - 200", 36, size=14, color=NAVY, bold=True),
        label(f"{p}_lblAutoInfo",
              '"Ces informations sont renseignées automatiquement. Après l\'envoi, une page '
              'vous permettra d\'ajouter les pièces jointes de chaque échantillon."',
              M + 64, c1_y + 52, "Parent.Width - 160", 30, size=11, color=INDIGO500),

    ]

    # ---- Tableau des échantillons -----------------------------------------
    c2_y = c1_y + c1_h + 16
    footer_h = 72
    children += [
        card(f"{p}_cardEch", M, c2_y, W, f"Parent.Height - {c2_y + footer_h + 8}"),
        label(f"{p}_lblEch",
              '"Échantillons à déclarer (" & CountRows(colEchantillons) & ")"',
              M + 24, c2_y + 12, 600, 30, size=14, color=NAVY, bold=True),
        button(f"{p}_btnAjouter", '"+  Ajouter un échantillon"',
               f"Parent.Width - {M + 24 + 230}", c2_y + 8, 230, 36,
               f"Collect(colEchantillons, {EMPTY_ROW});\nSet(varNextId, varNextId + 1)",
               primary=False),
    ]

    cols = [  # (clé, titre, fraction de largeur)
        ("Nom", "Nom échantillon *", 0.19),
        ("Ref", "Ref commerciale", 0.15),
        ("TypeSub", "Type de substance", 0.15),
        ("Source", "Tissue source", 0.15),
        ("Patho", "Pathologie", 0.15),
        ("Fourn", "Coordonnées fournisseur", 0.21),
    ]
    tbl_x = M + 24
    num_w, act_w, gap = 40, 96, 10
    avail = f"(Parent.Width - {2 * M + 48 + num_w + act_w} - {gap * len(cols)})"
    xs, x_expr = {}, f"{tbl_x + num_w}"
    for key, _, frac in cols:
        xs[key] = (x_expr, f"{avail} * {frac:.4f}")
        x_expr = f"{xs[key][0]} + {xs[key][1]} + {gap}"

    head_y = c2_y + 52
    children.append(rect(f"{p}_rectEntete", tbl_x, head_y, "Parent.Width - 112", 32,
                         INDIGO50))
    children.append(label(f"{p}_lblColNum", '"#"', tbl_x, head_y, num_w, 32, size=11,
                          color=NAVY, bold=True, Align="Align.Center"))
    for key, title, _ in cols:
        x, w = xs[key]
        children.append(label(f"{p}_lblCol{key}", f'"{title}"', x, head_y, w, 32,
                              size=11, color=NAVY, bold=True))

    def gx(key):
        return f"{xs[key][0]} - {tbl_x}"

    in_y = 10
    cells = [
        label(f"{p}_lblNum", "CountRows(Filter(colEchantillons, Id <= ThisItem.Id))",
              0, in_y, num_w, 36, size=12, color=INDIGO500, bold=True,
              Align="Align.Center"),
        text_input(f"{p}_txtNom", "ThisItem.Nom", gx("Nom"), in_y, xs["Nom"][1],
                   hint="Nom de l'échantillon", onchange=sync("Nom", "Self.Text"),
                   BorderColor=f"If(varTentative && IsBlank(Trim(Self.Text)), {CORAL}, {INDIGO200})"),
        text_input(f"{p}_txtRef", "ThisItem.Ref", gx("Ref"), in_y, xs["Ref"][1],
                   hint="Réf. commerciale", onchange=sync("Ref", "Self.Text")),
        text_input(f"{p}_txtType", "ThisItem.TypeSub", gx("TypeSub"), in_y,
                   xs["TypeSub"][1], hint="Type de substance",
                   onchange=sync("TypeSub", "Self.Text")),
        text_input(f"{p}_txtSource", "ThisItem.Source", gx("Source"), in_y,
                   xs["Source"][1], hint="Tissue source",
                   onchange=sync("Source", "Self.Text")),
        text_input(f"{p}_txtPatho", "ThisItem.Patho", gx("Patho"), in_y,
                   xs["Patho"][1], hint="Pathologie",
                   onchange=sync("Patho", "Self.Text")),
        text_input(f"{p}_txtFourn", "ThisItem.Fourn", gx("Fourn"), in_y,
                   xs["Fourn"][1], hint="Coordonnées fournisseur",
                   onchange=sync("Fourn", "Self.Text")),
        icon(f"{p}_icoDupliquer", "Icon.Copy", "Parent.TemplateWidth - 84", in_y + 2, 32,
             NAVY,
             onselect=("Collect(colEchantillons, {Id: varNextId, "
                       "Nom: nd_txtNom.Text & \" (copie)\", Ref: nd_txtRef.Text, "
                       "TypeSub: nd_txtType.Text, Source: nd_txtSource.Text, "
                       "Patho: nd_txtPatho.Text, Fourn: nd_txtFourn.Text});\nSet(varNextId, varNextId + 1)"),
             tooltip="Dupliquer cette ligne",
             PaddingTop=4, PaddingBottom=4, PaddingLeft=4, PaddingRight=4),
        icon(f"{p}_icoSupprimer", "Icon.Trash", "Parent.TemplateWidth - 44", in_y + 2, 32,
             CORAL,
             onselect="Remove(colEchantillons, LookUp(colEchantillons, Id = ThisItem.Id))",
             tooltip="Supprimer cette ligne",
             DisplayMode="If(CountRows(colEchantillons) > 1, DisplayMode.Edit, DisplayMode.Disabled)",
             DisabledColor=INDIGO200,
             PaddingTop=4, PaddingBottom=4, PaddingLeft=4, PaddingRight=4),
        rect(f"{p}_rectSep", 0, "Parent.TemplateHeight - 1", "Parent.TemplateWidth",
             1, INDIGO200),
    ]
    children.append(ctrl(f"{p}_galEchantillons", "Gallery@2.15.0", {
        "Items": "colEchantillons",
        "X": tbl_x, "Y": f"{p}_rectEntete.Y + {p}_rectEntete.Height + 4",
        "Width": "Parent.Width - 112",
        "Height": f"Parent.Height - Self.Y - {footer_h + 20}",
        "TemplateSize": 56, "TemplatePadding": 0,
        "Fill": TRANSPARENT, "TemplateFill": WHITE, "ShowScrollbar": "true",
        "BorderThickness": 0, "AccessibleLabel": '"Liste des échantillons à déclarer"',
    }, children=cells, variant="Vertical"))

    submit = f"""Notify("Envoi de " & CountRows(nd_galEchantillons.AllItems) & " échantillon(s) en cours…", NotificationType.Information);
Set(varTentative, true);
If(
    CountRows(Filter(nd_galEchantillons.AllItems, IsBlank(Trim(nd_txtNom.Text)))) > 0,
    Notify("Chaque échantillon doit avoir un nom.", NotificationType.Error),
    Set(varEnvoiEnCours, true);
    Clear(colCrees);
    ForAll(
        nd_galEchantillons.AllItems,
        Collect(
            colCrees,
            Patch(
                {DS},
                Defaults({DS}),
                {{
                    {C_NOM}: Trim(nd_txtNom.Text),
                    {C_REF}: nd_txtRef.Text,
                    {C_TYPE}: nd_txtType.Text,
                    {C_TISSU}: nd_txtSource.Text,
                    {C_PATHO}: nd_txtPatho.Text,
                    {C_FOURN}: nd_txtFourn.Text,
                    {C_DEMANDEUR}: User().FullName,
                    {C_DATE}: Text(Today(), "dd/mm/yyyy")
                }}
            )
        )
    );
    Set(varEnvoiEnCours, false);
    If(
        IsEmpty(Errors({DS})),
        Notify(CountRows(colCrees) & " échantillon(s) déclaré(s). Ajoutez maintenant les pièces jointes si besoin.", NotificationType.Success);
        Navigate(ScrPiecesJointes, ScreenTransition.Cover),
        Notify("Erreur SharePoint : " & First(Errors({DS})).Message, NotificationType.Error)
    )
)"""
    fy = f"Parent.Height - {footer_h - 12}"
    children += [
        button(f"{p}_btnAnnuler", '"Annuler"', "Parent.Width - 452", fy, 140, 44,
               "Navigate(ScrAccueil, ScreenTransition.UnCover)", primary=False),
        button(f"{p}_btnEnvoyer",
               'If(varEnvoiEnCours, "Envoi en cours…", "Envoyer " & CountRows(colEchantillons) & " demande(s)")',
               "Parent.Width - 296", fy, 264, 44, submit,
               DisplayMode="If(varEnvoiEnCours, DisplayMode.Disabled, DisplayMode.Edit)"),
    ]

    on_visible = f"""Set(varTentative, false);
Set(varEnvoiEnCours, false);
Set(varNextId, 1);
ClearCollect(colEchantillons, {{Id: 1, Nom: Coalesce(varNomPrefill, ""), Ref: "", TypeSub: "", Source: "", Patho: "", Fourn: ""}});
Set(varNomPrefill, "");
Set(varNextId, 2)"""
    return render_screen("ScrNouvelleDemande",
                         {"Fill": INDIGO50, "LoadingSpinnerColor": NAVY,
                          "OnVisible": on_visible}, children)


# =============================================================================
# 3. Mes demandes (la galerie s'appelle Gallery1 : utilisée par l'écran Détail)
# =============================================================================
def screen_mes_demandes():
    M = 32
    sub = (f'Concatenate(If(IsBlank(ThisItem.{C_REF}), "", "Réf. " & ThisItem.{C_REF} & "   "), '
           f'If(IsBlank(ThisItem.{C_TYPE}), "", ThisItem.{C_TYPE} & "   "), '
           f'If(IsBlank(ThisItem.{C_PATHO}), "", "· " & ThisItem.{C_PATHO} & "   "), '
           f'If(CountRows(ThisItem.{C_PJ}) > 0, "📎 " & CountRows(ThisItem.{C_PJ}), ""))')
    cells = [
        label("Title1", f"ThisItem.{C_NOM}", 24, 10, "Parent.TemplateWidth - 340", 28,
              size=14, color=NAVY, bold=True, OnSelect="Select(Parent)"),
        label("Subtitle1", sub, 24, 40, "Parent.TemplateWidth - 340", 24, size=12,
              color=TEXT, OnSelect="Select(Parent)"),
        label("md_lblDate", f'"Enregistrée le " & ThisItem.{C_DATE}',
              "Parent.TemplateWidth - 300", 10, 220, 24, size=11, color=INDIGO500,
              Align="Align.Right", OnSelect="Select(Parent)"),
        label("md_lblDemandeur", f"ThisItem.{C_DEMANDEUR}",
              "Parent.TemplateWidth - 300", 38, 220, 24, size=11, color=NAVY, bold=True,
              Align="Align.Right", OnSelect="Select(Parent)"),
        icon("NextArrow1", "Icon.ChevronRight", "Parent.TemplateWidth - 64", 18, 40,
             NAVY, onselect="Set(varSel, ThisItem);\nNavigate(ScrDetailDemande, ScreenTransition.Cover)",
             tooltip="Afficher le détail"),
        rect("Rectangle1", 0, 0, 4, "Parent.TemplateHeight - 1", CORAL,
             Visible="ThisItem.IsSelected", OnSelect="Select(Parent)"),
        rect("Separator1", 0, "Parent.TemplateHeight - 1", "Parent.TemplateWidth", 1,
             INDIGO200, OnSelect="Select(Parent)"),
    ]
    children = header("md", '"Mes demandes"',
                      '"Retrouvez tous les échantillons que vous avez déclarés"')
    children += [
        text_input("md_txtRecherche", '""', M, 112, 420, hint="Rechercher un échantillon…"),
        icon("md_icoRecherche", "Icon.Search", M + 384, 118, 24, INDIGO500),
        button("md_btnNouvelle", '"+  Nouvelle demande"', "Parent.Width - 252", 108,
               220, 40, "Navigate(ScrNouvelleDemande, ScreenTransition.Cover)"),
        card("md_cardListe", M, 164, "Parent.Width - 64", "Parent.Height - 196"),
        ctrl("Gallery1", "Gallery@2.15.0", {
            "Items": f"""SortByColumns(
    Filter(
        {DS},
        Author.Email = User().Email,
        IsBlank(md_txtRecherche.Text) || StartsWith({C_NOM}, md_txtRecherche.Text)
    ),
    "ID",
    SortOrder.Descending
)""",
            "X": M + 1, "Y": 165, "Width": "Parent.Width - 66",
            "Height": "Parent.Height - 198", "TemplateSize": 72, "TemplatePadding": 0,
            "Fill": TRANSPARENT,
            "TemplateFill": f"If(ThisItem.IsSelected, {INDIGO50}, {WHITE})",
            "AccessibleLabel": '"Liste de mes demandes"',
            "OnSelect": "Set(varSel, ThisItem);\nNavigate(ScrDetailDemande, ScreenTransition.Cover)"},
            children=cells, variant="Vertical"),
    ]
    return render_screen("ScrMesDemandes", {"Fill": INDIGO50,
                                            "LoadingSpinnerColor": NAVY}, children)


# =============================================================================
# 4. Détail d'une demande (lecture seule)
# =============================================================================
def screen_detail():
    M = 32
    sel = "varSel"

    def val(expr):
        return f'If(IsBlank({expr}), "—", Text({expr}))'

    left = [
        ("Nom échantillon", val(f"{sel}.{C_NOM}")),
        ("Ref commerciale", val(f"{sel}.{C_REF}")),
        ("Type de substance", val(f"{sel}.{C_TYPE}")),
        ("Tissue source", val(f"{sel}.{C_TISSU}")),
        ("Coordonnées fournisseur", val(f"{sel}.{C_FOURN}")),
    ]
    right = [
        ("Pathologie", val(f"{sel}.{C_PATHO}")),
        ("Nom demandeur", val(f"{sel}.{C_DEMANDEUR}")),
        ("Date enregistrement demande",
         val(f"{sel}.{C_DATE}")),
    ]
    top = 112
    col_w = "(Parent.Width - 64 - 48 - 32) / 2"
    x1 = f"{M} + 24"
    x2 = f"{M} + 24 + {col_w} + 32"
    children = header("dd", '"Détail de la demande"', f"{sel}.{C_NOM}",
                      back_text="←  Retour", back_action="Back()")
    children += [
        card("dd_card", M, top, "Parent.Width - 64", 440),
        label("dd_lblTitreBloc", '"Échantillon"', x1, top + 14, 400, 30, size=15,
              color=NAVY, bold=True),
    ]
    for prefix, x, items in (("G", x1, left), ("D", x2, right)):
        for i, (lab, expr) in enumerate(items):
            y = top + 56 + i * 72
            children.append(label(f"dd_lblK{prefix}{i + 1}", f'"{lab}"', x, y, col_w, 22,
                                  size=11, color=INDIGO500, bold=True))
            children.append(label(f"dd_lblV{prefix}{i + 1}", expr, x, y + 22, col_w, 32,
                                  size=14, color=TEXT))

    # Pièces jointes : liste cliquable (ouvre le fichier)
    pj_y = top + 56 + len(right) * 72
    children += [
        label("dd_lblKPJ", '"Pièces jointes"', x2, pj_y, col_w, 22, size=11,
              color=INDIGO500, bold=True),
        label("dd_lblAucunePJ", '"—"', x2, pj_y + 22, col_w, 32, size=14, color=TEXT,
              Visible=f"IsEmpty({sel}.{C_PJ})"),
        ctrl("dd_galPJ", "Gallery@2.15.0", {
            "Items": f"{sel}.{C_PJ}",
            "X": x2, "Y": pj_y + 22, "Width": col_w, "Height": 100,
            "TemplateSize": 30, "TemplatePadding": 0, "Fill": TRANSPARENT,
            "AccessibleLabel": '"Pièces jointes"'},
            children=[
                label("dd_lblPJNom", '"📎  " & ThisItem.DisplayName', 0, 0,
                      "Parent.TemplateWidth", 30, size=13, color=NAVY,
                      Underline="true", OnSelect="Launch(ThisItem.AbsoluteUri)",
                      Tooltip='"Ouvrir le fichier"'),
            ], variant="Vertical"),
    ]
    children.append(button("dd_btnPJ", '"📎  Ajouter / modifier les pièces jointes"',
                           f"{M}", top + 460, 360, 44,
                           "ClearCollect(colCrees, varSel);\nNavigate(ScrPiecesJointes, ScreenTransition.Cover)",
                           primary=False))
    return render_screen("ScrDetailDemande", {"Fill": INDIGO50,
                                              "LoadingSpinnerColor": NAVY}, children)


# =============================================================================
# 5. Pièces jointes : un formulaire SharePoint par échantillon créé
#    (seule méthode fiable sans Power Automate pour envoyer des fichiers)
# =============================================================================
def screen_pieces_jointes():
    M = 32
    top = 112
    left_w = 420
    children = header("pj", '"Pièces jointes"',
                      '"Sélectionnez un échantillon, ajoutez ses fichiers, puis enregistrez"',
                      back=False)
    # --- liste des échantillons créés
    cells = [
        label("pj_lblNom", "ThisItem.Titre", 16, 8, "Parent.TemplateWidth - 70", 26,
              size=13, color=NAVY, bold=True, OnSelect="Select(Parent)"),
        label("pj_lblInfo",
              'If(ThisItem.ID in colPJFaites.ID, "Pièces jointes enregistrées", "À compléter")',
              16, 34, "Parent.TemplateWidth - 70", 22, size=11,
              color=f"If(ThisItem.ID in colPJFaites.ID, {GREEN}, {INDIGO500})",
              OnSelect="Select(Parent)"),
        icon("pj_icoOk", "Icon.CheckBadge", "Parent.TemplateWidth - 44", 18, 28, GREEN,
             Visible="ThisItem.ID in colPJFaites.ID"),
        rect("pj_rectSel", 0, 0, 4, "Parent.TemplateHeight - 1", CORAL,
             Visible="ThisItem.IsSelected"),
        rect("pj_rectSep", 0, "Parent.TemplateHeight - 1", "Parent.TemplateWidth", 1,
             INDIGO200),
    ]
    children += [
        card("pj_cardListe", M, top, left_w, "Parent.Height - 200"),
        label("pj_lblListe", '"Échantillons (" & CountRows(colCrees) & ")"', M + 16,
              top + 10, left_w - 32, 30, size=14, color=NAVY, bold=True),
        ctrl("pj_galEch", "Gallery@2.15.0", {
            "Items": "colCrees",
            "X": M + 1, "Y": top + 48, "Width": left_w - 2,
            "Height": "Parent.Height - 250", "TemplateSize": 64, "TemplatePadding": 0,
            "Fill": TRANSPARENT,
            "TemplateFill": f"If(ThisItem.IsSelected, {INDIGO50}, {WHITE})",
            "AccessibleLabel": '"Échantillons déclarés"'},
            children=cells, variant="Vertical"),
    ]
    # --- formulaire SharePoint (pièces jointes seulement)
    fx = M + left_w + 24
    fw = f"Parent.Width - {fx + M}"
    att_card = ctrl("pj_cardPJ", "TypedDataCard@1.0.7", {
        "DataField": '"{Attachments}"',
        "Default": "ThisItem.'Pièces jointes'",
        "DisplayName": '"Pièces jointes"',
        "Required": "false",
        "Update": "pj_attPJ.Attachments",
        "Width": f"Parent.Width", "Height": 380, "X": 0, "Y": 0,
        "BorderColor": TRANSPARENT,
    }, children=[
        ctrl("pj_lblCleePJ", "Label@2.5.1", {
            "Text": '"📎  Fichiers de : " & pj_galEch.Selected.Titre',
            "X": 24, "Y": 10, "Width": "Parent.Width - 48", "Height": 34,
            "Font": FONT, "Size": 14, "FontWeight": "FontWeight.Bold", "Color": NAVY},
            metadata="FieldName"),
        ctrl("pj_attPJ", "Attachments@2.3.0", {
            "Items": "Parent.Default",
            "DisplayMode": "Parent.DisplayMode",
            "X": 24, "Y": 54, "Width": "Parent.Width - 48", "Height": 300,
            "MaxAttachments": 10, "MaxAttachmentSize": 10,
            "AddAttachmentText": '"Joindre un fichier"',
            "NoAttachmentsText": '"Aucun fichier joint"',
            "Font": FONT, "Size": 12, "Color": NAVY, "Fill": INDIGO50,
            "ItemFill": NAVY, "ItemColor": WHITE, "ItemSpacing": 10,
            "BorderColor": INDIGO200, "BorderThickness": 1,
            "BorderStyle": "BorderStyle.Dashed",
            "AccessibleLabel": '"Pièces jointes de l\'échantillon"'},
            metadata="FieldValue"),
    ], variant="ClassicAttachmentsEdit")
    children += [
        card("pj_cardForm", fx, top, fw, "Parent.Height - 200"),
        ctrl("pj_frmPJ", "Form@2.4.4", {
            "DataSource": DS,
            "DefaultMode": "FormMode.Edit",
            "Item": f"LookUp({DS}, ID = pj_galEch.Selected.ID)",
            "NumberOfColumns": 1,
            "X": fx + 1, "Y": top + 1, "Width": f"{fw} - 2", "Height": 400,
            "Fill": WHITE, "BorderColor": TRANSPARENT,
            "Visible": "!IsEmpty(colCrees)",
            "OnSuccess": ('Collect(colPJFaites, {ID: pj_galEch.Selected.ID});\n'
                          'Notify("Pièces jointes enregistrées pour " & pj_galEch.Selected.Titre & ".", NotificationType.Success)'),
            "OnFailure": 'Notify("Erreur : " & pj_frmPJ.Error, NotificationType.Error)',
        }, children=[att_card], variant="Classic", layout="Vertical"),
        label("pj_lblAide",
              '"Astuce : un fichier commun à plusieurs échantillons doit être joint à chacun d\'eux."',
              fx + 24, "Parent.Height - 140", f"{fw} - 48", 40, size=11, color=INDIGO500),
    ]
    fy = "Parent.Height - 60"
    children += [
        button("pj_btnEnregistrer", '"Enregistrer les pièces jointes"',
               "Parent.Width - 600", fy, 300, 44, "SubmitForm(pj_frmPJ)",
               DisplayMode="If(IsEmpty(colCrees), DisplayMode.Disabled, DisplayMode.Edit)"),
        button("pj_btnTerminer", '"Terminer  →"', "Parent.Width - 272", fy, 240, 44,
               "Navigate(ScrMesDemandes, ScreenTransition.Fade)", primary=False),
    ]
    return render_screen("ScrPiecesJointes", {"Fill": INDIGO50,
                                              "LoadingSpinnerColor": NAVY,
                                              "OnVisible": "Clear(colPJFaites)"},
                         children)


# =============================================================================
# 6. Bibliothèque des échantillons : tous les échantillons déclarés (tous demandeurs)
# =============================================================================
def screen_bibliotheque():
    M = 32
    sub = (f'Concatenate(If(IsBlank(ThisItem.{C_REF}), "", "Réf. " & ThisItem.{C_REF} & "   "), '
           f'If(IsBlank(ThisItem.{C_TYPE}), "", ThisItem.{C_TYPE} & "   "), '
           f'If(IsBlank(ThisItem.{C_TISSU}), "", "· " & ThisItem.{C_TISSU} & "   "), '
           f'If(IsBlank(ThisItem.{C_PATHO}), "", "· " & ThisItem.{C_PATHO}))')
    nav_detail = "Set(varSel, ThisItem);\nNavigate(ScrDetailDemande, ScreenTransition.Cover)"
    nav_new = ("Set(varNomPrefill, Trim(bib_txtRecherche.Text));\n"
               "Navigate(ScrNouvelleDemande, ScreenTransition.Cover)")
    cells = [
        label("bib_lblNom", f"ThisItem.{C_NOM}", 24, 10, "Parent.TemplateWidth - 360", 28,
              size=14, color=NAVY, bold=True, OnSelect=nav_detail),
        label("bib_lblSub", sub, 24, 40, "Parent.TemplateWidth - 360", 24, size=12,
              color=TEXT, OnSelect=nav_detail),
        label("bib_lblDecl",
              f'"Déclaré le " & ThisItem.{C_DATE} & '
              f'If(CountRows(ThisItem.{C_PJ}) > 0, "   📎 " & CountRows(ThisItem.{C_PJ}), "")',
              "Parent.TemplateWidth - 320", 10, 240, 24, size=11, color=INDIGO500,
              Align="Align.Right", OnSelect=nav_detail),
        label("bib_lblDemandeur", f'"par " & ThisItem.{C_DEMANDEUR}',
              "Parent.TemplateWidth - 320", 38, 240, 24, size=11, color=NAVY, bold=True,
              Align="Align.Right", OnSelect=nav_detail),
        icon("bib_icoDetail", "Icon.ChevronRight", "Parent.TemplateWidth - 64", 18, 40,
             NAVY, onselect=nav_detail, tooltip="Afficher le détail"),
        rect("bib_rectSep", 0, "Parent.TemplateHeight - 1", "Parent.TemplateWidth", 1,
             INDIGO200),
    ]
    search_y = 112
    list_y = search_y + 64
    children = header("bib", '"Bibliothèque des échantillons"',
                      '"Vérifiez si un échantillon est déjà déclaré avant de faire une demande"')
    children += [
        text_input("bib_txtRecherche", '""', M, search_y, 560, h=44,
                   hint="Rechercher par nom ou référence commerciale…", Size=14),
        icon("bib_icoRecherche", "Icon.Search", M + 520, search_y + 10, 24, INDIGO500),
        button("bib_btnEffacer", '"Effacer"', M + 576, search_y + 2, 110, 40,
               "Reset(bib_txtRecherche)", primary=False,
               Visible="!IsBlank(bib_txtRecherche.Text)"),
        button("bib_btnNouvelle", '"Échantillon absent ?  →  Nouvelle demande"',
               "Parent.Width - 412", search_y + 2, 380, 40, nav_new),
        card("bib_cardListe", M, list_y, "Parent.Width - 64", f"Parent.Height - {list_y + 32}"),
        ctrl("bib_galEch", "Gallery@2.15.0", {
            "Items": f"""SortByColumns(
    Filter(
        {DS},
        IsBlank(bib_txtRecherche.Text)
            || StartsWith({C_NOM}, bib_txtRecherche.Text)
            || StartsWith({C_REF}, bib_txtRecherche.Text)
    ),
    "Title",
    SortOrder.Ascending
)""",
            "X": M + 1, "Y": list_y + 1, "Width": "Parent.Width - 66",
            "Height": f"Parent.Height - {list_y + 34}", "TemplateSize": 72,
            "TemplatePadding": 0, "Fill": TRANSPARENT, "TemplateFill": WHITE,
            "ShowScrollbar": "true",
            "AccessibleLabel": '"Bibliothèque des échantillons"'},
            children=cells, variant="Vertical"),
        # --- aucun résultat : proposer la déclaration
        icon("bib_icoVide", "Icon.Warning", "(Parent.Width - 48) / 2", list_y + 70, 48,
             CORAL, Visible="IsEmpty(bib_galEch.AllItems)"),
        label("bib_lblVide",
              'If(IsBlank(bib_txtRecherche.Text), "La bibliothèque est vide.", '
              '"Aucun échantillon ne correspond à « " & bib_txtRecherche.Text & " ».")',
              M, list_y + 130, "Parent.Width - 64", 36, size=16, color=NAVY, bold=True,
              Align="Align.Center", Visible="IsEmpty(bib_galEch.AllItems)"),
        label("bib_lblVide2",
              '"Cet échantillon n\'est pas encore déclaré : vous pouvez le déclarer maintenant."',
              M, list_y + 168, "Parent.Width - 64", 28, size=12, color=INDIGO500,
              Align="Align.Center", Visible="IsEmpty(bib_galEch.AllItems)"),
        button("bib_btnDeclarer",
               'If(IsBlank(bib_txtRecherche.Text), "+  Déclarer un échantillon", '
               '"+  Déclarer « " & bib_txtRecherche.Text & " »")',
               "(Parent.Width - 420) / 2", list_y + 214, 420, 48, nav_new,
               Visible="IsEmpty(bib_galEch.AllItems)"),
    ]
    return render_screen("ScrBibliotheque", {"Fill": INDIGO50,
                                             "LoadingSpinnerColor": NAVY}, children)


# Formule OnSelect du bouton Envoyer en syntaxe française (« ; » et « ;; »)
def fr(src):
    out, instr, inq = [], False, False
    for ch in src:
        if ch == '"' and not inq:
            instr = not instr
        elif ch == "'" and not instr:
            inq = not inq
        elif not instr and not inq and ch == ';':
            out.append(';;'); continue
        elif not instr and not inq and ch == ',':
            out.append(';'); continue
        out.append(ch)
    return ''.join(out)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "1_ScrAccueil.pa.yaml": screen_accueil(),
        "2_ScrNouvelleDemande.pa.yaml": screen_nouvelle(),
        "3_ScrMesDemandes.pa.yaml": screen_mes_demandes(),
        "4_ScrDetailDemande.pa.yaml": screen_detail(),
        "5_ScrPiecesJointes.pa.yaml": screen_pieces_jointes(),
        "6_ScrBibliotheque.pa.yaml": screen_bibliotheque(),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print("écrit", OUT / name)

    for c in SCREENS["ScrNouvelleDemande"][1]:
        if c["name"] == "nd_btnEnvoyer":
            (OUT / "controles_seuls" / "2_bouton_Envoyer_OnSelect_FR.txt").write_text(
                fr(str(c["props"]["OnSelect"])) + "\n", encoding="utf-8")
    # Bouton Envoyer seul (à recoller via « Coller le code », indépendant de la langue)
    for c in SCREENS["ScrNouvelleDemande"][1]:
        if c["name"] == "nd_btnEnvoyer":
            (OUT / "controles_seuls" / "2_bouton_Envoyer.pa.yaml").write_text(
                "\n".join(render_ctrl(c, 0)) + "\n", encoding="utf-8")
    # Variante « contrôles seuls » : à coller dans un écran vide existant
    for i, (name, (props, children)) in enumerate(SCREENS.items(), 1):
        lines = []
        for c in children:
            lines.extend(render_ctrl(c, 0))
        (OUT / "controles_seuls" / f"{i}_{name}_controles.pa.yaml").parent.mkdir(exist_ok=True)
        (OUT / "controles_seuls" / f"{i}_{name}_controles.pa.yaml").write_text(
            "\n".join(lines) + "\n", encoding="utf-8")
        props_txt = "\n\n".join(f"### Propriété {k} (à coller dans la barre de formule)\n{fr(str(v))}" for k, v in sorted(props.items()))
        (OUT / "controles_seuls" / f"{i}_{name}_proprietes_ecran.txt").write_text(
            props_txt + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
