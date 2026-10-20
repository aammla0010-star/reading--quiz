import re
import streamlit as st

st.set_page_config(
    page_title="Read & Test | English Reading Quiz",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ───────────────────────── Content ─────────────────────────

MARKETS = [
    ("St. Lawrence Market", "Toronto, Canada"),
    ("Castries Market", "St. Lucia"),
    ("Kreta Ayer Wet Market", "Singapore"),
    ("La Vucciria Market", "Palermo, Italy"),
    ("Borough Market", "London, England"),
]

PASSAGE = [
    (
        "1  St Lawrence, Toronto, Canada",
        "St Lawrence food market, in Toronto, is 200 years old. "
        "There are a lot of shops with every kind of meat and seafood.",
    ),
    (
        "2  Castries Market, St Lucia",
        "Naturally, this island in the Caribbean has a market famous for fish and fruit. "
        "Try the local sauce – it's very hot and spicy!",
    ),
    (
        "3  Kreta Ayer Wet Market, Singapore",
        "There's a lot of different food here and there's also a great restaurant upstairs. "
        "Go at around 6 a.m. and have some tasty noodles for breakfast.",
    ),
    (
        "4  La Vucciria, Palermo, Italy",
        "There aren't many markets in the world with live music. "
        "But in Palermo, musicians play and sing as shoppers buy their sausages and fresh pasta.",
    ),
    (
        "5  Borough Market, London, England",
        "Borough Market is 1,000 years old and famous with food lovers. "
        "It's open every day, but try to go early – it's very popular, "
        "so there isn't much food left by the end of the day!",
    ),
]

QUESTIONS = [
    # ── True / False ──
    {"type": "tf", "q": "St Lawrence food market is in Toronto, Canada.", "answer": "True"},
    {"type": "tf", "q": "Castries Market is famous for meat and cheese.", "answer": "False"},
    {"type": "tf", "q": "The restaurant at Kreta Ayer Wet Market is downstairs.", "answer": "False"},
    {"type": "tf", "q": "Borough Market is open every day.", "answer": "True"},
    # ── Multiple choice (choose the correct answer) ──
    {
        "type": "mc",
        "q": "How old is St Lawrence market?",
        "options": ["50 years old", "100 years old", "200 years old", "1,000 years old"],
        "answer": "200 years old",
    },
    {
        "type": "mc",
        "q": "What is very hot and spicy in Castries Market?",
        "options": ["The fruit", "The local sauce", "The noodles", "The sausages"],
        "answer": "The local sauce",
    },
    {
        "type": "mc",
        "q": "What can you hear in La Vucciria?",
        "options": ["Church bells", "Traffic", "Live music", "Radio news"],
        "answer": "Live music",
    },
    # ── Short answer ──
    {
        "type": "short",
        "q": "Name one kind of food you can buy in St Lawrence market.",
        "answer": "Meat (or seafood)",
        "accepted": ["meat", "seafood", "sea food"],
    },
    {
        "type": "short",
        "q": "What tasty food can you have for breakfast at Kreta Ayer Wet Market?",
        "answer": "Noodles",
        "accepted": ["noodles", "noodle"],
    },
    {
        "type": "short",
        "q": "How old is Borough Market?",
        "answer": "1,000 years old",
        "accepted": ["1000", "1 000", "one thousand"],
    },
]

TYPE_LABEL = {"tf": "True or False", "mc": "Choose the correct answer", "short": "Short answer"}

# ───────────────────────── Styling ─────────────────────────

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Nunito:wght@400;600;700&display=swap');

/* ───── Colour palette: light (default) ───── */
:root {
    --bg: #FBEFDF;
    --bg-soft: #FFF8EE;
    --surface: #FFFFFF;
    --sand: #EBDDC6;
    --ink: #2A2A22;
    --muted: #5E5B4E;
    --accent: #1F4330;        /* headings / accent text */
    --btn: #1F4330;           /* primary button background */
    --btn-hover: #2F5A40;
    --wood: #D9A066;
    --wood-dark: #8A5A2B;
    --ok-bg: #E6F2E4;  --ok-bd: #9CC79A;  --ok-tx: #2E7D32;
    --bad-bg: #FBE5DF; --bad-bd: #E3A596; --bad-tx: #C0392B;
    --hero-bg: radial-gradient(1200px 300px at 50% -10%, rgba(255,255,255,.65), transparent 60%),
               linear-gradient(180deg, #CFE0E6 0%, #F2D9B5 45%, #E8C9A0 100%);
    color-scheme: light;
}

/* ───── Colour palette: dark ───── */
@media (prefers-color-scheme: dark) {
    :root {
        --bg: #131E18;
        --bg-soft: #1A2A22;
        --surface: #1E2D25;
        --sand: #2E4036;
        --ink: #F1EBDD;
        --muted: #C2BDAE;
        --accent: #A9DDB7;
        --btn: #3F7C57;
        --btn-hover: #4E9068;
        --wood: #D9A066;
        --wood-dark: #8A5A2B;
        --ok-bg: #1F3A27;  --ok-bd: #3F7C57;  --ok-tx: #8FD6A0;
        --bad-bg: #432722; --bad-bd: #A8584A; --bad-tx: #FF9C8B;
        --hero-bg: radial-gradient(1200px 300px at 50% -10%, rgba(255,255,255,.10), transparent 60%),
                   linear-gradient(180deg, #243845 0%, #4A3B2B 55%, #3B2D20 100%);
        color-scheme: dark;
    }
}

/* ───── Base ───── */
html, body, [class*="css"], .stApp { font-family: 'Nunito', sans-serif; }
.stApp { background: var(--bg); color: var(--ink); }
#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }
.block-container { padding: 1.2rem 1rem 3rem; max-width: 1180px; }

.stApp h1, .stApp h2, .stApp h3 { font-family: 'Baloo 2', sans-serif; color: var(--accent); }
.stApp p, .stApp li, .stApp label, .stApp span { color: inherit; }
.stApp [data-testid="stMarkdownContainer"] p { color: var(--ink); }
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] p { color: var(--muted); }
.stApp hr { border-color: var(--sand); }

/* Form widgets */
.stApp [data-testid="stForm"] { border: none; padding: 0; background: transparent; }
.stApp [data-testid="stRadio"] label, .stApp [data-testid="stRadio"] label p {
    color: var(--ink); font-size: 1.05rem;
}
.stApp [data-testid="stRadio"] label { padding: .25rem 0; min-height: 2.4rem; }
.stApp [data-testid="stTextInput"] input {
    background: var(--surface); color: var(--ink); border: 2px solid var(--sand);
    border-radius: 14px; font-size: 1.05rem; padding: .7rem .9rem;
}
.stApp [data-testid="stTextInput"] input::placeholder { color: var(--muted); opacity: .8; }
.stApp [data-testid="stTextInput"] input:focus { border-color: var(--btn); box-shadow: none; }
.stApp [data-testid="stTextInput"] div[data-baseweb="input"],
.stApp [data-testid="stTextInput"] div[data-baseweb="base-input"] { background: transparent; border: none; }

/* Buttons */
div.stButton > button, div.stFormSubmitButton > button {
    border-radius: 999px; font-family: 'Baloo 2', sans-serif; font-weight: 700;
    font-size: 1.05rem; padding: .55rem 1rem; min-height: 3rem; border: 2px solid transparent;
    background: var(--sand); color: var(--accent); width: 100%;
}
div.stButton > button p, div.stFormSubmitButton > button p { color: inherit; }
div.stButton > button:hover, div.stFormSubmitButton > button:hover {
    border-color: var(--btn); color: var(--accent);
}
div.stButton > button[kind="primary"], div.stFormSubmitButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] {
    background: var(--btn); color: #fff; border-color: var(--btn);
}
div.stButton > button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
    background: var(--btn-hover); color: #fff; border-color: #fff;
}
div.stButton > button:focus-visible, div.stFormSubmitButton > button:focus-visible {
    outline: 3px solid var(--wood); outline-offset: 2px;
}

