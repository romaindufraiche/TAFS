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


def ctrl(name, control, props, children=None, variant=None):
    return {"name": name, "control": control, "props": props,
            "children": children or [], "variant": variant}


def render_ctrl(c, indent):
    sp = " " * indent
    out = [f"{sp}- {c['name']}:", f"{sp}    Control: {c['control']}"]
    if c["variant"]:
        out.append(f"{sp}    Variant: {c['variant']}")
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


def header(prefix, title, subtitle, back=True):
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
        items.append(button(f"{prefix}_btnAccueil", '"←  Accueil"',
                            "Parent.Width - 172", 26, 140, 38,
                            "Navigate(ScrAccueil, ScreenTransition.UnCover)",
                            primary=False))
    return items


def card(name, x, y, w, h):
    return rect(name, x, y, w, h, WHITE, BorderColor=INDIGO200,
                BorderThickness=1, BorderStyle="BorderStyle.Solid")


# =============================================================================
# 1. Écran d'accueil : deux boutons, plus d'administration
# =============================================================================
def screen_accueil():
    tile_w, tile_h, gap = 460, 240, 48
    x1 = f"(Parent.Width - {2 * tile_w + gap}) / 2"
    x2 = f"{x1} + {tile_w + gap}"
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
                  44, size=12, color=TEXT, Align="Align.Center"),
        ]

    children = header("acc", '"Portail CODECOH"',
                      "\"Gestion des demandes d'échantillons\"", back=False)
    children += [
        label("acc_lblBonjour", '"Bonjour " & User().FullName', x1, 140,
              2 * tile_w + gap, 40, size=22, color=NAVY, bold=True),
        label("acc_lblIntro",
              '"Que souhaitez-vous faire ?"', x1, 182, 2 * tile_w + gap, 30,
              size=13, color=INDIGO500),
    ]
    children += tile("Nouvelle", x1, "Nouvelle demande",
                     "Déclarer un ou plusieurs échantillons en une seule fois",
                     "Icon.Add", "ScrNouvelleDemande")
    children += tile("MesDemandes", x2, "Mes demandes",
                     "Suivre l'état de mes déclarations CODECOH",
                     "Icon.DetailList", "ScrMesDemandes")
    children.append(label("acc_lblPied", '"Servier – Animals & Biologics Compliance"',
                          0, "Parent.Height - 36", "Parent.Width", 28, size=10,
                          color=INDIGO500, Align="Align.Center"))
    return render_screen("ScrAccueil", {"Fill": INDIGO50,
                                        "LoadingSpinnerColor": NAVY}, children)


# =============================================================================
# 2. Nouvelle demande : déclaration de plusieurs échantillons
# =============================================================================
EMPTY_ROW = '{Id: varNextId, Nom: "", Ref: "", TypeSub: "", Source: "", Lignee: ""}'


