import streamlit as st
from html import escape

# Section title
def ui_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


# Tooltip and status block
def ui_metric(label, value, tooltip=None, color="#fff", warning=None, warning_color=None):

    # Tooltip biztonságos, nem törik meg HTML-t
    if tooltip:
        safe_tooltip = escape(tooltip).replace("\n", "&#10;")
        tip = (
            f'<span class="tooltip">ⓘ'
            f'<span class="tooltiptext">{safe_tooltip}</span>'
            f'</span>'
        )
    else:
        tip = ""

    warning_html = (
        f"<div class='metric-warning' style='color:{warning_color or color};'>{warning}</div>"
        if warning else ""
    )

    html = f"""
        <div class="metric-block">
            <div class="metric-label">{label} {tip}</div>
            <div class="metric-value" style="color:{color};">{value}</div>
            {warning_html}
        </div>
    """

    st.markdown(html, unsafe_allow_html=True)