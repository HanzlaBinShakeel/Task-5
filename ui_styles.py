"""Modern UI styles for wellness Streamlit app."""

WELLNESS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background: linear-gradient(160deg, #faf5ff 0%, #f3e8ff 25%, #ecfdf5 70%, #f0fdf4 100%);
}

.hero-banner {
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 40%, #6366f1 100%);
    border-radius: 24px;
    padding: 2.2rem 2.4rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 24px 48px -12px rgba(124, 58, 237, 0.4);
    color: white;
}
.hero-banner h1 {
    color: white !important;
    font-size: 2.1rem !important;
    font-weight: 700 !important;
    margin: 0 0 0.5rem 0 !important;
}
.hero-banner p {
    color: rgba(255,255,255,0.94) !important;
    font-size: 1.05rem !important;
    margin: 0 !important;
    line-height: 1.5 !important;
}

.disclaimer-box {
    background: linear-gradient(90deg, #fdf4ff, #f0fdf4);
    border: 1px solid #e9d5ff;
    border-radius: 14px;
    padding: 1rem 1.25rem;
    margin: 1rem 0 1.5rem 0;
    font-size: 0.88rem;
    color: #5b21b6;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #faf5ff 100%);
    border-right: 1px solid #ede9fe;
}

motion-stat {
    display: block;
    background: white;
    border-radius: 14px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
    border: 1px solid #ede9fe;
    box-shadow: 0 2px 10px rgba(124, 58, 237, 0.06);
}
motion-stat strong { color: #7c3aed; font-size: 1.1rem; }
motion-stat span { color: #6b7280; font-size: 0.8rem; }

motion-pill {
    display: inline-block;
    background: #f5f3ff;
    color: #6d28d9;
    border-radius: 999px;
    padding: 0.35rem 0.85rem;
    margin: 0.2rem;
    font-size: 0.82rem;
    border: 1px solid #ddd6fe;
}

motion-pills { margin: 0.5rem 0 1rem 0; }

motion-pills-wrap { line-height: 2.2; }

motion-pills-wrap motion-pill { white-space: nowrap; }

div[data-testid="stChatMessage"] {
    background: white;
    border-radius: 18px;
    border: 1px solid #f3e8ff;
    box-shadow: 0 4px 16px rgba(124, 58, 237, 0.06);
}

#MainMenu, footer, header { visibility: hidden; }
</style>
"""
