import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Bookbot", page_icon="🤖", layout="wide")

supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

for k in ["access_token", "refresh_token", "user_id", "email", "company"]:
    if k not in st.session_state:
        st.session_state[k] = None

def clear_session():
    for k in ["access_token", "refresh_token", "user_id", "email", "company"]:
        st.session_state[k] = None

if not st.session_state.user_id:
    st.title("🤖 Bookbot")
    st.subheader("Uw administratie, onze AI.")
    st.write("Log in op uw Bookbot-account.")
    with st.form("login"):
        email = st.text_input("E-mailadres")
        password = st.text_input("Wachtwoord", type="password")
        submit = st.form_submit_button("Inloggen")
    if submit:
        try:
            auth = supabase.auth.sign_in_with_password({"email": email.strip(), "password": password})
            st.session_state.access_token = auth.session.access_token
            st.session_state.refresh_token = auth.session.refresh_token
            st.session_state.user_id = auth.user.id
            st.session_state.email = auth.user.email
            supabase.auth.set_session(auth.session.access_token, auth.session.refresh_token)
            result = supabase.table("companies").select("*").eq("user_id", auth.user.id).limit(1).execute()
            st.session_state.company = result.data[0] if result.data else None
            st.rerun()
        except Exception:
            st.error("Inloggen is niet gelukt. Controleer uw e-mailadres en wachtwoord.")
    st.stop()

try:
    supabase.auth.set_session(st.session_state.access_token, st.session_state.refresh_token)
except Exception:
    clear_session()
    st.rerun()

company = st.session_state.company or {}
company_name = company.get("name") or "Mijn onderneming"

with st.sidebar:
    st.title("🤖 Bookbot")
    st.caption("Uw administratie, onze AI.")
    st.write(f"**{company_name}**")
    st.caption(st.session_state.email or "")
    page = st.radio("Navigatie", ["Startpagina", "Documenten", "Boekhouding", "Btw", "Rapportages", "Fiscale assistent", "Instellingen"])
    if st.button("Uitloggen"):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
        clear_session()
        st.rerun()

if page == "Startpagina":
    st.title("Welkom bij Bookbot 👋")
    if company:
        st.success("✓ Uw Bookbot-account is gekoppeld aan Supabase.")
        a,b,c = st.columns(3)
        a.metric("Bedrijf", company.get("name") or "—")
        b.metric("Rechtsvorm", company.get("legal_form") or "—")
        c.metric("Land", company.get("country") or "—")
    else:
        st.warning("Er is nog geen bedrijf gekoppeld aan dit account.")
    st.subheader("Dashboard")
    a,b,c,d = st.columns(4)
    a.metric("Omzet", "€ 12.450")
    b.metric("Kosten", "€ 4.280")
    c.metric("Winst", "€ 8.170")
    d.metric("Btw", "€ 1.680")
    st.caption("De financiële cijfers zijn in V3 nog demo-data.")

elif page == "Documenten":
    st.title("📄 Documenten")
    st.file_uploader("Factuur of bon uploaden", type=["pdf","png","jpg","jpeg"])
    st.info("Volgende fase: uploads opslaan in Supabase Storage en automatisch analyseren.")

elif page == "Boekhouding":
    st.title("📚 Boekhouding")
    st.info("De echte boekingstabellen bouwen we in de volgende fase.")

elif page == "Btw":
    st.title("🧮 Btw")
    st.metric("Demo btw-saldo", "€ 1.680")

elif page == "Rapportages":
    st.title("📊 Rapportages")
    st.info("Rapportages worden later uit de echte boekingen berekend.")

elif page == "Fiscale assistent":
    st.title("🤖 Fiscale assistent")
    st.info("Deze wordt later gekoppeld aan uw echte administratie en fiscale regels.")

elif page == "Instellingen":
    st.title("⚙️ Bedrijfsgegevens")
    if company:
        st.text_input("Bedrijfsnaam", company.get("name") or "", disabled=True)
        st.text_input("KvK-nummer", company.get("kvk_number") or "", disabled=True)
        st.text_input("Btw-nummer", company.get("vat_number") or "", disabled=True)
        st.text_input("Rechtsvorm", company.get("legal_form") or "", disabled=True)
        st.text_input("Land", company.get("country") or "", disabled=True)

st.divider()
st.caption("Bookbot V3 • echte Supabase-login + company-koppeling • financiële modules nog demo")
