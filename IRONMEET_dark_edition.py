
import streamlit as st
import sqlite3
import hashlib
import json
from datetime import datetime, date
from statistics import mean

APP_TITLE = "IRONMEET — Competition Management System"
DB_FILE = "ironmeet.db"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# IRONMEET VISUAL SYSTEM — DARK ARENA
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap');

:root {
  --im-bg: #090c10;
  --im-panel: #11161d;
  --im-panel-2: #171e27;
  --im-border: #27313d;
  --im-text: #edf2f7;
  --im-muted: #95a2b2;
  --im-accent: #c6f135;
  --im-accent-dark: #9fca16;
}
.stApp { background: radial-gradient(ellipse at 75% -15%, #1c2a20 0%, #0b1015 38%, var(--im-bg) 76%); color: var(--im-text); }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
[data-testid="stHeader"] { background: rgba(9,12,16,.88); }
[data-testid="stToolbar"] { right: 1rem; }
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1500px; }
h1, h2, h3 { font-family: 'Barlow Condensed', sans-serif !important; letter-spacing: .035em; color: #f4f7fa; }
h1 { font-size: clamp(2.1rem, 4vw, 3.15rem) !important; font-weight: 800 !important; }
h2 { font-size: 1.85rem !important; font-weight: 700 !important; }
h3 { font-size: 1.35rem !important; font-weight: 700 !important; }
p, label, .stMarkdown, [data-testid="stCaptionContainer"] { color: var(--im-text); }
[data-testid="stCaptionContainer"] { color: var(--im-muted) !important; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #111820 0%, #0b1015 100%); border-right: 1px solid var(--im-border); }
[data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
[data-testid="stSidebar"] h1 { color: var(--im-accent) !important; font-size: 2rem !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] > label { color: var(--im-muted); font-weight: 700; text-transform: uppercase; letter-spacing: .09em; font-size: .72rem; }
[data-testid="stRadio"] [role="radiogroup"] { gap: .45rem; }
[data-testid="stRadio"] [role="radio"] { background: #151c24; border: 1px solid #27313d; border-radius: 11px; padding: .65rem .8rem; transition: all .15s ease; }
[data-testid="stRadio"] [role="radio"]:hover { border-color: var(--im-accent); background: #1a242b; }
[data-testid="stRadio"] [role="radio"][aria-checked="true"] { background: #253018; border: 1px solid var(--im-accent); }
[data-testid="stRadio"] [role="radio"][aria-checked="true"] p { color: var(--im-accent) !important; font-weight: 700; }
[data-testid="stMetric"] { background: linear-gradient(145deg, #171f28, #10151b); border: 1px solid var(--im-border); border-radius: 14px; padding: 1rem 1.1rem; box-shadow: 0 8px 24px rgba(0,0,0,.16); }
[data-testid="stMetricLabel"] { color: var(--im-muted) !important; font-size: .78rem; text-transform: uppercase; letter-spacing: .07em; }
[data-testid="stMetricValue"] { color: var(--im-accent) !important; font-family: 'Barlow Condensed', sans-serif; font-weight: 700; }
[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stExpander"], [data-testid="stForm"] { background: rgba(17,22,29,.88); border: 1px solid var(--im-border); border-radius: 14px; }
[data-testid="stExpander"] summary { font-weight: 700; }
.stTabs [data-baseweb="tab-list"] { gap: .35rem; border-bottom: 1px solid var(--im-border); }
.stTabs [data-baseweb="tab"] { background: #121820; border: 1px solid transparent; border-radius: 9px 9px 0 0; padding: .7rem 1rem; color: var(--im-muted); font-weight: 700; }
.stTabs [aria-selected="true"] { color: var(--im-accent) !important; background: #202a19 !important; border-color: #53652c !important; }
.stButton > button, [data-testid="stDownloadButton"] button { border-radius: 10px; border: 1px solid #3b4854; background: #1b242d; color: #f4f7fa; font-weight: 700; min-height: 2.65rem; transition: all .15s ease; }
.stButton > button:hover, [data-testid="stDownloadButton"] button:hover { border-color: var(--im-accent); color: var(--im-accent); transform: translateY(-1px); }
.stButton > button[kind="primary"], .stButton > button[data-testid="baseButton-primary"] { background: var(--im-accent); border-color: var(--im-accent); color: #10150a; }
.stButton > button[kind="primary"]:hover { background: #d7ff54; color: #10150a; }
input, textarea, [data-baseweb="select"] > div { background-color: #0e141a !important; color: var(--im-text) !important; border-color: #303b47 !important; border-radius: 9px !important; }
[data-baseweb="select"] span { color: var(--im-text) !important; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border: 1px solid var(--im-border); border-radius: 10px; overflow: hidden; }
[data-testid="stAlert"] { border-radius: 11px; border: 1px solid var(--im-border); }
hr { border-color: var(--im-border) !important; }
.stProgress > div > div > div > div { background-color: var(--im-accent); }
footer { visibility: hidden; }
@media (max-width: 800px) {
 .block-container { padding: 1.2rem 1rem 2rem; }
 [data-testid="stMetric"] { padding: .8rem; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# FEDERATION / RULE LIBRARY
# ============================================================

BODYBUILDING_FEDERATIONS = [
    "ICN", "IFBB", "NPC / NPC Worldwide", "WNBF / INBF",
    "INBA / PNBA", "WBFF", "NABBA", "WABBA", "PCA", "OCB",
    "NGA", "ANBF", "NANBF", "UFE", "USBF", "DFAC", "MuscleMania",
    "IBFA", "BNBF", "UKDFBA", "SNBF", "UNBA", "GBO", "NMA",
    "IBFF", "NPAA", "Custom Federation"
]

POWERLIFTING_FEDERATIONS = [
    "IPF", "Powerlifting America", "Powerlifting India", "USAPL",
    "USPA", "WRPF", "WPC", "WPO", "RPS", "APF", "IPA", "UPA",
    "GPC", "WPF", "WDFPF", "WPA", "100% RAW", "NASA", "IPL",
    "SPF", "CPU", "APL", "Custom Federation"
]

# These are deliberately editable libraries. Federation rules can vary by
# event/year, so the organizer can use "Custom" settings where required.
BODYBUILDING_CATEGORIES = {
    "ICN": [
        "Men's Bodybuilding", "Men's Classic Physique", "Men's Physique",
        "Men's Fitness Model", "Men's Muscle Model", "Men's Street Model",
        "Ms Bikini Model", "Ms Sports Model", "Ms Fitness Model",
        "Ms Figure", "Ms Street Model", "Ms Runway", "ICN Angels"
    ],
    "IFBB": [
        "Men's Bodybuilding", "Men's Classic Physique", "Men's Physique",
        "Men's Fitness", "Men's 212 Bodybuilding", "Women's Bodybuilding",
        "Women's Physique", "Women's Figure", "Women's Bikini",
        "Women's Wellness"
    ],
    "NPC / NPC Worldwide": [
        "Men's Bodybuilding", "Men's Classic Physique", "Men's Physique",
        "Men's Fitness", "Women's Bodybuilding", "Women's Physique",
        "Women's Figure", "Women's Bikini", "Women's Wellness", "Women's Fit Model"
    ],
    "WNBF / INBF": [
        "Men's Bodybuilding", "Men's Classic Physique", "Men's Physique",
        "Women's Bodybuilding", "Women's Figure", "Women's Bikini",
        "Women's Fit Body"
    ],
    "INBA / PNBA": [
        "Men's Bodybuilding", "Men's Classic Physique", "Men's Physique",
        "Women's Bodybuilding", "Women's Figure", "Women's Bikini",
        "Women's Physique", "Women's Fit Body"
    ],
    "WBFF": [
        "Men's Bodybuilding", "Men's Fitness Model", "Men's Muscle Model",
        "Women's Fitness", "Women's Bikini", "Women's Diva"
    ],
    "NABBA": [
        "Men's Bodybuilding", "Men's Athletic", "Men's Classic",
        "Women's Bodybuilding", "Women's Figure", "Women's Bikini"
    ],
    "WABBA": [
        "Men's Bodybuilding", "Men's Classic", "Women's Bodybuilding",
        "Women's Fitness"
    ],
}
DEFAULT_BB_CATEGORIES = [
    "Men's Bodybuilding", "Men's Classic Physique", "Men's Physique",
    "Women's Bodybuilding", "Women's Physique", "Women's Figure",
    "Women's Bikini", "Women's Wellness", "Other"
]

BB_SUBDIVISIONS = [
    "First Timers", "Teenage / Junior", "Under 21", "Under 23",
    "Novice", "Open", "30+", "40+", "50+", "60+", "70+", "Custom"
]

AGE_CATEGORIES = [
    "Sub-Junior", "Junior", "Senior / Open", "Masters", "Custom"
]

# Common class presets. The organizer can always choose Custom.
IPF_MEN_CLASSES = ["59 kg", "66 kg", "74 kg", "83 kg", "93 kg", "105 kg", "120 kg", "+120 kg"]
IPF_WOMEN_CLASSES = ["47 kg", "52 kg", "57 kg", "63 kg", "69 kg", "76 kg", "84 kg", "+84 kg"]

COMMON_PL_CLASSES = [
    "44 kg", "47 kg", "52 kg", "53 kg", "57 kg", "59 kg", "60 kg",
    "63 kg", "66 kg", "69 kg", "74 kg", "76 kg", "83 kg", "84 kg",
    "93 kg", "105 kg", "110 kg", "120 kg", "+120 kg", "+140 kg"
]

BB_POSES = {
    "Men's Bodybuilding": [
        "Front Double Biceps", "Front Lat Spread", "Side Chest",
        "Side Triceps", "Rear Double Biceps", "Rear Lat Spread",
        "Abdominals & Thighs", "Most Muscular"
    ],
    "Men's Classic Physique": [
        "Front Double Biceps", "Side Chest", "Back Double Biceps",
        "Abdominals & Thighs", "Classic Pose", "Favorite Classic Pose"
    ],
    "Men's Physique": [
        "Front", "Side", "Back", "Favorite Pose"
    ],
    "Women's Bodybuilding": [
        "Front Double Biceps", "Side Chest", "Side Triceps",
        "Rear Double Biceps", "Abdominals & Thighs", "Most Muscular"
    ],
    "Women's Physique": [
        "Front Double Biceps", "Side Chest", "Side Triceps",
        "Rear Double Biceps", "Abdominals & Thighs", "Favorite Pose"
    ],
    "Women's Figure": ["Front", "Side", "Back", "Quarter Turns"],
    "Women's Bikini": ["Front", "Back", "Quarter Turns", "Presentation"],
    "Women's Wellness": ["Front", "Side", "Back", "Quarter Turns"],
}
BB_FACTORS = [
    "Muscularity", "Symmetry", "Proportion", "Conditioning",
    "Definition / Separation", "Pose Execution", "Presentation"
]

PAYMENT_METHODS = ["Cash", "UPI", "Card", "Pending"]

# ============================================================
# DATABASE
# ============================================================

def conn():
    c = sqlite3.connect(DB_FILE, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = conn()
    cur = c.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS competitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            venue TEXT,
            country TEXT,
            federation TEXT NOT NULL,
            sport TEXT NOT NULL,
            organizer_pin_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS athletes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_id INTEGER NOT NULL,
            athlete_no TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT,
            gender TEXT,
            dob TEXT,
            country TEXT,
            phone TEXT,
            email TEXT,
            federation TEXT,
            sport TEXT NOT NULL,
            category TEXT,
            subdivision TEXT,
            age_category TEXT,
            weight_class TEXT,
            bodyweight REAL,
            registration_fee REAL DEFAULT 0,
            payment_method TEXT DEFAULT 'Pending',
            payment_reference TEXT,
            registration_status TEXT DEFAULT 'Registered',
            notes TEXT,
            created_at TEXT NOT NULL,
            UNIQUE(competition_id, athlete_no),
            FOREIGN KEY(competition_id) REFERENCES competitions(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS judges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Judge',
            pin_hash TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            UNIQUE(competition_id, name),
            FOREIGN KEY(competition_id) REFERENCES competitions(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            sport TEXT NOT NULL,
            category TEXT,
            subdivision TEXT,
            age_category TEXT,
            weight_class TEXT,
            judge_count INTEGER DEFAULT 3,
            status TEXT DEFAULT 'Not Started',
            current_lineup INTEGER DEFAULT 0,
            finalised INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY(competition_id) REFERENCES competitions(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS lineups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            lineup_no INTEGER NOT NULL,
            athlete_ids TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            UNIQUE(class_id, lineup_no),
            FOREIGN KEY(class_id) REFERENCES classes(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bb_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            lineup_id INTEGER NOT NULL,
            athlete_id INTEGER NOT NULL,
            judge_id INTEGER NOT NULL,
            pose TEXT NOT NULL,
            factor TEXT NOT NULL,
            score REAL NOT NULL,
            submitted_at TEXT NOT NULL,
            UNIQUE(lineup_id, athlete_id, judge_id, pose, factor)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bb_judge_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lineup_id INTEGER NOT NULL,
            judge_id INTEGER NOT NULL,
            submitted_at TEXT NOT NULL,
            UNIQUE(lineup_id, judge_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pl_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            athlete_id INTEGER NOT NULL,
            lift TEXT NOT NULL,
            attempt_no INTEGER NOT NULL,
            weight REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            UNIQUE(class_id, athlete_id, lift, attempt_no)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pl_judgments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id INTEGER NOT NULL,
            judge_id INTEGER NOT NULL,
            decision TEXT NOT NULL,
            reason TEXT,
            submitted_at TEXT NOT NULL,
            UNIQUE(attempt_id, judge_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS class_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            athlete_id INTEGER NOT NULL,
            placing INTEGER NOT NULL,
            score REAL,
            total REAL,
            details TEXT,
            UNIQUE(class_id, athlete_id)
        )
    """)

    c.commit()
    c.close()

def q(sql, params=(), fetch=False, many=False):
    c = conn()
    cur = c.cursor()
    if many:
        cur.executemany(sql, params)
    else:
        cur.execute(sql, params)
    if fetch:
        rows = cur.fetchall()
        c.close()
        return rows
    c.commit()
    last = cur.lastrowid
    c.close()
    return last

def one(sql, params=()):
    rows = q(sql, params, fetch=True)
    return rows[0] if rows else None

def all_rows(sql, params=()):
    return q(sql, params, fetch=True)

def hpin(pin):
    return hashlib.sha256(str(pin).encode()).hexdigest()

def check_pin(pin, hashed):
    return hpin(pin) == hashed

# ============================================================
# HELPERS
# ============================================================

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def selected_comp():
    cid = st.session_state.get("competition_id")
    return one("SELECT * FROM competitions WHERE id=?", (cid,)) if cid else None

def athletes_for_class(class_id):
    cls = one("SELECT * FROM classes WHERE id=?", (class_id,))
    if not cls:
        return []
    rows = all_rows("""
        SELECT a.* FROM athletes a
        JOIN lineups l ON instr(',' || l.athlete_ids || ',', ',' || a.id || ',') > 0
        WHERE l.class_id=?
        ORDER BY CAST(a.athlete_no AS INTEGER), a.id
    """, (class_id,))
    # remove duplicates while preserving order
    seen, out = set(), []
    for r in rows:
        if r["id"] not in seen:
            seen.add(r["id"])
            out.append(r)
    return out

def next_athlete_no(comp_id):
    rows = all_rows("SELECT athlete_no FROM athletes WHERE competition_id=?", (comp_id,))
    nums = []
    for r in rows:
        try:
            nums.append(int(r["athlete_no"]))
        except Exception:
            pass
    return str(max(nums) + 1 if nums else 1)

def category_options(federation):
    return BODYBUILDING_CATEGORIES.get(federation, DEFAULT_BB_CATEGORIES)

def pose_options(category):
    return BB_POSES.get(category, [
        "Front", "Side", "Back", "Quarter Turns", "Free / Comparison Pose"
    ])

def class_label(cls):
    bits = [cls["sport"], cls["category"] or ""]
    if cls["subdivision"]:
        bits.append(cls["subdivision"])
    if cls["age_category"]:
        bits.append(cls["age_category"])
    if cls["weight_class"]:
        bits.append(cls["weight_class"])
    return " • ".join([x for x in bits if x])

def current_lineup(class_id):
    cls = one("SELECT * FROM classes WHERE id=?", (class_id,))
    if not cls:
        return None
    return one(
        "SELECT * FROM lineups WHERE class_id=? AND lineup_no=?",
        (class_id, cls["current_lineup"])
    )

def judge_submitted(lineup_id, judge_id):
    return one(
        "SELECT id FROM bb_judge_submissions WHERE lineup_id=? AND judge_id=?",
        (lineup_id, judge_id)
    ) is not None

def all_bb_submitted(lineup_id, judge_count):
    row = one("SELECT COUNT(*) AS n FROM bb_judge_submissions WHERE lineup_id=?", (lineup_id,))
    return row["n"] >= judge_count

def pl_judge_count(class_id):
    cls = one("SELECT judge_count FROM classes WHERE id=?", (class_id,))
    return cls["judge_count"] if cls else 3

def ensure_pl_attempts(class_id):
    athletes = athletes_for_class(class_id)
    for a in athletes:
        for lift in ["Squat", "Bench", "Deadlift"]:
            for n in range(1, 4):
                exists = one("""
                    SELECT id FROM pl_attempts
                    WHERE class_id=? AND athlete_id=? AND lift=? AND attempt_no=?
                """, (class_id, a["id"], lift, n))
                if not exists:
                    q("""
                        INSERT INTO pl_attempts(class_id, athlete_id, lift, attempt_no, weight)
                        VALUES(?,?,?,?,0)
                    """, (class_id, a["id"], lift, n))

def bb_result_for_lineup(class_id, lineup_id):
    # Comparative ranking inside a lineup:
    # Each athlete gets a judge-average score over all pose/factor entries.
    # This is an app-level scoring model; organizer can use Custom Federation
    # when the federation requires a different official calculation method.
    rows = all_rows("""
        SELECT athlete_id, AVG(score) AS avg_score
        FROM bb_scores
        WHERE class_id=? AND lineup_id=?
        GROUP BY athlete_id
        ORDER BY avg_score DESC
    """, (class_id, lineup_id))
    return rows

def final_bb_results(class_id):
    # Combine lineup average scores across all finalized lineups.
    rows = all_rows("""
        SELECT athlete_id, AVG(score) AS score
        FROM bb_scores
        WHERE class_id=?
        GROUP BY athlete_id
        ORDER BY score DESC
    """, (class_id,))
    return rows

def pl_best(class_id, athlete_id, lift):
    rows = all_rows("""
        SELECT weight, status FROM pl_attempts
        WHERE class_id=? AND athlete_id=? AND lift=?
        ORDER BY attempt_no
    """, (class_id, athlete_id, lift))
    good = [r["weight"] for r in rows if r["status"] == "Good Lift"]
    return max(good) if good else 0

def calculate_pl_attempt_status(attempt_id):
    cnt = one("""
        SELECT COUNT(*) AS n FROM pl_judgments
        WHERE attempt_id=? AND decision='Good Lift'
    """, (attempt_id,))
    total = one("""
        SELECT COUNT(*) AS n FROM pl_judgments WHERE attempt_id=?
    """, (attempt_id,))
    if total["n"] == 0:
        return "Pending"
    return "Good Lift" if cnt["n"] >= (total["n"] // 2 + 1) else "No Lift"

def calculate_pl_results(class_id):
    athletes = athletes_for_class(class_id)
    data = []
    for a in athletes:
        sq = pl_best(class_id, a["id"], "Squat")
        be = pl_best(class_id, a["id"], "Bench")
        dl = pl_best(class_id, a["id"], "Deadlift")
        total = sq + be + dl
        data.append((a, sq, be, dl, total))
    data.sort(key=lambda x: x[4], reverse=True)
    return data

def save_class_results(class_id):
    cls = one("SELECT * FROM classes WHERE id=?", (class_id,))
    if cls["sport"] == "Bodybuilding":
        rows = final_bb_results(class_id)
        for i, r in enumerate(rows, 1):
            q("""
                INSERT INTO class_results(class_id, athlete_id, placing, score, total, details)
                VALUES(?,?,?,?,?,?)
                ON CONFLICT(class_id, athlete_id) DO UPDATE SET
                    placing=excluded.placing, score=excluded.score,
                    total=excluded.total, details=excluded.details
            """, (class_id, r["athlete_id"], i, r["score"], None, "Bodybuilding judging average"))
    else:
        rows = calculate_pl_results(class_id)
        for i, (a, sq, be, dl, total) in enumerate(rows, 1):
            q("""
                INSERT INTO class_results(class_id, athlete_id, placing, score, total, details)
                VALUES(?,?,?,?,?,?)
                ON CONFLICT(class_id, athlete_id) DO UPDATE SET
                    placing=excluded.placing, score=excluded.score,
                    total=excluded.total, details=excluded.details
            """, (class_id, a["id"], i, None, total, f"SQ {sq} / BP {be} / DL {dl}"))
    q("UPDATE classes SET finalised=1, status='Finalised' WHERE id=?", (class_id,))

# ============================================================
# SESSION / AUTH
# ============================================================

init_db()

if "mode" not in st.session_state:
    st.session_state.mode = "Organizer"
if "competition_id" not in st.session_state:
    st.session_state.competition_id = None
if "judge_id" not in st.session_state:
    st.session_state.judge_id = None
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("IRONMEET")
st.sidebar.markdown("**COMPETITION OS**  ·  **LIVE CONTROL**")
st.sidebar.caption("POWERLIFTING  /  BODYBUILDING")
st.sidebar.divider()

mode = st.sidebar.radio(
    "Open Screen",
    ["Organizer", "Judge", "Display"],
    index=["Organizer", "Judge", "Display"].index(st.session_state.mode)
)
st.session_state.mode = mode

competitions = all_rows("SELECT * FROM competitions ORDER BY id DESC")
if competitions:
    labels = {f'{c["id"]} — {c["name"]}': c["id"] for c in competitions}
    current_label = next(
        (k for k, v in labels.items() if v == st.session_state.competition_id),
        list(labels.keys())[0]
    )
    chosen = st.sidebar.selectbox("Competition", list(labels.keys()), index=list(labels.keys()).index(current_label))
    st.session_state.competition_id = labels[chosen]
else:
    st.sidebar.info("Create a competition from Organizer mode.")

if st.sidebar.button("🔄 Refresh"):
    st.rerun()

# ============================================================
# ORGANIZER
# ============================================================

def organizer_screen():
    st.title("IRONMEET  /  ORGANIZER")
    st.caption("COMPETITION CONTROL CENTER  •  Manage athletes, classes, judges and results")

    if not st.session_state.authenticated:
        st.subheader("Organizer Login")
        st.info("Use the organizer PIN created when the competition was created.")
        if not competitions:
            st.warning("Create your first competition below.")
        else:
            pin = st.text_input("Organizer PIN", type="password")
            if st.button("Login", type="primary"):
                comp = selected_comp()
                if comp and check_pin(pin, comp["organizer_pin_hash"]):
                    st.session_state.authenticated = True
                    st.success("Organizer login successful.")
                    st.rerun()
                else:
                    st.error("Incorrect PIN.")

    if not st.session_state.authenticated:
        st.divider()
        st.header("➕ Create Competition")
        # Keep these dependent selectors outside a form so changing the sport
        # immediately reruns the app and refreshes the federation options.
        sport = st.selectbox(
            "Primary sport",
            ["Bodybuilding", "Powerlifting", "Mixed"],
            key="create_comp_sport",
        )
        if sport == "Bodybuilding":
            federation_pool = BODYBUILDING_FEDERATIONS
        elif sport == "Powerlifting":
            federation_pool = POWERLIFTING_FEDERATIONS
        else:
            federation_pool = list(dict.fromkeys(BODYBUILDING_FEDERATIONS + POWERLIFTING_FEDERATIONS))

        # Reset a stale federation selection when the sport changes.
        current_federation = st.session_state.get("create_comp_federation")
        if current_federation not in federation_pool:
            st.session_state["create_comp_federation"] = federation_pool[0]
        federation = st.selectbox(
            "Federation",
            federation_pool,
            key="create_comp_federation",
        )

        # Normal widgets (rather than form widgets) retain their values during
        # the reruns caused by the Sport and Federation selectors.
        name = st.text_input(
            "Competition name", placeholder="Example: Bangalore Open 2027",
            key="create_comp_name",
        )
        event_date = st.date_input(
            "Event date", value=date.today(), key="create_comp_event_date",
        )
        venue = st.text_input("Venue", key="create_comp_venue")
        country = st.text_input("Country", value="India", key="create_comp_country")
        pin = st.text_input("Create organizer PIN", type="password", key="create_comp_pin")
        pin2 = st.text_input("Confirm organizer PIN", type="password", key="create_comp_pin_confirm")
        submit = st.button("Create Competition", type="primary", key="create_comp_submit")
        if submit:
            if not name.strip() or not pin:
                st.error("Competition name and PIN are required.")
            elif pin != pin2:
                st.error("PINs do not match.")
            else:
                cid = q("""
                    INSERT INTO competitions
                    (name,event_date,venue,country,federation,sport,organizer_pin_hash,created_at)
                    VALUES(?,?,?,?,?,?,?,?)
                """, (name.strip(), str(event_date), venue, country, federation, sport, hpin(pin), now()))
                st.session_state.competition_id = cid
                st.session_state.authenticated = True
                st.success("Competition created.")
                st.rerun()
        return

    comp = selected_comp()
    if not comp:
        st.error("Select a competition.")
        return

    st.success(f'Organizer active • {comp["name"]} • {comp["federation"]}')

    tabs = st.tabs([
        "📊 Dashboard", "👤 Register Athletes", "👥 Athletes",
        "🏷️ Classes & Lineups", "⚖️ Judges", "🎬 Run Class",
        "🏆 Results", "⚙️ Competition"
    ])

    # Dashboard
    with tabs[0]:
        athletes = all_rows("SELECT * FROM athletes WHERE competition_id=? ORDER BY id", (comp["id"],))
        classes = all_rows("SELECT * FROM classes WHERE competition_id=? ORDER BY id", (comp["id"],))
        paid = sum(float(a["registration_fee"] or 0) for a in athletes if a["payment_method"] != "Pending")
        pending = sum(float(a["registration_fee"] or 0) for a in athletes if a["payment_method"] == "Pending")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Registered Athletes", len(athletes))
        c2.metric("Classes", len(classes))
        c3.metric("Fees Collected", f"₹{paid:,.2f}")
        c4.metric("Pending Fees", f"₹{pending:,.2f}")

        st.subheader("Competition Overview")
        st.write({
            "Competition": comp["name"],
            "Date": comp["event_date"],
            "Venue": comp["venue"],
            "Country": comp["country"],
            "Federation": comp["federation"],
            "Sport": comp["sport"],
        })

        if classes:
            table = []
            for cls in classes:
                table.append({
                    "Class": class_label(cls),
                    "Judges": cls["judge_count"],
                    "Status": cls["status"],
                    "Lineup": cls["current_lineup"],
                    "Finalised": "Yes" if cls["finalised"] else "No",
                })
            st.dataframe(table, use_container_width=True)

    # Registration
    with tabs[1]:
        st.header("👤 Athlete Registration")
        st.caption("There is no fixed athlete limit. Every registration is stored in SQLite.")

        with st.form("athlete_reg"):
            left, right = st.columns(2)
            with left:
                athlete_no = st.text_input("Athlete number", value=next_athlete_no(comp["id"]))
                first_name = st.text_input("First name")
                last_name = st.text_input("Last name")
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                dob = st.date_input("Date of birth", value=date(2000, 1, 1))
                country = st.text_input("Athlete country", value=comp["country"])
                phone = st.text_input("Phone")
                email = st.text_input("Email")
            with right:
                sport = st.selectbox("Sport", ["Bodybuilding", "Powerlifting"])
                federation = st.selectbox(
                    "Federation",
                    BODYBUILDING_FEDERATIONS if sport == "Bodybuilding" else POWERLIFTING_FEDERATIONS
                )

                if sport == "Bodybuilding":
                    cats = category_options(federation)
                    category = st.selectbox("Category", cats)
                    subdivision = st.selectbox("Subdivision / Division", BB_SUBDIVISIONS)
                    age_category = st.selectbox("Age category", ["Not Applicable"] + AGE_CATEGORIES)
                    weight_class = ""
                    bodyweight = st.number_input("Bodyweight (kg)", min_value=0.0, step=0.1)
                else:
                    category = "Powerlifting"
                    subdivision = ""
                    age_category = st.selectbox("Age category", AGE_CATEGORIES)
                    classes_pl = IPF_MEN_CLASSES + IPF_WOMEN_CLASSES if federation == "IPF" else COMMON_PL_CLASSES
                    weight_class = st.selectbox("Weight class", classes_pl + ["Custom"])
                    if weight_class == "Custom":
                        weight_class = st.text_input("Custom weight class")
                    bodyweight = st.number_input("Bodyweight (kg)", min_value=0.0, step=0.1)

                st.markdown("### 💰 Registration Payment")
                registration_fee = st.number_input("Registration fee", min_value=0.0, step=100.0)
                payment_method = st.selectbox("Payment method", PAYMENT_METHODS)
                payment_reference = st.text_input("UPI/Card reference (optional)")
                registration_status = st.selectbox("Registration status", ["Registered", "Pending Verification", "Cancelled"])
                notes = st.text_area("Notes")

            save = st.form_submit_button("➕ Register Athlete", type="primary")

            if save:
                if not first_name.strip():
                    st.error("First name is required.")
                elif not athlete_no.strip():
                    st.error("Athlete number is required.")
                else:
                    try:
                        q("""
                            INSERT INTO athletes
                            (competition_id,athlete_no,first_name,last_name,gender,dob,country,phone,email,
                             federation,sport,category,subdivision,age_category,weight_class,bodyweight,
                             registration_fee,payment_method,payment_reference,registration_status,notes,created_at)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """, (
                            comp["id"], athlete_no.strip(), first_name.strip(), last_name.strip(),
                            gender, str(dob), country, phone, email, federation, sport, category,
                            subdivision, age_category, weight_class, bodyweight, registration_fee,
                            payment_method, payment_reference, registration_status, notes, now()
                        ))
                        st.success(f"Athlete #{athlete_no} registered successfully.")
                    except sqlite3.IntegrityError:
                        st.error("That athlete number already exists in this competition.")

    # Athletes
    with tabs[2]:
        st.header("👥 Athlete Database")
        athletes = all_rows(
            "SELECT * FROM athletes WHERE competition_id=? ORDER BY CAST(athlete_no AS INTEGER), id",
            (comp["id"],)
        )
        if not athletes:
            st.info("No athletes registered yet.")
        else:
            search = st.text_input("Search athlete number, name, email or phone")
            filtered = [
                a for a in athletes
                if not search or search.lower() in (
                    f'{a["athlete_no"]} {a["first_name"]} {a["last_name"] or ""} '
                    f'{a["email"] or ""} {a["phone"] or ""}'
                ).lower()
            ]
            display = [{
                "No.": a["athlete_no"],
                "Name": f'{a["first_name"]} {a["last_name"] or ""}'.strip(),
                "Sport": a["sport"],
                "Federation": a["federation"],
                "Category": a["category"],
                "Division": a["subdivision"],
                "Age": a["age_category"],
                "Weight Class": a["weight_class"],
                "Fee": a["registration_fee"],
                "Payment": a["payment_method"],
                "Status": a["registration_status"],
            } for a in filtered]
            st.dataframe(display, use_container_width=True, hide_index=True)

            st.subheader("Edit Payment / Registration")
            selected = st.selectbox(
                "Select athlete",
                [f'{a["athlete_no"]} — {a["first_name"]} {a["last_name"] or ""}' for a in filtered]
            )
            if selected:
                no = selected.split(" — ")[0]
                a = one("SELECT * FROM athletes WHERE competition_id=? AND athlete_no=?", (comp["id"], no))
                with st.form("edit_payment"):
                    fee = st.number_input("Fee", value=float(a["registration_fee"] or 0), min_value=0.0, step=100.0)
                    method = st.selectbox("Payment method", PAYMENT_METHODS, index=PAYMENT_METHODS.index(a["payment_method"]) if a["payment_method"] in PAYMENT_METHODS else 0)
                    ref = st.text_input("Payment reference", value=a["payment_reference"] or "")
                    status = st.selectbox("Registration status", ["Registered", "Pending Verification", "Cancelled"], index=["Registered", "Pending Verification", "Cancelled"].index(a["registration_status"]))
                    if st.form_submit_button("Save Athlete Update"):
                        q("""
                            UPDATE athletes SET registration_fee=?, payment_method=?,
                            payment_reference=?, registration_status=? WHERE id=?
                        """, (fee, method, ref, status, a["id"]))
                        st.success("Updated.")
                        st.rerun()

    # Classes / lineups
    with tabs[3]:
        st.header("🏷️ Classes & Lineups")

        with st.expander("➕ Create Competition Class", expanded=True):
            with st.form("create_class"):
                sport = st.selectbox("Class sport", ["Bodybuilding", "Powerlifting"])
                federation = comp["federation"]
                if sport == "Bodybuilding":
                    cats = category_options(federation)
                    category = st.selectbox("Category", cats)
                    subdivision = st.selectbox("Subdivision", BB_SUBDIVISIONS)
                    age_cat = st.selectbox("Age category", ["Not Applicable"] + AGE_CATEGORIES)
                    weight_class = ""
                else:
                    category = "Powerlifting"
                    subdivision = ""
                    age_cat = st.selectbox("Age category", AGE_CATEGORIES)
                    pl_classes = IPF_MEN_CLASSES + IPF_WOMEN_CLASSES if federation == "IPF" else COMMON_PL_CLASSES
                    weight_class = st.selectbox("Weight class", pl_classes + ["Custom"])
                    if weight_class == "Custom":
                        weight_class = st.text_input("Custom weight class")
                judge_count = st.selectbox("Number of judges/referees", [3, 4, 5], index=0)
                make = st.form_submit_button("Create Class", type="primary")
                if make:
                    q("""
                        INSERT INTO classes
                        (competition_id,name,sport,category,subdivision,age_category,weight_class,judge_count,created_at)
                        VALUES(?,?,?,?,?,?,?,?,?)
                    """, (
                        comp["id"],
                        f"{category} {subdivision} {age_cat} {weight_class}".strip(),
                        sport, category, subdivision, age_cat, weight_class, judge_count, now()
                    ))
                    st.success("Class created.")

        classes = all_rows("SELECT * FROM classes WHERE competition_id=? ORDER BY id", (comp["id"],))
        if classes:
            st.divider()
            cls_label_map = {f'{c["id"]} — {class_label(c)}': c["id"] for c in classes}
            chosen_class = st.selectbox("Select class to build lineup", list(cls_label_map.keys()))
            class_id = cls_label_map[chosen_class]
            cls = one("SELECT * FROM classes WHERE id=?", (class_id,))
            available = all_rows("""
                SELECT * FROM athletes
                WHERE competition_id=? AND sport=?
                ORDER BY CAST(athlete_no AS INTEGER), id
            """, (comp["id"], cls["sport"]))

            st.subheader("Assign athletes to lineups")
            if not available:
                st.warning("Register athletes for this sport first.")
            else:
                athlete_labels = [
                    f'{a["athlete_no"]} — {a["first_name"]} {a["last_name"] or ""} — {a["category"] or ""}'
                    for a in available
                ]
                chosen_athletes = st.multiselect(
                    "Select athletes for the next lineup",
                    athlete_labels
                )
                lineup_no = one(
                    "SELECT COALESCE(MAX(lineup_no),0)+1 AS n FROM lineups WHERE class_id=?",
                    (class_id,)
                )["n"]
                if st.button(f"Create Lineup {lineup_no}", type="primary"):
                    ids = []
                    for label in chosen_athletes:
                        no = label.split(" — ")[0]
                        a = one("SELECT id FROM athletes WHERE competition_id=? AND athlete_no=?", (comp["id"], no))
                        if a:
                            ids.append(str(a["id"]))
                    if not ids:
                        st.error("Select at least one athlete.")
                    else:
                        q(
                            "INSERT INTO lineups(class_id,lineup_no,athlete_ids) VALUES(?,?,?)",
                            (class_id, lineup_no, ",".join(ids))
                        )
                        st.success(f"Lineup {lineup_no} created.")
                        st.rerun()

                lineups = all_rows("SELECT * FROM lineups WHERE class_id=? ORDER BY lineup_no", (class_id,))
                for l in lineups:
                    ids = [int(x) for x in l["athlete_ids"].split(",") if x]
                    names = []
                    for aid in ids:
                        a = one("SELECT athlete_no,first_name,last_name FROM athletes WHERE id=?", (aid,))
                        if a:
                            names.append(f'#{a["athlete_no"]} {a["first_name"]} {a["last_name"] or ""}'.strip())
                    st.write(f'**Lineup {l["lineup_no"]}** — {l["status"]}')
                    st.write(" | ".join(names))

                if st.button("🧹 Reset Current Class Lineups", key=f"reset_{class_id}"):
                    if cls["status"] == "Not Started":
                        q("DELETE FROM lineups WHERE class_id=?", (class_id,))
                        st.success("Lineups reset.")
                        st.rerun()
                    else:
                        st.warning("Cannot reset after the class has started.")

    # Judges
    with tabs[4]:
        st.header("⚖️ Judge / Referee Management")
        st.info("Judges do not select athletes, classes, categories or lineups. The organizer controls all of that.")

        with st.form("add_judge"):
            jname = st.text_input("Judge / Referee name")
            jrole = st.selectbox("Role", ["Judge", "Referee", "Chairman"])
            jpin = st.text_input("Judge PIN", type="password")
            if st.form_submit_button("Add Judge"):
                if jname.strip() and jpin:
                    try:
                        q("""
                            INSERT INTO judges(competition_id,name,role,pin_hash,active)
                            VALUES(?,?,?,?,1)
                        """, (comp["id"], jname.strip(), jrole, hpin(jpin)))
                        st.success("Judge added.")
                    except sqlite3.IntegrityError:
                        st.error("That judge already exists.")
                else:
                    st.error("Name and PIN are required.")

        judges = all_rows("SELECT * FROM judges WHERE competition_id=? ORDER BY id", (comp["id"],))
        if judges:
            st.subheader("Configured Judges")
            st.dataframe([{
                "Name": j["name"], "Role": j["role"], "Active": bool(j["active"])
            } for j in judges], use_container_width=True, hide_index=True)

            st.caption("A class uses the first N active judges, where N is configured as 3, 4 or 5.")

    # Run class
    with tabs[5]:
        st.header("🎬 Run Class")
        classes = all_rows("SELECT * FROM classes WHERE competition_id=? ORDER BY id", (comp["id"],))
        if not classes:
            st.info("Create a class first.")
        else:
            cmap = {f'{c["id"]} — {class_label(c)}': c["id"] for c in classes}
            pick = st.selectbox("Select class", list(cmap.keys()))
            class_id = cmap[pick]
            cls = one("SELECT * FROM classes WHERE id=?", (class_id,))
            lineups = all_rows("SELECT * FROM lineups WHERE class_id=? ORDER BY lineup_no", (class_id,))

            if not lineups:
                st.warning("Create lineups first.")
            else:
                c1, c2, c3 = st.columns(3)
                c1.metric("Judges required", cls["judge_count"])
                c2.metric("Current lineup", cls["current_lineup"] or 0)
                c3.metric("Status", cls["status"])

                if cls["status"] == "Not Started":
                    if st.button("▶️ START CLASS", type="primary"):
                        q("UPDATE classes SET status='Running', current_lineup=1 WHERE id=?", (class_id,))
                        st.rerun()

                if cls["status"] == "Running":
                    l = current_lineup(class_id)
                    if not l:
                        st.error("Current lineup not found.")
                    else:
                        ids = [int(x) for x in l["athlete_ids"].split(",") if x]
                        names = []
                        for aid in ids:
                            a = one("SELECT * FROM athletes WHERE id=?", (aid,))
                            if a:
                                names.append(f'#{a["athlete_no"]} — {a["first_name"]} {a["last_name"] or ""}')
                        st.subheader(f'LINEUP {l["lineup_no"]}')
                        st.success("CURRENT: " + " | ".join(names))

                        if cls["sport"] == "Bodybuilding":
                            submitted = one(
                                "SELECT COUNT(*) AS n FROM bb_judge_submissions WHERE lineup_id=?",
                                (l["id"],)
                            )["n"]
                            st.metric("Judge submissions", f'{submitted}/{cls["judge_count"]}')

                            if submitted >= cls["judge_count"]:
                                st.success("✅ ALL JUDGES SUBMITTED — Organizer can press ENTER.")
                                if st.button("⌨️ ENTER — FINALIZE LINEUP & START NEXT", type="primary"):
                                    q("UPDATE lineups SET status='Finalised' WHERE id=?", (l["id"],))
                                    next_l = one("""
                                        SELECT * FROM lineups
                                        WHERE class_id=? AND lineup_no>?
                                        ORDER BY lineup_no LIMIT 1
                                    """, (class_id, l["lineup_no"]))
                                    if next_l:
                                        q("UPDATE classes SET current_lineup=? WHERE id=?", (next_l["lineup_no"], class_id))
                                        q("UPDATE lineups SET status='Running' WHERE id=?", (next_l["id"],))
                                        st.success(f'Lineup {next_l["lineup_no"]} started automatically.')
                                    else:
                                        save_class_results(class_id)
                                        st.success("🏆 FINAL LINEUP COMPLETE — CLASS FINALIZED.")
                                    st.rerun()
                            else:
                                st.warning("Waiting for every configured judge. Organizer ENTER is locked until all submissions arrive.")

                        else:
                            ensure_pl_attempts(class_id)
                            st.info("Powerlifting class: each attempt is finalized after the configured referees submit their decisions.")
                            attempts = all_rows("""
                                SELECT p.*, a.athlete_no, a.first_name, a.last_name
                                FROM pl_attempts p JOIN athletes a ON a.id=p.athlete_id
                                WHERE p.class_id=?
                                ORDER BY CAST(a.athlete_no AS INTEGER), p.lift, p.attempt_no
                            """, (class_id,))
                            rows = []
                            for p in attempts:
                                n = one("SELECT COUNT(*) AS n FROM pl_judgments WHERE attempt_id=?", (p["id"],))["n"]
                                rows.append({
                                    "Athlete": f'#{p["athlete_no"]} {p["first_name"]} {p["last_name"] or ""}',
                                    "Lift": p["lift"], "Attempt": p["attempt_no"],
                                    "Weight": p["weight"], "Judges In": f'{n}/{cls["judge_count"]}',
                                    "Status": p["status"]
                                })
                            st.dataframe(rows, use_container_width=True, hide_index=True)

                            pending_attempts = [p for p in attempts if p["status"] == "Pending"]
                            if pending_attempts:
                                p = pending_attempts[0]
                                st.subheader(f'Next Attempt: #{p["athlete_no"]} {p["first_name"]} — {p["lift"]} Attempt {p["attempt_no"]}')
                                w = st.number_input("Attempt weight (kg)", value=float(p["weight"]), min_value=0.0, step=0.5, key=f"w_{p['id']}")
                                if st.button("Save Attempt Weight"):
                                    q("UPDATE pl_attempts SET weight=? WHERE id=?", (w, p["id"]))
                                    st.success("Attempt weight saved.")
                            else:
                                if st.button("🏆 Finalize Powerlifting Class", type="primary"):
                                    save_class_results(class_id)
                                    st.success("Class finalized.")
                                    st.rerun()

    # Results
    with tabs[6]:
        st.header("🏆 Results")
        classes = all_rows("SELECT * FROM classes WHERE competition_id=? ORDER BY id", (comp["id"],))
        if classes:
            cmap = {f'{c["id"]} — {class_label(c)}': c["id"] for c in classes}
            pick = st.selectbox("Results class", list(cmap.keys()))
            class_id = cmap[pick]
            cls = one("SELECT * FROM classes WHERE id=?", (class_id,))
            results = all_rows("""
                SELECT r.*, a.athlete_no, a.first_name, a.last_name
                FROM class_results r JOIN athletes a ON a.id=r.athlete_id
                WHERE r.class_id=? ORDER BY r.placing
            """, (class_id,))
            if not results:
                st.info("No finalized results yet.")
            else:
                for r in results:
                    medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(r["placing"], f'{r["placing"]}.')
                    st.markdown(f"### {medal} #{r['athlete_no']} — {r['first_name']} {r['last_name'] or ''}")
                    if cls["sport"] == "Powerlifting":
                        st.write(f"**Total:** {r['total']} kg • {r['details']}")
                    else:
                        st.write(f"**Score:** {r['score']:.3f}")

                st.divider()
                st.subheader("Publish / Display")
                st.success("These are locked class results.")

    # Competition settings
    with tabs[7]:
        st.header("⚙️ Competition Settings")
        with st.form("edit_comp"):
            name = st.text_input("Name", value=comp["name"])
            event_date = st.date_input("Event date", value=date.fromisoformat(comp["event_date"]))
            venue = st.text_input("Venue", value=comp["venue"] or "")
            country = st.text_input("Country", value=comp["country"] or "")
            federation_pool = BODYBUILDING_FEDERATIONS + POWERLIFTING_FEDERATIONS
            federation = st.selectbox(
                "Federation",
                list(dict.fromkeys(federation_pool)),
                index=list(dict.fromkeys(federation_pool)).index(comp["federation"]) if comp["federation"] in dict.fromkeys(federation_pool) else 0
            )
            if st.form_submit_button("Save Competition Settings"):
                q("""
                    UPDATE competitions SET name=?, event_date=?, venue=?, country=?, federation=?
                    WHERE id=?
                """, (name, str(event_date), venue, country, federation, comp["id"]))
                st.success("Competition settings saved.")
                st.rerun()

        if st.button("Logout Organizer"):
            st.session_state.authenticated = False
            st.rerun()

# ============================================================
# JUDGE SCREEN
# ============================================================

def judge_screen():
    st.title("IRONMEET  /  OFFICIALS")
    st.caption("JUDGE & REFEREE CONSOLE  •  Submit decisions for the active lineup")
    comp = selected_comp()

    if not comp:
        st.warning("Organizer must create/select a competition first.")
        return

    if not st.session_state.judge_id:
        st.subheader("Judge Login")
        judges = all_rows("SELECT * FROM judges WHERE competition_id=? AND active=1 ORDER BY id", (comp["id"],))
        if not judges:
            st.warning("No judges configured by organizer.")
            return
        names = {f'{j["name"]} — {j["role"]}': j["id"] for j in judges}
        selected = st.selectbox("Judge", list(names.keys()))
        pin = st.text_input("PIN", type="password")
        if st.button("Login as Judge", type="primary"):
            j = one("SELECT * FROM judges WHERE id=?", (names[selected],))
            if check_pin(pin, j["pin_hash"]):
                st.session_state.judge_id = j["id"]
                st.success("Judge logged in.")
                st.rerun()
            else:
                st.error("Incorrect PIN.")
        return

    judge = one("SELECT * FROM judges WHERE id=?", (st.session_state.judge_id,))
    st.success(f'Logged in: {judge["name"]} • {judge["role"]}')

    classes = all_rows("""
        SELECT * FROM classes
        WHERE competition_id=? AND status='Running' AND finalised=0
        ORDER BY id
    """, (comp["id"],))

    if not classes:
        st.info("No class is currently running. The organizer controls the class.")
        if st.button("Logout"):
            st.session_state.judge_id = None
            st.rerun()
        return

    # Judge automatically gets the first running class. No class/athlete/pose
    # selection is required by the judge.
    cls = classes[0]
    l = current_lineup(cls["id"])

    if not l:
        st.info("Waiting for organizer to start the current lineup.")
        return

    ids = [int(x) for x in l["athlete_ids"].split(",") if x]
    athletes = [one("SELECT * FROM athletes WHERE id=?", (aid,)) for aid in ids]
    athletes = [a for a in athletes if a]

    st.header(f"LINEUP {l['lineup_no']}")
    st.write(" | ".join([f'#{a["athlete_no"]} {a["first_name"]} {a["last_name"] or ""}' for a in athletes]))

    if cls["sport"] == "Bodybuilding":
        if judge_submitted(l["id"], judge["id"]):
            st.success("✅ Your scores for this lineup have been submitted.")
            st.info("Wait for the organizer to press ENTER and start the next lineup.")
        else:
            poses = pose_options(cls["category"] or "")
            st.subheader("Judge the current lineup")

            score_values = {}
            for pose in poses:
                st.markdown(f"### {pose}")
                for a in athletes:
                    st.markdown(f"**#{a['athlete_no']} — {a['first_name']} {a['last_name'] or ''}**")
                    cols = st.columns(len(BB_FACTORS))
                    for idx, factor in enumerate(BB_FACTORS):
                        score_values[(a["id"], pose, factor)] = cols[idx].slider(
                            factor, 1.0, 10.0, 5.0, 0.5,
                            key=f"bb_{l['id']}_{judge['id']}_{a['id']}_{pose}_{factor}"
                        )

            if st.button("📤 SUBMIT MY JUDGING", type="primary"):
                for (aid, pose, factor), score in score_values.items():
                    q("""
                        INSERT INTO bb_scores
                        (class_id,lineup_id,athlete_id,judge_id,pose,factor,score,submitted_at)
                        VALUES(?,?,?,?,?,?,?,?)
                        ON CONFLICT(lineup_id,athlete_id,judge_id,pose,factor)
                        DO UPDATE SET score=excluded.score, submitted_at=excluded.submitted_at
                    """, (cls["id"], l["id"], aid, judge["id"], pose, factor, score, now()))
                q("""
                    INSERT OR IGNORE INTO bb_judge_submissions(lineup_id,judge_id,submitted_at)
                    VALUES(?,?,?)
                """, (l["id"], judge["id"], now()))
                st.success("Submitted. The organizer will advance the lineup.")
                st.rerun()

    else:
        ensure_pl_attempts(cls["id"])
        # Judge sees one pending attempt automatically.
        attempts = all_rows("""
            SELECT p.*, a.athlete_no, a.first_name, a.last_name
            FROM pl_attempts p JOIN athletes a ON a.id=p.athlete_id
            WHERE p.class_id=? AND p.status='Pending'
            ORDER BY
                CASE p.lift WHEN 'Squat' THEN 1 WHEN 'Bench' THEN 2 ELSE 3 END,
                p.attempt_no, CAST(a.athlete_no AS INTEGER)
        """, (cls["id"],))
        if not attempts:
            st.success("All attempts have been judged. Waiting for organizer to finalize.")
        else:
            p = attempts[0]
            st.subheader(f'#{p["athlete_no"]} — {p["first_name"]} {p["last_name"] or ""}')
            st.metric(f'{p["lift"]} • Attempt {p["attempt_no"]}', f'{p["weight"]} kg')
            st.write("Make your independent referee decision.")
            col1, col2 = st.columns(2)
            if col1.button("⬜ GOOD LIFT", type="primary", use_container_width=True):
                q("""
                    INSERT INTO pl_judgments(attempt_id,judge_id,decision,submitted_at)
                    VALUES(?,?,?,?)
                    ON CONFLICT(attempt_id,judge_id) DO UPDATE SET
                    decision=excluded.decision, submitted_at=excluded.submitted_at
                """, (p["id"], judge["id"], "Good Lift", now()))
                status = calculate_pl_attempt_status(p["id"])
                q("UPDATE pl_attempts SET status=? WHERE id=?", (status, p["id"]))
                st.success("Decision submitted.")
                st.rerun()
            if col2.button("🟥 NO LIFT", use_container_width=True):
                q("""
                    INSERT INTO pl_judgments(attempt_id,judge_id,decision,submitted_at)
                    VALUES(?,?,?,?)
                    ON CONFLICT(attempt_id,judge_id) DO UPDATE SET
                    decision=excluded.decision, submitted_at=excluded.submitted_at
                """, (p["id"], judge["id"], "No Lift", now()))
                status = calculate_pl_attempt_status(p["id"])
                q("UPDATE pl_attempts SET status=? WHERE id=?", (status, p["id"]))
                st.error("No-lift decision submitted.")
                st.rerun()

    if st.button("Logout Judge"):
        st.session_state.judge_id = None
        st.rerun()

# ============================================================
# DISPLAY SCREEN
# ============================================================

def display_screen():
    st.title("IRONMEET  /  ARENA DISPLAY")
    st.caption("LIVE COMPETITION VIEW  •  Lineups, attempts and finalized results")
    comp = selected_comp()
    if not comp:
        st.info("Select a competition.")
        return

    st.caption(f'{comp["name"]} • {comp["event_date"]} • {comp["venue"]}')

    running = all_rows("""
        SELECT * FROM classes WHERE competition_id=? AND status='Running' AND finalised=0
        ORDER BY id LIMIT 1
    """, (comp["id"],))

    if running:
        cls = running[0]
        l = current_lineup(cls["id"])
        st.header(class_label(cls))
        if l:
            st.subheader(f"LINEUP {l['lineup_no']}")
            ids = [int(x) for x in l["athlete_ids"].split(",") if x]
            cols = st.columns(max(1, min(len(ids), 5)))
            for i, aid in enumerate(ids):
                a = one("SELECT * FROM athletes WHERE id=?", (aid,))
                if a:
                    with cols[i % len(cols)]:
                        st.metric(f'#{a["athlete_no"]}', f'{a["first_name"]} {a["last_name"] or ""}')
            if cls["sport"] == "Bodybuilding":
                st.info("Judging in progress")
            else:
                st.info("Powerlifting attempts in progress")
    else:
        st.success("No class currently on stage.")

    st.divider()
    st.header("🏆 Finalized Results")
    classes = all_rows("""
        SELECT * FROM classes WHERE competition_id=? AND finalised=1 ORDER BY id DESC
    """, (comp["id"],))
    if not classes:
        st.info("Final results will appear here after the organizer finalizes a class.")
    else:
        for cls in classes:
            st.subheader(class_label(cls))
            results = all_rows("""
                SELECT r.*, a.athlete_no, a.first_name, a.last_name
                FROM class_results r JOIN athletes a ON a.id=r.athlete_id
                WHERE r.class_id=? ORDER BY r.placing
            """, (cls["id"],))
            for r in results:
                medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(r["placing"], f'{r["placing"]}.')
                if cls["sport"] == "Powerlifting":
                    st.write(f'{medal} #{r["athlete_no"]} — {r["first_name"]} {r["last_name"] or ""} — Total {r["total"]} kg')
                else:
                    st.write(f'{medal} #{r["athlete_no"]} — {r["first_name"]} {r["last_name"] or ""} — Score {r["score"]:.3f}')

    st.caption("Display refreshes when the page is refreshed. For a live venue setup, open this screen on the display computer and refresh periodically.")

# ============================================================
# ROUTER
# ============================================================

if st.session_state.mode == "Organizer":
    organizer_screen()
elif st.session_state.mode == "Judge":
    judge_screen()
else:
    display_screen()

st.divider()
st.caption("IRONMEET  •  COMPETITION OPERATIONS PLATFORM  •  LOCAL SQLITE EDITION")
