import streamlit as st
import random
import time
import json
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Wholesale2Flip Cartel - PRO",
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
    
    .pro-text {
        font-size: 1.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .beta-text {
        font-size: 0.65rem;
        color: #9ca3af;
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
        font-size: 4rem;
        font-weight: 900;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #10b981 0%, #34d399 50%, #6ee7b7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: #9ca3af;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Cards */
    .info-card {
        background: rgba(0, 0, 0, 0.4);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(124, 58, 237, 0.3);
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .stat-card {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(20px);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 900;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #9ca3af;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
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
        box-shadow: 0 8px 20px rgba(124, 58, 237, 0.4);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95);
        border: none;
        border-radius: 15px;
        padding: 1rem;
        font-size: 1.1rem;
        color: #1f2937;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Tutorial cards */
    .tutorial-card {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(20px);
    }
    
    .coming-soon {
        background: rgba(0, 0, 0, 0.3);
        border: 2px dashed #f59e0b;
        color: #f59e0b;
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
    }
    
    /* States list */
    .state-item {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        color: white;
        font-weight: 600;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    /* Profile form */
    .profile-form {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(20px);
    }
    
    /* Lightning leads */
    .leads-card {
        background: rgba(124, 58, 237, 0.1);
        border: 2px solid #7c3aed;
        border-radius: 25px;
        padding: 3rem;
        text-align: center;
        backdrop-filter: blur(20px);
    }
    
    .price-btn {
        background: #7c3aed;
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 12px;
        font-size: 1.2rem;
        font-weight: 700;
        cursor: pointer;
    }
    
    /* Hide Streamlit elements */
    .stSelectbox > div > div {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 10px;
        color: white;
    }
    
    .stTab {
        background: rgba(0, 0, 0, 0.4);
        border-radius: 10px;
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
if 'user_properties' not in st.session_state:
    st.session_state.user_properties = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'firstName': 'james',
        'lastName': 'edgar', 
        'email': 'thetreasury@jbhousinginvestments.com',
        'businessName': '',
        'phone': ''
    }

# Helper functions
def generate_property_data(address):
    """Generate realistic property analysis data"""
    estimated_value = random.randint(150000, 350000)
    arv = random.randint(200000, 450000)
    repair_costs = random.randint(15000, 55000)
    profit_potential = arv - estimated_value - repair_costs
    
    return {
        'address': address,
        'estimated_value': estimated_value,
        'arv': arv,
        'repair_costs': repair_costs,
        'profit_potential': profit_potential,
        'year_built': random.randint(1970, 2020),
        'sqft': random.randint(1200, 2700),
        'property_type': 'Single Family Home',
        'buyers': {
            'fix_flip': random.randint(3, 18),
            'creative': random.randint(2, 10),
            'rental': random.randint(1, 13)
        }
    }

def generate_state_data(state):
    """Generate buyer network data for a state"""
    return {
        'active_buyers': random.randint(15, 45),
        'success_rate': random.randint(80, 95),
        'avg_response_time': random.randint(2, 6),
        'avg_deal_size': random.randint(150000, 300000),
        'hot_deals': random.randint(5, 25),
        'avg_close_time': random.randint(10, 20)
    }

# Header
st.markdown"""
<div class="header">
    <div class="logo-container">
        <div class="logo-icon">W2F</div>
        <div class="logo-text">
            <div class="pro-text">PRO</div>
            <div class="beta-text">BETA</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("🏠 Home", key="nav_home"):
        st.session_state.current_page = 'Home'

with col2:
    if st.button("🏢 BuyBoxes", key="nav_buyboxes"):
        st.session_state.current_page = 'BuyBoxes'

with col3:
    if st.button("📊 Pipeline", key="nav_pipeline"):
        st.session_state.current_page = 'Pipeline'

with col4:
    if st.button("🎓 Tutorials", key="nav_tutorials"):
        st.session_state.current_page = 'Tutorials'

with col5:
    if st.button("👤 Profile", key="nav_profile"):
        st.session_state.current_page = 'Profile'

with col6:
    if st.button("⚡ Leads", key="nav_leads"):
        st.session_state.current_page = 'Lightning Leads'

# Page routing
if st.session_state.current_page == 'Home':
    # HOME PAGE
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Pop In Your Address</h1>
        <p class="hero-subtitle">Let's find you a buyer</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Address search
    address = st.text_input("", placeholder="Enter address...", key="address_search", label_visibility="collapsed")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔍 Search Property", key="search_btn"):
            if address:
                with st.spinner("🔍 Analyzing property..."):
                    time.sleep(2)
                    property_data = generate_property_data(address)
                    
                    st.success("✅ Property analysis complete!")
                    
                    # Display property analysis
                    st.markdown("### 🏠 Property Analysis Results")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="info-card">
                            <h4>📊 Property Details</h4>
                            <p><strong>Estimated Value:</strong> ${property_data['estimated_value']:,}</p>
                            <p><strong>Property Type:</strong> {property_data['property_type']}</p>
                            <p><strong>Year Built:</strong> {property_data['year_built']}</p>
                            <p><strong>Sq Ft:</strong> {property_data['sqft']:,} sq ft</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        grade = 'A' if property_data['profit_potential'] > 30000 else 'B'
                        st.markdown(f"""
                        <div class="info-card">
                            <h4>💰 Investment Potential</h4>
                            <p><strong>ARV:</strong> ${property_data['arv']:,}</p>
                            <p><strong>Repair Estimate:</strong> ${property_data['repair_costs']:,}</p>
                            <p><strong>Profit Potential:</strong> ${property_data['profit_potential']:,}</p>
                            <p><strong>Investment Grade:</strong> <span style="background: {'#10b981' if grade == 'A' else '#f59e0b'}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-weight: bold;">{grade}</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div class="info-card">
                            <h4>🎯 Available Buyers</h4>
                            <p><strong>Fix & Flip:</strong> {property_data['buyers']['fix_flip']} buyers</p>
                            <p><strong>Creative Finance:</strong> {property_data['buyers']['creative']} buyers</p>
                            <p><strong>Rental Investors:</strong> {property_data['buyers']['rental']} buyers</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("🤝 Connect to Buyers", key="connect_buyers"):
                            st.success("🤝 Connecting you to buyers...")
                            st.session_state.current_page = 'BuyBoxes'
                            st.rerun()
                    
                    with col2:
                        if st.button("💾 Save to Pipeline", key="save_pipeline"):
                            st.session_state.user_properties.append(property_data)
                            st.success("💾 Property saved to pipeline!")
                            st.session_state.current_page = 'Pipeline'
                            st.rerun()
                    
                    with col3:
                        if st.button("📊 Get Full Report", key="full_report"):
                            st.info("📊 Generating detailed report...")
            else:
                st.error("❌ Please enter a valid address")

elif st.session_state.current_page == 'BuyBoxes':
    # BUYBOXES PAGE
    st.markdown("# 🏢 BuyBoxes")
    
    # View toggle
    col1, col2 = st.columns([3, 1])
    with col2:
        view_mode = st.toggle("List View", value=True)
        if view_mode:
            st.info("🗺️ Switched to List View")
        else:
            st.info("🗺️ Switched to Map View")
    
    # Buyer tabs
    buyer_type = st.selectbox("Select Buyer Type:", 
                             ["Fix & Flip Buyers", "Creative Buyers", "Section 8 Buyers"])
    
    st.info(f"📋 Showing {buyer_type}")
    
    # States list
    st.markdown("### 📍 Select a State")
    
    states = ["ALABAMA", "ARIZONA", "COLORADO", "DELAWARE", "FLORIDA", "GEORGIA", "IDAHO", "INDIANA"]
    
    cols = st.columns(2)
    for i, state in enumerate(states):
        with cols[i % 2]:
            if st.button(state, key=f"state_{state}"):
                state_data = generate_state_data(state)
                
                st.success(f"📊 Loaded buyer network for {state}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div class="info-card">
                        <h4>📊 Active Network</h4>
                        <p><strong>Active Buyers:</strong> {state_data['active_buyers']}</p>
                        <p><strong>Success Rate:</strong> {state_data['success_rate']}%</p>
                        <p><strong>Avg Response Time:</strong> {state_data['avg_response_time']} hours</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="info-card">
                        <h4>💰 Market Data</h4>
                        <p><strong>Average Deal Size:</strong> ${state_data['avg_deal_size']:,}</p>
                        <p><strong>Hot Deals This Week:</strong> {state_data['hot_deals']}</p>
                        <p><strong>Avg Time to Close:</strong> {state_data['avg_close_time']} days</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"👥 View All Buyers in {state}", key=f"view_buyers_{state}"):
                        st.info(f"📋 Loading buyer directory for {state}...")
                
                with col2:
                    if st.button(f"📝 Submit Deal in {state}", key=f"submit_deal_{state}"):
                        st.info(f"📝 Opening deal submission form for {state}...")

elif st.session_state.current_page == 'Pipeline':
    # PIPELINE PAGE
    st.markdown("# 📊 Pipeline")
    
    # Stats
    total_properties = len(st.session_state.user_properties)
    waiting_properties = len([p for p in st.session_state.user_properties if not p.get('submitted', False)])
    submitted_properties = len([p for p in st.session_state.user_properties if p.get('submitted', False)])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_properties}</div>
            <div class="stat-label">Total Properties</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{waiting_properties}</div>
            <div class="stat-label">Properties waiting for dispo</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{submitted_properties}</div>
            <div class="stat-label">Properties submitted for dispo</div>
        </div>
        """, unsafe_allow_html=True)
    
    if total_properties == 0:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; color: #9ca3af; background: rgba(0, 0, 0, 0.2); border-radius: 20px; border: 2px dashed rgba(124, 58, 237, 0.3);">
            <h2 style="color: white; margin-bottom: 1rem;">No pipeline available</h2>
            <p>Submit your first property to get started with your investment pipeline.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### 🏠 Your Properties")
        for i, prop in enumerate(st.session_state.user_properties):
            with st.expander(f"📍 {prop['address']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Estimated Value:** ${prop['estimated_value']:,}")
                    st.write(f"**ARV:** ${prop['arv']:,}")
                    st.write(f"**Repair Costs:** ${prop['repair_costs']:,}")
                
                with col2:
                    st.write(f"**Profit Potential:** ${prop['profit_potential']:,}")
                    st.write(f"**Year Built:** {prop['year_built']}")
                    st.write(f"**Square Feet:** {prop['sqft']:,}")
                
                if st.button(f"🚀 Submit for Disposition", key=f"submit_{i}"):
                    st.session_state.user_properties[i]['submitted'] = True
                    st.success("✅ Property submitted for disposition!")
                    st.rerun()

elif st.session_state.current_page == 'Tutorials':
    # TUTORIALS PAGE
    st.markdown("# 🎓 Tutorials")
    
    st.markdown("## 1. Getting Started")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="coming-soon">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
            <h3>COMING SOON</h3>
            <p>In Development</p>
            <br>
            <h4 style="color: white;">How Wholesale2Flip Cartel works</h4>
            <p style="font-size: 0.9rem;">Learn about how Wholesale2Flip Cartel makes wholesaling extremely easy for beginners</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tutorial-card">
            <h4>▶️ How Wholesaling Works</h4>
            <p>How you can make money with Wholesale2Flip Cartel</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ Play Tutorial", key="play_wholesaling"):
            st.success("▶️ Playing tutorial: How Wholesaling Works")
    
    st.markdown("## 2. How To Submit Deals")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="tutorial-card">
            <h4>▶️ Deal Submission Process</h4>
            <p>Learn how to properly submit your deals for maximum success</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ Play Tutorial", key="play_submission"):
            st.success("▶️ Playing tutorial: Deal Submission Process")
    
    with col2:
        st.markdown("""
        <div class="coming-soon">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚡</div>
            <h4>COMING SOON</h4>
            <p>In Development</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="coming-soon">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚡</div>
            <h4>COMING SOON</h4>
            <p>In Development</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="coming-soon">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚡</div>
            <h4>COMING SOON</h4>
            <p>In Development</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_page == 'Profile':
    # PROFILE PAGE
    st.markdown("# 👤 Profile")
    
    tab1, tab2 = st.tabs(["My Account", "Subscription"])
    
    with tab1:
        st.markdown("""
        <div class="profile-form">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name", value=st.session_state.user_profile['firstName'])
            email = st.text_input("Email", value=st.session_state.user_profile['email'])
            phone = st.text_input("Phone", value=st.session_state.user_profile['phone'])
        
        with col2:
            last_name = st.text_input("Last Name", value=st.session_state.user_profile['lastName'])
            business_name = st.text_input("Business Name", value=st.session_state.user_profile['businessName'])
        
        if st.button("💾 Save Changes", key="save_profile"):
            if first_name and last_name and email:
                if '@' in email:
                    st.session_state.user_profile.update({
                        'firstName': first_name,
                        'lastName': last_name,
                        'email': email,
                        'businessName': business_name,
                        'phone': phone
                    })
                    st.success("✅ Profile updated successfully!")
                else:
                    st.error("❌ Please enter a valid email address")
            else:
                st.error("❌ Please fill in all required fields")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.info("💳 Subscription management coming soon...")

elif st.session_state.current_page == 'Lightning Leads':
    # LIGHTNING LEADS PAGE
    st.markdown("# ⚡ Lightning Leads")
    
    st.markdown("""
    <div class="leads-card">
        <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
            <span style="font-size: 2rem;">⚡</span>
            <h1 style="color: white; font-size: 2.5rem; font-weight: 800;">Lightning Leads</h1>
        </div>
        <p style="color: #9ca3af; font-size: 1.2rem; margin-bottom: 2rem;">How do Lightning Leads Work?</p>
        
        <div style="background: rgba(0, 0, 0, 0.4); border-radius: 15px; height: 300px; display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 2rem; border: 1px solid rgba(124, 58, 237, 0.3);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
            <h3 style="color: #f59e0b; font-size: 1.8rem; margin: 1rem 0;">COMING SOON</h3>
            <p style="color: #9ca3af;">In Development</p>
        </div>

        <div>
            <h2 style="color: white; font-size: 1.8rem; margin-bottom: 0.5rem;">Sign up for Lightning Leads</h2>
            <p style="color: #9ca3af; margin-bottom: 1.5rem;">to get unlimited access to premium on market leads</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("⚡ Subscribe for $39.99/Month", key="subscribe_leads"):
            with st.spinner("💳 Processing Lightning Leads subscription..."):
                time.sleep(2)
            st.success("⚡ Lightning Leads activated! Welcome to premium leads.")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 4rem; padding: 2rem; color: #6b7280; border-top: 1px solid rgba(124, 58, 237, 0.2);">
    <p>© 2025 Wholesale2Flip Cartel. All rights reserved.</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh for demo purposes (optional)
if st.checkbox("🔄 Auto-refresh demo data", value=False):
    time.sleep(1)
    st.rerun()