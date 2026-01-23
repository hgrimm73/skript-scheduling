import streamlit as st
import datetime

# --- KONFIGURATION ---
st.set_page_config(page_title="Stadion Scheduling Assistent", layout="wide")

# CSS für Checklisten-Optik und Alignment
st.markdown("""
    <style>
    .stCheckbox { margin-bottom: -15px; padding-top: 10px; }
    .stCodeBlock { margin-top: -10px; }
    .Erledigt { opacity: 0.4; filter: grayscale(100%); }
    </style>
    """, unsafe_allow_html=True)

ANPFIFF_ZEITEN = ["15:30", "17:30", "18:30", "18:45", "19:30", "20:00", "20:30", "20:45", "21:00"]

# Hilfsfunktion für AM/PM Konvertierung
def to_ampm(time_str):
    try:
        # Extrahiert nur HH:MM falls ca. oder Text dabei steht
        clean_time = "".join(filter(lambda x: x in "0123456789:", time_str[:5]))
        t = datetime.datetime.strptime(clean_time, "%H:%M")
        return t.strftime("%I:%M %p").lstrip("0")
    except:
        return time_str # Falls "ca. 20:30" etc.

MD_MATRIX = {
    "stadion_offen": ["13:15", "15:15", "16:15", "16:30", "17:15", "17:45", "18:15", "18:30", "18:45"],
    "akkr": ["07:00"] * 9,
    "nmd_start_ref": ["06:00"] * 9,
    "p18_ref_row": ["07:00", "09:00", "10:00", "10:15", "11:00", "11:30", "12:00", "12:15", "12:30"],
    "vorkontrollen": [
        ("Vorkontrollen - START", ["07:00", "09:00", "10:00", "10:15", "11:00", "11:30", "12:00", "12:15", "12:30"]),
        ("Vorkontrollen - ENDE", ["09:00", "11:00", "11:45", "12:15", "13:00", "13:30", "13:45", "13:45", "13:45"]),
        ("Museum - START", ["09:45", "11:45", "11:45", "13:45", "13:45", "13:45", "13:45", "13:45", "13:45"]),
        ("PRE-Content - START", ["12:00", "14:00", "15:00", "15:15", "16:00", "16:30", "17:00", "17:15", "17:30"]),
        ("POST-Content - ENDE", ["20:30", "22:30", "23:30", "23:45", "00:30", "01:00", "01:30", "01:45", "02:00"])
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

# --- LOGIN ---
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
    bereich = st.selectbox("Bereich", ["Touchpoints (Skripte)", "Vorkontrollen & Wegeleitung"])
    st.divider()
    run = st.button("Scheduling", type="primary", use_container_width=True)

if run or "last_run" in st.session_state:
    st.session_state["last_run"] = True
    idx = ANPFIFF_ZEITEN.index(anpfiff)
    is_bl = wettbewerb == "Bundesliga"
    
    if "Touchpoints" in bereich:
        ref_anpfiff = datetime.datetime.strptime(anpfiff, "%H:%M")
        ref_nmd = datetime.datetime.strptime(MD_MATRIX["nmd_start_ref"][idx], "%H:%M")
        ref_p18 = datetime.datetime.strptime(MD_MATRIX["p18_ref_row"][idx], "%H:%M")
        ref_open = datetime.datetime.strptime(MD_MATRIX["stadion_offen"][idx], "%H:%M")
        akkr_time = datetime.datetime.strptime(MD_MATRIX["akkr"][idx], "%H:%M")
        prio18_anchor = ref_p18 - datetime.timedelta(minutes=5)
        
        main_scripts = []
        for prio, cl_n, bl_n in SKRIPTE_BASE:
            name = (bl_n if is_bl else cl_n).replace("XX.XX.20XX", datum)
            if "EingangNord" in name: dt = akkr_time
            elif prio == 1: dt = ref_nmd - datetime.timedelta(minutes=5)
            elif 3 <= prio <= 18: dt = prio18_anchor - datetime.timedelta(minutes=(18-prio)*5)
            elif prio == 19: dt = ref_anpfiff - datetime.timedelta(hours=4, minutes=5)
            elif prio == 20: dt = ref_anpfiff - datetime.timedelta(hours=3, minutes=5)
            else: continue
            main_scripts.append({'prio': prio, 'name': name, 'dt': dt})

        # Kollisions-Check
        main_scripts.sort(key=lambda x: x['prio'])
        used = set()
        for s in main_scripts:
            while s['dt'].strftime("%H:%M") in used: s['dt'] -= datetime.timedelta(minutes=5)
            used.add(s['dt'].strftime("%H:%M"))

        # --- AUSGABE ---
        for s in main_scripts:
            p = s['prio']
            # Jedes Skript bekommt einen eindeutigen Key für die Checkbox
            checked = st.checkbox(f"Erledigt", key=f"check_{p}")
            
            # CSS Klasse falls erledigt
            div_class = "Erledigt" if checked else ""
            
            st.markdown(f'<div class="{div_class}">', unsafe_allow_html=True)
            c1, c2 = st.columns([5, 1])
            c1.code(s['name'], language=None)
            c2.markdown(f"#### **{to_ampm(s['dt'].strftime('%H:%M'))}**")
            
            # States Logik
            def st_row(lbl, z):
                sc1, sc2 = st.columns([5, 1])
                sc1.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp; └─ *{lbl}*")
                sc2.markdown(f"**{to_ampm(z)}**")

            if p == 1:
                st_row("State: MD Content - ab 3,5h vor Anpfiff", (ref_anpfiff - datetime.timedelta(hours=3, minutes=30)).strftime("%H:%M"))
                st_row("State: MD Content ab Stadionöffnung", ref_open.strftime("%H:%M"))
                st_row("State: Verkehrsführung ab 70. Minute", (ref_anpfiff + datetime.timedelta(hours=1, minutes=25)).strftime("%H:%M"))
            elif p == 2:
                st_row("State: PreMatch mit Hospitality", ref_open.strftime("%H:%M"))
                st_row("State: PostMatch ab 2. Halbzeit", (ref_anpfiff + datetime.timedelta(minutes=45)).strftime("%H:%M"))
            elif p in [5, 6, 7, 8, 17]:
                st_row("State: Welcome Only", ref_open.strftime("%H:%M"))
                st_row("State: PRE-Match", (ref_open + datetime.timedelta(minutes=15)).strftime("%H:%M"))
            elif p in [9, 10, 11, 12, 13, 15, 16]:
                st_row("State: Welcome Only", (ref_open + datetime.timedelta(minutes=15)).strftime("%H:%M"))
                st_row("State: PRE-Match", (ref_open + datetime.timedelta(minutes=30)).strftime("%H:%M"))
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.divider()

    else:
        # Vorkontrollen & Wegeleitung
        for k in ["vorkontrollen", "wegeleitung"]:
            st.subheader(k.capitalize())
            for label, zeiten in MD_MATRIX[k]:
                c1, c2 = st.columns([5, 1])
                c1.markdown(label)
                c2.markdown(f"**{to_ampm(zeiten[idx])}**")
