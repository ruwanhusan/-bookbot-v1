import streamlit as st
import pandas as pd
import altair as alt
from supabase import create_client

st.set_page_config(page_title="Bookbot", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# ---------- Styling ----------
st.markdown("""
<style>
:root{
 --navy:#071b36; --navy2:#0d2b52; --blue:#1677ff; --bg:#f5f8fc;
 --text:#10213c; --muted:#66758c; --line:#e5ebf3; --green:#16a36a; --red:#e54b4b;
}
.stApp {background:var(--bg);}
.block-container {padding-top:1.25rem; padding-bottom:2rem; max-width:1600px;}
section[data-testid="stSidebar"] {background:linear-gradient(180deg,#071b36 0%,#092448 100%); border-right:0;}
section[data-testid="stSidebar"] * {color:#fff;}
section[data-testid="stSidebar"] div[role="radiogroup"] label {
 padding:10px 12px; border-radius:10px; margin:2px 0;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {background:rgba(255,255,255,.08);}
div[data-testid="stMetric"]{
 background:#fff;border:1px solid var(--line);border-radius:16px;padding:17px 18px;
 box-shadow:0 4px 18px rgba(20,45,80,.04);
}
[data-testid="stMetricLabel"] {color:#5f6f86;}
[data-testid="stMetricValue"] {color:#10213c;}
.bb-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px;
box-shadow:0 4px 18px rgba(20,45,80,.04);margin-bottom:14px;}
.bb-ai{background:linear-gradient(160deg,#071b36,#0b315f);border-radius:18px;padding:20px;color:white;min-height:370px;}
.bb-ai h3,.bb-ai p{color:white;}
.bb-chip{display:inline-block;background:#eef5ff;color:#1769d2;padding:7px 10px;border-radius:9px;margin:4px 3px;font-size:13px;}
.bb-alert{padding:12px 14px;border-bottom:1px solid #edf1f6;}
.bb-title{font-size:30px;font-weight:800;color:#10213c;margin:4px 0;}
.bb-sub{color:#66758c;margin-bottom:20px;}
.bb-banner{background:linear-gradient(110deg,#071b36,#164a7e);border-radius:18px;padding:22px 26px;color:#fff;margin-top:12px;}
.bb-banner h3,.bb-banner p{color:#fff;margin:0;}
.stButton>button {border-radius:10px;font-weight:700;}
div[data-testid="stDataFrame"] {border-radius:14px;overflow:hidden;border:1px solid var(--line);}
</style>
""", unsafe_allow_html=True)

# ---------- Supabase ----------
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception:
    st.error("Supabase Secrets ontbreken. Controleer SUPABASE_URL en SUPABASE_KEY in Streamlit Secrets.")
    st.stop()

for k in ["access_token","refresh_token","user_id","email","company"]:
    st.session_state.setdefault(k, None)

def clear_session():
    for k in ["access_token","refresh_token","user_id","email","company"]:
        st.session_state[k] = None

def do_login(email, password):
    auth = supabase.auth.sign_in_with_password({"email":email.strip(),"password":password})
    st.session_state.access_token = auth.session.access_token
    st.session_state.refresh_token = auth.session.refresh_token
    st.session_state.user_id = auth.user.id
    st.session_state.email = auth.user.email
    supabase.auth.set_session(auth.session.access_token, auth.session.refresh_token)
    res = supabase.table("companies").select("*").eq("user_id", auth.user.id).limit(1).execute()
    st.session_state.company = res.data[0] if res.data else None

# ---------- Login ----------
if not st.session_state.user_id:
    left, mid, right = st.columns([1,1.2,1])
    with mid:
        st.markdown("""
        <div class="bb-card" style="margin-top:70px;text-align:center;padding:34px">
        <div style="font-size:52px">🤖</div>
        <div style="font-size:34px;font-weight:850;color:#10213c">Book<span style="color:#1677ff">bot</span></div>
        <p style="color:#66758c">Uw administratie, onze AI.</p>
        </div>""", unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("E-mailadres")
            password = st.text_input("Wachtwoord", type="password")
            login_btn = st.form_submit_button("Inloggen", use_container_width=True)
        if login_btn:
            try:
                do_login(email, password)
                st.rerun()
            except Exception:
                st.error("Inloggen is niet gelukt. Controleer uw gegevens.")
    st.stop()

try:
    supabase.auth.set_session(st.session_state.access_token, st.session_state.refresh_token)
except Exception:
    clear_session()
    st.rerun()

company = st.session_state.company or {}
company_name = company.get("name") or "Mijn onderneming"

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("""
    <div style="padding:8px 4px 16px">
      <div style="font-size:28px;font-weight:850">🤖 Book<span style="color:#45a0ff">bot</span></div>
      <div style="font-size:12px;opacity:.78">Uw administratie, onze AI.</div>
    </div>
    """, unsafe_allow_html=True)
    page = st.radio(
        "Navigatie",
        ["🏠 Dashboard","📄 Documenten","📚 Boekhouding","🧮 Btw","📊 Rapportages","✨ AI Assistent","⚙️ Instellingen"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("INGELOGD ALS")
    st.write(f"**{company_name}**")
    st.caption(st.session_state.email or "")
    st.write("")
    if st.button("↪ Uitloggen", use_container_width=True):
        try: supabase.auth.sign_out()
        except Exception: pass
        clear_session()
        st.rerun()

# ---------- Demo datasets ----------
months = ["Jan","Feb","Mrt","Apr","Mei","Jun","Jul","Aug","Sep"]
chart_df = pd.DataFrame({
    "Maand": months,
    "Omzet":[80000,85000,105000,125000,115000,122000,135000,158000,143000],
    "Kosten":[43000,47000,68000,82000,76000,92000,85000,96000,83000]
})
profit_df = pd.DataFrame({"Maand":months,"Winst":[19000,28000,34000,30000,39000,36000,47000,51000,61000]})

# ---------- Dashboard ----------
if page == "🏠 Dashboard":
    st.markdown(f'<div class="bb-title">Goedemiddag 👋</div><div class="bb-sub">Hier is een overzicht van de financiële situatie van <b>{company_name}</b>.</div>', unsafe_allow_html=True)

    m1,m2,m3,m4 = st.columns(4)
    m1.metric("📈 Omzet","€ 125.430","12% t.o.v. vorig kwartaal")
    m2.metric("📉 Kosten","€ 78.210","5% t.o.v. vorig kwartaal", delta_color="inverse")
    m3.metric("📊 Winst","€ 47.220","18% t.o.v. vorig kwartaal")
    m4.metric("🧮 Te betalen btw","€ 8.430","Q3 2026")

    main, ai = st.columns([3.15,1.05], gap="medium")
    with main:
        c1,c2 = st.columns([1.35,1])
        with c1:
            st.markdown('<div class="bb-card"><b>Omzet & kosten</b>', unsafe_allow_html=True)
            long = chart_df.melt("Maand", var_name="Type", value_name="Bedrag")
            chart = alt.Chart(long).mark_bar().encode(
                x=alt.X("Maand:N", sort=months, title=None),
                y=alt.Y("Bedrag:Q", title=None),
                xOffset="Type:N",
                color=alt.Color("Type:N", scale=alt.Scale(range=["#176fd1","#b9d7fa"]), legend=alt.Legend(orient="top"))
            ).properties(height=260)
            st.altair_chart(chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="bb-card"><b>Winstontwikkeling</b>', unsafe_allow_html=True)
            line = alt.Chart(profit_df).mark_area(line={"color":"#159b63"}, color="#dff4e9").encode(
                x=alt.X("Maand:N", sort=months, title=None),
                y=alt.Y("Winst:Q", title=None)
            ).properties(height=260)
            st.altair_chart(line, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        t1,t2 = st.columns([1,1.15])
        with t1:
            st.markdown('<div class="bb-card"><b>Recente transacties</b></div>', unsafe_allow_html=True)
            tx = pd.DataFrame([
                ["Albert Heijn","Inkoop","- € 124,35","Vandaag"],
                ["Coolblue","Kantoorbenodigdheden","- € 349,00","Vandaag"],
                ["ABN AMRO","Omzet","+ € 2.450,00","9 sep 2026"],
                ["KPN","Telecom","- € 62,50","8 sep 2026"],
                ["Shell","Brandstof","- € 89,20","7 sep 2026"],
            ], columns=["Relatie","Categorie","Bedrag","Datum"])
            st.dataframe(tx, use_container_width=True, hide_index=True)
        with t2:
            st.markdown("""
            <div class="bb-card"><b>Uw aandacht nodig &nbsp; 🔴 3</b>
              <div class="bb-alert">📄 <b>1 factuur nog niet verwerkt</b><br><span style="color:#78869a">Geüpload op 8 sep 2026</span></div>
              <div class="bb-alert">🧮 <b>Btw-aangifte Q3 2026</b><br><span style="color:#78869a">Deadline: 31 okt 2026</span></div>
              <div class="bb-alert">📌 <b>3 mogelijke onkostenposten</b><br><span style="color:#78869a">Nog te categoriseren</span></div>
              <div class="bb-alert">⚠️ <b>Controleer afwijkende boeking</b><br><span style="color:#78869a">€ 1.250,00 – 5 sep 2026</span></div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="bb-banner"><h3>“Een sterke administratie is de basis voor vrijheid.”</h3>
        <p>Laat de cijfers voor u werken. Bookbot regelt de rest.</p></div>
        """, unsafe_allow_html=True)

    with ai:
        st.markdown("""
        <div class="bb-ai">
          <div style="font-size:28px">🤖</div>
          <h3>Bookbot AI</h3>
          <p style="opacity:.8">Uw persoonlijke fiscale en financiële assistent.</p>
          <div class="bb-chip">Analyseer mijn kosten</div><br>
          <div class="bb-chip">Hoeveel btw moet ik betalen?</div><br>
          <div class="bb-chip">Maak een winstprognose</div><br>
          <div class="bb-chip">Geef belastingbespaartips</div><br>
          <div class="bb-chip">Leg deze boeking uit</div>
        </div>
        """, unsafe_allow_html=True)
        question = st.text_input("Vraag aan Bookbot", placeholder="Stel hier uw vraag...", label_visibility="collapsed")
        if question:
            st.info("De AI-interface staat klaar. De echte financiële AI koppelen we in een volgende fase.")
        st.markdown('<div class="bb-card"><b>Snelle acties</b><br><br>📤 Factuur uploaden<br><br>➕ Nieuwe boeking<br><br>🧮 Btw-aangifte<br><br>📥 Rapport downloaden</div>', unsafe_allow_html=True)

elif page == "📄 Documenten":
    st.title("📄 Documenten")
    st.caption("Upload, controleer en verwerk facturen en bonnen.")
    st.file_uploader("Sleep een factuur of bon hierheen", type=["pdf","png","jpg","jpeg"])
    docs = pd.DataFrame([
        ["Adobe","Factuur","€ 72,60","🟡 Controle"],
        ["Coolblue","Factuur","€ 599,00","🔴 Handmatig"],
        ["NS Zakelijk","Factuur","€ 184,50","🟢 Verwerkt"],
    ], columns=["Leverancier","Type","Bedrag","Status"])
    st.dataframe(docs, use_container_width=True, hide_index=True)

elif page == "📚 Boekhouding":
    st.title("📚 Boekhouding")
    st.caption("Alle boekingen en transacties op één plek.")
    st.dataframe(pd.DataFrame([
        ["12-09-2026","Albert Heijn","Inkoop","€ 124,35","Verwerkt"],
        ["11-09-2026","Coolblue","Kantoor","€ 349,00","Verwerkt"],
        ["09-09-2026","Klantfactuur #084","Omzet","€ 2.450,00","Verwerkt"],
    ], columns=["Datum","Omschrijving","Grootboek","Bedrag","Status"]), use_container_width=True, hide_index=True)

elif page == "🧮 Btw":
    st.title("🧮 Btw")
    a,b,c = st.columns(3)
    a.metric("Verschuldigde btw","€ 12.580")
    b.metric("Voorbelasting","€ 4.150")
    c.metric("Te betalen","€ 8.430")
    st.warning("Demo: deze bedragen zijn nog niet uit echte boekingen berekend.")

elif page == "📊 Rapportages":
    st.title("📊 Rapportages")
    st.subheader("Omzet & kosten")
    st.bar_chart(chart_df.set_index("Maand")[["Omzet","Kosten"]])
    st.info("Later genereren we hier winst-en-verliesrekening, balans en exportbestanden uit echte boekingen.")

elif page == "✨ AI Assistent":
    st.title("✨ Bookbot AI Assistent")
    st.caption("Uw persoonlijke fiscale en financiële assistent.")
    for prompt in ["Analyseer mijn kosten","Hoeveel btw moet ik betalen?","Maak een winstprognose","Leg mijn grootste kostenposten uit"]:
        if st.button(prompt):
            st.session_state["demo_ai"] = prompt
    q = st.chat_input("Stel uw vraag aan Bookbot...")
    if q or st.session_state.get("demo_ai"):
        userq = q or st.session_state.pop("demo_ai")
        with st.chat_message("user"): st.write(userq)
        with st.chat_message("assistant"):
            st.write("De professionele AI-interface werkt. In de volgende fase koppelen we deze aan echte boekingen en gecontroleerde fiscale regels.")

elif page == "⚙️ Instellingen":
    st.title("⚙️ Instellingen")
    if company:
        st.text_input("Bedrijfsnaam", company.get("name") or "", disabled=True)
        st.text_input("KvK-nummer", company.get("kvk_number") or "", disabled=True)
        st.text_input("Btw-nummer", company.get("vat_number") or "", disabled=True)
        st.text_input("Rechtsvorm", company.get("legal_form") or "", disabled=True)
        st.text_input("Land", company.get("country") or "", disabled=True)
        st.success("Deze bedrijfsgegevens worden live uit Supabase gelezen.")
    else:
        st.warning("Geen gekoppeld company-record gevonden.")

st.caption("Bookbot V4 Professional • Supabase-login actief • financiële cijfers zijn voorlopig demo-data.")
