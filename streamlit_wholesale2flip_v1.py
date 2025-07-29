import streamlit as st
import random
import time
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Wholesale2Flip Cartel - V1",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    .stDeployButton {display:none;}
    .stDecoration {display:none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #1a0033 0%, #2d1b4e 25%, #4a2c7a 50%, #2d1b4e 75%, #1a0033 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Header styling */
    .header {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(124, 58, 237, 0.2);
        padding: 1rem 2rem;
        margin-bottom: 2rem;
        border-radius: 10px;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .logo-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        font-size: 1rem;
    }
    
    .logo-text {
        color: white;
    }
    
    .v1-text {
        font-size: 1.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .free-text {
        font-size: 0.65rem;
        color: #10b981;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 4rem 0;
        margin: 2rem 0;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 50%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #9ca3af;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    .upgrade-banner {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
        border: 2px solid #a855f7;
    }
    
    .upgrade-text {
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .upgrade-features {
        color: #e0e7ff;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
    
    /* Limited feature styling */
    .limited-card {
        background: rgba(0, 0, 0, 0.4);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(245, 158, 11, 0.3);
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        position: relative;
    }
    
    .limited-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        color: white;
        font-weight: 600;
    }
    
    .locked-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        color: #f59e0b;
    }
    
    /* Basic cards */
    .basic-card {
        background: rgba(0, 0, 0, 0.4);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(16, 185, 129, 0.3);
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .basic-stat-card {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(20px);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #10b981;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #9ca3af;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.4);
    }
    
    /* Pro button styling */
    .pro-button {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #f59e0b;
        border-radius: 15px;
        padding: 1rem;
        font-size: 1.1rem;
        color: #1f2937;
    }
    
    /* Free tier limitations */
    .limitation-banner {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid #f59e0b;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #f59e0b;
        text-align: center;
        font-weight: 600;
    }
    
    /* Comparison table */
    .comparison-table {
        background: rgba(0, 0, 0, 0.4);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    .feature-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .feature-name {
        color: white;
        font-weight: 500;
    }
    
    .feature-v1 {
        color: #f59e0b;
        font-weight: 600;
    }
    
    .feature-pro {
        color: #7c3aed;
        font-weight: 600;
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'
if 'search_count' not in st.session_state:
    st.session_state.search_count = 0
if 'daily_searches' not in st.session_state:
    st.session_state.daily_searches = 0

# Daily search limit for free tier
DAILY_SEARCH_LIMIT = 3

# Helper functions
def generate_basic_property_data(address):
    """Generate basic property data for free tier"""
    estimated_value = random.randint(150000, 300000)
    
    return {
        'address': address,
        'estimated_value': estimated_value,
        'property_type': 'Single Family Home',
        'basic_info': True
    }

def check_daily_limit():
    """Check if user has exceeded daily search limit"""
    return st.session_state.daily_searches >= DAILY_SEARCH_LIMIT

# Header
st.markdown("""
<div class="header">
    <div class="logo-container">
        <div class="logo-icon">W2F</div>
        <div class="logo-text">
            <div class="v1-text">V1</div>
            <div class="free-text">FREE</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Upgrade Banner
st.markdown("""
<div class="upgrade-banner">
    <div class="upgrade-text">🚀 Upgrade to Wholesale2Flip PRO for Full Access!</div>
    <div class="upgrade-features">
        Unlimited searches • Advanced analytics • Buyer networks • Lightning leads • Full pipeline management
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("⭐ UPGRADE TO PRO - $97/Month", key="upgrade_pro"):
        st.balloons()
        st.success("🎉 Redirecting to PRO subscription page...")
        st.info("💳 You'll get access to all premium features including unlimited searches, advanced analytics, buyer networks, and lightning leads!")

# Navigation
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏠 Home", key="nav_home"):
        st.session_state.current_page = 'Home'

with col2:
    if st.button("🏢 Basic Search", key="nav_search"):
        st.session_state.current_page = 'Basic Search'

with col3:
    if st.button("📊 Features", key="nav_features"):
        st.session_state.current_page = 'Features'

with col4:
    if st.button("💎 Compare Plans", key="nav_compare"):
        st.session_state.current_page = 'Compare Plans'

with col5:
    if st.button("📞 Contact", key="nav_contact"):
        st.session_state.current_page = 'Contact'

# Page routing
if st.session_state.current_page == 'Home':
    # HOME PAGE
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Welcome to Wholesale2Flip</h1>
        <p class="hero-subtitle">Start your real estate wholesaling journey with our free V1 platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="basic-card">
            <h4>🔍 Basic Property Search</h4>
            <p>Search up to 3 properties per day</p>
            <p>Get basic property information</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="limited-card">
            <h4>🧠 AI-Powered Analysis</h4>
            <p>• GPT-powered deal underwriting</p>
            <p>• Multifamily & creative finance tools</p>
            <p>• Script generation for sellers/buyers</p>
            <p>• 5x5 objection handling scripts</p>
            <div class="limited-overlay">
                <div class="locked-icon">🔒</div>
                <div>PRO Feature</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="limited-card">
            <h4>🧠 AI-Powered Tools</h4>
            <p>GPT deal analysis & script generation</p>
            <div class="limited-overlay">
                <div class="locked-icon">🔒</div>
                <div>PRO Only</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="limited-card">
            <h4>📊 Advanced Analytics</h4>
            <p>ARV calculations, profit analysis</p>
            <div class="limited-overlay">
                <div class="locked-icon">🔒</div>
                <div>PRO Only</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="limited-card">
            <h4>🤝 Buyer Networks</h4>
            <p>Connect with investors</p>
            <div class="limited-overlay">
                <div class="locked-icon">🔒</div>
                <div>PRO Only</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Statistics (basic)
    st.markdown("### 📈 Your Progress")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="basic-stat-card">
            <div class="stat-number">{st.session_state.search_count}</div>
            <div class="stat-label">Total Searches</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        remaining = max(0, DAILY_SEARCH_LIMIT - st.session_state.daily_searches)
        st.markdown(f"""
        <div class="basic-stat-card">
            <div class="stat-number">{remaining}</div>
            <div class="stat-label">Searches Left Today</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="basic-stat-card">
            <div class="stat-number">∞</div>
            <div class="stat-label">PRO Searches</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_page == 'AI Tools':
    # AI TOOLS PAGE (Locked for V1)
    st.markdown("# 🧠 AI-Powered Tools")
    
    # New GPT Tools Banner (Locked)
    st.markdown("""
    <div class="upgrade-banner">
        <div class="upgrade-text">🔥 NEW GPT-POWERED TOOLS – NOW LIVE IN PRO</div>
        <div class="upgrade-features">
            Built by The Treasury — builders in the lab, not gurus on the 'Gram
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="limited-card">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">🧠</div>
                <div>
                    <h4 style="margin-bottom: 0.25rem;">Multifamily & Creative Deal Analyzer</h4>
                    <span style="background: #10b981; color: white; padding: 0.2rem 0.6rem; border-radius: 8px; font-size: 0.7rem; font-weight: 600;">BETA</span>
                </div>
            </div>
            
            <div style="margin-bottom: 1rem;">
                <p><strong>💡 What It Does:</strong></p>
                <ul style="font-size: 0.9rem; margin-left: 1rem; color: #e5e7eb;">
                    <li>🔍 Analyze Multifamily, SubTo, Seller Finance deals</li>
                    <li>📈 Return Low/Med/High offer tiers</li>
                    <li>💸 Calculate Down Payments + Entry Fees</li>
                    <li>🧾 Generate DSCR, IRR, Cap Rate, CoC</li>
                    <li>📄 Create investor-ready summaries & PDFs</li>
                </ul>
            </div>
            
            <div style="background: rgba(16, 185, 129, 0.1); border-radius: 8px; padding: 0.75rem; margin-bottom: 1rem;">
                <p style="color: #10b981; font-weight: 600; margin-bottom: 0.25rem;">🎯 Quick Command:</p>
                <code style="background: rgba(0,0,0,0.5); color: #34d399; padding: 0.25rem 0.5rem; border-radius: 4px; font-family: monospace; font-size: 0.8rem;">-Underwrite</code>
            </div>
            
            <div class="limited-overlay">
                <div class="locked-icon">🔒</div>
                <div>PRO Only</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="limited-card">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">👑</div>
                <div>
                    <h4 style="margin-bottom: 0.25rem;">Empire ScriptMaster AI</h4>
                    <span style="background: #f59e0b; color: white; padding: 0.2rem 0.6rem; border-radius: 8px; font-size: 0.7rem; font-weight: 600;">PHASE IV</span>
                </div>
            </div>
            
            <div style="margin-bottom: 1rem;">
                <p><strong>🎯 Your Script Squad in Code:</strong></p>
                <ul style="font-size: 0.9rem; margin-left: 1rem; color: #e5e7eb;">
                    <li>📞 Every seller script</li>
                    <li>🤝 Every buyer objection</li>
                    <li>📈 Every agent pitch</li>
                    <li>🎬 5x5 format: 5 responses × 5 reply options</li>
                    <li>✅ Roleplay-ready & closer-tested</li>
                </ul>
            </div>
            
            <div style="background: rgba(245, 158, 11, 0.1); border-radius: 8px; padding: 0.75rem; margin-bottom: 1rem;">
                <p style="color: #f59e0b; font-weight: 600; margin-bottom: 0.25rem;">⚡ Quick Command:</p>
                <code style="background: rgba(0,0,0,0.5); color: #fbbf24; padding: 0.25rem 0.5rem; border-radius: 4px; font-family: monospace; font-size: 0.8rem;">-Scriptai</code>
            </div>
            
            <div class="limited-overlay">
                <div class="locked-icon">🔒</div>
                <div>PRO Only</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Example Use Cases (Limited Preview)
    st.markdown("### 💡 Example Use Cases (PRO Only)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="limited-card" style="padding: 1rem;">
            <h5 style="color: #10b981; margin-bottom: 0.5rem;">🏢 Multifamily Analysis</h5>
            <p style="color: #e5e7eb; font-style: italic; font-size: 0.85rem;">"Analyze this 12-unit apartment building at $1.2M with $8,500/month gross rents"</p>
            <div class="limited-overlay">
                <div class="locked-icon">🔒</div>
                <div style="font-size: 0.8rem;">Upgrade to PRO</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="limited-card" style="padding: 1rem;">
            <h5 style="color: #f59e0b; margin-bottom: 0.5rem;">📞 Seller Scripts</h5>
            <p style="color: #e5e7eb; font-style: italic; font-size: 0.85rem;">"Build a Wrap script for a seller with $80K equity who wants full price"</p>
            <div class="limited-overlay">
                <div class="locked-icon">🔒</div>
                <div style="font-size: 0.8rem;">Upgrade to PRO</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Upgrade CTA
    st.markdown("""
    <div class="upgrade-banner">
        <div class="upgrade-text">🎯 Unlock GPT-Powered Deal Analysis & Script Generation</div>
        <div class="upgrade-features">
            Join thousands using our AI tools to close more deals faster
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Upgrade to PRO for AI Tools", key="upgrade_ai_tools"):
            st.balloons()
            st.success("🎉 Unlock AI-powered deal analysis and script generation!")

elif st.session_state.current_page == 'Basic Search':
    # BASIC SEARCH PAGE
    st.markdown("# 🔍 Basic Property Search")
    
    # Daily limit warning
    if check_daily_limit():
        st.markdown("""
        <div class="limitation-banner">
            ⚠️ You've reached your daily limit of 3 searches. Upgrade to PRO for unlimited searches!
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Upgrade to PRO for Unlimited Searches", key="upgrade_unlimited"):
            st.success("🎉 Redirecting to PRO subscription...")
    else:
        st.info(f"🔢 Free searches remaining today: {DAILY_SEARCH_LIMIT - st.session_state.daily_searches}")
        
        # Address search
        address = st.text_input("Enter Property Address:", placeholder="123 Main St, Dallas TX", key="basic_search")
        
        if st.button("🔍 Search Property (Basic)", key="basic_search_btn", disabled=check_daily_limit()):
            if address:
                with st.spinner("🔍 Searching property..."):
                    time.sleep(1.5)
                    st.session_state.daily_searches += 1
                    st.session_state.search_count += 1
                    property_data = generate_basic_property_data(address)
                    
                    st.success("✅ Basic property information found!")
                    
                    # Basic property info
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="basic-card">
                            <h4>🏠 Basic Property Info</h4>
                            <p><strong>Address:</strong> {property_data['address']}</p>
                            <p><strong>Estimated Value:</strong> ${property_data['estimated_value']:,}</p>
                            <p><strong>Property Type:</strong> {property_data['property_type']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div class="limited-card">
                            <h4>💰 Advanced Analysis</h4>
                            <p>ARV, repair costs, profit potential</p>
                            <div class="limited-overlay">
                                <div class="locked-icon">🔒</div>
                                <div>Upgrade to PRO</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Upgrade prompt
                    st.markdown("""
                    <div class="upgrade-banner">
                        <div class="upgrade-text">🎯 Want detailed property analysis?</div>
                        <div class="upgrade-features">
                            Get ARV calculations, repair estimates, profit potential, buyer connections, and more!
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("⭐ See Full Analysis in PRO", key="upgrade_analysis"):
                        st.success("🚀 Upgrade to PRO to unlock advanced property analysis!")
            else:
                st.error("❌ Please enter a valid address")

elif st.session_state.current_page == 'Features':
    # FEATURES PAGE
    st.markdown("# 🎯 Platform Features")
    
    st.markdown("## 🆓 V1 Free Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="basic-card">
            <h4>✅ Basic Property Search</h4>
            <p>• 3 searches per day</p>
            <p>• Basic property information</p>
            <p>• Property type identification</p>
            <p>• Estimated values</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="basic-card">
            <h4>✅ Learning Resources</h4>
            <p>• Basic wholesaling guides</p>
            <p>• Getting started tutorials</p>
            <p>• Community access</p>
            <p>• Email support</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("## 💎 PRO Features (Locked)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="limited-card">
            <h4>🚀 Advanced Analytics</h4>
            <p>• Unlimited property searches</p>
            <p>• ARV calculations</p>
            <p>• Repair cost estimates</p>
            <p>• Profit potential analysis</p>
            <div class="limited-overlay">
                <div class="locked-icon">🔒</div>
                <div>PRO Feature</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="limited-card">
            <h4>🤝 Buyer Networks</h4>
            <p>• State-by-state buyer lists</p>
            <p>• Fix & flip investors</p>
            <p>• Creative finance buyers</p>
            <p>• Direct buyer connections</p>
            <div class="limited-overlay">
                <div class="locked-icon">🔒</div>
                <div>PRO Feature</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="limited-card">
            <h4>⚡ Lightning Leads</h4>
            <p>• Premium lead generation</p>
            <p>• Off-market opportunities</p>
            <p>• Hot deal alerts</p>
            <p>• Priority notifications</p>
            <div class="limited-overlay">
                <div class="locked-icon">🔒</div>
                <div>PRO Feature</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Upgrade CTA
    st.markdown("""
    <div class="upgrade-banner">
        <div class="upgrade-text">🎯 Ready to unlock all features?</div>
        <div class="upgrade-features">
            Join thousands of successful wholesalers using Wholesale2Flip PRO
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Upgrade to PRO Now", key="upgrade_features"):
        st.balloons()
        st.success("🎉 Welcome to the PRO experience!")

elif st.session_state.current_page == 'Compare Plans':
    # COMPARE PLANS PAGE
    st.markdown("# 💎 Compare Plans")
    
    # Plan comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.1); border: 2px solid #10b981; border-radius: 20px; padding: 2rem; text-align: center;">
            <h3 style="color: #10b981; margin-bottom: 1rem;">🆓 V1 FREE</h3>
            <div style="font-size: 2rem; font-weight: bold; color: white; margin-bottom: 1rem;">$0</div>
            <div style="color: #9ca3af; margin-bottom: 2rem;">per month</div>
            
            <div style="text-align: left; color: white;">
                <p>✅ 3 property searches per day</p>
                <p>✅ Basic property information</p>
                <p>✅ Learning resources</p>
                <p>✅ Community access</p>
                <p>✅ Email support</p>
                <br>
                <p style="color: #9ca3af;">❌ Advanced analytics</p>
                <p style="color: #9ca3af;">❌ Buyer networks</p>
                <p style="color: #9ca3af;">❌ Lightning leads</p>
                <p style="color: #9ca3af;">❌ Pipeline management</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🎉 You're currently on the FREE plan!")
    
    with col2:
        st.markdown("""
        <div style="background: rgba(124, 58, 237, 0.1); border: 2px solid #7c3aed; border-radius: 20px; padding: 2rem; text-align: center; position: relative;">
            <div style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: #7c3aed; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">MOST POPULAR</div>
            
            <h3 style="color: #7c3aed; margin-bottom: 1rem;">🚀 PRO</h3>
            <div style="font-size: 2rem; font-weight: bold; color: white; margin-bottom: 1rem;">$97</div>
            <div style="color: #9ca3af; margin-bottom: 2rem;">per month</div>
            
            <div style="text-align: left; color: white;">
                <p>✅ Everything in FREE</p>
                <p>✅ Unlimited property searches</p>
                <p>✅ Advanced property analytics</p>
                <p>✅ ARV & profit calculations</p>
                <p>✅ State buyer networks</p>
                <p>✅ Direct buyer connections</p>
                <p>✅ Pipeline management</p>
                <p>✅ Lightning leads ($39.99 add-on)</p>
                <p>✅ Priority support</p>
                <p>✅ Live training sessions</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⭐ UPGRADE TO PRO", key="upgrade_comparison"):
            st.balloons()
            st.success("🎉 Thank you for upgrading! Redirecting to checkout...")
    
    # Feature comparison table
    st.markdown("### 📊 Detailed Feature Comparison")
    
    st.markdown("""
    <div class="comparison-table">
        <div class="feature-row">
            <div class="feature-name">Property Searches</div>
            <div class="feature-v1">3 per day</div>
            <div class="feature-pro">Unlimited</div>
        </div>
        <div class="feature-row">
            <div class="feature-name">Property Analysis</div>
            <div class="feature-v1">Basic Info</div>
            <div class="feature-pro">Advanced Analytics</div>
        </div>
        <div class="feature-row">
            <div class="feature-name">ARV Calculations</div>
            <div class="feature-v1">❌</div>
            <div class="feature-pro">✅</div>
        </div>
        <div class="feature-row">
            <div class="feature-name">Repair Estimates</div>
            <div class="feature-v1">❌</div>
            <div class="feature-pro">✅</div>
        </div>
        <div class="feature-row">
            <div class="feature-name">Buyer Networks</div>
            <div class="feature-v1">❌</div>
            <div class="feature-pro">✅</div>
        </div>
        <div class="feature-row">
            <div class="feature-name">Pipeline Management</div>
            <div class="feature-v1">❌</div>
            <div class="feature-pro">✅</div>
        </div>
        <div class="feature-row">
            <div class="feature-name">GPT-Powered Analysis</div>
            <div class="feature-v1">❌</div>
            <div class="feature-pro">✅</div>
        </div>
        <div class="feature-row">
            <div class="feature-name">Script Generation AI</div>
            <div class="feature-v1">❌</div>
            <div class="feature-pro">✅</div>
        </div>
        <div class="feature-row">
            <div class="feature-name">Multifamily Underwriter</div>
            <div class="feature-v1">❌</div>
            <div class="feature-pro">✅</div>
        </div>
        <div class="feature-row">
            <div class="feature-name">Empire ScriptMaster AI</div>
            <div class="feature-v1">❌</div>
            <div class="feature-pro">✅</div>
        </div>
        <div class="feature-row">
            <div class="feature-name">Support</div>
            <div class="feature-v1">Email</div>
            <div class="feature-pro">Priority + Live Chat</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_page == 'Contact':
    # CONTACT PAGE
    st.markdown("# 📞 Contact Us")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="basic-card">
            <h4>📧 Get in Touch</h4>
            <p><strong>Email:</strong> support@wholesale2flipcartel.com</p>
            <p><strong>Phone:</strong> (555) 123-4567</p>
            <p><strong>Hours:</strong> Mon-Fri 9AM-6PM EST</p>
            <br>
            <p><strong>Sales:</strong> sales@wholesale2flipcartel.com</p>
            <p><strong>Support:</strong> help@wholesale2flipcartel.com</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="basic-card">
            <h4>🤝 Connect With Us</h4>
            <p>• Facebook: @Wholesale2FlipCartel</p>
            <p>• Instagram: @W2FCartel</p>
            <p>• YouTube: Wholesale2Flip Channel</p>
            <p>• LinkedIn: Wholesale2Flip Cartel</p>
            <br>
            <p>• Discord Community</p>
            <p>• Telegram Group</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Contact form
    st.markdown("### 💬 Send us a Message")
    
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        subject = st.selectbox("Subject", [
            "General Question",
            "Technical Support", 
            "Billing Question",
            "Feature Request",
            "Partnership Inquiry"
        ])
        message = st.text_area("Message", height=150)
        
        if st.form_submit_button("📤 Send Message"):
            if name and email and message:
                st.success("✅ Thank you! Your message has been sent. We'll get back to you within 24 hours.")
                st.balloons()
            else:
                st.error("❌ Please fill in all required fields")
    
    # FAQ Section
    st.markdown("### ❓ Frequently Asked Questions")
    
    with st.expander("🔍 How many searches do I get with the free version?"):
        st.write("The V1 free version includes 3 property searches per day. This resets every 24 hours. Upgrade to PRO for unlimited searches!")
    
    with st.expander("💎 What's included in the PRO version?"):
        st.write("PRO includes unlimited searches, advanced property analytics, ARV calculations, buyer networks, pipeline management, and priority support. Lightning Leads is available as an add-on for $39.99/month.")
    
    with st.expander("💳 How does billing work?"):
        st.write("PRO is billed monthly at $97/month. You can cancel anytime. Lightning Leads is an optional add-on for $39.99/month.")
    
    with st.expander("🤝 Do you offer buyer networks in all states?"):
        st.write("Our PRO version includes buyer networks in all 50 states. We have Fix & Flip buyers, Creative Finance buyers, and Section 8 buyers in our database.")
    
    with st.expander("📞 What kind of support do you provide?"):
        st.write("Free users get email support. PRO users get priority support, live chat, and access to live training sessions.")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 4rem; padding: 2rem; color: #6b7280; border-top: 1px solid rgba(245, 158, 11, 0.2);">
    <div style="margin-bottom: 1rem;">
        <strong style="color: #f59e0b;">Ready to upgrade?</strong>
        <p style="margin: 0.5rem 0;">Join thousands of successful wholesalers using Wholesale2Flip PRO</p>
    </div>
    <p>© 2025 Wholesale2Flip Cartel V1. All rights reserved.</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">Built with ❤️ using Streamlit | Free Tier</p>
</div>
""", unsafe_allow_html=True)

# Persistent upgrade reminder
if st.session_state.search_count > 5:
    st.sidebar.markdown("""
    ### 🚀 Ready for PRO?
    
    You've made **{}** searches! 
    
    **Upgrade benefits:**
    - ✅ Unlimited searches
    - ✅ Advanced analytics  
    - ✅ Buyer networks
    - ✅ Pipeline management
    
    **Special offer: First month 50% off!**
    """.format(st.session_state.search_count))
    
    if st.sidebar.button("⭐ Upgrade Now - $48.50", key="sidebar_upgrade"):
        st.balloons()
        st.success("🎉 Thank you for upgrading to PRO!")

# Reset daily searches (for demo purposes)
if st.sidebar.button("🔄 Reset Daily Searches (Demo)", key="reset_demo"):
    st.session_state.daily_searches = 0
    st.success("✅ Daily searches reset for demo purposes!")