import json
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components


def init_page_styles() -> None:
    st.markdown(
        """
        <style>
        /* Headings */
        h3 {
            font-size: 20px !important;
            font-weight: 600;
        }

        /* Primary button styling */
        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #000091 !important;
            color: white !important;
            border: none !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            background-color: #1212FF !important;
        }

        /* Custom link button styling */
        .custom-button {
            background-color: transparent;
            color: #000091;
            border: 2px solid #000091;
            padding: 12px 28px;
            font-size: 20px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            text-align: center;
            text-decoration: none;
            display: inline-block;
        }
        .custom-button:hover {
            background-color: #000091;
            color: white;
            border-color: #000091;
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def info_banner(text: str) -> None:
    st.markdown(
        f"""
        <div style="
            background-color:#E3ECFF;
            color:#000091;
            border:1px solid #B5C7F9;
            padding:18px;
            border-radius:7px;
            margin-bottom:24px;
            ">
            <span style="font-size:20px; font-weight:normal;">
                {text}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def copy_to_clipboard_button(text_to_copy: str, button_id: str = "copy_btn", height: int = 60) -> None:
    safe_text = json.dumps(text_to_copy)
    html = f"""
        <button
            id="{button_id}"
            onclick="copyToClipboard(this)"
            style="
                background-color:#4CAF50;
                color:white;
                border:none;
                padding:8px 16px;
                border-radius:8px;
                cursor:pointer;
                margin-top:1rem;
                width:100%;
            ">
            📋 Copy to clipboard
        </button>
        <script>
        function copyToClipboard(button) {{
            const originalText = button.innerHTML;
            const text = {safe_text};
            navigator.clipboard.writeText(text).then(() => {{
                button.innerHTML = "✅ Copied!";
                setTimeout(() => {{
                    button.innerHTML = originalText;
                }}, 3000);
            }}).catch(err => {{
                console.error('Failed to copy: ', err);
                button.innerHTML = "❌ Failed to copy";
                setTimeout(() => {{
                    button.innerHTML = originalText;
                }}, 3000);
            }});
        }}
        </script>
    """
    components.html(html, height=height)


def validation_status_indicator(is_valid: bool, error_msg: Optional[str] = None) -> None:
    if is_valid:
        st.markdown(
            """
            <div style="
                background-color:#d4f6dd;
                border:1px solid #7ac89b;
                padding:4px 6px;
                border-radius:4px;
                display:inline-block;
                margin-top:4px;
            ">
                <span style="font-size:12px;">✅ Valid API key</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="
                background-color:#ffd6d6;
                border:1px solid:#ff9b9b;
                padding:4px 6px;
                border-radius:4px;
                display:inline-block;
                margin-top:4px;
            ">
                <span style="font-size:12px;">❌ {error_msg or "Invalid API key"}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