/* ───── Top bar ───── */
.brand { display:flex; align-items:center; gap:.7rem; }
.brand .logo { font-size:2.2rem; }
.brand .t1 { font-family:'Baloo 2'; font-weight:800; font-size:1.7rem; color:var(--accent); line-height:1; }
.brand .t2 { font-size:.95rem; color:var(--ink); }

/* ───── Hero (the container itself is the hero background) ───── */
.st-key-hero {
    border-radius: 28px; padding: 2rem 1.5rem 1.2rem; margin-top: .8rem;
    background: var(--hero-bg); overflow: hidden;
}
.signpost { display:flex; flex-direction:column; gap:.55rem; }
.sign {
    background: linear-gradient(180deg, #E3B67F, #D9A066); color:#2A2A22;
    padding:.55rem 1.4rem .55rem .9rem; font-size:.92rem; line-height:1.2;
    clip-path: polygon(0 0, 92% 0, 100% 50%, 92% 100%, 0 100%);
    box-shadow: 0 2px 0 #8A5A2B; border-left: 6px solid #8A5A2B;
}
.sign b { font-family:'Baloo 2'; font-size:1.02rem; display:block; color:#2A2A22; }
.sign:nth-child(odd) { transform: rotate(-1.5deg); }
.sign:nth-child(even) { transform: rotate(1deg); margin-left:.4rem; }

.board {
    background: linear-gradient(180deg, #E8BE8A, #D9A066); border: 4px solid #8A5A2B;
    border-radius: 34px 34px 20px 20px; padding: 1.4rem 1rem .8rem; text-align:center;
    box-shadow: 0 6px 0 rgba(138,90,43,.35);
}
.stApp .board h1 {
    font-size: clamp(2rem, 6vw, 3.9rem); line-height: .95; margin:0;
    font-weight: 800; color: #1F4330; text-transform: uppercase; letter-spacing: .01em;
}
.board .sub {
    background: #FBEFDF; color: #2A2A22; border-radius: 22px; padding:.7rem 1rem; margin:1rem auto 0;
    max-width: 92%; font-size: clamp(.95rem, 2.6vw, 1.1rem); font-weight:600;
}
.emoji-row { font-size: clamp(1.8rem, 6vw, 2.6rem); text-align:center; letter-spacing:.3rem; margin-top:1rem; }
.chalk {
    background:#2E3A33; color:#F3F0E6; border:5px solid #8A5A2B; border-radius:10px;
    padding:1rem; text-align:center; font-family:'Baloo 2'; font-size:1.3rem; transform: rotate(2deg);
}

/* Feature strip */
.strip { display:grid; grid-template-columns: repeat(4, 1fr); gap:1rem; text-align:center; margin-top:1.6rem; }
.strip div { padding:.4rem; border-right:2px solid var(--wood); }
.strip div:last-child { border-right:none; }
.strip .ic { font-size:2.2rem; }
.strip .lb { font-family:'Baloo 2'; font-weight:600; font-size:1.05rem; color:var(--accent); }

/* ───── Cards / quiz ───── */
.card {
    background: var(--surface); border:2px solid var(--sand); border-radius:22px;
    padding:1.3rem 1.5rem; margin-bottom:1rem;
}
.stApp .card h3 { margin:0 0 .4rem; font-size:1.35rem; color: var(--accent); }
.stApp .card p { font-size:1.12rem; line-height:1.75; margin:0; max-width:70ch; color: var(--ink); }
.qtag {
    display:inline-block; background:var(--sand); color:var(--accent); border-radius:999px;
    padding:.1rem .8rem; font-size:.85rem; font-weight:700; margin-bottom:.4rem;
}
.qtext { font-size:1.12rem; font-weight:700; margin-bottom:.3rem; color: var(--ink); }

/* ───── Results ───── */
.score-ring {
    width: 190px; height: 190px; border-radius: 50%; margin: 0 auto;
    display:flex; align-items:center; justify-content:center;
}
.score-ring .inner {
    background: var(--bg); width:150px; height:150px; border-radius:50%;
    display:flex; align-items:center; justify-content:center; flex-direction:column;
}
.score-ring .pct { font-family:'Baloo 2'; font-size:3rem; font-weight:800; color:var(--accent); line-height:1; }
.score-ring .of { font-size:1rem; font-weight:700; color:var(--ink); }
.stat {
    text-align:center; background:var(--surface); border:2px solid var(--sand);
    border-radius:20px; padding:1rem; color:var(--ink); font-weight:600;
}
.stat .n { font-family:'Baloo 2'; font-size:2.2rem; font-weight:800; line-height:1; }
.stat .n.ok { color: var(--ok-tx); }
.stat .n.bad { color: var(--bad-tx); }
.cheer {
    background:var(--btn); color:#fff; border-radius:22px; padding:1.2rem 1.6rem;
    font-family:'Baloo 2'; font-size:1.35rem; text-align:center; margin:1.2rem 0;
}
.res { border-radius:16px; padding:.9rem 1.2rem; margin-bottom:.7rem; font-size:1.05rem; color:var(--ink); }
.res.ok { background:var(--ok-bg); border:2px solid var(--ok-bd); }
.res.bad { background:var(--bad-bg); border:2px solid var(--bad-bd); }
.res .rq { font-weight:700; }

/* ───── Tablets (≤ 900px) ───── */
@media (max-width: 900px) {
    .st-key-hero { padding: 1.4rem 1rem 1rem; }
    .st-key-hero [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: 1rem !important; }
    .st-key-hero [data-testid="stColumn"], .st-key-hero [data-testid="column"] {
        flex: 1 1 calc(50% - 1rem) !important; min-width: calc(50% - 1rem) !important;
    }
    .st-key-hero [data-testid="stColumn"]:nth-child(2), .st-key-hero [data-testid="column"]:nth-child(2) {
        flex: 1 1 100% !important; min-width: 100% !important; order: -1;
    }
}

/* ───── Phones (≤ 640px) ───── */
@media (max-width: 640px) {
    .block-container { padding: .8rem .7rem 2.5rem; }

    /* top bar: brand on its own row, nav buttons in a 2×2 grid */
    .st-key-topbar [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: .5rem !important; }
    .st-key-topbar [data-testid="stColumn"], .st-key-topbar [data-testid="column"] {
        flex: 1 1 calc(50% - .5rem) !important; min-width: calc(50% - .5rem) !important;
    }
    .st-key-topbar [data-testid="stColumn"]:first-child, .st-key-topbar [data-testid="column"]:first-child {
        flex: 1 1 100% !important; min-width: 100% !important;
    }
    .brand .t1 { font-size: 1.4rem; }
    .brand .logo { font-size: 1.8rem; }

    /* hero: everything stacked, welcome board first */
    .st-key-hero { border-radius: 20px; padding: 1rem .8rem .8rem; }
    .st-key-hero [data-testid="stColumn"], .st-key-hero [data-testid="column"] {
        flex: 1 1 100% !important; min-width: 100% !important;
    }
    .sign { font-size: .88rem; }
    .chalk { font-size: 1.1rem; }

    .strip { grid-template-columns: repeat(2, 1fr); gap:.6rem; }
    .strip div { border-right: none; }
    .strip .ic { font-size: 1.8rem; }
    .strip .lb { font-size: .95rem; }

    .card { padding: 1rem 1.1rem; border-radius: 18px; }
    .stApp .card p { font-size: 1.05rem; line-height: 1.65; }
    .stApp .card h3 { font-size: 1.2rem; }

    .score-ring { width: 160px; height: 160px; }
    .score-ring .inner { width: 126px; height: 126px; }
    .score-ring .pct { font-size: 2.4rem; }
    .cheer { font-size: 1.15rem; padding: 1rem 1.1rem; }
    .res { font-size: 1rem; padding: .8rem 1rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ───────────────────────── State ─────────────────────────

ss = st.session_state
ss.setdefault("page", "Home")
ss.setdefault("submitted", False)
ss.setdefault("answers", {})
ss.setdefault("version", 0)  # changes on retake so the widgets reset


def go(page: str):
    ss.page = page


def normalize(text: str) -> str:
    text = re.sub(r"[^a-z0-9 ]", " ", (text or "").lower())
    return re.sub(r"\s+", " ", text).strip()


def is_correct(q: dict, given) -> bool:
    if given is None or str(given).strip() == "":
        return False
    if q["type"] in ("tf", "mc"):
        return given == q["answer"]
    g = f" {normalize(given)} "
    return any(f" {normalize(a)} " in g for a in q["accepted"])


def grade():
    results = []
    for i, q in enumerate(QUESTIONS):
        given = ss.answers.get(i)
        results.append({"q": q, "given": given, "ok": is_correct(q, given)})
    return results


def retake():
    ss.answers = {}
    ss.submitted = False
    ss.version += 1
    ss.page = "Quiz"


# ───────────────────────── Top bar ─────────────────────────

NAV = [("Home", "🏠"), ("Read", "📖"), ("Quiz", "📝"), ("Results", "🏆")]

with st.container(key="topbar"):
    brand, *navcols = st.columns([2.4, 1, 1, 1, 1])
    with brand:
        st.markdown(
            '<div class="brand"><div class="logo">🛒</div><div>'
            '<div class="t1">Read &amp; Test</div><div class="t2">English Reading Quiz</div>'
            "</div></div>",
            unsafe_allow_html=True,
        )
    for col, (name, icon) in zip(navcols, NAV):
        with col:
            st.button(
                f"{icon} {name}",
                key=f"nav_{name}",
                type="primary" if ss.page == name else "secondary",
                on_click=go,
                args=(name,),
            )

# ───────────────────────── Page 1: Home ─────────────────────────

if ss.page == "Home":
    signs = "".join(f'<div class="sign"><b>{n}</b>({c})</div>' for n, c in MARKETS)

    with st.container(key="hero"):
        left, mid, right = st.columns([1.15, 1.9, 1.05], gap="medium")
        with left:
            st.markdown(f'<div class="signpost">{signs}</div>', unsafe_allow_html=True)
            st.markdown('<div class="emoji-row">🧺🍎🍊🍇</div>', unsafe_allow_html=True)
        with mid:
            st.markdown(
                '<div class="board"><h1>Welcome to<br>the Markets!</h1>'
                '<div class="sub">Explore five amazing food markets around the world.</div></div>',
                unsafe_allow_html=True,
            )
            st.write("")
            st.button("READ NOW  →", key="read_now", type="primary", on_click=go, args=("Read",))
            st.markdown('<div class="emoji-row">🛒🥬🍅</div>', unsafe_allow_html=True)
        with right:
            st.markdown('<div class="chalk">Fresh Food<br>Good Mood ♡</div>', unsafe_allow_html=True)
            st.markdown('<div class="emoji-row">👩‍🍳🥖</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="strip">'
        '<div><div class="ic">🌍</div><div class="lb">Discover<br>Global Markets</div></div>'
        '<div><div class="ic">📖</div><div class="lb">Read &amp; Learn</div></div>'
        '<div><div class="ic">✅</div><div class="lb">Test Your Knowledge</div></div>'
        '<div><div class="ic">🏆</div><div class="lb">See Your Results</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

# ───────────────────────── Page 2: Read ─────────────────────────

elif ss.page == "Read":
    st.markdown("## Top 5 | Food markets")
    st.caption("Food markets are great places to find interesting local food. Here are our top five markets from around the world.")
    for title, body in PASSAGE:
        st.markdown(f'<div class="card"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)
    _, c, _ = st.columns([1, 1, 1])
    with c:
        st.button("Go Quiz Now  →", key="go_quiz", type="primary", on_click=go, args=("Quiz",))

# ───────────────────────── Page 3: Quiz ─────────────────────────

elif ss.page == "Quiz":
    st.markdown("## Quiz Time")
    st.caption("10 questions: True or False, Choose the correct answer, and Short answer.")

    if ss.submitted:
        st.info("You already submitted this quiz. You can see your results or try again.")
        c1, c2 = st.columns(2)
        c1.button("See my results", type="primary", on_click=go, args=("Results",))
        c2.button("Try again", on_click=retake)
    else:
        with st.form("quiz_form"):
            collected = {}
            for i, q in enumerate(QUESTIONS):
                key = f"q{i}_{ss.version}"
                st.markdown(
                    f'<span class="qtag">Question {i + 1} · {TYPE_LABEL[q["type"]]}</span>'
                    f'<div class="qtext">{q["q"]}</div>',
                    unsafe_allow_html=True,
                )
                if q["type"] == "tf":
                    collected[i] = st.radio(
                        q["q"], ["True", "False"], index=None, key=key,
                        horizontal=True, label_visibility="collapsed",
                    )
                elif q["type"] == "mc":
                    collected[i] = st.radio(
                        q["q"], q["options"], index=None, key=key, label_visibility="collapsed",
                    )
                else:
                    collected[i] = st.text_input(
                        q["q"], key=key, placeholder="Type your answer here",
                        label_visibility="collapsed",
                    )
                st.divider()
            submitted = st.form_submit_button("Submit answers", type="primary")

        if submitted:
            ss.answers = collected
            ss.submitted = True
            ss.page = "Results"
            st.rerun()

# ───────────────────────── Page 4: Results ─────────────────────────

elif ss.page == "Results":
    st.markdown("## Your Results")

    if not ss.submitted:
        st.warning("You haven't finished the quiz yet. Take the quiz to see your results.")
        st.button("Go to the quiz", type="primary", on_click=go, args=("Quiz",))
    else:
        results = grade()
        total = len(results)
        right_n = sum(r["ok"] for r in results)
        wrong_n = total - right_n
        pct = round(right_n / total * 100)

        if pct == 100:
            msg = "🌟 Perfect score! You are a true market expert. Amazing work!"
        elif pct >= 80:
            msg = "🎉 Excellent work! You understood the text very well. Keep it up!"
        elif pct >= 60:
            msg = "👏 Good job! You are doing well. Read once more and you will get even higher."
        elif pct >= 40:
            msg = "💪 Nice try! Every attempt makes you better. Read the text again and try once more."
        else:
            msg = "🌱 Don't give up! Learning takes time. Read the text again slowly and you will improve."

        ring = f"background: conic-gradient(var(--accent) {pct * 3.6}deg, var(--sand) 0);"
        c1, c2, c3 = st.columns([1.2, 1, 1], vertical_alignment="center")
        with c1:
            st.markdown(
                f'<div class="score-ring" style="{ring}"><div class="inner">'
                f'<div class="pct">{pct}%</div><div class="of">{right_n} / {total}</div></div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="stat"><div class="n ok">{right_n}</div>Correct answers</div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="stat"><div class="n bad">{wrong_n}</div>Wrong answers</div>',
                unsafe_allow_html=True,
            )

        st.markdown(f'<div class="cheer">{msg}</div>', unsafe_allow_html=True)

        wrong = [(i, r) for i, r in enumerate(results, 1) if not r["ok"]]
        right = [(i, r) for i, r in enumerate(results, 1) if r["ok"]]

        st.markdown("### ❌ Wrong answers")
        if not wrong:
            st.success("No wrong answers. Great job!")
        for i, r in wrong:
            given = r["given"] if r["given"] not in (None, "") else "No answer"
            st.markdown(
                f'<div class="res bad"><div class="rq">{i}. {r["q"]}</div>'
                f'Your answer: <b>{given}</b><br>Correct answer: <b>{r["q"]["answer"]}</b></div>',
                unsafe_allow_html=True,
            )

        st.markdown("### ✅ Correct answers")
        if not right:
            st.info("No correct answers this time. Try again!")
        for i, r in right:
            st.markdown(
                f'<div class="res ok"><div class="rq">{i}. {r["q"]}</div>'
                f'Your answer: <b>{r["given"]}</b></div>',
                unsafe_allow_html=True,
            )

        b1, b2 = st.columns(2)
        b1.button("📖 Read again", on_click=go, args=("Read",))
        b2.button("🔁 Try the quiz again", type="primary", on_click=retake)
