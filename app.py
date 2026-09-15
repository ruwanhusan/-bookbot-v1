import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bookbot", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.stApp {background:#f5f7fb;color:#0b1f3a}
section[data-testid="stSidebar"] {background:#071b36;}
section[data-testid="stSidebar"] * {color:white;}
.hero {padding:28px 32px;border-radius:22px;background:linear-gradient(120deg,#071b36,#123e78);color:white;margin-bottom:22px}
.card {background:white;border:1px solid #e7ebf2;border-radius:18px;padding:20px;box-shadow:0 4px 18px rgba(10,30,60,.05)}
.small {color:#68758a;font-size:.9rem}
.status-green {color:#169b62;font-weight:700}
.status-yellow {color:#d58a00;font-weight:700}
.status-red {color:#d33b3b;font-weight:700}
div[data-testid="stMetric"] {background:white;border:1px solid #e7ebf2;padding:16px;border-radius:16px}
.stButton>button {border-radius:12px;font-weight:700}
</style>
""", unsafe_allow_html=True)

if "docs" not in st.session_state:
    st.session_state.docs = [
        ["Bol.com","€ 242,00","Kantoorbenodigdheden","🟢 Automatisch"],
        ["NS Zakelijk","€ 184,50","Vervoerskosten","🟢 Automatisch"],
        ["Adobe","€ 72,60","Software","🟡 Controle"],
        ["Coolblue","€ 599,00","Computerapparatuur","🔴 Handmatig"],
    ]

with st.sidebar:
    st.markdown("## 🤖 Bookbot")
    st.caption("Uw administratie, onze AI.")
    page = st.radio("Navigatie", ["Startpagina","Documenten","Boekhouding","Btw","Rapportages","Fiscale assistent","Instellingen"], label_visibility="collapsed")
    st.divider()
    st.caption("Demo-administratie")
    st.write("**Husan Administratie**")
    st.caption("🇳🇱 Nederlandse fiscale regels")

if page == "Startpagina":
    st.markdown("""<div class="hero"><h1>Goedemiddag 👋</h1>
    <p>Uw administratie is bijgewerkt. Bookbot heeft vandaag 12 documenten gecontroleerd.</p></div>""", unsafe_allow_html=True)
    a,b,c,d = st.columns(4)
    a.metric("Omzet","€ 12.450","+8,4%")
    b.metric("Kosten","€ 4.280","-2,1%")
    c.metric("Winst","€ 8.170","+14,7%")
    d.metric("Btw te betalen","€ 1.680")
    st.subheader("⚡ Uw aandacht nodig")
    c1,c2 = st.columns(2)
    with c1:
        st.info("Adobe-factuur vraagt om controle van de boekingscategorie.")
    with c2:
        st.warning("Coolblue-document heeft onvoldoende AI-zekerheid.")
    st.subheader("Recente transacties")
    st.dataframe(pd.DataFrame(st.session_state.docs, columns=["Leverancier","Bedrag","Categorie","Status"]), use_container_width=True, hide_index=True)
    st.subheader("✨ Bookbot AI-inzicht")
    st.success("Uw softwarekosten liggen deze maand hoger dan gemiddeld. Controleer of alle abonnementen nog zakelijk nodig zijn.")

elif page == "Documenten":
    st.title("📄 Documenten")
    st.caption("Upload facturen en bonnen. Bookbot maakt daarna een boekingsvoorstel.")
    f = st.file_uploader("Document uploaden", type=["pdf","png","jpg","jpeg"])
    if f:
        st.success(f"{f.name} is ontvangen.")
        if st.button("🤖 Analyseer met Bookbot"):
            st.session_state.analysis = True
    if st.session_state.get("analysis"):
        st.subheader("AI-boekingsvoorstel")
        c1,c2,c3 = st.columns(3)
        c1.metric("Excl. btw","€ 60,00")
        c2.metric("Btw 21%","€ 12,60")
        c3.metric("Incl. btw","€ 72,60")
        st.write("**Leverancier:** Adobe")
        st.write("**Categorie:** Software")
        st.write("**Btw-code:** 21% voorbelasting")
        st.warning("🟡 Controle vereist — zekerheid 84%")
        if st.button("✓ Goedkeuren en boeken"):
            st.success("Demo: boekingsvoorstel goedgekeurd.")
    st.dataframe(pd.DataFrame(st.session_state.docs, columns=["Leverancier","Bedrag","Categorie","Status"]), use_container_width=True, hide_index=True)

elif page == "Boekhouding":
    st.title("📚 Boekhouding")
    data = pd.DataFrame([
        ["2026-09-02","NS Zakelijk","Vervoerskosten",152.48,32.02,184.50,"🟢"],
        ["2026-09-05","Adobe","Software",60.00,12.60,72.60,"🟡"],
        ["2026-09-08","Coolblue","Computerapparatuur",495.04,103.96,599.00,"🔴"],
    ], columns=["Datum","Relatie","Grootboek","Excl. btw","Btw","Totaal","Status"])
    st.dataframe(data, use_container_width=True, hide_index=True)
    st.caption("AI doet voorstellen; de boekhoud- en controleregels bepalen of een boeking automatisch verwerkt mag worden.")

elif page == "Btw":
    st.title("🧮 Btw")
    a,b,c = st.columns(3)
    a.metric("Verschuldigde btw","€ 2.520")
    b.metric("Voorbelasting","€ 840")
    c.metric("Saldo","€ 1.680")
    st.progress(0.78, text="Administratie 78% gecontroleerd")
    st.subheader("Btw-controle")
    st.success("Geen dubbele facturen gevonden.")
    st.info("2 documenten vragen nog om controle voordat de aangifte compleet is.")

elif page == "Rapportages":
    st.title("📊 Rapportages")
    chart = pd.DataFrame({"Omzet":[7800,9100,10400,12450],"Kosten":[3600,3900,4100,4280]}, index=["Jun","Jul","Aug","Sep"])
    st.bar_chart(chart)
    st.subheader("Resultaat")
    st.metric("Winst lopende periode","€ 8.170","+14,7%")
    st.info("Bookbot ziet een stijgende omzet terwijl de kosten relatief stabiel blijven.")

elif page == "Fiscale assistent":
    st.title("🤖 Fiscale assistent")
    st.caption("Stel vragen over uw administratie en Nederlandse fiscale regels.")
    q = st.chat_input("Bijvoorbeeld: hoeveel btw moet ik betalen?")
    if q:
        with st.chat_message("user"): st.write(q)
        with st.chat_message("assistant"):
            if "btw" in q.lower():
                st.write("Op basis van deze demo-administratie is het huidige btw-saldo **€ 1.680 te betalen**. Er staan nog 2 documenten open voor controle.")
            else:
                st.write("In de uiteindelijke versie combineert Bookbot uw eigen administratie met gecontroleerde Nederlandse fiscale regels om deze vraag te beantwoorden.")

elif page == "Instellingen":
    st.title("⚙️ Instellingen")
    st.text_input("Bedrijfsnaam","Husan Administratie")
    st.selectbox("Rechtsvorm",["Eenmanszaak","BV","VOF"])
    st.text_input("KvK-nummer","12345678")
    st.selectbox("Taal",["Nederlands","English","Français","Deutsch","Español","Andere taal"])
    st.selectbox("Fiscaal land",["Nederland"])
    st.slider("Minimale AI-zekerheid voor automatisch verwerken",70,99,92)
    st.checkbox("Proactieve AI-inzichten",True)
    st.checkbox("Waarschuwen voor dubbele facturen",True)
    st.button("Instellingen opslaan")

st.divider()
st.caption("Bookbot V2 Professional Prototype • Demo-omgeving • Geen echte boekingen of aangiften.")
