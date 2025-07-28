import streamlit as st
import time
import base64
from datetime import datetime
from pathlib import Path
from io import BytesIO
from cv_optimizer import CVOptimizer  # Import the CVOptimizer class
from jd_keyword_extractor import extract_jd_keywords
# ================================
# 🎨 MODERN PROFESSIONAL STYLING
# ================================
def load_modern_css():
    """Load modern, professional CSS styling with beautiful color grading and typography"""
    st.markdown("""
    <style>
        /* Import Beautiful Modern Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
        
        /* CSS Variables - Beautiful Dark Theme Color System */
        :root {
            --primary: #6366f1;
            --primary-light: #818cf8;
            --primary-dark: #4f46e5;
            --primary-glow: rgba(99, 102, 241, 0.3);
            
            --secondary: #06b6d4;
            --secondary-light: #22d3ee;
            --secondary-dark: #0891b2;
            
            --accent: #f59e0b;
            --accent-light: #fbbf24;
            --accent-dark: #d97706;
            
            --success: #10b981;
            --success-light: #34d399;
            --success-dark: #059669;
            --success-glow: rgba(16, 185, 129, 0.3);
            
            --warning: #f59e0b;
            --warning-light: #fbbf24;
            --warning-glow: rgba(245, 158, 11, 0.3);
            
            --danger: #ef4444;
            --danger-light: #f87171;
            --info: #3b82f6;
            
            /* Dark Theme Neutrals */
            --neutral-50: #0a0a0a;
            --neutral-100: #171717;
            --neutral-200: #262626;
            --neutral-300: #404040;
            --neutral-400: #525252;
            --neutral-500: #737373;
            --neutral-600: #a3a3a3;
            --neutral-700: #d4d4d4;
            --neutral-800: #e5e5e5;
            --neutral-900: #f5f5f5;
            
            /* Dark Background System */
            --bg-primary: #111111;
            --bg-secondary: #1a1a1a;
            --bg-tertiary: #262626;
            --bg-elevated: #1f1f1f;
            --bg-overlay: rgba(17, 17, 17, 0.95);
            
            /* Dark Theme Text Colors */
            --text-primary: #ffffff;
            --text-secondary: #d4d4d4;
            --text-tertiary: #a3a3a3;
            --text-quaternary: #525252;
            --text-inverse: #000000;
            
            /* Dark Theme Borders */
            --border-light: #262626;
            --border-primary: #404040;
            --border-secondary: #525252;
            --border-focus: var(--primary);
            
            /* Enhanced Shadows for Dark Theme */
            --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.8);
            --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.8), 0 1px 2px -1px rgb(0 0 0 / 0.8);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.8), 0 2px 4px -2px rgb(0 0 0 / 0.8);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.8), 0 4px 6px -4px rgb(0 0 0 / 0.8);
            --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.8), 0 8px 10px -6px rgb(0 0 0 / 0.8);
            --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.9);
            --shadow-colored: 0 8px 32px var(--primary-glow);
            
            /* Premium Typography */
            --font-body: 'Outfit', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            --font-heading: 'Space Grotesk', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
            
            /* Modern Spacing Scale */
            --space-1: 0.25rem;
            --space-2: 0.5rem;
            --space-3: 0.75rem;
            --space-4: 1rem;
            --space-5: 1.25rem;
            --space-6: 1.5rem;
            --space-8: 2rem;
            --space-10: 2.5rem;
            --space-12: 3rem;
            --space-16: 4rem;
            --space-20: 5rem;
            
            /* Border Radius Scale */
            --radius-sm: 0.375rem;
            --radius-md: 0.5rem;
            --radius-lg: 0.75rem;
            --radius-xl: 1rem;
            --radius-2xl: 1.5rem;
            --radius-full: 9999px;
        }

        /* Navigation Specific Styles */
        .nav-container {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-elevated) 100%);
            padding: var(--space-6) var(--space-8);
            border-radius: var(--radius-2xl);
            border: 1px solid var(--border-light);
            box-shadow: var(--shadow-lg);
            margin: var(--space-8) var(--space-8) var(--space-12) var(--space-8);
            position: sticky;
            top: var(--space-4);
            z-index: 1000;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        
        .nav-title {
            font-family: var(--font-heading);
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            text-align: center;
            margin-bottom: var(--space-6);
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        /* Enhanced Navigation Button Styles */
        .nav-button-container {
            display: flex;
            justify-content: center;
            gap: var(--space-3);
            flex-wrap: wrap;
        }

        /* Override Streamlit button styles for navigation */
        .nav-button-container .stButton > button {
            background: var(--bg-tertiary) !important;
            color: var(--text-secondary) !important;
            border: 1px solid var(--border-primary) !important;
            border-radius: var(--radius-lg) !important;
            padding: var(--space-4) var(--space-6) !important;
            font-family: var(--font-body) !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: var(--shadow-sm) !important;
            position: relative !important;
            overflow: hidden !important;
            min-width: 100px !important;
            text-transform: capitalize !important;
        }

        .nav-button-container .stButton > button:hover {
            background: var(--bg-elevated) !important;
            color: var(--text-primary) !important;
            border-color: var(--primary) !important;
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-md), 0 0 20px var(--primary-glow) !important;
        }

        .nav-button-container .stButton > button:focus {
            outline: none !important;
            box-shadow: var(--shadow-md), 0 0 0 3px var(--primary-glow) !important;
        }

        /* Active navigation button style */
        .nav-button-active .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
            color: white !important;
            border-color: var(--primary) !important;
            box-shadow: var(--shadow-md), 0 0 20px var(--primary-glow) !important;
            font-weight: 600 !important;
        }

        .nav-button-active .stButton > button:hover {
            background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%) !important;
            color: white !important;
        }

        /* Global Styling */
        .main .block-container {
            padding-top: 0;
            padding-bottom: var(--space-8);
            max-width: 1200px;
        }
        .stApp {
            background: #000000;
            min-height: 100vh;
        }
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Beautiful Typography System */
        html, body, [class*="css"] {
            font-family: var(--font-body);
            font-weight: 400;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-heading) !important;
            font-weight: 600 !important;
            line-height: 1.2 !important;
            letter-spacing: -0.025em !important;
            color: var(--text-primary) !important;
        }
        h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
        h2 { font-size: 2rem !important; font-weight: 700 !important; }
        h3 { font-size: 1.5rem !important; font-weight: 600 !important; }
        h4 { font-size: 1.25rem !important; font-weight: 600 !important; }
        p, span, div {
            color: var(--text-secondary);
        }
        /* Premium Header Section */
        .app-header {
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-elevated) 100%);
            padding: var(--space-10) var(--space-8);
            border-radius: var(--radius-2xl);
            box-shadow: var(--shadow-xl), 0 0 0 1px var(--border-light);
            border: 1px solid var(--border-light);
            margin: var(--space-8) var(--space-8) var(--space-12) var(--space-8);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .app-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, var(--primary) 50%, transparent 100%);
        }
        .app-title {
            font-family: var(--font-heading);
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: var(--space-4);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: var(--space-4);
            letter-spacing: -0.05em;
        }
        .app-subtitle {
            font-size: 1.25rem;
            font-weight: 500;
            color: var(--text-secondary);
            margin-bottom: var(--space-8);
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.7;
        }
        .trust-indicators {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: var(--space-8);
            flex-wrap: wrap;
            margin-top: var(--space-6);
        }
        .trust-item {
            display: flex;
            align-items: center;
            gap: var(--space-3);
            color: var(--text-tertiary);
            font-size: 0.875rem;
            font-weight: 500;
            padding: var(--space-3) var(--space-4);
            background: var(--bg-secondary);
            border-radius: var(--radius-full);
            border: 1px solid var(--border-light);
            transition: all 0.2s ease;
        }
        .trust-item:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
            border-color: var(--primary);
            color: var(--text-secondary);
        }
        /* Sticky Progress Section */
        .progress-container {
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-elevated) 100%);
            border-radius: var(--radius-xl);
            padding: var(--space-8);
            border: 1px solid var(--border-light);
            box-shadow: var(--shadow-lg);
            margin-bottom: var(--space-10);
            position: sticky;
            top: var(--space-4);
            z-index: 100;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            overflow: hidden;
        }
        .progress-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: var(--space-5);
        }
        .progress-title {
            font-family: var(--font-heading);
            font-size: 1.375rem;
            font-weight: 600;
            color: var(--text-primary);
        }
        .progress-percentage {
            font-size: 1rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .progress-bar {
            width: 100%;
            height: 12px;
            background: var(--neutral-200);
            border-radius: var(--radius-full);
            overflow: hidden;
            margin-bottom: var(--space-6);
            position: relative;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
            border-radius: var(--radius-full);
            transition: width 0.8s ease;
            position: relative;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
        }
        .progress-steps {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: var(--space-4);
        }
        .progress-step {
            display: flex;
            align-items: center;
            gap: var(--space-4);
            padding: var(--space-4);
            border-radius: var(--radius-lg);
            background: var(--bg-secondary);
            transition: all 0.3s ease;
            border: 1px solid var(--border-light);
        }
        .progress-step.completed {
            background: linear-gradient(135deg, var(--success-glow), var(--bg-secondary));
            border-color: var(--success);
            box-shadow: 0 4px 12px var(--success-glow);
        }
        .step-status {
            width: 28px;
            height: 28px;
            border-radius: var(--radius-full);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8125rem;
            font-weight: 700;
            flex-shrink: 0;
            transition: all 0.3s ease;
        }
        .step-status.pending {
            background: var(--neutral-300);
            color: var(--neutral-600);
        }
        .step-status.completed {
            background: linear-gradient(135deg, var(--success) 0%, var(--success-light) 100%);
            color: white;
            box-shadow: 0 4px 12px var(--success-glow);
        }
        .step-label {
            font-size: 0.9375rem;
            font-weight: 500;
            color: var(--text-primary);
        }
        /* Premium Section Cards */
        .section-card {
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-elevated) 100%);
            border-radius: var(--radius-2xl);
            border: 1px solid var(--border-light);
            box-shadow: var(--shadow-lg);
            overflow: hidden;
            margin-bottom: var(--space-10);
            transition: all 0.3s ease;
        }
        .section-card:hover {
            box-shadow: var(--shadow-xl), var(--shadow-colored);
            transform: translateY(-2px);
        }
        .section-header {
            padding: var(--space-8) var(--space-8);
            border-bottom: 1px solid var(--border-light);
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--neutral-100) 100%);
            position: relative;
        }
        .section-title {
            font-family: var(--font-heading);
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: var(--space-3);
            display: flex;
            align-items: center;
            gap: var(--space-3);
        }
        .section-subtitle {
            color: var(--text-secondary);
            font-size: 1rem;
            font-weight: 400;
            line-height: 1.6;
        }
        .section-content {
            padding: var(--space-8);
        }
        /* Beautiful Status Messages */
        .status-message {
            padding: var(--space-5) var(--space-6);
            border-radius: var(--radius-lg);
            margin: var(--space-5) 0;
            display: flex;
            align-items: flex-start;
            gap: var(--space-4);
            font-size: 0.9375rem;
            line-height: 1.6;
            font-weight: 500;
            border: 1px solid;
            position: relative;
            overflow: hidden;
        }
        .status-success {
            background: linear-gradient(135deg, var(--success-glow), rgba(16, 185, 129, 0.1));
            border-color: rgba(16, 185, 129, 0.5);
            color: var(--success-light);
        }
        .status-warning {
            background: linear-gradient(135deg, var(--warning-glow), rgba(245, 158, 11, 0.1));
            border-color: rgba(245, 158, 11, 0.5);
            color: var(--accent-light);
        }
        .status-info {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(59, 130, 246, 0.1));
            border-color: rgba(59, 130, 246, 0.5);
            color: #93c5fd;
        }
        /* Enhanced Streamlit Components */
        .stFileUploader > div {
            border: 2px dashed var(--border-primary);
            border-radius: var(--radius-xl);
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--neutral-100) 100%);
            padding: var(--space-10);
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .stFileUploader > div:hover {
            border-color: var(--primary);
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, var(--bg-secondary) 100%);
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        .stTextArea > div > div > textarea {
            border: 1px solid var(--border-primary) !important;
            border-radius: var(--radius-lg) !important;
            font-family: var(--font-body) !important;
            font-size: 0.9375rem !important;
            background: var(--bg-primary) !important;
            transition: all 0.3s ease !important;
            padding: var(--space-5) !important;
            line-height: 1.6 !important;
            color: var(--text-primary) !important;
            resize: vertical !important;
        }
        .stTextArea > div > div > textarea:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 4px var(--primary-glow) !important;
            outline: none !important;
        }
        .stTextArea > div > div > textarea::placeholder {
            color: var(--text-tertiary) !important;
            font-style: italic !important;
        }
        /* Premium Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-lg) !important;
            padding: var(--space-4) var(--space-6) !important;
            font-family: var(--font-body) !important;
            font-size: 0.9375rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: var(--shadow-md), 0 0 20px var(--primary-glow) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-lg), 0 0 30px var(--primary-glow) !important;
        }
        .stButton > button:focus {
            outline: none !important;
            box-shadow: var(--shadow-lg), 0 0 0 4px var(--primary-glow) !important;
        }
        .stButton > button:disabled {
            background: var(--neutral-300) !important;
            color: var(--neutral-500) !important;
            transform: none !important;
            box-shadow: none !important;
            cursor: not-allowed !important;
        }
        /* Word Count */
        .word-count {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 0.5rem;
            padding: 0.5rem 0;
            font-size: 0.875rem;
            color: var(--text-tertiary);
        }
        .count-status {
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .count-good {
            background: rgba(5, 150, 105, 0.1);
            color: var(--success);
        }
        .count-warning {
            background: rgba(217, 119, 6, 0.1);
            color: var(--warning);
        }
        /* Requirements List */
        .requirements-list {
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
            margin-top: 1rem;
            font-size: 0.875rem;
            color: var(--text-tertiary);
        }
        .requirement-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        /* Responsive Design */
        @media (max-width: 768px) {
            .app-title {
                font-size: 2rem;
            }
            
            .trust-indicators {
                gap: 1rem;
            }
            
            .requirements-list {
                gap: 1rem;
            }
            
            .progress-steps {
                grid-template-columns: 1fr;
            }

            .nav-button-container {
                gap: var(--space-2);
            }

            .nav-button-container .stButton > button {
                font-size: 0.75rem !important;
                padding: var(--space-3) var(--space-4) !important;
                min-width: 80px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ================================
# 🔧 SESSION STATE MANAGEMENT
# ================================
def render_top_navbar():
    """Render beautiful navigation bar with functional buttons"""
    nav_items = {
        'Home': '🏠',
        'About': '📘', 
        'Help': '❓',
        'Pricing': '💰',
        'My Account': '👤'
    }
    
    current_page = st.session_state.get('active_nav', 'Home')
    
    
    # Create columns for navigation buttons
    cols = st.columns(len(nav_items))
    
    for idx, (nav_item, icon) in enumerate(nav_items.items()):
        with cols[idx]:
            # Add custom CSS class for active button
            button_class = "nav-button-active" if current_page == nav_item else ""
            st.markdown(f'<div class="{button_class}">', unsafe_allow_html=True)
            
            if st.button(
                f"{icon} {nav_item}",
                key=f"nav_{nav_item.lower().replace(' ', '_')}",
                use_container_width=True,
                help=f"Navigate to {nav_item} page"
            ):
                st.session_state.active_nav = nav_item
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_progress_section():
    """Render real-time progress tracking"""
    # Track all 3 steps including file upload
    all_steps = [st.session_state.file_uploaded, st.session_state.job_description_added, st.session_state.template_selected]
    completed_steps = sum(all_steps)
    progress = int((completed_steps / len(all_steps)) * 100)
    
    # Step statuses for display
    step1_status = "completed" if st.session_state.file_uploaded else "pending"
    step2_status = "completed" if st.session_state.job_description_added else "pending"
    step3_status = "completed" if st.session_state.template_selected else "pending"
    
    step1_icon = "✓" if st.session_state.file_uploaded else "1"
    step2_icon = "✓" if st.session_state.job_description_added else "2"
    step3_icon = "✓" if st.session_state.template_selected else "3"
    
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-header">
            <div class="progress-title">Setup Progress</div>
            <div class="progress-percentage">{progress}% Complete</div>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%;"></div>
        </div>
        <div class="progress-steps">
            <div class="progress-step {step1_status}">
                <div class="step-status {step1_status}">{step1_icon}</div>
                <span class="step-label">Upload CV</span>
            </div>
            <div class="progress-step {step2_status}">
                <div class="step-status {step2_status}">{step2_icon}</div>
                <span class="step-label">Job Description</span>
            </div>
            <div class="progress-step {step3_status}">
                <div class="step-status {step3_status}">{step3_icon}</div>
                <span class="step-label">Template Selection</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state with error handling and validation"""
    try:
        # Navigation state
        if 'active_nav' not in st.session_state:
            st.session_state.active_nav = 'Home'
            
        # Core state variables
        if 'file_uploaded' not in st.session_state:
            st.session_state.file_uploaded = False
        if 'job_description_added' not in st.session_state:
            st.session_state.job_description_added = False
        if 'template_selected' not in st.session_state:
            st.session_state.template_selected = False  # Fixed: should start as False
        if 'selected_template' not in st.session_state:
            st.session_state.selected_template = 'professional'
        if 'uploaded_file_info' not in st.session_state:
            st.session_state.uploaded_file_info = None
        if 'job_description' not in st.session_state:
            st.session_state.job_description = ""
        if 'word_count' not in st.session_state:
            st.session_state.word_count = 0
        if 'optimization_complete' not in st.session_state:
            st.session_state.optimization_complete = False
        if 'processing_errors' not in st.session_state:
            st.session_state.processing_errors = []
        
        # CVOptimizer specific state
        if 'cv_text' not in st.session_state:
            st.session_state.cv_text = ""
        if 'template_config' not in st.session_state:
            st.session_state.template_config = {}
        if 'optimized_cv' not in st.session_state:
            st.session_state.optimized_cv = ""
        
        # Initialize optimizer
        if 'cv_optimizer' not in st.session_state:
            st.session_state.cv_optimizer = CVOptimizer()
            
        # Validate session state integrity
        if st.session_state.selected_template not in ['professional', 'modern', 'executive', 'creative']:
            st.session_state.selected_template = 'professional'
            
    except Exception as e:
        st.error(f"Error initializing application: {str(e)}")
        # Reset to defaults on error
        st.session_state.clear()
        initialize_session_state()

# ================================
# 🎨 UI COMPONENTS
# ================================
def render_header():
    """Render modern app header"""
    st.markdown("""
    <div class="app-header">
        <div class="app-title">
            ✂️ Tailor
        </div>
        <div class="app-subtitle">
            Professional CV optimization powered by AI - designed specifically for the UK job market and modern ATS systems
        </div>
        <div class="trust-indicators">
            <div class="trust-item">
                <span>✅ 95% ATS Pass Rate</span>
            </div>
            <div class="trust-item">
                <span>⚡ 30-Second Processing</span>
            </div>
            <div class="trust-item">
                <span>⭐ 50K+ CVs Optimized</span>
            </div>
            <div class="trust-item">
                <span>🔒 GDPR Compliant</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_upload_section():
    """Enhanced upload section with CV text extraction"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-title">
                📄 Step 1: Upload Your CV
            </div>
            <div class="section-subtitle">Upload your current CV to begin the optimization process</div>
        </div>
        <div class="section-content">
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your CV file",
        type=['pdf', 'docx', 'doc'],
        help="Upload your CV in PDF or Word format (maximum 10MB)",
        label_visibility="collapsed",
        key="cv_file_uploader"
    )
    
    if uploaded_file:
        # Validate the uploaded file
        is_valid, validation_message = validate_uploaded_file(uploaded_file)
        
        if is_valid:
            # Extract CV text using the optimizer
            optimizer = st.session_state.cv_optimizer
            success, extracted_text = optimizer.extract_cv_text(uploaded_file)
            
            if success:
                # Store in session state
                st.session_state.cv_text = extracted_text
                st.session_state.file_uploaded = True
                
                # Process file info
                file_info = get_file_info(uploaded_file)
                if file_info:
                    st.session_state.uploaded_file_info = file_info
                
                # Show enhanced success message
                st.markdown(f"""
                <div class="status-message status-success">
                    <span>✅</span>
                    <div>
                        <strong>{file_info['name'] if file_info else uploaded_file.name}</strong> uploaded and processed successfully
                        <br><small>Text extracted • {len(extracted_text.split())} words • Ready for optimization</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show extracted text preview
                with st.expander("📄 Preview Extracted Text"):
                    st.text_area(
                        "Extracted CV Content", 
                        value=extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text,
                        height=200,
                        disabled=True
                    )
                
            else:
                st.session_state.file_uploaded = False
                st.error(f"❌ Failed to extract text: {extracted_text}")
        else:
            # Show validation error
            st.session_state.file_uploaded = False
            st.error(f"❌ {validation_message}")
    else:
        # Reset file upload state when no file
        st.session_state.file_uploaded = False
        # Show requirements when no file is uploaded
        st.markdown("""
        <div class="requirements-list">
            <div class="requirement-item">
                <span>✅ PDF & Word (.docx) supported</span>
            </div>
            <div class="requirement-item">
                <span>✅ Maximum 10MB file size</span>
            </div>
            <div class="requirement-item">
                <span>✅ Secure processing & GDPR compliant</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    return uploaded_file

def render_job_description_section():
    """Enhanced job description section"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-title">
                🎯 Step 2: Target Job Description
            </div>
            <div class="section-subtitle">Paste the complete job posting to optimize your CV for this specific role</div>
        </div>
        <div class="section-content">
    """, unsafe_allow_html=True)
    
    job_description = st.text_area(
        "Job Description",
        height=200,
        placeholder="""Paste the complete job description here...
Include everything for best results:
• Job title and company information
• Key responsibilities and requirements
• Required skills and qualifications
• Experience level and preferred background
• Company culture and values""",
        help="Copy the entire job posting for best results",
        label_visibility="collapsed",
        key="job_description_input"
    )
    
    # Real-time word count and validation
    if job_description:
        # Use optimizer to set job description
        optimizer = st.session_state.cv_optimizer
        optimizer.set_job_description(job_description)
        
        words = len(job_description.split())
        st.session_state.job_description = job_description
        st.session_state.word_count = words
        
        if words >= 50:
            st.session_state.job_description_added = True
            status_class = "count-good"
            status_text = "Excellent!"
            message = "Perfect! Your job description provides excellent detail for optimization."
            message_type = "success"
        elif words >= 20:
            st.session_state.job_description_added = False
            status_class = "count-warning"
            status_text = f"Add {50 - words} more words"
            message = f"Good start! Add {50 - words} more words for optimal results."
            message_type = "info"
        else:
            st.session_state.job_description_added = False
            status_class = "count-warning"
            status_text = "Add more details"
            message = None
            message_type = None
        
        # Word count display
        st.markdown(f"""
        <div class="word-count">
            <span>{words} words</span>
            <span class="count-status {status_class}">{status_text}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Status message
        if message:
            status_icon = "✅" if message_type == 'success' else "ℹ️"
            
            st.markdown(f"""
            <div class="status-message status-{message_type}">
                <span>{status_icon}</span>
                <span>{message}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # JD Keyword Extraction - ADDED THIS SECTION
        if words >= 50:
            extract_jd_keywords_simple()
            
    else:
        # Reset job description state when empty
        st.session_state.job_description_added = False
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    return job_description

def extract_jd_keywords_simple():
    """Simple function to extract JD keywords and show results"""
    
    # Check if we have a job description
    if not st.session_state.job_description:
        st.error("No job description available")
        return
    
    # Show extract button
    if st.button("🔍 Extract Keywords from Job Description"):
        
        # Get API key
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        
        # Show processing
        with st.spinner("🤖 Extracting keywords..."):
            success, result = extract_jd_keywords(st.session_state.job_description, api_key)
        
        # Show results
        if success:
            st.success(f"✅ Keywords saved to: {result}")
            
            # Load and display the JSON
            import json
            try:
                with open(result, 'r') as f:
                    data = json.load(f)
                
                st.markdown("### 🎯 Extracted Keywords:")
                st.json(data)
                    
            except Exception as e:
                st.error(f"Error loading results: {e}")
        else:
            st.error(f"❌ Failed: {result}")

def render_template_section():
    """Enhanced template selection with YAML loading"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-title">
                🎨 Step 3: Choose Your Template
            </div>
            <div class="section-subtitle">Select a professional template that matches your industry and career level</div>
        </div>
        <div class="section-content">
    """, unsafe_allow_html=True)
    
    templates = {
        'professional': {
            'name': 'Professional', 
            'desc': 'Clean, corporate design perfect for traditional industries'
        },
        'modern': {
            'name': 'Modern', 
            'desc': 'Contemporary layout ideal for tech and startups'
        },
        'executive': {
            'name': 'Executive', 
            'desc': 'Sophisticated design for senior leadership positions'
        },
        'creative': {
            'name': 'Creative', 
            'desc': 'Visually striking format for design and media roles'
        }
    }
    
    # Template selection
    cols = st.columns(len(templates))
    for idx, (key, template) in enumerate(templates.items()):
        with cols[idx]:
            if st.button(
                f"{template['name']}",
                key=f"template_{key}",
                help=template['desc'],
                use_container_width=True
            ):
                # Load template configuration using optimizer
                optimizer = st.session_state.cv_optimizer
                success, message = optimizer.load_template_config(key)
                
                if success:
                    st.session_state.selected_template = key
                    st.session_state.template_selected = True
                    st.session_state.template_config = optimizer.template_config
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
    
    # Show selected template info
    if st.session_state.get('template_selected'):
        selected = templates[st.session_state.selected_template]
        st.markdown(f"""
        <div class="status-message status-info" style="margin-top: 1rem;">
            <span>🎨</span>
            <span><strong>{selected['name']} Template Selected:</strong> {selected['desc']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_optimization_section():
    """Render optimization action section"""
    # Still need file upload, job description, and template for optimization
    all_ready = (st.session_state.file_uploaded and 
                st.session_state.job_description_added and 
                st.session_state.template_selected)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if all_ready:
            if st.button(
                "🚀 Optimize My CV Now",
                key="optimize_btn",
                help="Start the AI optimization process",
                use_container_width=True,
                type="primary"
            ):
                optimize_cv()
        else:
            missing = []
            if not st.session_state.file_uploaded:
                missing.append("Upload CV")
            if not st.session_state.job_description_added:
                missing.append("Add Job Description")
            if not st.session_state.template_selected:
                missing.append("Choose Template")
            
            st.button(
                f"Complete Setup: {', '.join(missing)}",
                disabled=True,
                use_container_width=True,
                help="Complete the required steps below"
            )
    
    # Show completion status
    if all_ready:
        st.markdown("""
        <div class="status-message status-success" style="text-align: center; margin-top: 1rem;">
            <span>🎉</span>
            <span><strong>Ready to transform your career!</strong> All requirements complete.</span>
        </div>
        """, unsafe_allow_html=True)

# ================================
# 📄 PAGE CONTENT FUNCTIONS
# ================================
def render_home_page():
    """Render the main home page with CV optimization"""
    render_header()
    
    # Input sections first - these UPDATE the session state
    render_upload_section()
    render_job_description_section() 
    render_template_section()
    
    # Progress and optimization sections last - these READ the session state
    render_progress_section()
    render_optimization_section()
    
    # Show completion message if optimization is done
    if st.session_state.optimization_complete:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, var(--success), var(--success-dark));
            color: white;
            padding: var(--space-8);
            border-radius: var(--radius-2xl);
            text-align: center;
            margin-top: var(--space-8);
            box-shadow: var(--shadow-xl);
        ">
            <div style="font-size: 3rem; margin-bottom: var(--space-4);">🎉</div>
            <h3 style="color: white; margin-bottom: var(--space-3); font-family: var(--font-heading);">
                Congratulations!
            </h3>
            <p style="opacity: 0.9; margin: 0; font-size: 1.125rem; line-height: 1.6;">
                Your optimized CV is ready to help you land your dream job. 
                <br>Good luck with your applications!
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_about_page():
    """Render the About page"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-title">
                📘 About Tailor
            </div>
            <div class="section-subtitle">Your AI-powered career companion designed for the modern UK job market</div>
        </div>
        <div class="section-content">
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Our Mission
    
    At Tailor, we believe that every professional deserves a CV that truly represents their skills and potential. Our AI-powered platform is specifically designed for the UK job market, ensuring your CV meets the latest ATS (Applicant Tracking System) requirements and industry standards.
    
    ### Why Choose Tailor?
    
    **🎯 UK Market Expertise**  
    Built specifically for British employers and recruitment processes
    
    **🤖 Advanced AI Technology**  
    State-of-the-art natural language processing optimizes your content
    
    **⚡ Lightning Fast**  
    Professional results in under 60 seconds
    
    **🔒 Privacy First**  
    GDPR compliant with enterprise-grade security
    
    **✅ Proven Results**  
    95% ATS pass rate with over 50,000 successful optimizations
    
    ### How It Works
    
    1. **Upload** your current CV in any format
    2. **Paste** the job description you're targeting
    3. **Choose** from our professional templates
    4. **Download** your optimized, ATS-friendly CV
    
    ### Our Technology
    
    Tailor uses advanced machine learning algorithms trained on thousands of successful UK job applications. We continuously update our models based on the latest recruitment trends and ATS requirements.
    
    ### Support & Contact
    
    Need help? Our support team is here to assist you:
    - 📧 Email: support@tailor.ai
    - 💬 Live Chat: Available 9 AM - 6 PM GMT
    - 📚 Knowledge Base: Comprehensive guides and tutorials
    """)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_help_page():
    """Render the Help page"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-title">
                ❓ Help Center
            </div>
            <div class="section-subtitle">Get answers to common questions and learn how to get the best results</div>
        </div>
        <div class="section-content">
    """, unsafe_allow_html=True)
    
    # FAQ Section
    with st.expander("🔧 Getting Started"):
        st.markdown("""
        **Q: What file formats do you support?**  
        A: We support PDF (.pdf) and Microsoft Word (.docx, .doc) files up to 10MB.
        
        **Q: How long does the optimization take?**  
        A: Most CVs are optimized in 30-60 seconds, depending on file size and complexity.
        
        **Q: Do I need to create an account?**  
        A: No account required! You can use Tailor immediately without registration.
        """)
    
    with st.expander("📝 CV Optimization Tips"):
        st.markdown("""
        **Q: How detailed should my job description be?**  
        A: Include the complete job posting for best results. The more details you provide, the better we can match your CV to the role.
        
        **Q: Which template should I choose?**  
        A: 
        - **Professional**: Traditional industries (finance, law, consulting)
        - **Modern**: Tech, startups, creative agencies  
        - **Executive**: Senior leadership positions
        - **Creative**: Design, media, arts industries
        
        **Q: Can I optimize the same CV for multiple jobs?**  
        A: Absolutely! We recommend creating a tailored version for each application.
        """)
    
    with st.expander("🔒 Privacy & Security"):
        st.markdown("""
        **Q: Is my data secure?**  
        A: Yes! We use enterprise-grade encryption and are fully GDPR compliant. Your data is never stored permanently.
        
        **Q: Who can see my CV?**  
        A: Only you. We don't share, sell, or store your personal information.
        
        **Q: How long do you keep my data?**  
        A: Processing data is automatically deleted after 24 hours.
        """)
    
    with st.expander("⚡ Troubleshooting"):
        st.markdown("""
        **Q: My file won't upload. What should I do?**  
        A: 
        - Check file size (max 10MB)
        - Ensure it's PDF or Word format
        - Try refreshing the page
        
        **Q: The optimization seems stuck. Help!**  
        A: 
        - Refresh the page and try again
        - Check your internet connection
        - Contact support if the issue persists
        
        **Q: I'm not happy with the results. Can I get a refund?**  
        A: Contact our support team and we'll work to resolve any issues.
        """)
    
    # Contact Information
    st.markdown("""
    ### 📞 Still Need Help?
    
    Our support team is here to help:
    
    - **Live Chat**: Click the chat icon (9 AM - 6 PM GMT)
    - **Email**: support@tailor.ai
    - **Phone**: +44 20 7946 0958
    - **Response Time**: Within 2 hours during business hours
    """)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_pricing_page():
    """Render the Pricing page"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-title">
                💰 Pricing Plans
            </div>
            <div class="section-subtitle">Choose the perfect plan for your career needs</div>
        </div>
        <div class="section-content">
    """, unsafe_allow_html=True)
    
    # Pricing Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-xl);
            padding: var(--space-8);
            text-align: center;
            height: 400px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <div>
                <h3 style="color: var(--text-primary); margin-bottom: var(--space-4);">🚀 Free</h3>
                <div style="font-size: 2rem; font-weight: 700; color: var(--primary); margin-bottom: var(--space-4);">£0</div>
                <div style="color: var(--text-tertiary); margin-bottom: var(--space-6);">Perfect for trying out Tailor</div>
                <ul style="text-align: left; color: var(--text-secondary); line-height: 1.8;">
                    <li>✅ 1 CV optimization</li>
                    <li>✅ Basic templates</li>
                    <li>✅ ATS optimization</li>
                    <li>✅ PDF download</li>
                    <li>❌ Priority support</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Get Started Free", key="free_plan", use_container_width=True):
            st.session_state.active_nav = 'Home'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, var(--primary-glow), var(--bg-secondary));
            border: 2px solid var(--primary);
            border-radius: var(--radius-xl);
            padding: var(--space-8);
            text-align: center;
            height: 400px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
        ">
            <div style="
                position: absolute;
                top: -10px;
                left: 50%;
                transform: translateX(-50%);
                background: var(--primary);
                color: white;
                padding: 4px 16px;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 600;
            ">MOST POPULAR</div>
            <div>
                <h3 style="color: var(--text-primary); margin-bottom: var(--space-4);">⭐ Pro</h3>
                <div style="font-size: 2rem; font-weight: 700; color: var(--primary); margin-bottom: var(--space-4);">£9.99</div>
                <div style="color: var(--text-tertiary); margin-bottom: var(--space-6);">per month</div>
                <ul style="text-align: left; color: var(--text-secondary); line-height: 1.8;">
                    <li>✅ Unlimited CV optimizations</li>
                    <li>✅ Premium templates</li>
                    <li>✅ Advanced ATS optimization</li>
                    <li>✅ Multiple formats (PDF, Word)</li>
                    <li>✅ Priority support</li>
                    <li>✅ Cover letter templates</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Upgrade to Pro", key="pro_plan", use_container_width=True, type="primary"):
            st.success("🎉 Redirecting to checkout...")
    
    with col3:
        st.markdown("""
        <div style="
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-xl);
            padding: var(--space-8);
            text-align: center;
            height: 400px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <div>
                <h3 style="color: var(--text-primary); margin-bottom: var(--space-4);">🏢 Enterprise</h3>
                <div style="font-size: 2rem; font-weight: 700; color: var(--primary); margin-bottom: var(--space-4);">Custom</div>
                <div style="color: var(--text-tertiary); margin-bottom: var(--space-6);">For teams and organizations</div>
                <ul style="text-align: left; color: var(--text-secondary); line-height: 1.8;">
                    <li>✅ Everything in Pro</li>
                    <li>✅ Team management</li>
                    <li>✅ Analytics dashboard</li>
                    <li>✅ API access</li>
                    <li>✅ Custom branding</li>
                    <li>✅ Dedicated support</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Contact Sales", key="enterprise_plan", use_container_width=True):
            st.info("📧 Our sales team will contact you within 24 hours!")
    
    # FAQ Section
    st.markdown("""
    ### 💡 Frequently Asked Questions
    
    **Can I cancel anytime?**  
    Yes! Cancel your subscription anytime with no questions asked.
    
    **Do you offer refunds?**  
    We offer a 30-day money-back guarantee for all paid plans.
    
    **Is there a student discount?**  
    Yes! Students get 50% off Pro plans with valid student ID.
    
    **Can I upgrade or downgrade?**  
    You can change your plan anytime. Changes take effect immediately.
    """)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def render_account_page():
    """Render the My Account page"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-title">
                👤 My Account
            </div>
            <div class="section-subtitle">Manage your profile, settings, and CV history</div>
        </div>
        <div class="section-content">
    """, unsafe_allow_html=True)
    
    # Account tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "📊 Dashboard", "⚙️ Settings", "📚 History"])
    
    with tab1:
        st.markdown("### 👤 Profile Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("First Name", value="John", key="first_name")
            st.text_input("Email", value="john@example.com", key="email")
            st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Marketing", "Other"], key="industry")
        
        with col2:
            st.text_input("Last Name", value="Doe", key="last_name")
            st.text_input("Phone", value="+44 7xxx xxx xxx", key="phone")
            st.selectbox("Career Level", ["Entry Level", "Mid-Level", "Senior", "Executive"], key="career_level")
        
        if st.button("Update Profile", type="primary"):
            st.success("✅ Profile updated successfully!")
    
    with tab2:
        st.markdown("### 📊 Your Dashboard")
        
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("CVs Optimized", "12", "+3 this month")
        with col2:
            st.metric("ATS Score Avg", "94%", "+5% improvement")
        with col3:
            st.metric("Applications", "47", "+8 this week")
        with col4:
            st.metric("Interviews", "6", "+2 this month")
        
        # Recent Activity
        st.markdown("### 📈 Recent Activity")
        activities = [
            "✅ CV optimized for 'Senior Developer' role - 2 hours ago",
            "📄 Downloaded CV template 'Modern' - 1 day ago", 
            "🎯 Optimized for 'Product Manager' position - 3 days ago",
            "⭐ Upgraded to Pro plan - 1 week ago"
        ]
        
        for activity in activities:
            st.markdown(f"- {activity}")
    
    with tab3:
        st.markdown("### ⚙️ Account Settings")
        
        # Notifications
        st.checkbox("Email notifications", value=True)
        st.checkbox("SMS notifications", value=False)
        st.checkbox("Marketing updates", value=True)
        
        # Privacy
        st.markdown("### 🔒 Privacy Settings")
        st.checkbox("Share usage analytics", value=True)
        st.checkbox("Allow data for service improvement", value=True)
        
        # Danger Zone
        st.markdown("### ⚠️ Danger Zone")
        if st.button("Delete Account", type="secondary"):
            st.error("⚠️ This action cannot be undone!")
    
    with tab4:
        st.markdown("### 📚 CV History")
        
        # CV History Table
        history_data = [
            {"Date": "2025-01-15", "Job Title": "Senior Developer", "Company": "TechCorp", "Status": "Downloaded", "ATS Score": "96%"},
            {"Date": "2025-01-12", "Job Title": "Product Manager", "Company": "StartupXYZ", "Status": "Downloaded", "ATS Score": "94%"},
            {"Date": "2025-01-10", "Job Title": "Full Stack Developer", "Company": "WebAgency", "Status": "Downloaded", "ATS Score": "92%"},
        ]
        
        for item in history_data:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 3, 2, 2, 1])
                with col1:
                    st.write(item["Date"])
                with col2:
                    st.write(f"**{item['Job Title']}** at {item['Company']}")
                with col3:
                    st.write(item["Status"])
                with col4:
                    st.write(item["ATS Score"])
                with col5:
                    st.button("📥", key=f"download_{item['Date']}", help="Download CV")
                st.divider()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ================================
