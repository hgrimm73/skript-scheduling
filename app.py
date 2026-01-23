import streamlit as st
import datetime

# --- KONFIGURATION ---
st.set_page_config(page_title="Stadion Scheduling Assistent", layout="wide")

# CSS für Checklisten-Optik und Alignment
st.markdown("""
    <style>
    .stCheckbox { margin-bottom: -15px; padding-top: 10px; }
    .stCodeBlock { margin-top: -10px; }
    .Erledigt { 
        opacity: 0.3; 
        filter: grayscale(100%); 
        text-decoration: line-through;
    }
    /* Fix für Spalten-Abstände */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

ANPFIFF_ZEITEN = ["15:30", "17:30", "18:30", "18:45", "19:30", "20:00", "20:30", "20:45", "21:00"]

# Robuste Hilfsfunktion für AM/PM Konvertierung
def to_ampm(time_str):
    if not time_str or "ca." in time_str.lower():
        # Behandelt Spezialfälle wie "ca. 20:30"
        prefix = "ca. " if "ca." in time_str.lower() else ""
        raw = time_str.lower().replace("ca.", "").strip()
        try:
            t = datetime.datetime.strptime(raw[:5], "%H:%M")
            return prefix + t.strftime("%I:%M %p").lstrip("0")
        except:
            return time_str
    try:
        t = datetime.datetime.strptime(time_str[:5], "%H:%M")
        return t.strftime("%I:%M %p").lstrip("0")
    except:
        return time_str

MD_MATRIX = {
    "stadion_offen": ["13:15", "15:15", "16:15", "16:30", "17:15", "17:45", "18:15", "18:30", "18:45"],
    "akkr": ["07:00"] * 9,
    "nmd_start_ref": ["06:00"] * 9,
    "p18_ref_row": ["07:00", "09:00", "10:00", "10:15", "11:00", "11:30", "12:00", "12:15", "12:30"],
    
    "vorkontrollen": [
        ("Vorkontrollen - Timeline: LED-Service für W&W Spieltagstest - START", ["07:00", "09:00", "10:00", "10:15", "11:00", "11:30", "12:00", "12:15", "12:30"]),
        ("Vorkontrollen - Timeline: LED-Service für W&W Spieltagstest - ENDE", ["09:00", "11:00", "11:45", "12:15", "13:00", "13:30", "13:45", "13:45", "13:45"]),
        ("Vorkontrollen - Timeline: Museums Content - START", ["09:45", "11:45", "11:45", "13:45", "13:45", "13:45", "13:45", "13:45", "13:45"]),
        ("Vorkontrollen - Timeline: Museums Content - ENDE", ["12:00", "14:00", "15:00", "15:15", "16:00", "16:30", "17:00", "17:15", "17:30"]),
        ("Vorkontrollen - Timeline: PRE-Content - START", ["12:00", "14:00", "15:00", "15:15", "16:00", "16:30", "17:00", "17:15", "17:30"]),
        ("Vorkontrollen - Timeline: PRE-Content - ENDE", ["16:55", "18:55", "19:55", "19:15", "20:55", "21:25", "21:55", "21:15", "22:25"]),
        ("Vorkontrollen - Timeline: POST-Content - START", ["16:55", "18:55", "19:55", "19:15", "20:55", "21:25", "21:55", "21:15", "22:25"]),
        ("Vorkontrollen - Timeline: POST-Content - ENDE", ["20:30", "22:30", "23:30", "23:45", "00:30", "01:00", "01:30", "01:45", "02:00"])
    ],
    
    "wegeleitung": [
        ("Wegeleitung - NMD Content ausspielen - START", ["06:00"] * 9),
        ("Wegeleitung - NMD Content ausspielen - ENDE", ["12:00", "14:00", "15:00", "15:15", "16:00", "16:30", "17:00", "17:15", "17:30"]),
        ("Wegeleitung - MD Content ausspielen - START", ["12:00", "14:00", "15:00", "15:15", "16:00", "16:30", "17:00", "17:15", "17:30"]),
        ("Wegeleitung - MD Content ausspielen - ENDE", ["20:30", "22:30", "23:30", "23:45", "00:30", "01:00", "01:30", "01:45", "02:00"])
    ]
}

SKRIPTE_BASE = [
    (1, "MD - FCB - Verkehrsführung inkl. P0 Pförtner - Ebene 0 - XX.XX.20XX", "MD - FCB - Verkehrsführung inkl. P0 Pförtner - Ebene 0 - XX.XX.20XX"),
    (2, "CL-EingangNord-XX.XX.20XX", "BL-EingangNord-XX.XX.20XX"),
    (3, "CL-Kioske-E6-XX.XX.20XX", "BL-Kioske-E6-XX.XX.20XX"),
    (4, "CL-Kioske-E2-XX.XX.20XX", "BL-Kioske-E2-XX.XX.20XX"),
    (5, "CL-Kioske E2 Screen an Wand-XX.XX.20XX", "BL-Kioske E2 Screen an Wand-XX.XX.20XX"),
    (6, "CL-Umlauf-E6-XX.XX.20XX", "BL-Umlauf-E6-XX.XX.20XX"),
    (7, "CL-Umlauf-E2-XX.XX.20XX", "BL-Umlauf-E2-XX.XX.20XX"),
    (8, "CL-SocialWall-XX.XX.20XX", "BL-SocialWall-XX.XX.20XX"),
    (9, "CL-WZW RT Screens übereinander-MixedZone-SpielertunnelTVs-XX.XX.20XX", "BL-WZW RT Screens übereinander-MixedZone-SpielertunnelTVs-XX.XX.20XX"),
    (10, "CL-Infoscreens-E5-XX.XX.20XX", "BL-Infoscreens-E5-XX.XX.20XX"),
    (11, "CL-Rolltreppen-WZW-BusinessArea-XX.XX.20XX", "BL-Rolltreppen-WZW-BusinessArea-XX.XX.20XX"),
    (12, "CL-BusinessClub-E4-XX.XX.20XX", "BL-BusinessClub-E4-XX.XX.20XX"),
    (13, "CL-Audi Empfang-E4-XX.XX.20XX", "BL-Audi Empfang-E4-XX.XX.20XX"),
    (14, "CL-AudiWall-WZW-XX.XX.20XX", "BL-AudiWall-WZW-XX.XX.20XX"),
    (15, "CL-BusinessWall-XX.XX.20XX", "BL-BusinessWall-XX.XX.20XX"),
    (16, "CL-Empfangstheken Durchgänge-XX.XX.20XX", "BL-Empfangstheken Durchgänge-XX.XX.20XX"),
    (17, "CL-Fantreff Süd-XX.XX.20XX", "BL-Fantreff Süd-XX.XX.20XX"),
    (18, "CL-Spielertunnel-XX.XX.20XX", "BL-Spielertunnel-XX.XX.20XX"),
    (19, "CL-Gästeparkhaus-LED-XX.XX.20XX", "BL-Gästeparkhaus-LED-XX.XX.20XX"),
    (20, "CL-Audi Tiefgarage-S0 E1-alle gleich-XX.XX.20XX", "BL-Audi Tiefgarage-S0 E1-alle gleich-XX.XX.20XX")
]

# --- PASSWORT PRÜFUNG ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    pwd = st.text_input("Passwort", type="password")
    if pwd == "makeitso!":
        st.session_state["password_correct"] = True
        st.rerun()
    else: st.stop()

# --- APP ---
st.title("⚽ Stadion Scheduling Assistent")

with st.sidebar:
    st.header("Konfiguration")
    datum_dt = st.date_input("Datum", datetime.date.today())
    datum = datum_dt.strftime("%d.%m.%Y")
    wettbewerb = st.selectbox("Wettbewerb", ["Bundesliga", "Champions League"])
    anpfiff = st.selectbox("Anpfiff", ANPFIFF_ZEITEN)
    bereich = st.selectbox("Bereich", ["Touchpoints (Skripte)", "Vorkontrollen", "Wegeleitung"])
    st.divider()
    run = st.button("Scheduling", type="primary", use_container_width=True)

if run or "last_run" in st.session_state:
    st.session_state["last_run"] = True
    idx = ANPFIFF_ZEITEN.index(anpfiff)
    is_bl = wettbewerb == "Bundesliga"
    
    if bereich == "Touchpoints (Skripte)":
        # Referenzzeiten
        ref_anp = datetime.datetime.strptime(anpfiff, "%H:%M")
        ref_nmd = datetime.datetime.strptime(MD_MATRIX["nmd_start_ref"][idx], "%H:%M")
        ref_p18 = datetime.datetime.strptime(MD_MATRIX["p18_ref_row"][idx], "%H:%M")
        ref_open = datetime.datetime.strptime(MD_MATRIX["stadion_offen"][idx], "%H:%M")
        akkr_t = datetime.datetime.strptime(MD_MATRIX["akkr"][idx], "%H:%M")
        prio18_anchor = ref_p18 - datetime.timedelta(minutes=5)
        
        main_scripts = []
        for prio, cl_n, bl_n in SKRIPTE_BASE:
            name = (bl_n if is_bl else cl_n).replace("XX.XX.20XX", datum)
            if "EingangNord" in name: dt = akkr_t
            elif prio == 1: dt = ref_nmd - datetime.timedelta(minutes=5)
            elif 3 <= prio <= 18: dt = prio18_anchor - datetime.timedelta(minutes=(18-prio)*5)
            elif prio == 19: dt = ref_anp - datetime.timedelta(hours=4, minutes=5)
            elif prio == 20: dt = ref_anp - datetime.timedelta(hours=3, minutes=5)
            else: continue
            main_scripts.append({'prio': prio, 'name': name, 'dt': dt})

        # Kollisions-Check
        main_scripts.sort(key=lambda x: x['prio'])
        used = set()
        for s in main_scripts:
            while s['dt'].strftime("%H:%M") in used: s['dt'] -= datetime.timedelta(minutes=5)
            used.add(s['dt'].strftime("%H:%M"))

        # --- AUSGABE TOUCHPOINTS ---
        st.subheader(f"Touchpoints Scheduling ({anpfiff} Uhr)")
        for s in main_scripts:
            p = s['prio']
            is_done = st.checkbox(f"Erledigt", key=f"check_{p}")
            style_class = "Erledigt" if is_done else ""
            
            st.markdown(f'<div class="{style_class}">', unsafe_allow_html=True)
            c1, c2 = st.columns([5, 1.2])
            c1.code(s['name'], language=None)
            c2.markdown(f"#### **{to_ampm(s['dt'].strftime('%H:%M'))}**")
            
            def add_st(lbl, z):
                sc1, sc2 = st.columns([5, 1.2])
                sc1.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp; └─ *{lbl}*")
                sc2.markdown(f"**{to_ampm(z)}**")

            if p == 1:
                add_st("MD Content - ab 3,5h vor Anpfiff", (ref_anp - datetime.timedelta(hours=3, minutes=30)).strftime("%H:%M"))
                add_st("MD Content ab Stadionöffnung", ref_open.strftime("%H:%M"))
                add_st("Verkehrsführung ab 70. Minute", (ref_anp + datetime.timedelta(hours=1, minutes=25)).strftime("%H:%M"))
            elif p == 2:
                add_st("PreMatch mit Hospitality", ref_open.strftime("%H:%M"))
                add_st("PostMatch ab 2. Halbzeit", (ref_anp + datetime.timedelta(minutes=45)).strftime("%H:%M"))
            elif p in [5, 6, 7, 8, 17]:
                add_st("State: Welcome Only", ref_open.strftime("%H:%M"))
                add_st("State: PRE-Match", (ref_open + datetime.timedelta(minutes=15)).strftime("%H:%M"))
            elif p in [9, 10, 11, 12, 13, 15, 16]:
                add_st("State: Welcome Only", (ref_open + datetime.timedelta(minutes=15)).strftime("%H:%M"))
                add_st("State: PRE-Match", (ref_open + datetime.timedelta(minutes=30)).strftime("%H:%M"))
            st.markdown('</div>', unsafe_allow_html=True)
            st.divider()

    elif bereich == "Vorkontrollen":
        st.subheader("Vorkontrollen Übersicht")
        for label, zeiten in MD_MATRIX["vorkontrollen"]:
            c1, c2 = st.columns([5, 1.2])
            c1.markdown(label)
            c2.markdown(f"**{to_ampm(zeiten[idx])}**")
        st.divider()

    elif bereich == "Wegeleitung":
        st.subheader("Wegeleitung Übersicht")
        for label, zeiten in MD_MATRIX["wegeleitung"]:
            c1, c2 = st.columns([5, 1.2])
            c1.markdown(label)
            c2.markdown(f"**{to_ampm(zeiten[idx])}**")
        st.divider()
