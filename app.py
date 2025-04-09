# ✅ Debe ser la primera instrucción
import streamlit as st
st.set_page_config(page_title="Aplicación Financiera", layout="wide")

# 📦 Librerías
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from deep_translator import GoogleTranslator

# 🎨 Estilo personalizado
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        h1, h2, h3, h4 {
            color: #003366;
        }
        .stApp {
            font-family: 'Segoe UI', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Análisis Financiero de Empresas (Yahoo Finance)")

# 🔎 Función para obtener info de empresa
def get_company_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        company_name = info.get("longName", "Nombre no disponible")
        sector = info.get("sector", "Sector no disponible")
        description = info.get("longBusinessSummary", "Descripción no disponible.")
        # Traducir al español
        try:
            description = GoogleTranslator(source='auto', target='es').translate(description)
        except:
            pass
        return company_name, sector, description
    except Exception as e:
        return None, None, f"Error al obtener datos: {str(e)}"

# 📉 Función para obtener precios históricos
def get_historical_prices(symbol, years):
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=years * 365)
        stock = yf.Ticker(symbol)
        hist = stock.history(start=start_date, end=end_date)
        return hist[['Close']]
    except Exception as e:
        return None

# 📈 CAGR
def calculate_cagr(prices, years):
    if prices is None or prices.empty:
        return None
    start_price = prices.iloc[0]['Close']
    end_price = prices.iloc[-1]['Close']
    cagr = ((end_price / start_price) ** (1 / years) - 1) * 100
    return round(cagr, 2)

# 📊 Volatilidad
def calculate_volatility(prices):
    if prices is None or prices.empty:
        return None
    returns = prices['Close'].pct_change().dropna()
    volatility = np.std(returns) * np.sqrt(252) * 100
    return round(volatility, 2)

# 🧭 Sidebar
ticker = st.sidebar.text_input("🔍 Ingrese el símbolo (Ej: AAPL, TSLA, MSFT)", "")

if ticker:
    company_name, sector, description = get_company_info(ticker)
    if company_name:
        st.subheader(f"📌 {company_name}")
        st.write(f"**Sector:** {sector}")
        st.markdown(f"📝 {description}")

        # Precios históricos
        prices_1y = get_historical_prices(ticker, 1)
        prices_3y = get_historical_prices(ticker, 3)
        prices_5y = get_historical_prices(ticker, 5)

        # 📈 Gráfica de precios simple
        st.subheader("📈 Precio Histórico (últimos 5 años)")
        if isinstance(prices_5y, pd.DataFrame):
            st.line_chart(prices_5y['Close'], use_container_width=True)

        # 📊 CAGR
        cagr_1y = calculate_cagr(prices_1y, 1)
        cagr_3y = calculate_cagr(prices_3y, 3)
        cagr_5y = calculate_cagr(prices_5y, 5)

        st.subheader("📊 Rendimientos Anualizados (CAGR)")
        df_cagr = pd.DataFrame({
            "Periodo": ["1 Año", "3 Años", "5 Años"],
            "CAGR (%)": [cagr_1y, cagr_3y, cagr_5y]
        })
        st.dataframe(df_cagr, hide_index=True)

        st.markdown("""
        > *📌 El rendimiento anualizado (CAGR) se calcula como:*  
        `((Precio Final / Precio Inicial) ^ (1 / Años)) - 1`
        """)

        # 🎯 Volatilidad
        volatility = calculate_volatility(prices_5y)
        st.subheader("📌 Volatilidad Anualizada")
        st.write(f"**Riesgo estimado:** {volatility}%")
        st.markdown("""
        > *La volatilidad mide la variabilidad de los rendimientos diarios y se expresa como desviación estándar anualizada.*
        """)
    else:
        st.error("❌ No se pudo obtener información. Verifique el símbolo ingresado.")