def screen_nouvelle():
    M = 32                       # marge
    W = "Parent.Width - 64"      # largeur utile
    p = "nd"

    def sync(field, expr):
        return (f"Patch(colEchantillons, LookUp(colEchantillons, Id = ThisItem.Id), "
                f"{{{field}: {expr}}})")

    # ---- Bloc 1 : informations communes -----------------------------------
    c1_y, c1_h = 108, 196
    col_w = "(Parent.Width - 64 - 48 - 64) / 3"
    def col_x(i):
        return f"{M + 24} + {i} * ({col_w} + 32)" if i else str(M + 24)

    common = [
        ("txtTitre", "Titre / projet", '""', "Ex. : Projet X – lot de novembre"),
        ("txtDemandeur", "Nom du demandeur", "User().FullName", "Nom du demandeur"),
        ("txtFournisseur", "Nom du fournisseur", '""', "Fournisseur"),
        ("txtAdrFournisseur", "Adresse du fournisseur", '""', "Adresse du fournisseur"),
        ("txtAdrExpediteur", "Adresse de l'expéditeur", '""', "Adresse de l'expéditeur"),
        ("txtCommentaires", "Commentaires", '""', "Commentaire (facultatif)"),
    ]
    children = header(p, '"Nouvelle demande"',
                      '"Renseignez les informations communes, puis ajoutez autant '
                      'd\'échantillons que nécessaire"')
    children += [
        card(f"{p}_cardCommun", M, c1_y, W, c1_h),
        label(f"{p}_lblCommun", '"1. Informations communes à tous les échantillons"',
              M + 24, c1_y + 12, 800, 30, size=14, color=NAVY, bold=True),
    ]
    for i, (n, lab, default, hint) in enumerate(common):
        r, c = divmod(i, 3)
        y = c1_y + 50 + r * 72
        children.append(label(f"{p}_lbl{n[3:]}", f'"{lab}"', col_x(c), y, col_w, 22,
                              size=11, color=INDIGO500, bold=True))
        children.append(text_input(f"{p}_{n}", default, col_x(c), y + 24, col_w,
                                   hint=hint))

    # ---- Bloc 2 : tableau des échantillons --------------------------------
    c2_y = c1_y + c1_h + 16
    footer_h = 72
    children += [
        card(f"{p}_cardEch", M, c2_y, W, f"Parent.Height - {c2_y + footer_h + 8}"),
        label(f"{p}_lblEch",
              '"2. Échantillons (" & CountRows(colEchantillons) & ")"',
              M + 24, c2_y + 12, 600, 30, size=14, color=NAVY, bold=True),
        button(f"{p}_btnAjouter", '"+  Ajouter un échantillon"',
               f"Parent.Width - {M + 24 + 230}", c2_y + 8, 230, 36,
               f"Collect(colEchantillons, {EMPTY_ROW});\nSet(varNextId, varNextId + 1)",
               primary=False),
    ]

    # Colonnes du tableau (en fraction de la largeur disponible)
    cols = [  # (clé, titre, fraction)
        ("Nom", "Nom échantillon *", 0.22),
        ("Ref", "Référence commerciale", 0.17),
        ("TypeSub", "Type de substance", 0.17),
        ("Source", "Source tissu", 0.15),
        ("Lignee", "Lignée cellulaire", 0.17),
    ]
    tbl_x = M + 24
    num_w, act_w, gap = 40, 96, 10
    avail = f"(Parent.Width - {2 * M + 48 + num_w + act_w} - {gap * len(cols)})"
    xs, x_expr = {}, f"{tbl_x + num_w}"
    for key, _, frac in cols:
        xs[key] = (x_expr, f"{avail} * {frac / 0.88:.4f}")
        x_expr = f"{xs[key][0]} + {xs[key][1]} + {gap}"

    head_y = c2_y + 52
    children.append(rect(f"{p}_rectEntete", tbl_x, head_y, "Parent.Width - 112", 32,
                         INDIGO50))
    children.append(label(f"{p}_lblColNum", '"#"', tbl_x, head_y, num_w, 32, size=11,
                          color=NAVY, bold=True, Align="Align.Center"))
    for key, title, _ in cols:
        x, w = xs[key]
        children.append(label(f"{p}_lblCol{key}", f'"{title}"', x,
                              head_y, w, 32, size=11, color=NAVY, bold=True))

    # Cellules de la galerie (coordonnées relatives à la galerie)
    def gx(key):
        return f"{xs[key][0]} - {tbl_x}"

    row_h = 56
    in_y = 10
    lignee_known = ("!IsBlank(LookUp('x_Référentiel Lignées', "
                    "Title = Trim(nd_txtLignee.Text)))")
    cells = [
        label(f"{p}_lblNum",
              "CountRows(Filter(colEchantillons, Id <= ThisItem.Id))",
              0, in_y, num_w, 36, size=12, color=INDIGO500, bold=True,
              Align="Align.Center"),
        text_input(f"{p}_txtNom", "ThisItem.Nom", gx("Nom"), in_y, xs["Nom"][1],
                   hint="Nom de l'échantillon",
                   onchange=sync("Nom", "Self.Text"),
                   BorderColor=f"If(varTentative && IsBlank(Trim(Self.Text)), {CORAL}, {INDIGO200})"),
        text_input(f"{p}_txtRef", "ThisItem.Ref", gx("Ref"), in_y, xs["Ref"][1],
                   hint="Réf. commerciale", onchange=sync("Ref", "Self.Text")),
        ctrl(f"{p}_cbType", "Classic/ComboBox@2.4.0", {
            "Items": "Choices([@'x_Demandes CODECOH'].Tyoedesubstance)",
            "DefaultSelectedItems": "Filter(Choices([@'x_Demandes CODECOH'].Tyoedesubstance), Value = ThisItem.TypeSub)",
            "DisplayFields": '["Value"]', "SearchFields": '["Value"]',
            "SelectMultiple": "false", "IsSearchable": "false",
            "InputTextPlaceholder": '"Choisir…"',
            "OnChange": sync("TypeSub", "Self.Selected.Value"),
            "X": gx("TypeSub"), "Y": in_y, "Width": xs["TypeSub"][1], "Height": 36,
            "Font": FONT, "Size": 12, "Color": TEXT, "Fill": WHITE,
            "BorderColor": INDIGO200, "HoverBorderColor": INDIGO500,
            "ChevronBackground": WHITE, "ChevronFill": NAVY,
            "ChevronHoverBackground": INDIGO50, "ChevronHoverFill": NAVY,
            "SelectionFill": NAVY, "SelectionColor": WHITE,
            "HoverFill": INDIGO50, "HoverColor": TEXT,
            "PressedFill": NAVY, "PressedColor": WHITE,
            "AccessibleLabel": '"Type de substance"'}),
        text_input(f"{p}_txtSource", "ThisItem.Source", gx("Source"), in_y,
                   xs["Source"][1], hint="Source tissu",
                   onchange=sync("Source", "Self.Text")),
        text_input(f"{p}_txtLignee", "ThisItem.Lignee", gx("Lignee"), in_y,
                   f"{xs['Lignee'][1]} - 34", hint="Lignée cellulaire",
                   onchange=sync("Lignee", "Self.Text")),
        icon(f"{p}_icoLignee",
             f"If({lignee_known}, Icon.CheckBadge, Icon.Warning)",
             f"{gx('Lignee')} + {xs['Lignee'][1]} - 28", in_y + 6, 24,
             f"If({lignee_known}, {GREEN}, {CORAL})",
             tooltip="",
             Tooltip=f'If({lignee_known}, "Lignée connue du référentiel", '
                     '"Nouvelle lignée : non présente dans le référentiel")',
             Visible="!IsBlank(Trim(nd_txtLignee.Text))"),
        icon(f"{p}_icoDupliquer", "Icon.Copy",
             "Parent.TemplateWidth - 84", in_y + 2, 32, NAVY,
             onselect=(f"Collect(colEchantillons, {{Id: varNextId, "
                       "Nom: nd_txtNom.Text & \" (copie)\", Ref: nd_txtRef.Text, "
                       "TypeSub: nd_cbType.Selected.Value, Source: nd_txtSource.Text, "
                       "Lignee: nd_txtLignee.Text});\nSet(varNextId, varNextId + 1)"),
             tooltip="Dupliquer cette ligne",
             PaddingTop=4, PaddingBottom=4, PaddingLeft=4, PaddingRight=4),
        icon(f"{p}_icoSupprimer", "Icon.Trash",
             "Parent.TemplateWidth - 44", in_y + 2, 32, CORAL,
             onselect="Remove(colEchantillons, LookUp(colEchantillons, Id = ThisItem.Id))",
             tooltip="Supprimer cette ligne",
             DisplayMode="If(CountRows(colEchantillons) > 1, DisplayMode.Edit, DisplayMode.Disabled)",
             DisabledColor=INDIGO200,
             PaddingTop=4, PaddingBottom=4, PaddingLeft=4, PaddingRight=4),
        rect(f"{p}_rectSep", 0, "Parent.TemplateHeight - 1", "Parent.TemplateWidth",
             1, INDIGO200),
    ]
    gal_y = head_y + 36
    children.append(ctrl(f"{p}_galEchantillons", "Gallery@2.15.0", {
        "Items": "colEchantillons",
        "X": tbl_x, "Y": gal_y, "Width": "Parent.Width - 112",
        "Height": f"Parent.Height - {gal_y + footer_h + 20}",
        "TemplateSize": row_h, "TemplatePadding": 0,
        "Fill": TRANSPARENT, "TemplateFill": WHITE, "ShowScrollbar": "true",
        "BorderThickness": 0, "AccessibleLabel": '"Liste des échantillons à déclarer"',
    }, children=cells, variant="Vertical"))

    # ---- Pied de page : avertissement + boutons ---------------------------
    nb_new = ("CountRows(Filter(nd_galEchantillons.AllItems, "
              "!IsBlank(Trim(nd_txtLignee.Text)) && IsBlank(LookUp('x_Référentiel Lignées', "
              "Title = Trim(nd_txtLignee.Text)))))")
    submit = f"""Set(varTentative, true);
If(
    CountRows(Filter(nd_galEchantillons.AllItems, IsBlank(Trim(nd_txtNom.Text)))) > 0,
    Notify("Chaque échantillon doit avoir un nom.", NotificationType.Error),
    Set(varEnvoiEnCours, true);
    ClearCollect(
        colCrees,
        ForAll(
            nd_galEchantillons.AllItems,
            Patch(
                'x_Demandes CODECOH',
                Defaults('x_Demandes CODECOH'),
                {{
                    Titre: If(IsBlank(Trim(nd_txtTitre.Text)), Trim(nd_txtNom.Text), Trim(nd_txtTitre.Text)),
                    'Nom échantillon': Trim(nd_txtNom.Text),
                    'Référence commerciale': nd_txtRef.Text,
                    'Type de substance': nd_cbType.Selected,
                    'Source tissu': nd_txtSource.Text,
                    'Lignée cellulaire': Trim(nd_txtLignee.Text),
                    'Nom fournisseur': nd_txtFournisseur.Text,
                    'Adresse fournisseur': nd_txtAdrFournisseur.Text,
                    'Adresse expéditeur': nd_txtAdrExpediteur.Text,
                    'Nom demandeur': nd_txtDemandeur.Text,
                    Commentaires: nd_txtCommentaires.Text
                }}
            )
        )
    );
    Set(varEnvoiEnCours, false);
    If(
        IsEmpty(Errors('x_Demandes CODECOH')),
        Notify(CountRows(colCrees) & " échantillon(s) déclaré(s) avec succès.", NotificationType.Success);
        Navigate(ScrMesDemandes, ScreenTransition.Fade),
        Notify("Erreur lors de l'enregistrement : " & First(Errors('x_Demandes CODECOH')).Message, NotificationType.Error)
    )
)"""
    fy = f"Parent.Height - {footer_h - 12}"
    children += [
        icon(f"{p}_icoInfo", "Icon.Warning", M, f"{fy} + 10", 24, CORAL,
             tooltip="Nouvelles lignées", Visible=f"{nb_new} > 0"),
        label(f"{p}_lblInfo",
              f'{nb_new} & " nouvelle(s) lignée(s) hors référentiel : pensez à joindre '
              'la documentation (certificat, fiche fournisseur) à la demande."',
              M + 32, fy, "Parent.Width - 640", 44, size=11, color=CORAL,
              Visible=f"{nb_new} > 0"),
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
ClearCollect(colEchantillons, {EMPTY_ROW});
Set(varNextId, 2);
Reset(nd_txtTitre);
Reset(nd_txtDemandeur);
Reset(nd_txtFournisseur);
Reset(nd_txtAdrFournisseur);
Reset(nd_txtAdrExpediteur);
Reset(nd_txtCommentaires)"""
    return render_screen("ScrNouvelleDemande",
                         {"Fill": INDIGO50, "LoadingSpinnerColor": NAVY,
                          "OnVisible": on_visible}, children)


# =============================================================================
# 3. Mes demandes : même contenu, charte Servier
#    (la galerie garde le nom Gallery1 : ScrDetailDemande utilise Gallery1.Selected)
# =============================================================================
def screen_mes_demandes():
    M = 32
    cells = [
        label("Title1", "ThisItem.Titre", 24, 10, "Parent.TemplateWidth - 340", 28,
              size=14, color=NAVY, bold=True, OnSelect="Select(Parent)"),
        label("Subtitle1", "ThisItem.'Nom échantillon'", 24, 40,
              "Parent.TemplateWidth - 340", 24, size=12, color=TEXT,
              OnSelect="Select(Parent)"),
        label("md_lblDate", '"Créée le " & Text(ThisItem.Created, "dd/mm/yyyy")',
              "Parent.TemplateWidth - 300", 10, 220, 24, size=11, color=INDIGO500,
              Align="Align.Right", OnSelect="Select(Parent)"),
        label("md_lblCodecoh",
              'If(IsBlank(ThisItem.\'Numéro CODECOH\'), "En cours de traitement", '
              '"N° CODECOH : " & ThisItem.\'Numéro CODECOH\')',
              "Parent.TemplateWidth - 300", 38, 220, 24, size=11,
              color=f"If(IsBlank(ThisItem.'Numéro CODECOH'), {CORAL}, {GREEN})",
              bold=True, Align="Align.Right", OnSelect="Select(Parent)"),
        icon("NextArrow1", "Icon.ChevronRight", "Parent.TemplateWidth - 64", 18, 40,
             NAVY, onselect="Navigate(ScrDetailDemande, ScreenTransition.Cover)",
             tooltip="Afficher le détail"),
        rect("Rectangle1", 0, 0, 4, "Parent.TemplateHeight - 1", CORAL,
             Visible="ThisItem.IsSelected", OnSelect="Select(Parent)"),
        rect("Separator1", 0, "Parent.TemplateHeight - 1", "Parent.TemplateWidth", 1,
             INDIGO200, OnSelect="Select(Parent)"),
    ]
    children = header("md", '"Mes demandes"',
                      '"Retrouvez toutes les demandes que vous avez déposées"')
    children += [
        text_input("md_txtRecherche", '""', M, 112, 420, hint="Rechercher un échantillon…"),
        icon("md_icoRecherche", "Icon.Search", M + 384, 118, 24, INDIGO500),
        button("md_btnNouvelle", '"+  Nouvelle demande"', "Parent.Width - 252", 108,
               220, 40, "Navigate(ScrNouvelleDemande, ScreenTransition.Cover)"),
        card("md_cardListe", M, 164, "Parent.Width - 64", "Parent.Height - 196"),
        ctrl("Gallery1", "Gallery@2.15.0", {
            "Items": """SortByColumns(
    Filter(
        'x_Demandes CODECOH',
        Author.Email = User().Email,
        IsBlank(md_txtRecherche.Text) || StartsWith('Nom échantillon', md_txtRecherche.Text)
    ),
    "ID",
    SortOrder.Descending
)""",
            "X": M + 1, "Y": 165, "Width": "Parent.Width - 66",
            "Height": "Parent.Height - 198", "TemplateSize": 72, "TemplatePadding": 0,
            "Fill": TRANSPARENT, "TemplateFill": f"If(ThisItem.IsSelected, {INDIGO50}, {WHITE})",
            "AccessibleLabel": '"Liste de mes demandes"'},
            children=cells, variant="Vertical"),
    ]
    return render_screen("ScrMesDemandes", {"Fill": INDIGO50,
                                            "LoadingSpinnerColor": NAVY}, children)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "1_ScrAccueil.pa.yaml": screen_accueil(),
        "2_ScrNouvelleDemande.pa.yaml": screen_nouvelle(),
        "3_ScrMesDemandes.pa.yaml": screen_mes_demandes(),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print("écrit", OUT / name)
    # Variante « contrôles seuls » : à coller dans un écran vide existant
    for i, (name, (props, children)) in enumerate(SCREENS.items(), 1):
        lines = []
        for c in children:
            lines.extend(render_ctrl(c, 0))
        (OUT / "controles_seuls" / f"{i}_{name}_controles.pa.yaml").parent.mkdir(exist_ok=True)
        (OUT / "controles_seuls" / f"{i}_{name}_controles.pa.yaml").write_text(
            "\n".join(lines) + "\n", encoding="utf-8")
        props_txt = "\n\n".join(f"### Propriété {k} (à coller dans la barre de formule)\n{v}" for k, v in sorted(props.items()))
        (OUT / "controles_seuls" / f"{i}_{name}_proprietes_ecran.txt").write_text(
            props_txt + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