# 🔧 UTILITY FUNCTIONS
# ================================
def get_file_info(uploaded_file):
    """Get formatted file information with validation"""
    try:
        if not uploaded_file:
            return None
            
        size_bytes = uploaded_file.size
        size_mb = size_bytes / (1024 * 1024)
        
        # Format file size
        if size_mb < 1:
            size_formatted = f"{size_bytes / 1024:.1f} KB"
        else:
            size_formatted = f"{size_mb:.1f} MB"
        
        # Determine file type
        if uploaded_file.type == "application/pdf":
            type_friendly = "PDF Document"
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            type_friendly = "Word Document"
        else:
            type_friendly = "Unknown Document"
        
        # Estimate processing time based on file size
        if size_mb < 1:
            processing_time = "Less than 30 seconds"
        elif size_mb < 3:
            processing_time = "30-60 seconds"
        elif size_mb < 5:
            processing_time = "1-2 minutes"
        else:
            processing_time = "2-3 minutes"
        
        return {
            'name': uploaded_file.name,
            'size_bytes': size_bytes,
            'size_mb': size_mb,
            'size_formatted': size_formatted,
            'type': uploaded_file.type,
            'type_friendly': type_friendly,
            'processing_time': processing_time
        }
    except Exception as e:
        st.error(f"Error processing file information: {str(e)}")
        return None

