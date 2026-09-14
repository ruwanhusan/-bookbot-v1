import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Bookbot", page_icon="🤖", layout="wide")

if "transactions" not in st.session_state:
    st.session_state.transactions = [
        {"id":"000001","date":"14-09-2026","supplier":"Adobe","description":"Adobe Creative Cloud","net":100.00,"vat":21.00,"gross":121.00,"vat_rate":"21%","account":"Softwarekosten","status":"Goedgekeurd"},
        {"id":"000002","date":"12-09-2026","supplier":"Bol.com","description":"Kantoorbenodigdheden","net":49.59,"vat":10.41,"gross":60.00,"vat_rate":"21%","account":"Kantoorkosten","status":"Goedgekeurd"},
        {"id":"000003","date":"10-09-2026","supplier":"NS","description":"Zakelijke treinreis","net":45.87,"vat":4.13,"gross":50.00,"vat_rate":"9%","account":"Reiskosten","status":"Controle"},
    ]

def euro(x):
    return f"€ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def totals():
    df = pd.DataFrame(st.session_state.transactions)
    if df.empty:
        return 0,0,0,0
    return df["gross"].sum(), df["net"].sum(), df["vat"].sum(), df["net"].sum()

st.markdown("""
<style>
.block-container {max-width: 1250px; padding-top: 2rem;}
.bookbot-title {font-size: 34px; font-weight: 800; margin-bottom: 0;}
.bookbot-sub {color:#64748b; margin-bottom:25px;}
.status {padding:5px 10px; border-radius:12px; font-weight:700;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# 🤖 Bookbot")
    st.caption("AI Boekhouden voor de eenmanszaak")
    page = st.radio("Navigatie", ["Dashboard", "Document uploaden", "Transacties", "Btw-overzicht", "Fiscale assistent"])
    st.divider()
    st.caption("V1 Prototype")
    st.info("AI-analyse is in deze demo gesimuleerd. Er worden geen echte aangiften ingediend.")

st.markdown('<div class="bookbot-title">Bookbot</div>', unsafe_allow_html=True)
st.markdown('<div class="bookbot-sub">Slimmer boekhouden. Eerst controleren, dan boeken.</div>', unsafe_allow_html=True)

if page == "Dashboard":
    gross, net, vat, profit = totals()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Omzet", euro(7500))
    c2.metric("Kosten", euro(net))
    c3.metric("Te betalen btw*", euro(vat))
    c4.metric("Winst indicatie", euro(7500-net))
    st.caption("*Prototypeberekening op basis van de huidige transacties; geen aangifteberekening.")

    st.subheader("Actie nodig")
    pending = [x for x in st.session_state.transactions if x["status"] != "Goedgekeurd"]
    if pending:
        for x in pending:
            st.warning(f"🟡 {x['supplier']} — {x['description']} — {euro(x['gross'])} — controle vereist")
    else:
        st.success("Alles is gecontroleerd.")

    st.subheader("Recente transacties")
    df = pd.DataFrame(st.session_state.transactions)
    st.dataframe(df[["id","date","supplier","description","gross","vat","account","status"]], use_container_width=True, hide_index=True)

    st.subheader("Bookbot AI-insight")
    st.info("Je softwarekosten zijn deze maand relatief hoog. Controleer of alle abonnementen zakelijk worden gebruikt en bewaar de bijbehorende facturen.")

elif page == "Document uploaden":
    st.header("📄 Document uploaden")
    st.write("Upload een factuur of bon. Bookbot maakt daarna een boekingsvoorstel.")
    uploaded = st.file_uploader("Upload PDF, JPG, JPEG of PNG", type=["pdf","jpg","jpeg","png"])

    if uploaded:
        st.success(f"Document ontvangen: **{uploaded.name}**")
        st.divider()
        st.subheader("🤖 AI-uitlezing")
        st.caption("Demo-analyse — echte OCR/API-koppeling volgt in de volgende versie.")

        col1,col2 = st.columns(2)
        with col1:
            supplier = st.text_input("Leverancier", "Adobe")
            invoice_date = st.date_input("Factuurdatum", date.today())
            invoice_number = st.text_input("Factuurnummer", "AD-2026-0914")
        with col2:
            gross = st.number_input("Totaal incl. btw", min_value=0.0, value=121.0, step=0.01)
            vat_rate = st.selectbox("Btw-tarief", ["21%", "9%", "0%", "Vrijgesteld"])
            confidence = st.slider("AI-confidence", 0, 100, 98)

        rate = {"21%":0.21, "9%":0.09, "0%":0.0, "Vrijgesteld":0.0}[vat_rate]
        vat = gross * rate / (1+rate) if rate else 0
        net = gross-vat

        st.subheader("📚 Boekingsvoorstel")
        account = st.selectbox("Grootboekrekening", ["Softwarekosten","Kantoorkosten","Reiskosten","Marketingkosten","Overige bedrijfskosten"])
        st.write(f"**Debet:** {account} — {euro(net)}")
        st.write(f"**Debet:** Te vorderen btw — {euro(vat)}")
        st.write(f"**Credit:** Crediteuren — {euro(gross)}")

        if confidence >= 95:
            st.success("🟢 Hoge zekerheid — klaar voor goedkeuring")
        elif confidence >= 80:
            st.warning("🟡 Middelmatige zekerheid — controle aanbevolen")
        else:
            st.error("🔴 Lage zekerheid — handmatige controle vereist")

        if st.button("✅ Boeking goedkeuren", type="primary"):
            new_id = f"{len(st.session_state.transactions)+1:06d}"
            st.session_state.transactions.append({
                "id":new_id,
                "date":invoice_date.strftime("%d-%m-%Y"),
                "supplier":supplier,
                "description":uploaded.name,
                "net":round(net,2),
                "vat":round(vat,2),
                "gross":round(gross,2),
                "vat_rate":vat_rate,
                "account":account,
                "status":"Goedgekeurd"
            })
            st.success(f"Boeking #{new_id} is opgeslagen.")
            st.balloons()

elif page == "Transacties":
    st.header("🧾 Transacties")
    df = pd.DataFrame(st.session_state.transactions)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("Boeking controleren")
    ids = [x["id"] for x in st.session_state.transactions]
    selected = st.selectbox("Selecteer boeking", ids)
    item = next(x for x in st.session_state.transactions if x["id"] == selected)
    st.write(f"**{item['supplier']} — {item['description']}**")
    st.write(f"Bedrag: **{euro(item['gross'])}** · btw: **{euro(item['vat'])}** · rekening: **{item['account']}**")
    if item["status"] != "Goedgekeurd":
        if st.button("Goedkeuren", type="primary"):
            item["status"] = "Goedgekeurd"
            st.success("Boeking goedgekeurd.")
            st.rerun()
    else:
        st.success("🟢 Deze boeking is goedgekeurd.")

elif page == "Btw-overzicht":
    st.header("🧮 Btw-overzicht")
    df = pd.DataFrame(st.session_state.transactions)
    output_vat = 0.0
    input_vat = df["vat"].sum() if not df.empty else 0
    st.metric("Voorbelasting uit huidige transacties", euro(input_vat))
    st.metric("Uitgaande btw", euro(output_vat))
    st.metric("Indicatief saldo", euro(output_vat-input_vat))
    st.warning("Dit is alleen een prototype-overzicht. Het vervangt geen officiële btw-aangifte.")

elif page == "Fiscale assistent":
    st.header("💬 Fiscale assistent")
    st.write("Vraag iets over je administratie. In V1 gebruikt deze demo de transacties die in Bookbot staan.")
    question = st.chat_input("Bijvoorbeeld: hoeveel btw heb ik als voorbelasting?")
    if question:
        df = pd.DataFrame(st.session_state.transactions)
        input_vat = df["vat"].sum() if not df.empty else 0
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            q = question.lower()
            if "btw" in q and ("voorbelasting" in q or "aftrek" in q):
                st.write(f"Op basis van de huidige prototype-transacties staat er ongeveer **{euro(input_vat)}** aan btw geregistreerd als voorbelasting.")
            elif "kosten" in q:
                st.write(f"De huidige geregistreerde kosten bedragen ongeveer **{euro(df['net'].sum())}** exclusief btw.")
            elif "winst" in q:
                st.write(f"Bij een voorbeeldomzet van € 7.500 en de huidige kosten is de indicatieve winst ongeveer **{euro(7500-df['net'].sum())}**.")
            else:
                st.write("In deze V1-demo kan ik vooral vragen over de huidige transacties beantwoorden. In de volgende versie koppelen we een echte AI-assistent aan de administratie.")
