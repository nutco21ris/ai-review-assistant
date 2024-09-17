import streamlit as st
import logging
from assistant.app import main


logging.getLogger("streamlit").setLevel(logging.ERROR)
if __name__ == "__main__":
    main()