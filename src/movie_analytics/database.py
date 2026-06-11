import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_engine():

    db_url = os.getenv('DATABASE_URL') or st.secrets["DATABASE_URL"]

    if not db_url:
        raise ValueError("DATABASE_URL is not set in environment variables")
    
    return create_engine(db_url)