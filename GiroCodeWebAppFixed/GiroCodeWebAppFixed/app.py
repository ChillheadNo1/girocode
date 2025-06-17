
import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

def erstelle_girocode(name, iban, betrag, zweck, bic=""):
    # Korrektes Format sicherstellen
    try:
        betrag = f"EUR{float(betrag):.2f}" if betrag else ""
    except:
        st.error("Ungültiger Betrag")
        return None

    name = name.strip()[:70]
    iban = iban.replace(" ", "")
    bic = bic.strip()
    zweck = zweck.strip()[:140]

    # Muss genau 9 Zeilen enthalten
    data_lines = [
        "BCD",              # 1: Service Tag
        "001",              # 2: Version
        "1",                # 3: Charset (1 = UTF-8)
        "SCT",              # 4: SEPA Credit Transfer
        bic,                # 5: BIC (optional, aber muss leerer String sein, keine Zeile auslassen)
        iban,               # 6: IBAN
        name,               # 7: Empfängername
        betrag,             # 8: Betrag im Format EUR123.45
        zweck               # 9: Verwendungszweck
    ]
    girocode_text = "\n".join(data_lines)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(girocode_text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

st.title("💸 GiroCode Generator (konform)")

name = st.text_input("Empfängername", "Max Mustermann")
iban = st.text_input("IBAN", "DE89370400440532013000")
betrag = st.text_input("Betrag in EUR", "123.45")
zweck = st.text_input("Verwendungszweck", "Miete Mai 2025")
bic = st.text_input("BIC (optional)")

if st.button("GiroCode erzeugen"):
    buf = erstelle_girocode(name, iban, betrag, zweck, bic)
    if buf:
        st.image(buf)
        st.download_button("📥 QR-Code herunterladen", buf.getvalue(), "girocode.png", "image/png")
