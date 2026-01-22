import streamlit as st
import datetime

# --- KONFIGURATION & DATEN ---
st.set_page_config(page_title="Stadion Scheduling Tool", layout="wide")

ANPFIFF_ZEITEN = ["15:30", "17:30", "18:30", "18:45", "19:30", "20:00", "20:30", "20:45", "21:00"]
LABEL_WIDTH = 90

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
        ("Vorkontrollen - Timeline: POST-Content - ENDE", ["ca. 20:30", "ca. 22:30", "ca. 23:30", "ca. 23:45", "ca. 00:30", "ca. 01:00", "ca. 01:30", "ca. 01:45", "ca. 02:00"])
    ],
    "wegeleitung": [
        ("Wegeleitung - NMD Content ausspielen - START", ["06:00"] * 9),
        ("Wegeleitung - NMD Content ausspielen - ENDE", ["12:00", "14:00", "15:00", "15:15", "16:00", "16:30", "17:00", "17:15", "17:30"]),
        ("Wegeleitung - MD Content ausspielen - START", ["12:00", "14:00", "15:00", "15:15", "16:00", "16:30", "17:00", "17:15", "17:30"]),
        ("Wegeleitung - MD Content ausspielen - ENDE", ["ca. 20:30", "ca. 22:30", "ca. 23:30", "ca. 23:45", "ca. 00:30", "ca. 01:00", "ca. 01:30", "ca. 01:45", "ca. 02:00"])
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

# --- LOGIN LOGIK ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "makeitso!":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Passwort eingeben", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Passwort eingeben", type="password", on_change=password_entered, key="password")
        st.error("Falsches Passwort")
        return False
    else:
        return True

# --- HAUPTPROGRAMM ---
if check_password():
    st.title("⚽ Stadion Scheduling Assistent")

    # Sidebar für Einstellungen
    with st.sidebar:
        st.header("Konfiguration")
        datum = st.date_input("Spieldatum", datetime.date.today()).strftime("%d.%m.%Y")
        wettbewerb = st.selectbox("Wettbewerb", ["Bundesliga", "Champions League"])
        anpfiff = st.selectbox("Anpfiffzeit", ANPFIFF_ZEITEN)
        bereich = st.selectbox("Bereich", ["Vorkontrollen", "Wegeleitung", "Touchpoints (Skripte)"])
        run_btn = st.button("Scheduling")

    if run_btn:
        idx = ANPFIFF_ZEITEN.index(anpfiff)
        is_bl = wettbewerb == "Bundesliga"
        
        output_buffer = []
        output_buffer.append(f"ERGEBNIS FÜR: {wettbewerb} | DATUM: {datum} | ANPFIFF: {anpfiff}")
        output_buffer.append("="*110 + "\n")

        if bereich == "Vorkontrollen":
            for label, zeiten in MD_MATRIX["vorkontrollen"]:
                output_buffer.append(f"{label.ljust(LABEL_WIDTH, '.')} | {zeiten[idx]}")
        
        elif bereich == "Wegeleitung":
            for label, zeiten in MD_MATRIX["wegeleitung"]:
                output_buffer.append(f"{label.ljust(LABEL_WIDTH, '.')} | {zeiten[idx]}")

        elif bereich == "Touchpoints (Skripte)":
            ref_anpfiff = datetime.datetime.strptime(anpfiff, "%H:%M")
            ref_nmd_start = datetime.datetime.strptime(MD_MATRIX["nmd_start_ref"][idx], "%H:%M")
            ref_p18_row = datetime.datetime.strptime(MD_MATRIX["p18_ref_row"][idx], "%H:%M")
            ref_opening = datetime.datetime.strptime(MD_MATRIX["stadion_offen"][idx], "%H:%M")
            akkr_time = datetime.datetime.strptime(MD_MATRIX["akkr"][idx], "%H:%M")

            prio18_anchor = ref_p18_row - datetime.timedelta(minutes=5)
            
            main_scripts = []
            for prio, cl_n, bl_n in SKRIPTE_BASE:
                raw_name = bl_n if is_bl else cl_n
                name = raw_name.replace("XX.XX.20XX", datum)
                if "EingangNord" in name or "Eingang Nord" in name:
                    dt = akkr_time
                elif prio == 1:
                    dt = ref_nmd_start - datetime.timedelta(minutes=5)
                elif 3 <= prio <= 18:
                    dt = prio18_anchor - datetime.timedelta(minutes=(18-prio)*5)
                elif prio == 19:
                    dt = ref_anpfiff - datetime.timedelta(hours=4, minutes=5)
                elif prio == 20:
                    dt = ref_anpfiff - datetime.timedelta(hours=3, minutes=5)
                else: continue
                main_scripts.append({'prio': prio, 'name': name, 'dt': dt})

            # Kollisions-Check
            main_scripts.sort(key=lambda x: x['prio'])
            used_times = set()
            for script in main_scripts:
                curr_dt = script['dt']
                while curr_dt.strftime("%H:%M") in used_times:
                    curr_dt -= datetime.timedelta(minutes=5)
                script['dt'] = curr_dt
                used_times.add(curr_dt.strftime("%H:%M"))

            for script in main_scripts:
                time_str = script['dt'].strftime("%H:%M")
                prio = script['prio']
                output_buffer.append(f"{script['name'].ljust(LABEL_WIDTH, '.')} | Start: {time_str}")
                
                # States hinzufügen
                def add_state(label, zeit):
                    display_text = f"    ... {label}"
                    output_buffer.append(f"{display_text.ljust(LABEL_WIDTH, '.')} | {zeit}")

                if prio == 1:
                    add_state("MD Content - nur mit Akkreditierung - ab 3,5h...", (ref_anpfiff - datetime.timedelta(hours=3, minutes=30)).strftime("%H:%M"))
                    add_state("MD Content ab Stadionöffnung bis 70. Minute", ref_opening.strftime("%H:%M"))
                    add_state("MD Content Verkehrsführung ab 70. Minute", (ref_anpfiff + datetime.timedelta(hours=1, minutes=25)).strftime("%H:%M"))
                elif prio == 2:
                    add_state("PreMatch mit Hospitality ab Stadionöffnung", ref_opening.strftime("%H:%M"))
                    add_state("PostMatch ab 2. Halbzeit", (ref_anpfiff + datetime.timedelta(minutes=45)).strftime("%H:%M"))
                elif prio in [5, 6, 7, 8, 17]:
                    add_state("State: Welcome Only", ref_opening.strftime("%H:%M"))
                    add_state("State: PRE-Match", (ref_opening + datetime.timedelta(minutes=15)).strftime("%H:%M"))
                elif prio in [9, 10, 11, 12, 13, 15, 16]:
                    add_state("State: Welcome Only", (ref_opening + datetime.timedelta(minutes=15)).strftime("%H:%M"))
                    add_state("State: PRE-Match", (ref_opening + datetime.timedelta(minutes=30)).strftime("%H:%M"))

        # Anzeige in einem monospaced Code-Block für perfekte Ausrichtung
        st.code("\n".join(output_buffer), language="text")