def validate_uploaded_file(uploaded_file):
    """Validate uploaded file with comprehensive checks"""
    try:
        if not uploaded_file:
            return False, "No file uploaded"
            
        # Check file type
        valid_types = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/msword'
        ]
        
        if uploaded_file.type not in valid_types:
            return False, "Invalid file type. Please upload a PDF or Word document."
        
        # Check file size (10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB in bytes
        if uploaded_file.size > max_size:
            return False, f"File too large. Maximum size is 10MB, your file is {uploaded_file.size / (1024 * 1024):.1f}MB."
        
        # Check file name
        if len(uploaded_file.name) > 255:
            return False, "File name too long. Please rename your file."
            
        # Basic content validation (check if file is not empty)
        if uploaded_file.size == 0:
            return False, "File appears to be empty. Please upload a valid document."
            
        return True, "File is valid"
        
    except Exception as e:
        return False, f"Error validating file: {str(e)}"

def optimize_cv():
    """Enhanced CV optimization with AI processing"""
    try:
        progress_container = st.empty()
        
        # Validate inputs before processing
        if not st.session_state.file_uploaded:
            st.error("❌ Please upload your CV first")
            return
            
        if not st.session_state.job_description_added:
            st.error("❌ Please add a job description")
            return
            
        if not st.session_state.template_selected:
            st.error("❌ Please select a template")
            return
        
        # Get API key from Streamlit secrets
        try:
            api_key = st.secrets["ANTHROPIC_API_KEY"]
            
        except KeyError:
            st.error("❌ API key not configured. Please add ANTHROPIC_API_KEY to your Streamlit secrets.")
            return
        # Get optimizer and check rendercv availability before starting
        optimizer = st.session_state.cv_optimizer
        rendercv_available, rendercv_msg = optimizer.check_rendercv_availability()
        
        if not rendercv_available:
            st.warning(f"⚠️ PDF generation unavailable: {rendercv_msg}")
            st.info("💡 You'll get an optimized YAML file. Install `rendercv` for PDF generation.")
        
        with progress_container.container():
            st.markdown("""
            <div style="
                background: var(--bg-primary);
                border-radius: 16px;
                padding: 2rem;
                text-align: center;
                border: 1px solid var(--border-primary);
                box-shadow: var(--shadow-sm);
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <h3 style="color: var(--text-primary); font-family: var(--font-heading); margin-bottom: 0.5rem;">
                    AI is optimizing your CV...
                </h3>
                <p style="color: var(--text-secondary); margin-bottom: 2rem;">
                    Creating your career-changing CV with Claude Haiku 3.5
                </p>
            </div>
            """, unsafe_allow_html=True            )
            
            # Use the optimizer for AI processing (already defined above)
            
            # Load prompt template
            success, msg = optimizer.load_prompt_template("prompt_1.txt")
            if not success:
                st.error(f"❌ Error loading prompt: {msg}")
                return
            
            # Substitute variables with your specific format
            success, final_prompt = substitute_prompt_variables(optimizer)
            if not success:
                st.error(f"❌ Error preparing prompt: {final_prompt}")
                return
            
            with open(r"C:\Users\likit\Desktop\pythonProject\CV_Reader\prototype_3\code\final_prompt.txt", "w", encoding="utf-8") as f:
                f.write(final_prompt)
                
            # Setup AI client and optimize
            if not optimizer.setup_ai_client(api_key):
                st.error("❌ Failed to setup AI client")
                return
            
            success, result = optimizer.optimize_cv_with_ai(final_prompt)

        
        # Clear progress and show results
        progress_container.empty()
        
        if success:
            st.session_state.optimization_complete = True
            st.session_state.optimized_cv = result
            
            # Save to output directory
            save_success, yaml_path = optimizer.save_optimized_cv(result)
            if save_success:
                st.info(f"💾 CV saved as YAML to: {yaml_path}")
                
                # Generate PDF from YAML
                with st.spinner("🔄 Generating PDF..."):
                    pdf_success, pdf_path = optimizer.generate_pdf_from_yaml(yaml_path)
                
                if pdf_success:
                    st.success("📄 PDF generated successfully!")
                    
                    # Preview PDF inside Streamlit
                    try:
                        with open(pdf_path, "rb") as f:
                            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                            pdf_view = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>'
                            st.markdown("### 📖 PDF Preview")
                            st.markdown(pdf_view, unsafe_allow_html=True)
                    except Exception as e:
                        st.warning(f"Could not preview PDF: {str(e)}")
                    
                    # Download buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        try:
                            with open(pdf_path, "rb") as f:
                                st.download_button(
                                    "📥 Download PDF",
                                    f.read(),
                                    file_name=Path(pdf_path).name,
                                    mime="application/pdf",
                                    use_container_width=True,
                                    type="primary"
                                )
                        except Exception as e:
                            st.error(f"Error preparing PDF download: {str(e)}")
                    
                    with col2:
                        try:
                            with open(yaml_path, "r", encoding='utf-8') as f:
                                st.download_button(
                                    "📄 Download YAML",
                                    f.read(),
                                    file_name=Path(yaml_path).name,
                                    mime="text/yaml",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Error preparing YAML download: {str(e)}")
                else:
                    st.error(f"❌ PDF generation failed: {pdf_path}")
                    
                    # Still offer YAML download as fallback
                    st.markdown("### 📄 YAML Download Available")
                    try:
                        with open(yaml_path, "r", encoding='utf-8') as f:
                            st.download_button(
                                "📄 Download YAML (Fallback)",
                                f.read(),
                                file_name=Path(yaml_path).name,
                                mime="text/yaml",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Error preparing YAML download: {str(e)}")
                        
                    # Show installation instructions
                    st.markdown("""
                    **💡 To enable PDF generation:**
                    
                    1. **Install rendercv:**
                       ```bash
                       pip install rendercv
                       ```
                    
                    2. **Restart your Streamlit app** after installation
                    
                    3. **Re-run the optimization** to get both YAML and PDF
                    
                    **Why PDF generation failed:**
                    The YAML file contains all your optimized CV data, but we need the `rendercv` tool to convert it to a beautifully formatted PDF.
                    """)
            
            # Enhanced success message
            st.success("🎉 Your CV has been successfully optimized!")
            st.balloons()
            
            # Show optimized CV text
            st.markdown("### 📄 Your Optimized CV Content")
            st.text_area(
                "Optimized CV Content",
                value=result,
                height=400,
                help="Your professionally optimized CV content"
            )
                
            # Show optimization summary
            st.markdown("""
            <div style="
                background: var(--bg-secondary);
                padding: 1.5rem;
                border-radius: 12px;
                margin-top: 1rem;
                border: 1px solid var(--border-light);
            ">
                <h4 style="color: var(--text-primary); margin-bottom: 1rem;">✨ Optimization Complete</h4>
                <ul style="color: var(--text-secondary); margin: 0; padding-left: 1.5rem;">
                    <li>ATS compatibility optimized</li>
                    <li>Keywords strategically placed</li>
                    <li>Professional formatting applied</li>
                    <li>Content enhanced for impact</li>
                    <li>Saved as structured YAML for easy editing</li>
                    <li>PDF automatically generated for immediate use</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Show YAML structure info
            with st.expander("📋 File Formats & Structure"):
                st.markdown("""
                **Your optimized CV is available in two formats:**
                
                ### 📄 PDF Format
                - **✅ Ready to submit** to employers
                - **✅ Professional formatting** applied
                - **✅ ATS-friendly** layout
                - **✅ Print-ready** quality
                
                ### 📊 YAML Format  
                - **✅ Easy to edit** individual sections
                - **✅ Structured and organized** data
                - **✅ Machine-readable** for further processing
                - **✅ Contains optimization metadata** for reference
                
                **YAML Structure includes:**
                - **📊 Metadata**: Generation date, template used, optimization version
                - **📄 Raw Content**: The complete optimized CV text
                - **🗂️ Parsed Sections**: Automatically detected CV sections
                - **🔍 Analysis**: Keywords, word count, template alignment
                """)
                
                # Show a small preview of the YAML structure
                sample_yaml = """
metadata:
  generated_date: "2025-01-21T10:30:00"
  template_used: "professional"
  optimization_version: "1.0"

raw_content: |
  [Your complete optimized CV content here]

parsed_sections:
  "Professional Summary": |
    [Optimized summary section]
  "Work Experience": |
    [Enhanced work experience]
  "Skills": |
    [Targeted skills section]

analysis:
  total_words: 450
  sections_found: ["Professional Summary", "Work Experience", "Education", "Skills"]
  job_description_keywords: ["leadership", "management", "python", "agile"]
                """
                st.code(sample_yaml, language="yaml")
        else:
            st.error(f"❌ Optimization failed: {result}")
        
    except Exception as e:
        st.error(f"❌ Error during optimization: {str(e)}")

def substitute_prompt_variables(optimizer):
    """
    Substitute variables in prompt template for your specific format
    Replaces [INSERT_TEMPLATE], [INSERT_JOB_DESCRIPTION], [INSERT_CV]
    
    Args:
        optimizer: CVOptimizer instance with loaded data
        
    Returns:
        Tuple of (success: bool, final_prompt: str)
    """
    try:
        if not optimizer.prompt_template:
            return False, "No prompt template loaded"
        
        if not optimizer.cv_text:
            return False, "No CV text available"
        
        if not optimizer.job_description:
            return False, "No job description available"
        
        if not optimizer.template_config:
            return False, "No template configuration loaded"
        
        # Your specific variable substitutions
        final_prompt = optimizer.prompt_template.replace("[INSERT_CV]", optimizer.cv_text)
        final_prompt = final_prompt.replace("[INSERT_JOB_DESCRIPTION]", optimizer.job_description)
        final_prompt = final_prompt.replace("[INSERT_TEMPLATE]", str(optimizer.template_config))
        
        return True, final_prompt
        
    except Exception as e:
        return False, f"Error substituting variables: {str(e)}"

# Add debug function for development
def render_debug_section():
    """Add this to your app for development/debugging"""
    with st.expander("🔧 Debug Information (Development)"):
        if st.button("🔍 Show Debug Info"):
            optimizer = st.session_state.cv_optimizer
            dir_info = optimizer.get_directory_info()
            templates_available = optimizer.list_available_templates()
            
            # Check rendercv availability
            rendercv_available, rendercv_msg = optimizer.check_rendercv_availability()
            if not rendercv_available:
                st.warning(f"⚠️ {rendercv_msg}")
                st.info("PDF generation will be skipped. You'll still get the optimized YAML file.")
            
            st.markdown("### 📁 Directory Structure")
            st.json(dir_info)
            
            st.markdown("### 📄 Available Templates")
            st.json(templates_available)
            
            st.markdown("### 🔧 Tools Status")
            st.json({
                "rendercv_available": rendercv_available,
                "rendercv_status": rendercv_msg
            })
            
            # Check if prompt file exists
            from pathlib import Path
            prompt_file = Path(dir_info['prompts_dir']) / "prompt_1.txt"
            st.markdown(f"### 📝 Prompt File Status")
            st.write(f"prompt_1.txt exists: {prompt_file.exists()}")
            
            if prompt_file.exists():
                try:
                    with open(prompt_file, 'r') as f:
                        content = f.read()
                    st.text_area("Prompt Content Preview", content[:500] + "..." if len(content) > 500 else content)
                except Exception as e:
                    st.error(f"Error reading prompt file: {e}")

# ================================
# 🏠 MAIN APPLICATION
# ================================
def configure_page():
    """Configure Streamlit page settings with modern options"""
    st.set_page_config(
        page_title="Tailor - AI CV Optimizer",
        page_icon="✂️",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': 'https://tailor.ai/help',
            'Report a bug': 'https://tailor.ai/support',
            'About': "Professional CV optimization powered by AI for the UK job market"
        }
    )

def main():
    """Main application function with comprehensive error handling"""
    try:
        configure_page()
        load_modern_css()
        initialize_session_state()
        
        # Render navigation
        render_top_navbar()
        
        # Route to different pages based on navigation
        active_page = st.session_state.get("active_nav", "Home")
        
        if active_page == "About":
            render_about_page()
        elif active_page == "Help":
            render_help_page()
        elif active_page == "Pricing":
            render_pricing_page()
        elif active_page == "My Account":
            render_account_page()
        else:
            # Default Home page
            render_home_page()
            
        # Add debug section for development (remove in production)
        # if st.secrets.get("DEBUG_MODE", False):
        #     render_debug_section()
                
    except Exception as e:
        # Global error handler
        st.error(f"❌ Application Error: {str(e)}")
        st.markdown("""
        <div class="error-boundary">
            <h4>Something went wrong</h4>
            <p>Please refresh the page and try again. If the problem persists, contact support.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Offer to reset session state
        if st.button("🔄 Reset Application"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()