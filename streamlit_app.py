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

# Custom CSS
def load_css():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        margin-bottom: 2rem;
        opacity: 0.95;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #1e3a8a;
        margin-bottom: 1rem;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #e5e7eb;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 900;
        color: #1e3a8a;
        display: block;
    }
    
    .stat-label {
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.9rem;
    }
    
    .pricing-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        text-align: center;
        border: 2px solid transparent;
        height: 100%;
    }
    
    .pricing-card.featured {
        border-color: #1e3a8a;
        transform: scale(1.05);
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    .plan-price {
        font-size: 3rem;
        font-weight: 900;
        color: #1e3a8a;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .success-message {
        background: #10b981;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #ef4444;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Database functions
def init_db():
    """Initialize the database"""
    conn = sqlite3.connect('wholesale2flip.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Buyer qualifications table
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

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(name, email, password):
    """Save user to database"""
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
    """Verify user credentials"""
    try:
        conn = sqlite3.connect('wholesale2flip.db')
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute('SELECT id, name FROM users WHERE email = ? AND password_hash = ?', 
                      (email, password_hash))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, user[1]  # Return success and name
        else:
            return False, "Invalid email or password"
    except Exception as e:
        return False, f"Login error: {str(e)}"

def save_buyer_qualification(data):
    """Save buyer qualification to database"""
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
        return True, "Successfully added to buyer network!"
    except Exception as e:
        return False, f"Error saving qualification: {str(e)}"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Initialize database
init_db()

# Load CSS
load_css()

def show_hero():
    """Display hero section"""
    st.markdown("""
    <div class="main-header">
        <h1 class="hero-title">Master Real Estate Wholesaling & Flipping</h1>
        <p class="hero-subtitle">Connect with verified buyers, analyze deals instantly, and scale your real estate business with our AI-powered matching platform.</p>
    </div>
    """, unsafe_allow_html=True)

def show_stats():
    """Display statistics"""
    st.markdown("### Platform Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">15K+</span>
            <span class="stat-label">Active Investors</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">$2.8B</span>
            <span class="stat-label">Deals Closed</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">47%</span>
            <span class="stat-label">Avg ROI</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">72hrs</span>
            <span class="stat-label">Avg Close Time</span>
        </div>
        """, unsafe_allow_html=True)

def show_features():
    """Display features section"""
    st.markdown("## Why Choose Wholesale2Flip?")
    st.markdown("*Advanced tools and verified networks to accelerate your real estate success*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 AI-Powered Deal Matching</h3>
            <p>Our proprietary algorithm analyzes market data and investor preferences to match properties with the perfect buyers in real-time.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Instant Deal Analysis</h3>
            <p>Advanced calculators for ARV, repair costs, profit margins, and ROI with real-time market comparables and rental estimates.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📱 Mobile Deal Management</h3>
            <p>Manage your entire pipeline on-the-go with our mobile app featuring contract templates and e-signature integration.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>💰 Verified Cash Buyers</h3>
            <p>Access to over 15,000 pre-qualified cash buyers, fix-and-flip investors, and rental property buyers with proof of funds.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🏠 Off-Market Properties</h3>
            <p>Exclusive access to distressed properties, foreclosures, and motivated seller leads before they hit the MLS.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Discord Integration</h3>
            <p>Seamlessly connect with our Discord community for live deal discussions, mentorship, and instant buyer notifications.</p>
        </div>
        """, unsafe_allow_html=True)

def show_login_signup():
    """Display login/signup forms"""
    if not st.session_state.logged_in:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Login")
            with st.form("login_form"):
                email = st.text_input("Email Address")
                password = st.text_input("Password", type="password")
                login_submit = st.form_submit_button("Sign In")
                
                if login_submit:
                    if email and password:
                        success, message = verify_user(email, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user_name = message
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Please fill in all fields")
        
        with col2:
            st.markdown("### Create Account")
            with st.form("signup_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email Address", key="signup_email")
                password = st.text_input("Password", type="password", key="signup_password")
                signup_submit = st.form_submit_button("Start Free Trial")
                
                if signup_submit:
                    if name and email and password:
                        success, message = save_user(name, email, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user_name = name
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Please fill in all fields")
    else:
        st.success(f"Welcome back, {st.session_state.user_name}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.rerun()

def show_buyer_qualification():
    """Display buyer qualification form"""
    st.markdown("## Join Our Verified Buyer Network")
    st.markdown("*Get exclusive access to deals that match your investment criteria*")
    
    with st.form("buyer_qualification_form"):
        st.markdown("### Investor Profile")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *")
            email = st.text_input("Email Address *")
        
        with col2:
            phone = st.text_input("Phone Number *")
            location = st.text_input("Primary Investment Markets *", 
                                   placeholder="e.g., Atlanta, Birmingham, Memphis")
        
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
                else:
                    st.error(message)
            else:
                st.error("Please fill in all required fields (marked with *)")

def show_pricing():
    """Display pricing plans"""
    st.markdown("## Choose Your Growth Plan")
    st.markdown("*Scale your real estate business with the right tools and support*")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <h3>Starter</h3>
            <div class="plan-price">$97</div>
            <p><em>per month</em></p>
            <ul style="text-align: left; margin: 1rem 0;">
                <li>Access to basic deal flow</li>
                <li>Standard buyer database (5K+ buyers)</li>
                <li>Basic deal analysis tools</li>
                <li>Email support</li>
                <li>Monthly market reports</li>
                <li>Discord community access</li>
                <li>Mobile app access</li>
            </ul>
            <p><strong>Perfect for:</strong><br>New investors getting started</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Free Trial", key="starter"):
            st.success("You've selected the Starter plan! Redirecting to checkout...")
    
    with col2:
        st.markdown("""
        <div class="pricing-card featured">
            <div style="background: #f59e0b; color: white; padding: 0.5rem; border-radius: 15px; margin-bottom: 1rem;">
                <strong>MOST POPULAR</strong>
            </div>
            <h3>Professional</h3>
            <div class="plan-price">$197</div>
            <p><em>per month</em></p>
            <ul style="text-align: left; margin: 1rem 0;">
                <li>Everything in Starter</li>
                <li>Premium buyer network (15K+ buyers)</li>
                <li>AI-powered deal matching</li>
                <li>Advanced analytics & reporting</li>
                <li>Priority deal notifications</li>
                <li>Live training sessions (weekly)</li>
                <li>Contract templates & e-signatures</li>
                <li>Phone support</li>
                <li>CRM & lead management</li>
            </ul>
            <p><strong>Perfect for:</strong><br>Active investors ready to scale</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Most Popular Choice", key="professional"):
            st.success("You've selected the Professional plan! Redirecting to checkout...")
    
    with col3:
        st.markdown("""
        <div class="pricing-card">
            <h3>Elite</h3>
            <div class="plan-price">$397</div>
            <p><em>per month</em></p>
            <ul style="text-align: left; margin: 1rem 0;">
                <li>Everything in Professional</li>
                <li>Exclusive off-market deals</li>
                <li>Personal deal coach</li>
                <li>Direct lender connections</li>
                <li>Custom market analysis</li>
                <li>White-glove transaction support</li>
                <li>Mastermind group access</li>
                <li>API access for automation</li>
                <li>Dedicated account manager</li>
            </ul>
            <p><strong>Perfect for:</strong><br>High-volume investors & teams</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Go Elite", key="elite"):
            st.success("You've selected the Elite plan! Redirecting to checkout...")

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Features", "Join Network", "Pricing", "Login/Signup"])

# Main content based on navigation
if page == "Home":
    show_hero()
    show_stats()
    show_features()
elif page == "Features":
    show_features()
elif page == "Join Network":
    show_buyer_qualification()
elif page == "Pricing":
    show_pricing()
elif page == "Login/Signup":
    show_login_signup()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 2rem;">
    <p>&copy; 2025 Wholesale2Flip. All rights reserved. | Built for serious real estate investors.</p>
    <p>📧 hello@wholesale2flip.com | 📞 (555) 123-FLIP</p>
</div>
""", unsafe_allow_html=True)