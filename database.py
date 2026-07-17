import streamlit as st
from sqlalchemy import create_engine

@st.cache_resource
def get_engine():
    return create_engine(
        f"postgresql+psycopg2://"
        f"postgres.tmwslhqirwpcbajuebsp:"
        f"{st.secrets['DB_PASSWORD']}"
        "@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres"
    )