import os
from dotenv import load_dotenv
import streamlit as st
import requests


load_dotenv()


import streamlit as st
import requests


API_KEY = st.secrets["API_KEY"]
API_BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/"
LATEST_RATES_URL = API_BASE_URL + "latest/"
SUPPORTED_CODES_URL = API_BASE_URL + "codes"

# Your existing code here...


CURRENCY_EMOJIS = {
    "USD": "🇺🇸", "EUR": "🇪🇺", "INR": "🇮🇳", "JPY": "🇯🇵",
    "GBP": "🇬🇧", "AUD": "🇦🇺", "CAD": "🇨🇦", "CHF": "🇨🇭",
    "CNY": "🇨🇳", "SGD": "🇸🇬", "NZD": "🇳🇿", "AED": "🇦🇪",
}


@st.cache_data(ttl=86400)
def get_supported_currencies():
    try:
        response = requests.get(SUPPORTED_CODES_URL)
        response.raise_for_status()
        data = response.json()
        if data.get("result") == "success":
            return data.get("supported_codes")
    except Exception as e:
        st.error(f"Failed to fetch currencies: {e}")
    return None

def get_latest_rates(base_currency):
    try:
        response = requests.get(f"{LATEST_RATES_URL}{base_currency}")
        response.raise_for_status()
        data = response.json()
        if data.get("result") == "success":
            return data.get("conversion_rates"), data.get("time_last_update_utc")
    except Exception as e:
        st.error(f"Failed to fetch rates: {e}")
    return None, None


st.set_page_config(page_title="Currency Converter 💸", layout="centered", page_icon="💸")


st.markdown("""
<style>
html, body {
    background: linear-gradient(135deg, #121212, #191414);
    color: #1DB954;
    font-family: 'Poppins', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #121212, #191414);
}
h1, h2, h3, h4 {
    color: #1DB954;
    text-align: center;
    font-size: 30px; /* Reduced font size */
}
input, select {
    background-color: #2a2a2a !important;
    color: #1DB954 !important;
    border: none !important;
    font-size: 22px; /* Increased font size for inputs */
    padding: 10px; /* Padding to make input fields more comfortable */
}
.glass-box {
    backdrop-filter: blur(15px);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 2rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    text-align: center;
    transition: all 0.3s ease-in-out;
}
.glass-box:hover {
    transform: scale(1.02);
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
}
.stButton>button {
    background-color: #1DB954;
    color: black;
    font-weight: bold;
    border-radius: 30px;
    padding: 1rem 3rem;
    border: none;
    box-shadow: 0 0 20px #1DB954, 0 0 40px #1DB954;
    transition: all 0.3s ease;
    font-size: 24px;  /* Adjusted font size for the button */
    display: block;
    margin-left: auto;
    margin-right: auto;
}
.stButton>button:hover {
    background-color: #1ed760;
    box-shadow: 0 0 25px #1ed760, 0 0 50px #1ed760;
}
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
.stButton>button {
    animation: pulse 2s ease-in-out infinite;
}
body {
    background: url('https://www.transparenttextures.com/patterns/hex-grid.png') repeat;
    background-size: 100px 100px;
}
footer {
    text-align: center;
    font-size: 14px;
    margin-top: 2rem;
    color: #1DB954;
}
footer a {
    color: #1DB954;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# Title and UI
st.title("Currency Converter 💸")

supported = get_supported_currencies()

if supported:
    currencies = {code: name for code, name in supported}

    # User input
    col1, col2 = st.columns(2)
    with col1:
        from_currency = st.selectbox(
            "From",
            options=list(currencies.keys()),
            format_func=lambda x: f"{CURRENCY_EMOJIS.get(x, '')} {x} - {currencies[x]}"
        )
    with col2:
        to_currency = st.selectbox(
            "To",
            options=list(currencies.keys()),
            format_func=lambda x: f"{CURRENCY_EMOJIS.get(x, '')} {x} - {currencies[x]}"
        )

    amount = st.number_input("Amount", min_value=0, value=1, step=1, label_visibility="collapsed")

    # Center Convert Button
    if st.button("Convert 💱", key="convert_button"):
        rates, last_updated = get_latest_rates(from_currency)

        if rates and to_currency in rates:
            converted_amount = amount * rates[to_currency]
            st.markdown(f"""
            <div class='glass-box'>
                <h2>{amount:.2f} {from_currency} → {converted_amount:.2f} {to_currency}</h2>
                <small>Last updated: {last_updated}</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Something went wrong. Please try again.")
else:
    st.error("Could not load currency list. Please try again later.")


st.markdown("""
<footer>
    Powered by <a href="https://www.exchangerate-api.com/">ExchangeRate-API</a>  |  Designed by Hardik with ❤️
</footer>
""", unsafe_allow_html=True)
