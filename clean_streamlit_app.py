import streamlit as st
import sqlite3
import json
from datetime import datetime
import hashlib
import os

# Page configuration
st.set_page_config(
    page_title="Wholesale2Flip - Master Real Estate Wholesaling & Flipping",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS that matches the original design
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Root variables */
    :root {
        --primary-color: #1e3a8a;
        --secondary-color: #f59e0b;
        --accent-color: #10b981;
        --danger-color: #ef4444;
        --dark-color: #1f2937;
        --light-color: #f8fafc;
        --gradient-primary: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        --gradient-secondary: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
        --shadow-xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        background: var(--gradient-primary);
    }
    
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* Header */
    .header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 1rem 0;
        margin-bottom: 0;
        box-shadow: var(--shadow-lg);
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .header-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .logo {
        font-size: 2.2rem;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }
    
    .nav {
        display: flex;
        gap: 2.5rem;
        align-items: center;
    }
    
    .nav a {
        text-decoration: none;
        color: var(--dark-color);
        font-weight: 600;
        transition: color 0.3s ease;
        position: relative;
        cursor: pointer;
    }
    
    .nav a:hover {
        color: var(--primary-color);
    }
    
    /* Hero Section */
    .hero {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
        background: var(--gradient-primary);
        padding: 4rem 20px;
    }
    
    .hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%);
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(1deg); }
    }
    
    .hero-content {
        position: relative;
        z-index: 10;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .hero h1 {
        font-size: clamp(3rem, 6vw, 5.5rem);
        font-weight: 900;
        margin-bottom: 1.5rem;
        line-height: 1.1;
        background: linear-gradient(45deg, #fff 0%, #e2e8f0 50%, #fff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }
    
    .hero .subtitle {
        font-size: 1.4rem;
        margin-bottom: 2rem;
        opacity: 0.95;
        font-weight: 500;
        line-height: 1.6;
    }
    
    .hero-buttons {
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 2.5rem;
    }
    
    /* Stats Section */
    .stats {
        background: white;
        padding: 4rem 20px;
        margin-top: -2rem;
        position: relative;
        z-index: 100;
        border-radius: 25px 25px 0 0;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        text-align: center;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .stat-item {
        padding: 1.5rem;
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 900;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: block;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Features Section */
    .features {
        padding: 6rem 20px;
        background: var(--light-color);
    }
    
    .features h2 {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #6b7280;
        margin-bottom: 4rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2.5rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .feature-card {
        background: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        box-shadow: var(--shadow-lg);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-primary);
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: var(--shadow-xl);
    }
    
    .feature-icon {
        width: 90px;
        height: 90px;
        background: var(--gradient-primary);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-size: 2.5rem;
        color: white;
        box-shadow: var(--shadow-lg);
        font-weight: bold;
    }
    
    .feature-card h3 {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--dark-color);
    }
    
    .feature-card p {
        color: #6b7280;
        line-height: 1.7;
        font-size: 1rem;
    }
    
    /* Buttons */
    .btn {
        padding: 1.25rem 2.5rem;
        border: none;
        border-radius: 15px;
        cursor: pointer;
        font-weight: 700;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 1.1rem;
    }
    
    .btn-primary {
        background: var(--gradient-primary);
        color: white;
        box-shadow: var(--shadow-lg);
    }
    
    .btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-xl);
    }
    
    .btn-secondary {
        background: transparent;
        color: var(--primary-color);
        border: 2px solid var(--primary-color);
    }
    
    .btn-secondary:hover {
        background: var(--primary-color);
        color: white;
        transform: translateY(-2px);
    }
    
    .btn-accent {
        background: var(--gradient-secondary);
        color: white;
        box-shadow: var(--shadow-lg);
    }
    
    .btn-accent:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: var(--shadow-xl);
    }
    
    /* Form Sections */
    .form-section {
        background: white;
        padding: 4rem 20px;
        margin: 2rem 0;
    }
    
    .qualification-form {
        max-width: 800px;
        margin: 0 auto;
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: var(--shadow-xl);
    }
    
    /* Pricing */
    .pricing {
        padding: 6rem 20px;
        background: white;
    }
    
    .pricing-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .pricing-card {
        background: white;
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        box-shadow: var(--shadow-lg);
        position: relative;
        transition: all 0.4s ease;
        border: 2px solid transparent;
    }
    
    .pricing-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-xl);
    }
    
    .pricing-card.featured {
        border-color: var(--primary-color);
        transform: scale(1.05);
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    .pricing-card.featured::before {
        content: "Most Popular";
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--gradient-secondary);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .plan-name {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: var(--dark-color);
    }
    
    .plan-price {
        font-size: 3.5rem;
        font-weight: 900;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .plan-period {
        color: #6b7280;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    
    .check-icon {
        background: var(--accent-color);
        color: white;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-size: 0.7rem;
        font-weight: bold;
    }
    
    /* Streamlit specific overrides */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1.25rem 2.5rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-size: 1.1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: var(--shadow-xl) !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 12px !important;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px !important;
        border: 2px solid #e5e7eb !important;
        padding: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1) !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: var(--accent-color) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .stError {
        background: var(--danger-color) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    /* Footer */
    .footer {
        background: var(--dark-color);
        color: white;
        padding: 4rem 20px 2rem;
        text-align: center;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .hero h1 {
            font-size: 3rem !important;
        }
        
        .hero-buttons {
            flex-direction: column;
            align-items: center;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .pricing-grid {
            grid-template-columns: 1fr;
        }
        
        .pricing-card.featured {
            transform: none;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Database functions
def init_db():
    """Initialize the database"""
    try:
        conn = sqlite3.connect('wholesale2flip.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS buyer_qualifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                location TEXT NOT NULL,
                strategy TEXT NOT NULL,
                budget_min INTEGER,
                budget_max INTEGER,
                funding_type TEXT,
                proof_of_funds TEXT,
                experience TEXT,
                timeline TEXT,
                monthly_deals TEXT,
                special_requirements TEXT,
                newsletter BOOLEAN DEFAULT 0,
                discord BOOLEAN DEFAULT 0,
                mentorship BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database initialization error: {e}")
        return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(name, email, password):
    try:
        conn = sqlite3.connect('wholesale2flip.db')
        cursor = conn.cursor()
        password_hash = hash_password(password)
        cursor.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)', 
                      (name, email, password_hash))
        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Email already exists"
    except Exception as e:
        return False, f"Error creating account: {str(e)}"

def verify_user(email, password):
    try:
        conn = sqlite3.connect('wholesale2flip.db')
        cursor = conn.cursor()
        password_hash = hash_password(password)
        cursor.execute('SELECT id, name FROM users WHERE email = ? AND password_hash = ?', 
                      (email, password_hash))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, user[1]
        else:
            return False, "Invalid email or password"
    except Exception as e:
        return False, f"Login error: {str(e)}"

def save_buyer_qualification(data):
    try:
        conn = sqlite3.connect('wholesale2flip.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO buyer_qualifications (
                name, email, phone, location, strategy, budget_min, budget_max,
                funding_type, proof_of_funds, experience, timeline, monthly_deals,
                special_requirements, newsletter, discord, mentorship
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], data['email'], data['phone'], data['location'],
            json.dumps(data['strategy']), data['budget_min'], data['budget_max'],
            data['funding_type'], data['proof_of_funds'], data['experience'],
            data['timeline'], data['monthly_deals'], data['special_requirements'],
            data['newsletter'], data['discord'], data['mentorship']
        ))
        
        conn.commit()
        conn.close()
        return True, "Congratulations! You've been added to our verified buyer network. You'll start receiving qualified deals within 24 hours."
    except Exception as e:
        return False, f"Error saving qualification: {str(e)}"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# Initialize database
init_db()
load_css()

# Header
st.markdown("""
<div class="header">
    <div class="header-content">
        <div class="logo">Wholesale2Flip</div>
        <nav class="nav">
            <a href="#home">Home</a>
            <a href="#features">Features</a>
            <a href="#platform">Platform</a>
            <a href="#qualification">Join Network</a>
            <a href="#pricing">Pricing</a>
        </nav>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero" id="home">
    <div class="hero-content">
        <h1>Master Real Estate Wholesaling & Flipping</h1>
        <p class="subtitle">Connect with verified buyers, analyze deals instantly, and scale your real estate business with our AI-powered matching platform.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Buttons
col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
with col2:
    if st.button("Join Buyer Network", key="hero_join"):
        st.info("Scroll down to fill out the buyer qualification form!")
with col4:
    if st.button("Explore Platform", key="hero_explore"):
        st.info("Platform demo - scroll down to see features!")

# Stats Section
st.markdown("""
<div class="stats">
    <div class="stats-grid">
        <div class="stat-item">
            <span class="stat-number">15K+</span>
            <span class="stat-label">Active Investors</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">$2.8B</span>
            <span class="stat-label">Deals Closed</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">47%</span>
            <span class="stat-label">Avg ROI</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">72hrs</span>
            <span class="stat-label">Avg Close Time</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class="features" id="features">
    <h2>Why Choose Wholesale2Flip?</h2>
    <p class="section-subtitle">Advanced tools and verified networks to accelerate your real estate success</p>
    
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">AI</div>
            <h3>AI-Powered Deal Matching</h3>
            <p>Our proprietary algorithm analyzes market data and investor preferences to match properties with the perfect buyers in real-time.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">$</div>
            <h3>Verified Cash Buyers</h3>
            <p>Access to over 15,000 pre-qualified cash buyers, fix-and-flip investors, and rental property buyers with proof of funds.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Instant Deal Analysis</h3>
            <p>Advanced calculators for ARV, repair costs, profit margins, and ROI with real-time market comparables and rental estimates.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🏠</div>
            <h3>Off-Market Properties</h3>
            <p>Exclusive access to distressed properties, foreclosures, and motivated seller leads before they hit the MLS.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3>Mobile Deal Management</h3>
            <p>Manage your entire pipeline on-the-go with our mobile app featuring contract templates and e-signature integration.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">NET</div>
            <h3>Discord Integration</h3>
            <p>Seamlessly connect with our Discord community for live deal discussions, mentorship, and instant buyer notifications.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Platform Demo Section
st.markdown("""
<div class="form-section" id="platform">
    <div style="max-width: 1400px; margin: 0 auto;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center;">
            <div>
                <h2 style="font-size: 3rem; font-weight: 900; margin-bottom: 1.5rem; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Professional-Grade Platform</h2>
                <p style="font-size: 1.2rem; color: #6b7280; margin-bottom: 2rem; line-height: 1.7;">Built by wholesalers, for wholesalers. Our platform combines cutting-edge technology with real-world experience to give you the competitive edge.</p>
                
                <div style="margin-bottom: 2rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem; font-weight: 600; color: var(--dark-color);">
                        <div style="background: var(--accent-color); color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-size: 0.8rem; font-weight: bold;">OK</div>
                        API integrations with major platforms
                    </div>
                </div>
            </div>
            
            <div style="background: var(--gradient-primary); border-radius: 20px; padding: 2rem; color: white; text-align: center; box-shadow: var(--shadow-xl);">
                <h3>Live Platform Demo</h3>
                <p>See how our AI matches your property with qualified buyers in seconds</p>
                <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 2rem; margin: 1rem 0;">
                    <p><strong>Demo Property:</strong> 123 Main St, Atlanta, GA</p>
                    <p><strong>ARV:</strong> $185,000 | <strong>Repair:</strong> $35,000</p>
                    <p><strong>Your Price:</strong> $120,000</p>
                    <div style="margin: 1rem 0; padding: 1rem; background: rgba(16, 185, 129, 0.2); border-radius: 8px;">
                        <strong>3 Qualified Buyers Found!</strong><br>
                        • Fix & Flip Investor (Atlanta Metro)<br>
                        • Rental Portfolio Builder<br>
                        • Cash Buyer Network
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Authentication Section
if not st.session_state.logged_in:
    st.markdown("---")
    st.markdown("### Get Started Today")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### **Login to Your Account**")
        with st.form("login_form"):
            email = st.text_input("Email Address", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            login_submit = st.form_submit_button("Sign In")
            
            if login_submit:
                if email and password:
                    success, message = verify_user(email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_name = message
                        st.success(f"Welcome back, {message}!")
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")
    
    with col2:
        st.markdown("#### **Create Your Free Account**")
        with st.form("signup_form"):
            name = st.text_input("Full Name", key="signup_name")
            email = st.text_input("Email Address", key="signup_email")
            password = st.text_input("Create Password", type="password", key="signup_password")
            signup_submit = st.form_submit_button("Start Free Trial")
            
            if signup_submit:
                if name and email and password:
                    success, message = save_user(name, email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_name = name
                        st.success(f"Welcome to Wholesale2Flip, {name}! Your free trial has started.")
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")
else:
    st.success(f"Welcome back, {st.session_state.user_name}!")
    if st.button("Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.rerun()

# Buyer Qualification Form
st.markdown("---")
st.markdown("""
<div class="form-section" id="qualification">
    <div class="qualification-form">
        <h2 style="text-align: center; font-size: 3rem; font-weight: 900; margin-bottom: 1rem; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Join Our Verified Buyer Network</h2>
        <p style="text-align: center; font-size: 1.3rem; color: #6b7280; margin-bottom: 3rem;">Get exclusive access to deals that match your investment criteria</p>
    </div>
</div>
""", unsafe_allow_html=True)

with st.form("buyer_qualification_form"):
    st.markdown("### Investor Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name *", key="qual_name")
        email = st.text_input("Email Address *", key="qual_email")
    
    with col2:
        phone = st.text_input("Phone Number *", key="qual_phone")
        location = st.text_input("Primary Investment Markets *", placeholder="e.g., Atlanta, Birmingham, Memphis", key="qual_location")
    
    st.markdown("### Investment Strategy")
    st.markdown("What best describes your investment focus? (Select all that apply)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        fix_flip = st.checkbox("Fix & Flip Properties")
        rental = st.checkbox("Buy & Hold Rentals")
    with col2:
        section8 = st.checkbox("Section 8 / Low-Income Housing")
        luxury = st.checkbox("High-End Properties ($400K+)")
    with col3:
        commercial = st.checkbox("Commercial Real Estate")
        wholesale = st.checkbox("Wholesale to Other Investors")
    
    st.markdown("### Financial Capacity")
    col1, col2 = st.columns(2)
    
    with col1:
        budget_min = st.selectbox("Minimum Purchase Price", [
            "", "$25,000", "$50,000", "$75,000", "$100,000", "$150,000", "$200,000+"
        ])
        funding_type = st.selectbox("Funding Method", [
            "", "Cash Only", "Conventional Financing", "Hard Money Lenders", 
            "Private Lenders", "Creative Financing", "Combination of Methods"
        ])
    
    with col2:
        budget_max = st.selectbox("Maximum Purchase Price", [
            "", "$100,000", "$200,000", "$300,000", "$500,000", "$750,000", "$1,000,000+"
        ])
        proof_of_funds = st.selectbox("Proof of Funds Available?", [
            "", "Yes - Can provide immediately", "Have pre-approval letter", 
            "Working on securing funds", "Not yet available"
        ])
    
    st.markdown("### Experience Level")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        experience = st.selectbox("Real Estate Investment Experience", [
            "", "Beginner (0-2 deals)", "Intermediate (3-10 deals)", 
            "Experienced (11-25 deals)", "Expert (25+ deals)"
        ])
    
    with col2:
        timeline = st.selectbox("How quickly can you close?", [
            "", "7 days or less", "14 days", "21 days", "30 days", "45+ days"
        ])
    
    with col3:
        monthly_deals = st.selectbox("How many deals do you want per month?", [
            "", "1-2 deals", "3-5 deals", "6-10 deals", "10+ deals"
        ])
    
    st.markdown("### Additional Information")
    special_requirements = st.text_area("Special Requirements or Preferences",
                                      placeholder="e.g., specific neighborhoods, property types, renovation budget limits, etc.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        newsletter = st.checkbox("Subscribe to weekly deal alerts")
    with col2:
        discord = st.checkbox("Join our Discord community")
    with col3:
        mentorship = st.checkbox("Interested in mentorship program")
    
    submit_qualification = st.form_submit_button("Join Verified Buyer Network")
    
    if submit_qualification:
        if name and email and phone and location:
            # Collect strategy data
            strategy = []
            if fix_flip: strategy.append("fix-flip")
            if rental: strategy.append("rental")
            if section8: strategy.append("section8")
            if luxury: strategy.append("luxury")
            if commercial: strategy.append("commercial")
            if wholesale: strategy.append("wholesale")
            
            qualification_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'location': location,
                'strategy': strategy,
                'budget_min': budget_min,
                'budget_max': budget_max,
                'funding_type': funding_type,
                'proof_of_funds': proof_of_funds,
                'experience': experience,
                'timeline': timeline,
                'monthly_deals': monthly_deals,
                'special_requirements': special_requirements,
                'newsletter': newsletter,
                'discord': discord,
                'mentorship': mentorship
            }
            
            success, message = save_buyer_qualification(qualification_data)
            if success:
                st.success(message)
                st.balloons()
            else:
                st.error(message)
        else:
            st.error("Please fill in all required fields (marked with *)")

# Pricing Section
st.markdown("---")
st.markdown("""
<div class="pricing" id="pricing">
    <h2 style="text-align: center; font-size: 3rem; font-weight: 900; margin-bottom: 1rem; background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Choose Your Growth Plan</h2>
    <p style="text-align: center; font-size: 1.3rem; color: #6b7280; margin-bottom: 4rem;">Scale your real estate business with the right tools and support</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# Helper function to create feature list item
def create_feature_item(text):
    return f'''<li style="display: flex; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid #f3f4f6;">
        <div class="check-icon">OK</div>
        {text}
    </li>'''

with col1:
    st.markdown(f"""
    <div class="pricing-card">
        <div class="plan-name">Starter</div>
        <div class="plan-price">$97</div>
        <div class="plan-period">per month</div>
        <ul style="text-align: left; margin: 1rem 0; list-style: none;">
            {create_feature_item("Access to basic deal flow")}
            {create_feature_item("Standard buyer database (5K+ buyers)")}
            {create_feature_item("Basic deal analysis tools")}
            {create_feature_item("Email support")}
            {create_feature_item("Monthly market reports")}
            {create_feature_item("Discord community access")}
            {create_feature_item("Mobile app access")}
        </ul>
        <p style="margin-bottom: 2rem;"><strong>Perfect for:</strong><br>New investors getting started</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start Free Trial", key="starter"):
        st.success("You've selected the Starter plan! Redirecting to secure checkout...")

with col2:
    st.markdown(f"""
    <div class="pricing-card featured">
        <div class="plan-name">Professional</div>
        <div class="plan-price">$197</div>
        <div class="plan-period">per month</div>
        <ul style="text-align: left; margin: 1rem 0; list-style: none;">
            {create_feature_item("Everything in Starter")}
            {create_feature_item("Premium buyer network (15K+ buyers)")}
            {create_feature_item("AI-powered deal matching")}
            {create_feature_item("Advanced analytics & reporting")}
            {create_feature_item("Priority deal notifications")}
            {create_feature_item("Live training sessions (weekly)")}
            {create_feature_item("Contract templates & e-signatures")}
            {create_feature_item("Phone support")}
            {create_feature_item("CRM & lead management")}
        </ul>
        <p style="margin-bottom: 2rem;"><strong>Perfect for:</strong><br>Active investors ready to scale</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Most Popular Choice", key="professional"):
        st.success("You've selected the Professional plan! Redirecting to secure checkout...")

with col3:
    st.markdown(f"""
    <div class="pricing-card">
        <div class="plan-name">Elite</div>
        <div class="plan-price">$397</div>
        <div class="plan-period">per month</div>
        <ul style="text-align: left; margin: 1rem 0; list-style: none;">
            {create_feature_item("Everything in Professional")}
            {create_feature_item("Exclusive off-market deals")}
            {create_feature_item("Personal deal coach")}
            {create_feature_item("Direct lender connections")}
            {create_feature_item("Custom market analysis")}
            {create_feature_item("White-glove transaction support")}
            {create_feature_item("Mastermind group access")}
            {create_feature_item("API access for automation")}
            {create_feature_item("Dedicated account manager")}
        </ul>
        <p style="margin-bottom: 2rem;"><strong>Perfect for:</strong><br>High-volume investors & teams</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Go Elite", key="elite"):
        st.success("You've selected the Elite plan! Redirecting to secure checkout...")

# Footer
st.markdown("""
<div class="footer">
    <div style="max-width: 1400px; margin: 0 auto;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 3rem; margin-bottom: 3rem;">
            <div>
                <h3 style="margin-bottom: 1.5rem; background: var(--gradient-secondary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 700;">Wholesale2Flip</h3>
                <p>The premier platform for real estate wholesaling and investment. Connect with verified buyers, analyze deals instantly, and scale your business.</p>
                <div style="margin-top: 1rem;">
                    <p>Email: hello@wholesale2flip.com</p>
                    <p>Phone: (555) 123-FLIP</p>
                </div>
            </div>
            <div>
                <h3 style="margin-bottom: 1.5rem; background: var(--gradient-secondary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 700;">Platform</h3>
                <p>• Features</p>
                <p>• How It Works</p>
                <p>• Pricing</p>
                <p>• API Documentation</p>
                <p>• Mobile App</p>
            </div>
            <div>
                <h3 style="margin-bottom: 1.5rem; background: var(--gradient-secondary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 700;">Resources</h3>
                <p>• Learning Center</p>
                <p>• Deal Calculator</p>
                <p>• Market Reports</p>
                <p>• Contract Templates</p>
                <p>• Discord Community</p>
            </div>
            <div>
                <h3 style="margin-bottom: 1.5rem; background: var(--gradient-secondary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 700;">Support</h3>
                <p>• Help Center</p>
                <p>• Contact Support</p>
                <p>• System Status</p>
                <p>• Privacy Policy</p>
                <p>• Terms of Service</p>
            </div>
        </div>
        <div style="text-align: center; padding-top: 2rem; border-top: 1px solid #374151; color: #9ca3af;">
            <p>&copy; 2025 Wholesale2Flip. All rights reserved. | Built for serious real estate investors.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True) 600; color: var(--dark-color);">
                        <div style="background: var(--accent-color); color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-size: 0.8rem; font-weight: bold;">OK</div>
                        Real-time property alerts & notifications
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 1rem; font-weight: 600; color: var(--dark-color);">
                        <div style="background: var(--accent-color); color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-size: 0.8rem; font-weight: bold;">OK</div>
                        Automated buyer matching system
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 1rem; font-weight: 600; color: var(--dark-color);">
                        <div style="background: var(--accent-color); color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-size: 0.8rem; font-weight: bold;">OK</div>
                        Advanced deal analysis & reporting
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 1rem; font-weight: 600; color: var(--dark-color);">
                        <div style="background: var(--accent-color); color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-size: 0.8rem; font-weight: bold;">OK</div>
                        Contract management & e-signatures
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 1rem; font-weight: 600; color: var(--dark-color);">
                        <div style="background: var(--accent-color); color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-size: 0.8rem; font-weight: bold;">OK</div>
                        CRM with lead tracking & follow-up
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 1rem; font-weight: 600; color: var(--dark-color);">
                        <div style="background: var(--accent-color); color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-size: 0.8rem; font-weight: bold;">OK</div>
                        Market analytics & trend insights
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 1rem; font-weight: 600; color: var(--dark-color);">
                        <div style="background: var(--accent-color); color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-size: 0.8rem; font-weight: bold;">OK</div>
                        Team collaboration tools
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 1rem; font-weight: