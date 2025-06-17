
import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

def erstelle_girocode(name, iban, betrag, zweck, bic=""):
    try:
        betrag = f"EUR{float(betrag):.2f}" if betrag else ""
    except:
        st.error("Ungültiger Betrag")
        return None

    daten = "\n".join(["BCD","001","1","SCT",bic, iban.replace(" ",""), name[:70], betrag, zweck[:140]])
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(daten)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

st.title("💸 GiroCode Generator")

name = st.text_input("Empfängername", "Max Mustermann")
iban = st.text_input("IBAN", "DE89370400440532013000")
betrag = st.text_input("Betrag in EUR", "123.45")
zweck = st.text_input("Verwendungszweck", "Rechnung")
bic = st.text_input("BIC (optional)")

if st.button("GiroCode erzeugen"):
    buf = erstelle_girocode(name, iban, betrag, zweck, bic)
    if buf:
        st.image(buf)
        st.download_button("📥 QR-Code herunterladen", buf.getvalue(), "girocode.png", "image/png")
