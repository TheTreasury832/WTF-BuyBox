import streamlit as st

st.markdown("""
    <style>
        .your-custom-class {
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .action-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }

        .btn-primary, .btn-secondary {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }

        .btn-primary {
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(124, 58, 237, 0.4);
        }

        .btn-secondary {
            background: rgba(0, 0, 0, 0.4);
            color: white;
            border: 1px solid rgba(124, 58, 237, 0.5);
            backdrop-filter: blur(10px);
        }

        .btn-secondary:hover {
            background: rgba(124, 58, 237, 0.2);
            transform: translateY(-1px);
        }

        .toast {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            z-index: 2000;
            max-width: 400px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            animation: slideInRight 0.3s ease;
        }

        .toast.success {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border: 1px solid #34d399;
        }

        .toast.error {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            border: 1px solid #f87171;
        }

        .toast.info {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            border: 1px solid #60a5fa;
        }

        .toast.loading {
            background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
            border: 1px solid #a78bfa;
        }

        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                gap: 1rem;
                padding: 1rem;
            }

            .nav {
                flex-wrap: wrap;
                justify-content: center;
                gap: 0.5rem;
            }

            .main-content {
                padding: 1rem;
            }

            .hero-title {
                font-size: 2.5rem;
            }

            .house-3d {
                width: 300px;
                height: 200px;
            }

            .stats-grid, .tutorial-grid {
                grid-template-columns: 1fr;
            }

            .property-info {
                grid-template-columns: 1fr;
            }

            .action-buttons {
                flex-direction: column;
            }

            .modal-content {
                width: 95%;
                margin: 1rem;
            }
        }

        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 0.8s linear infinite;
            margin-right: 0.5rem;
        }

        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }

        .nav-button:focus,
        .tab-btn:focus,
        .profile-tab:focus,
        .save-btn:focus,
        .price-btn:focus {
            outline: 2px solid #7c3aed;
            outline-offset: 2px;
        }

        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(124, 58, 237, 0.5);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(124, 58, 237, 0.7);
        }

        body {
            overflow-x: hidden;
        }

        .main-content {
            position: relative;
            z-index: 20;
        }
    </style>
""", unsafe_allow_html=True)
    
    <script>
        // Define functions IMMEDIATELY before any HTML that uses them
        
        // Global state management
        let currentPage = 'home';
        let userProperties = [];
        let currentBuyerTab = 'fix-flip';

        // Core page switching functionality - DEFINED FIRST
        function switchPage(pageId) {
            console.log(`Switching to page: ${pageId}`);
            
            try {
                // Hide all pages
                const pages = document.querySelectorAll('.page');
                pages.forEach(page => {
                    page.classList.remove('active');
                });
                
                // Show target page
                const targetPage = document.getElementById(pageId);
                if (targetPage) {
                    targetPage.classList.add('active');
                    currentPage = pageId;
                    
                    // Update navigation active state
                    const navButtons = document.querySelectorAll('.nav-button');
                    navButtons.forEach(btn => {
                        btn.classList.remove('active');
                    });
                    
                    // Find and activate the correct nav button
                    const activeNavButton = Array.from(navButtons).find(btn => 
                        btn.textContent.toLowerCase().includes(pageId) || 
                        (pageId === 'leads' && btn.textContent.includes('Leads'))
                    );
                    
                    if (activeNavButton) {
                        activeNavButton.classList.add('active');
                    }
                    
                    // Initialize page-specific content
                    initializePage(pageId);
                    
                    console.log(`Successfully switched to ${pageId}`);
                } else {
                    console.error(`Page ${pageId} not found`);
                }
            } catch (error) {
                console.error('Error switching pages:', error);
                showToast('Error switching pages. Please try again.', 'error');
            }
        }

        // All other functions defined here so they're available immediately
        function showToast(message, type = 'info') {
            try {
                // Remove existing toasts
                const existingToasts = document.querySelectorAll('.toast');
                existingToasts.forEach(toast => toast.remove());
                
                const toast = document.createElement('div');
                toast.className = `toast ${type}`;
                
                // Add loading spinner for loading toasts
                if (type === 'loading') {
                    message = `<span class="loading-spinner"></span>${message}`;
                }
                
                toast.innerHTML = message;
                document.body.appendChild(toast);
                
                // Auto remove after 4 seconds (except loading)
                if (type !== 'loading') {
                    setTimeout(() => {
                        if (toast.parentNode) {
                            toast.style.animation = 'slideInRight 0.3s ease reverse';
                            setTimeout(() => toast.remove(), 300);
                        }
                    }, 4000);
                }
            } catch (error) {
                console.error('Error showing toast:', error);
            }
        }

        function initializePage(pageId) {
            try {
                switch(pageId) {
                    case 'pipeline':
                        setTimeout(animateStats, 100);
                        break;
                    case 'home':
                        setTimeout(() => {
                            const searchInput = document.getElementById('addressInput');
                            if (searchInput) searchInput.focus();
                        }, 100);
                        break;
                }
            } catch (error) {
                console.error('Error initializing page:', error);
            }
        }

        function handleEnterKey(event) {
            if (event.key === 'Enter') {
                performSearch();
            }
        }

        function performSearch() {
            try {
                const input = document.getElementById('addressInput');
                const address = input.value.trim();
                
                if (!address) {
                    showToast('Please enter a valid address', 'error');
                    return;
                }
                
                showToast('🔍 Analyzing property...', 'loading');
                
                setTimeout(() => {
                    const propertyData = generatePropertyData(address);
                    removeLoadingToast();
                    showPropertyAnalysis(propertyData);
                    input.value = '';
                }, 2500);
            } catch (error) {
                console.error('Search error:', error);
                showToast('Search failed. Please try again.', 'error');
            }
        }

        function generatePropertyData(address) {
            const estimatedValue = Math.floor(Math.random() * 200000 + 150000);
            const arv = Math.floor(Math.random() * 250000 + 200000);
            const repairCosts = Math.floor(Math.random() * 40000 + 15000);
            const profitPotential = arv - estimatedValue - repairCosts;
            
            return {
                address: address,
                estimatedValue: estimatedValue,
                arv: arv,
                repairCosts: repairCosts,
                profitPotential: profitPotential,
                yearBuilt: Math.floor(Math.random() * 50) + 1970,
                sqft: Math.floor(Math.random() * 1500) + 1200,
                propertyType: 'Single Family Home',
                buyers: {
                    fixFlip: Math.floor(Math.random() * 15) + 3,
                    creative: Math.floor(Math.random() * 8) + 2,
                    rental: Math.floor(Math.random() * 12) + 1
                }
            };
        }

        function showPropertyAnalysis(data) {
            try {
                const grade = data.profitPotential > 30000 ? 'A' : 'B';
                const gradeClass = grade === 'A' ? 'grade-a' : 'grade-b';
                
                const modal = document.createElement('div');
                modal.className = 'modal';
                modal.innerHTML = `
                    <div class="modal-content">
                        <div class="modal-header">
                            <h2>🏠 Property Analysis: ${data.address}</h2>
                            <span class="close-modal" onclick="closeModal(this)">&times;</span>
                        </div>
                        <div class="modal-body">
                            <div class="property-info">
                                <div class="info-card">
                                    <h3>📊 Property Details</h3>
                                    <p><strong>Estimated Value:</strong> ${data.estimatedValue.toLocaleString()}</p>
                                    <p><strong>Property Type:</strong> ${data.propertyType}</p>
                                    <p><strong>Year Built:</strong> ${data.yearBuilt}</p>
                                    <p><strong>Sq Ft:</strong> ${data.sqft.toLocaleString()} sq ft</p>
                                </div>
                                
                                <div class="info-card">
                                    <h3>💰 Investment Potential</h3>
                                    <p><strong>ARV:</strong> ${data.arv.toLocaleString()}</p>
                                    <p><strong>Repair Estimate:</strong> ${data.repairCosts.toLocaleString()}</p>
                                    <p><strong>Profit Potential:</strong> ${data.profitPotential.toLocaleString()}</p>
                                    <p><strong>Investment Grade:</strong> <span class="${gradeClass}">${grade}</span></p>
                                </div>
                                
                                <div class="info-card">
                                    <h3>🎯 Available Buyers</h3>
                                    <div class="buyer-list">
                                        <div class="buyer-item">
                                            <span class="buyer-type">Fix & Flip</span>
                                            <span class="buyer-count">${data.buyers.fixFlip} buyers</span>
                                        </div>
                                        <div class="buyer-item">
                                            <span class="buyer-type">Creative Finance</span>
                                            <span class="buyer-count">${data.buyers.creative} buyers</span>
                                        </div>
                                        <div class="buyer-item">
                                            <span class="buyer-type">Rental Investors</span>
                                            <span class="buyer-count">${data.buyers.rental} buyers</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="action-buttons">
                                <button class="btn-primary" onclick="connectToBuyers('${data.address}')">Connect to Buyers</button>
                                <button class="btn-secondary" onclick="saveToPipeline(${JSON.stringify(data).replace(/"/g, '&quot;')})">Save to Pipeline</button>
                                <button class="btn-secondary" onclick="getDetailedReport('${data.address}')">Get Full Report</button>
                            </div>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(modal);
                
                modal.addEventListener('click', function(e) {
                    if (e.target === modal) {
                        closeModal(modal.querySelector('.close-modal'));
                    }
                });
            } catch (error) {
                console.error('Error showing property analysis:', error);
                showToast('Error displaying property analysis', 'error');
            }
        }

        function connectToBuyers(address) {
            showToast(`🤝 Connecting you to buyers for ${address}...`, 'success');
            closeModal(document.querySelector('.close-modal'));
            setTimeout(() => switchPage('buyboxes'), 1000);
        }

        function saveToPipeline(propertyData) {
            userProperties.push(propertyData);
            updatePipelineStats();
            showToast(`💾 Property saved to pipeline!`, 'success');
            closeModal(document.querySelector('.close-modal'));
            setTimeout(() => switchPage('pipeline'), 1000);
        }

        function getDetailedReport(address) {
            showToast(`📊 Generating detailed report for ${address}...`, 'info');
            closeModal(document.querySelector('.close-modal'));
        }

        function switchBuyerTab(button, tabType) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            currentBuyerTab = tabType;
            showToast(`Switched to ${button.textContent}`, 'info');
        }

        function selectState(state) {
            showToast(`🔍 Loading buyers for ${state}...`, 'loading');
            
            setTimeout(() => {
                removeLoadingToast();
                const buyerCount = Math.floor(Math.random() * 30) + 15;
                const avgPrice = Math.floor(Math.random() * 150000) + 150000;
                const hotDeals = Math.floor(Math.random() * 20) + 5;
                showStateInfo(state, buyerCount, avgPrice, hotDeals);
            }, 1500);
        }

        function showStateInfo(state, buyerCount, avgPrice, hotDeals) {
            const modal = document.createElement('div');
            modal.className = 'modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>🏢 ${state} Buyer Network</h2>
                        <span class="close-modal" onclick="closeModal(this)">&times;</span>
                    </div>
                    <div class="modal-body">
                        <div class="property-info">
                            <div class="info-card">
                                <h3>📊 Active Network</h3>
                                <p><strong>Active Buyers:</strong> ${buyerCount}</p>
                                <p><strong>Success Rate:</strong> ${Math.floor(Math.random() * 15) + 80}%</p>
                                <p><strong>Avg Response Time:</strong> ${Math.floor(Math.random() * 4) + 2} hours</p>
                            </div>
                            <div class="info-card">
                                <h3>💰 Market Data</h3>
                                <p><strong>Average Deal Size:</strong> ${avgPrice.toLocaleString()}</p>
                                <p><strong>Hot Deals This Week:</strong> ${hotDeals}</p>
                                <p><strong>Avg Time to Close:</strong> ${Math.floor(Math.random() * 10) + 10} days</p>
                            </div>
                        </div>
                        <div class="action-buttons">
                            <button class="btn-primary" onclick="viewBuyers('${state}')">View All Buyers</button>
                            <button class="btn-secondary" onclick="submitDeal('${state}')">Submit Deal</button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
        }

        function viewBuyers(state) {
            showToast(`📋 Loading buyer directory for ${state}...`, 'info');
            closeModal(document.querySelector('.close-modal'));
        }

        function submitDeal(state) {
            showToast(`📝 Opening deal submission form for ${state}...`, 'info');
            closeModal(document.querySelector('.close-modal'));
        }

        function toggleView(toggle) {
            const viewType = toggle.checked ? 'List View' : 'Map View';
            showToast(`🗺️ Switched to ${viewType}`, 'info');
        }

        function updatePipelineStats() {
            try {
                const total = userProperties.length;
                const waiting = userProperties.filter(p => !p.submitted).length;
                const submitted = userProperties.filter(p => p.submitted).length;
                
                const totalEl = document.getElementById('totalProperties');
                const waitingEl = document.getElementById('waitingProperties');
                const submittedEl = document.getElementById('submittedProperties');
                
                if (totalEl) totalEl.textContent = total;
                if (waitingEl) waitingEl.textContent = waiting;
                if (submittedEl) submittedEl.textContent = submitted;
            } catch (error) {
                console.error('Error updating pipeline stats:', error);
            }
        }

        function animateStats() {
            try {
                const stats = ['totalProperties', 'waitingProperties', 'submittedProperties'];
                stats.forEach(statId => {
                    const element = document.getElementById(statId);
                    if (element) {
                        const finalValue = parseInt(element.textContent) || 0;
                        let currentValue = 0;
                        const increment = Math.max(1, Math.ceil(finalValue / 15));
                        
                        const timer = setInterval(() => {
                            currentValue += increment;
                            if (currentValue >= finalValue) {
                                currentValue = finalValue;
                                clearInterval(timer);
                            }
                            element.textContent = currentValue;
                        }, 80);
                    }
                });
            } catch (error) {
                console.error('Error animating stats:', error);
            }
        }

        function playTutorial(title) {
            showToast(`▶️ Playing tutorial: ${title}`, 'info');
        }

        function switchProfileTab(button, tabType) {
            document.querySelectorAll('.profile-tab').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            if (tabType === 'subscription') {
                showToast('💳 Subscription management coming soon...', 'info');
            }
        }

        function saveProfile() {
            try {
                const firstName = document.getElementById('firstName').value.trim();
                const lastName = document.getElementById('lastName').value.trim();
                const email = document.getElementById('email').value.trim();
                
                if (!firstName || !lastName || !email) {
                    showToast('❌ Please fill in all required fields', 'error');
                    return;
                }
                
                if (!email.includes('@')) {
                    showToast('❌ Please enter a valid email address', 'error');
                    return;
                }
                
                showToast('✅ Profile updated successfully!', 'success');
            } catch (error) {
                console.error('Error saving profile:', error);
                showToast('Error saving profile', 'error');
            }
        }

        function subscribeLightningLeads() {
            showToast('💳 Processing Lightning Leads subscription...', 'loading');
            
            setTimeout(() => {
                removeLoadingToast();
                showToast('⚡ Lightning Leads activated! Welcome to premium leads.', 'success');
            }, 2500);
        }

        function showNotifications() {
            const notifications = [
                { icon: '🏠', message: 'New property match found in Dallas, TX', time: '2 minutes ago' },
                { icon: '👥', message: '3 new buyers joined your network', time: '1 hour ago' },
                { icon: '⚡', message: 'Lightning Leads subscription active', time: '1 day ago' },
                { icon: '💰', message: 'Deal closed: $15,000 profit!', time: '2 days ago' }
            ];
            
            const modal = document.createElement('div');
            modal.className = 'modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>🔔 Notifications</h2>
                        <span class="close-modal" onclick="closeModal(this)">&times;</span>
                    </div>
                    <div class="modal-body">
                        ${notifications.map(notif => `
                            <div class="info-card" style="margin-bottom: 1rem; cursor: pointer;" onclick="markNotificationRead(this)">
                                <div style="display: flex; align-items: center; gap: 1rem;">
                                    <span style="font-size: 1.5rem;">${notif.icon}</span>
                                    <div style="flex: 1;">
                                        <p style="margin-bottom: 0.25rem;"><strong>${notif.message}</strong></p>
                                        <p style="color: #9ca3af; font-size: 0.8rem; margin-bottom: 0;">${notif.time}</p>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                        <div class="action-buttons" style="margin-top: 1.5rem;">
                            <button class="btn-primary" onclick="markAllRead()">Mark All Read</button>
                            <button class="btn-secondary" onclick="closeModal(document.querySelector('.close-modal'))">Close</button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
        }

        function markNotificationRead(element) {
            element.style.opacity = '0.5';
            element.style.pointerEvents = 'none';
            showToast('✅ Notification marked as read', 'success');
        }

        function markAllRead() {
            const notifications = document.querySelectorAll('.info-card');
            notifications.forEach(notif => {
                if (notif.onclick) {
                    notif.style.opacity = '0.5';
                    notif.style.pointerEvents = 'none';
                }
            });
            showToast('✅ All notifications marked as read', 'success');
        }

        function handleLogout() {
            if (confirm('Are you sure you want to log out?')) {
                showToast('👋 Logging out...', 'loading');
                setTimeout(() => {
                    removeLoadingToast();
                    showToast('✅ Successfully logged out', 'success');
                }, 2000);
            }
        }

        function removeLoadingToast() {
            const loadingToasts = document.querySelectorAll('.toast.loading');
            loadingToasts.forEach(toast => {
                toast.style.animation = 'slideInRight 0.3s ease reverse';
                setTimeout(() => toast.remove(), 300);
            });
        }

        function closeModal(closeBtn) {
            const modal = closeBtn.closest('.modal');
            if (modal) {
                modal.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => modal.remove(), 300);
            }
            removeLoadingToast();
        }

        // Initialize demo data
        function initializeDemoData() {
            const sampleProperties = [
                {
                    address: "123 Demo Street, Sample City TX",
                    estimatedValue: 175000,
                    submitted: false
                },
                {
                    address: "456 Example Ave, Test Town FL",
                    estimatedValue: 220000,
                    submitted: true
                }
            ];
            
            userProperties.push(...sampleProperties);
            updatePipelineStats();
        }

        // Add fadeOut animation
        const additionalStyles = document.createElement('style');
        additionalStyles.textContent = `
            @keyframes fadeOut {
                from { opacity: 1; transform: scale(1); }
                to { opacity: 0; transform: scale(0.95); }
            }
        `;
        document.head.appendChild(additionalStyles);

        // Initialize immediately
        console.log('🚀 Functions defined, initializing...');
        initializeDemoData();

        // Show welcome message
        setTimeout(() => {
            showToast('🎉 Welcome to Wholesale2Flip Cartel Pro!', 'success');
        }, 1000);
    </script>
</head>
<body>
    <div class="main-bg"></div>
    
    <header class="header">
        <div class="logo">
            <div class="logo-icon">W2F</div>
            <div class="logo-text">
                <div class="pro">PRO</div>
                <div class="beta">BETA</div>
            </div>
        </div>
        
        <nav class="nav">
            <button class="nav-button active" onclick="switchPage('home')">Home</button>
            <button class="nav-button" onclick="switchPage('buyboxes')">BuyBoxes</button>
            <button class="nav-button" onclick="switchPage('pipeline')">Pipeline</button>
            <button class="nav-button" onclick="switchPage('tutorials')">Tutorials</button>
            <button class="nav-button" onclick="switchPage('profile')">Profile</button>
            <button class="nav-button leads" onclick="switchPage('leads')">Leads</button>
        </nav>
        
        <div class="header-right">
            <button class="notification-btn" onclick="showNotifications()">🔔</button>
            <button class="logout-btn" onclick="handleLogout()">
                🚪 Log Out
            </button>
        </div>
    </header>

    <main class="main-content">
        <!-- HOME PAGE -->
        <div id="home" class="page active">
            <section class="hero-section">
                <div class="house-3d">
                    <div class="house-structure">
                        <div class="house-base"></div>
                        <div class="house-roof"></div>
                        <div class="house-windows"></div>
                        <div class="house-windows"></div>
                    </div>
                </div>
                
                <h1 class="hero-title">Pop In Your Address</h1>
                <p class="hero-subtitle">Let's find you a buyer</p>
                
                <div class="address-search">
                    <div class="search-container">
                        <div class="search-icon" onclick="performSearch()">🔍</div>
                        <input type="text" class="search-input" placeholder="Enter address..." 
                               id="addressInput" onkeypress="handleEnterKey(event)">
                    </div>
                </div>
            </section>
        </div>

        <!-- BUYBOXES PAGE -->
        <div id="buyboxes" class="page">
            <div class="page-header">
                <h1 class="page-title">BuyBoxes</h1>
                <div class="view-toggle">
                    <span>Map View</span>
                    <label class="toggle-switch">
                        <input type="checkbox" checked onchange="toggleView(this)">
                        <span class="slider"></span>
                    </label>
                    <span>List View</span>
                </div>
            </div>

            <div class="buyer-tabs">
                <button class="tab-btn active" onclick="switchBuyerTab(this, 'fix-flip')">Fix & Flip Buyers</button>
                <button class="tab-btn" onclick="switchBuyerTab(this, 'creative')">Creative Buyers</button>
                <button class="tab-btn" onclick="switchBuyerTab(this, 'section8')">Section 8 Buyers</button>
            </div>

            <div class="states-container">
                <div class="state-item" onclick="selectState('ALABAMA')">ALABAMA</div>
                <div class="state-item" onclick="selectState('ARIZONA')">ARIZONA</div>
                <div class="state-item" onclick="selectState('COLORADO')">COLORADO</div>
                <div class="state-item" onclick="selectState('DELAWARE')">DELAWARE</div>
                <div class="state-item" onclick="selectState('FLORIDA')">FLORIDA</div>
                <div class="state-item" onclick="selectState('GEORGIA')">GEORGIA</div>
                <div class="state-item" onclick="selectState('IDAHO')">IDAHO</div>
                <div class="state-item" onclick="selectState('INDIANA')">INDIANA</div>
            </div>
        </div>

        <!-- PIPELINE PAGE -->
        <div id="pipeline" class="page">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-info">
                        <h3 id="totalProperties">0</h3>
                        <p>Total Properties</p>
                    </div>
                    <div class="stat-icon home">🏠</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-info">
                        <h3 id="waitingProperties">0</h3>
                        <p>Properties waiting for dispo</p>
                    </div>
                    <div class="stat-icon search">🔍</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-info">
                        <h3 id="submittedProperties">0</h3>
                        <p>Properties submitted for dispo</p>
                    </div>
                    <div class="stat-icon heart">💜</div>
                </div>
            </div>

            <div class="empty-state">
                <h2>No pipeline available</h2>
                <p>Submit your first property to get started with your investment pipeline.</p>
            </div>
        </div>

        <!-- TUTORIALS PAGE -->
        <div id="tutorials" class="page">
            <div class="tutorial-section">
                <h2>1. Getting Started</h2>
                <div class="tutorial-grid">
                    <div class="tutorial-card coming-soon">
                        <div class="coming-soon-icon">⚡</div>
                        <h3>COMING SOON</h3>
                        <p>In Development</p>
                        <div style="margin-top: 1rem;">
                            <h4 style="color: white; margin-bottom: 0.5rem; font-size: 1rem;">How Wholesale2Flip Cartel works</h4>
                            <p style="font-size: 0.85rem;">Learn about how Wholesale2Flip Cartel makes wholesaling extremely easy for beginners</p>
                        </div>
                    </div>
                    
                    <div class="tutorial-card" onclick="playTutorial('How Wholesaling Works')">
                        <div class="tutorial-video">
                            <div class="play-btn">▶</div>
                        </div>
                        <div class="tutorial-content">
                            <h3>How Wholesaling Works</h3>
                            <p>How you can make money with Wholesale2Flip Cartel</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="tutorial-section">
                <h2>2. How To Submit Deals</h2>
                <div class="tutorial-grid">
                    <div class="tutorial-card" onclick="playTutorial('Deal Submission Process')">
                        <div class="tutorial-video">
                            <div class="play-btn">▶</div>
                        </div>
                        <div class="tutorial-content">
                            <h3>Deal Submission Process</h3>
                            <p>Learn how to properly submit your deals for maximum success</p>
                        </div>
                    </div>
                    
                    <div class="tutorial-card coming-soon">
                        <div class="coming-soon-icon">⚡</div>
                        <h3>COMING SOON</h3>
                        <p>In Development</p>
                    </div>
                    
                    <div class="tutorial-card coming-soon">
                        <div class="coming-soon-icon">⚡</div>
                        <h3>COMING SOON</h3>
                        <p>In Development</p>
                    </div>
                    
                    <div class="tutorial-card coming-soon">
                        <div class="coming-soon-icon">⚡</div>
                        <h3>COMING SOON</h3>
                        <p>In Development</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- PROFILE PAGE -->
        <div id="profile" class="page">
            <div class="profile-container">
                <div class="profile-tabs">
                    <button class="profile-tab active" onclick="switchProfileTab(this, 'account')">My Account</button>
                    <button class="profile-tab" onclick="switchProfileTab(this, 'subscription')">Subscription</button>
                </div>

                <div class="profile-form">
                    <div class="form-group">
                        <label for="firstName">First Name</label>
                        <input type="text" id="firstName" value="james">
                    </div>
                    
                    <div class="form-group">
                        <label for="lastName">Last Name</label>
                        <input type="text" id="lastName" value="edgar">
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" id="email" value="thetreasury@jbhousinginvestments.com">
                    </div>
                    
                    <div class="form-group">
                        <label for="businessName">Business Name</label>
                        <input type="text" id="businessName" placeholder="Business Name">
                    </div>
                    
                    <div class="form-group">
                        <label for="phone">Phone</label>
                        <input type="tel" id="phone" placeholder="Phone Number">
                    </div>
                    
                    <button class="save-btn" onclick="saveProfile()">Save Changes</button>
                </div>
            </div>
        </div>

        <!-- LIGHTNING LEADS PAGE -->
        <div id="leads" class="page">
            <div class="leads-container">
                <div class="leads-card">
                    <div class="leads-header">
                        <span style="font-size: 2rem;">⚡</span>
                        <h1>Lightning Leads</h1>
                    </div>
                    <p class="leads-subtitle">How do Lightning Leads Work?</p>
                    
                    <div class="leads-video">
                        <div class="coming-soon-icon">⚡</div>
                        <h3 style="color: #f59e0b; font-size: 1.8rem; margin: 1rem 0;">COMING SOON</h3>
                        <p style="color: #9ca3af;">In Development</p>
                    </div>

                    <div class="signup-section">
                        <h2>Sign up for Lightning Leads</h2>
                        <p>to get unlimited access to premium on market leads</p>
                        <button class="price-btn" onclick="subscribeLightningLeads()">$39.99 /Month</button>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        // Global state management
        let currentPage = 'home';
        let userProperties = [];
        let currentBuyerTab = 'fix-flip';

        // Core page switching functionality
        function switchPage(pageId) {
            console.log(`Switching to page: ${pageId}`);
            
            // Hide all pages
            const pages = document.querySelectorAll('.page');
            pages.forEach(page => {
                page.classList.remove('active');
            });
            
            // Show target page
            const targetPage = document.getElementById(pageId);
            if (targetPage) {
                targetPage.classList.add('active');
                currentPage = pageId;
                
                // Update navigation active state
                const navButtons = document.querySelectorAll('.nav-button');
                navButtons.forEach(btn => {
                    btn.classList.remove('active');
                });
                
                // Find and activate the correct nav button
                const activeNavButton = Array.from(navButtons).find(btn => 
                    btn.textContent.toLowerCase().includes(pageId) || 
                    (pageId === 'leads' && btn.textContent.includes('Leads'))
                );
                
                if (activeNavButton) {
                    activeNavButton.classList.add('active');
                }
                
                // Initialize page-specific content
                initializePage(pageId);
                
                console.log(`Successfully switched to ${pageId}`);
            } else {
                console.error(`Page ${pageId} not found`);
            }
        }

        // Initialize page-specific functionality
        function initializePage(pageId) {
            switch(pageId) {
                case 'pipeline':
                    animateStats();
                    break;
                case 'home':
                    // Focus on search input
                    setTimeout(() => {
                        const searchInput = document.getElementById('addressInput');
                        if (searchInput) searchInput.focus();
                    }, 100);
                    break;
            }
        }

        // Address search functionality
        function handleEnterKey(event) {
            if (event.key === 'Enter') {
                performSearch();
            }
        }

        function performSearch() {
            const input = document.getElementById('addressInput');
            const address = input.value.trim();
            
            if (!address) {
                showToast('Please enter a valid address', 'error');
                return;
            }
            
            // Show loading toast
            showToast('🔍 Analyzing property...', 'loading');
            
            // Simulate API call
            setTimeout(() => {
                const propertyData = generatePropertyData(address);
                removeLoadingToast();
                showPropertyAnalysis(propertyData);
                input.value = ''; // Clear input
            }, 2500);
        }

        // Generate realistic property data
        function generatePropertyData(address) {
            const estimatedValue = Math.floor(Math.random() * 200000 + 150000);
            const arv = Math.floor(Math.random() * 250000 + 200000);
            const repairCosts = Math.floor(Math.random() * 40000 + 15000);
            const profitPotential = arv - estimatedValue - repairCosts;
            
            return {
                address: address,
                estimatedValue: estimatedValue,
                arv: arv,
                repairCosts: repairCosts,
                profitPotential: profitPotential,
                yearBuilt: Math.floor(Math.random() * 50) + 1970,
                sqft: Math.floor(Math.random() * 1500) + 1200,
                propertyType: 'Single Family Home',
                buyers: {
                    fixFlip: Math.floor(Math.random() * 15) + 3,
                    creative: Math.floor(Math.random() * 8) + 2,
                    rental: Math.floor(Math.random() * 12) + 1
                }
            };
        }

        // Show property analysis modal
        function showPropertyAnalysis(data) {
            const grade = data.profitPotential > 30000 ? 'A' : 'B';
            const gradeClass = grade === 'A' ? 'grade-a' : 'grade-b';
            
            const modal = document.createElement('div');
            modal.className = 'modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>🏠 Property Analysis: ${data.address}</h2>
                        <span class="close-modal" onclick="closeModal(this)">&times;</span>
                    </div>
                    <div class="modal-body">
                        <div class="property-info">
                            <div class="info-card">
                                <h3>📊 Property Details</h3>
                                <p><strong>Estimated Value:</strong> ${data.estimatedValue.toLocaleString()}</p>
                                <p><strong>Property Type:</strong> ${data.propertyType}</p>
                                <p><strong>Year Built:</strong> ${data.yearBuilt}</p>
                                <p><strong>Sq Ft:</strong> ${data.sqft.toLocaleString()} sq ft</p>
                            </div>
                            
                            <div class="info-card">
                                <h3>💰 Investment Potential</h3>
                                <p><strong>ARV:</strong> ${data.arv.toLocaleString()}</p>
                                <p><strong>Repair Estimate:</strong> ${data.repairCosts.toLocaleString()}</p>
                                <p><strong>Profit Potential:</strong> ${data.profitPotential.toLocaleString()}</p>
                                <p><strong>Investment Grade:</strong> <span class="${gradeClass}">${grade}</span></p>
                            </div>
                            
                            <div class="info-card">
                                <h3>🎯 Available Buyers</h3>
                                <div class="buyer-list">
                                    <div class="buyer-item">
                                        <span class="buyer-type">Fix & Flip</span>
                                        <span class="buyer-count">${data.buyers.fixFlip} buyers</span>
                                    </div>
                                    <div class="buyer-item">
                                        <span class="buyer-type">Creative Finance</span>
                                        <span class="buyer-count">${data.buyers.creative} buyers</span>
                                    </div>
                                    <div class="buyer-item">
                                        <span class="buyer-type">Rental Investors</span>
                                        <span class="buyer-count">${data.buyers.rental} buyers</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="action-buttons">
                            <button class="btn-primary" onclick="connectToBuyers('${data.address}')">Connect to Buyers</button>
                            <button class="btn-secondary" onclick="saveToPipeline(${JSON.stringify(data).replace(/"/g, '&quot;')})">Save to Pipeline</button>
                            <button class="btn-secondary" onclick="getDetailedReport('${data.address}')">Get Full Report</button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Close on background click
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    closeModal(modal.querySelector('.close-modal'));
                }
            });
        }

        // Action functions
        function connectToBuyers(address) {
            showToast(`🤝 Connecting you to buyers for ${address}...`, 'success');
            closeModal(document.querySelector('.close-modal'));
            setTimeout(() => switchPage('buyboxes'), 1000);
        }

        function saveToPipeline(propertyData) {
            userProperties.push(propertyData);
            updatePipelineStats();
            showToast(`💾 Property saved to pipeline!`, 'success');
            closeModal(document.querySelector('.close-modal'));
            setTimeout(() => switchPage('pipeline'), 1000);
        }

        function getDetailedReport(address) {
            showToast(`📊 Generating detailed report for ${address}...`, 'info');
            closeModal(document.querySelector('.close-modal'));
        }

        // BuyBoxes page functions
        function switchBuyerTab(button, tabType) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            currentBuyerTab = tabType;
            showToast(`Switched to ${button.textContent}`, 'info');
        }

        function selectState(state) {
            showToast(`🔍 Loading buyers for ${state}...`, 'loading');
            
            setTimeout(() => {
                removeLoadingToast();
                const buyerCount = Math.floor(Math.random() * 30) + 15;
                const avgPrice = Math.floor(Math.random() * 150000) + 150000;
                const hotDeals = Math.floor(Math.random() * 20) + 5;
                showStateInfo(state, buyerCount, avgPrice, hotDeals);
            }, 1500);
        }

        function showStateInfo(state, buyerCount, avgPrice, hotDeals) {
            const modal = document.createElement('div');
            modal.className = 'modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>🏢 ${state} Buyer Network</h2>
                        <span class="close-modal" onclick="closeModal(this)">&times;</span>
                    </div>
                    <div class="modal-body">
                        <div class="property-info">
                            <div class="info-card">
                                <h3>📊 Active Network</h3>
                                <p><strong>Active Buyers:</strong> ${buyerCount}</p>
                                <p><strong>Success Rate:</strong> ${Math.floor(Math.random() * 15) + 80}%</p>
                                <p><strong>Avg Response Time:</strong> ${Math.floor(Math.random() * 4) + 2} hours</p>
                            </div>
                            <div class="info-card">
                                <h3>💰 Market Data</h3>
                                <p><strong>Average Deal Size:</strong> ${avgPrice.toLocaleString()}</p>
                                <p><strong>Hot Deals This Week:</strong> ${hotDeals}</p>
                                <p><strong>Avg Time to Close:</strong> ${Math.floor(Math.random() * 10) + 10} days</p>
                            </div>
                        </div>
                        <div class="action-buttons">
                            <button class="btn-primary" onclick="viewBuyers('${state}')">View All Buyers</button>
                            <button class="btn-secondary" onclick="submitDeal('${state}')">Submit Deal</button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
        }

        function viewBuyers(state) {
            showToast(`📋 Loading buyer directory for ${state}...`, 'info');
            closeModal(document.querySelector('.close-modal'));
        }

        function submitDeal(state) {
            showToast(`📝 Opening deal submission form for ${state}...`, 'info');
            closeModal(document.querySelector('.close-modal'));
        }

        function toggleView(toggle) {
            const viewType = toggle.checked ? 'List View' : 'Map View';
            showToast(`🗺️ Switched to ${viewType}`, 'info');
        }

        // Pipeline functions
        function updatePipelineStats() {
            const total = userProperties.length;
            const waiting = userProperties.filter(p => !p.submitted).length;
            const submitted = userProperties.filter(p => p.submitted).length;
            
            document.getElementById('totalProperties').textContent = total;
            document.getElementById('waitingProperties').textContent = waiting;
            document.getElementById('submittedProperties').textContent = submitted;
        }

        function animateStats() {
            const stats = ['totalProperties', 'waitingProperties', 'submittedProperties'];
            stats.forEach(statId => {
                const element = document.getElementById(statId);
                const finalValue = parseInt(element.textContent);
                let currentValue = 0;
                const increment = Math.max(1, Math.ceil(finalValue / 15));
                
                const timer = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= finalValue) {
                        currentValue = finalValue;
                        clearInterval(timer);
                    }
                    element.textContent = currentValue;
                }, 80);
            });
        }

        // Tutorial functions
        function playTutorial(title) {
            showToast(`▶️ Playing tutorial: ${title}`, 'info');
        }

        // Profile functions
        function switchProfileTab(button, tabType) {
            document.querySelectorAll('.profile-tab').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            if (tabType === 'subscription') {
                showToast('💳 Subscription management coming soon...', 'info');
            }
        }

        function saveProfile() {
            const firstName = document.getElementById('firstName').value.trim();
            const lastName = document.getElementById('lastName').value.trim();
            const email = document.getElementById('email').value.trim();
            
            if (!firstName || !lastName || !email) {
                showToast('❌ Please fill in all required fields', 'error');
                return;
            }
            
            if (!email.includes('@')) {
                showToast('❌ Please enter a valid email address', 'error');
                return;
            }
            
            showToast('✅ Profile updated successfully!', 'success');
        }

        // Lightning Leads functions
        function subscribeLightningLeads() {
            showToast('💳 Processing Lightning Leads subscription...', 'loading');
            
            setTimeout(() => {
                removeLoadingToast();
                showToast('⚡ Lightning Leads activated! Welcome to premium leads.', 'success');
            }, 2500);
        }

        // Header functions
        function showNotifications() {
            const notifications = [
                { icon: '🏠', message: 'New property match found in Dallas, TX', time: '2 minutes ago' },
                <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wholesale2Flip - PRO</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #0a0a0a;
            color: white;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Main gradient background matching screenshots */
        .main-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, 
                #1a0033 0%, 
                #2d1b4e 25%, 
                #4a2c7a 50%, 
                #2d1b4e 75%, 
                #1a0033 100%);
            z-index: -2;
        }

        /* Overlay pattern for depth */
        .main-bg::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.2) 0%, transparent 50%),
                        radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
            z-index: -1;
        }

        /* Header exactly matching screenshot */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(124, 58, 237, 0.2);
            position: relative;
            z-index: 100;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
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
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
        }

        .logo-text .pro {
            font-size: 1.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
        }

        .logo-text .beta {
            font-size: 0.65rem;
            color: #9ca3af;
            margin-top: -3px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Navigation exactly matching screenshot */
        .nav {
            display: flex;
            gap: 0rem;
        }

        .nav-button {
            color: #9ca3af;
            padding: 0.75rem 1.5rem;
            border: none;
            background: transparent;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s ease;
            position: relative;
            border-radius: 8px;
        }

        .nav-button:hover {
            color: white;
            background: rgba(124, 58, 237, 0.1);
        }

        .nav-button.active {
            color: #7c3aed;
            background: rgba(124, 58, 237, 0.15);
        }

        .nav-button.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            height: 2px;
            background: #7c3aed;
            border-radius: 1px;
        }

        .nav-button.leads {
            color: #f59e0b;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .nav-button.leads::before {
            content: "⚡";
            font-size: 1rem;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .notification-btn {
            background: #7c3aed;
            border: none;
            padding: 0.6rem;
            border-radius: 50%;
            color: white;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
        }

        .notification-btn:hover {
            background: #6d28d9;
            transform: scale(1.05);
        }

        .logout-btn {
            background: #ef4444;
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        }

        .logout-btn:hover {
            background: #dc2626;
            transform: translateY(-1px);
        }

        /* Main content container */
        .main-content {
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
            position: relative;
            z-index: 10;
        }

        /* Page system */
        .page {
            display: none;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
        }

        .page.active {
            display: block;
            opacity: 1;
            transform: translateY(0);
        }

        /* HOME PAGE - Pop In Your Address */
        .hero-section {
            text-align: center;
            padding: 6rem 0;
            position: relative;
            min-height: 80vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        /* 3D House background effect matching screenshot */
        .house-3d {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 600px;
            height: 400px;
            opacity: 0.6;
            z-index: -1;
        }

        .house-structure {
            position: relative;
            width: 100%;
            height: 100%;
            transform-style: preserve-3d;
            transform: rotateX(15deg) rotateY(-15deg);
        }

        .house-base {
            position: absolute;
            width: 400px;
            height: 250px;
            background: linear-gradient(135deg, #2a2a3a 0%, #1a1a2a 100%);
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            border-radius: 8px;
            box-shadow: 0 20px 40px rgba(124, 58, 237, 0.2);
        }

        .house-roof {
            position: absolute;
            width: 0;
            height: 0;
            border-left: 220px solid transparent;
            border-right: 220px solid transparent;
            border-bottom: 100px solid #f59e0b;
            left: 50%;
            top: 20%;
            transform: translateX(-50%);
            filter: drop-shadow(0 10px 20px rgba(245, 158, 11, 0.3));
        }

        .house-windows {
            position: absolute;
            width: 60px;
            height: 80px;
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            left: 30%;
            top: 40%;
            border-radius: 4px;
            box-shadow: 0 0 20px rgba(251, 191, 36, 0.4);
        }

        .house-windows:nth-child(2) {
            left: 60%;
        }

        .hero-title {
            font-size: 4.5rem;
            font-weight: 900;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #10b981 0%, #34d399 50%, #6ee7b7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.1;
            text-shadow: 0 0 40px rgba(16, 185, 129, 0.3);
            position: relative;
            z-index: 2;
        }

        .hero-subtitle {
            font-size: 1.4rem;
            color: #9ca3af;
            margin-bottom: 3rem;
            font-weight: 500;
            position: relative;
            z-index: 2;
        }

        .address-search {
            max-width: 600px;
            margin: 0 auto;
            position: relative;
            z-index: 2;
        }

        .search-container {
            position: relative;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            backdrop-filter: blur(10px);
        }

        .search-input {
            width: 100%;
            padding: 1.5rem 1.5rem 1.5rem 4rem;
            border: none;
            background: transparent;
            color: #1f2937;
            font-size: 1.1rem;
            outline: none;
            font-weight: 500;
        }

        .search-input::placeholder {
            color: #6b7280;
        }

        .search-icon {
            position: absolute;
            left: 1.5rem;
            top: 50%;
            transform: translateY(-50%);
            color: #7c3aed;
            font-size: 1.3rem;
            cursor: pointer;
        }

        /* BUYBOXES PAGE */
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
        }

        .page-title {
            font-size: 2.5rem;
            font-weight: 800;
            color: white;
        }

        .view-toggle {
            display: flex;
            gap: 1rem;
            align-items: center;
            color: #9ca3af;
            font-weight: 600;
        }

        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 30px;
        }

        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #374151;
            transition: 0.4s;
            border-radius: 30px;
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 22px;
            width: 22px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: 0.4s;
            border-radius: 50%;
        }

        input:checked + .slider {
            background-color: #7c3aed;
        }

        input:checked + .slider:before {
            transform: translateX(30px);
        }

        .buyer-tabs {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 2rem;
        }

        .tab-btn {
            padding: 1rem 2rem;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(124, 58, 237, 0.3);
            color: #9ca3af;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        .tab-btn:hover {
            border-color: #7c3aed;
            color: white;
        }

        .tab-btn.active {
            background: #7c3aed;
            color: white;
            border-color: #7c3aed;
        }

        .states-container {
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid #7c3aed;
            border-radius: 20px;
            padding: 1.5rem;
            backdrop-filter: blur(20px);
        }

        .state-item {
            padding: 1.2rem 1.5rem;
            border-bottom: 1px solid rgba(124, 58, 237, 0.2);
            cursor: pointer;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            color: #e5e7eb;
            letter-spacing: 1px;
        }

        .state-item:hover {
            background: rgba(124, 58, 237, 0.2);
            color: white;
            transform: translateX(8px);
            border-left: 4px solid #7c3aed;
            padding-left: calc(1.5rem - 4px);
        }

        .state-item:last-child {
            border-bottom: none;
        }

        /* PIPELINE PAGE */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }

        .stat-card {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: 20px;
            padding: 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            backdrop-filter: blur(20px);
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            border-color: #7c3aed;
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(124, 58, 237, 0.2);
        }

        .stat-info h3 {
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            color: white;
        }

        .stat-info p {
            color: #9ca3af;
            font-size: 0.9rem;
            font-weight: 500;
        }

        .stat-icon {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }

        .stat-icon.home {
            background: rgba(59, 130, 246, 0.2);
            color: #3b82f6;
        }

        .stat-icon.search {
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
        }

        .stat-icon.heart {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }

        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            color: #9ca3af;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 20px;
            border: 2px dashed rgba(124, 58, 237, 0.3);
            backdrop-filter: blur(10px);
        }

        .empty-state h2 {
            font-size: 2rem;
            margin-bottom: 1rem;
            color: white;
            font-weight: 700;
        }

        /* TUTORIALS PAGE */
        .tutorial-section {
            margin-bottom: 3rem;
        }

        .tutorial-section h2 {
            font-size: 1.8rem;
            margin-bottom: 2rem;
            color: white;
            font-weight: 700;
        }

        .tutorial-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }

        .tutorial-card {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: 20px;
            overflow: hidden;
            transition: all 0.3s ease;
            cursor: pointer;
            backdrop-filter: blur(20px);
        }

        .tutorial-card:hover {
            transform: translateY(-8px);
            border-color: #7c3aed;
            box-shadow: 0 20px 40px rgba(124, 58, 237, 0.2);
        }

        .tutorial-video {
            position: relative;
            height: 200px;
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .play-btn {
            width: 60px;
            height: 60px;
            background: #ef4444;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3);
        }

        .play-btn:hover {
            transform: scale(1.1);
            background: #dc2626;
        }

        .tutorial-content {
            padding: 1.5rem;
        }

        .tutorial-content h3 {
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
            color: white;
            font-weight: 600;
        }

        .tutorial-content p {
            color: #9ca3af;
            line-height: 1.5;
            font-size: 0.9rem;
        }

        .coming-soon {
            background: rgba(0, 0, 0, 0.3) !important;
            border: 2px dashed #f59e0b !important;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #f59e0b;
            min-height: 280px;
        }

        .coming-soon-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .coming-soon h3 {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            color: #f59e0b !important;
            font-weight: 700;
        }

        .coming-soon p {
            color: #9ca3af !important;
            font-weight: 500;
        }

        /* PROFILE PAGE */
        .profile-container {
            max-width: 700px;
        }

        .profile-tabs {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .profile-tab {
            padding: 1rem 2rem;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .profile-tab.active {
            background: #7c3aed;
            color: white;
        }

        .profile-tab:not(.active) {
            background: rgba(0, 0, 0, 0.4);
            color: #9ca3af;
            border: 1px solid rgba(124, 58, 237, 0.3);
        }

        .profile-tab:not(.active):hover {
            border-color: #7c3aed;
            color: white;
        }

        .profile-form {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: 20px;
            padding: 2.5rem;
            backdrop-filter: blur(20px);
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: white;
            font-weight: 600;
        }

        .form-group input {
            width: 100%;
            padding: 1rem;
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: 10px;
            background: rgba(0, 0, 0, 0.3);
            color: white;
            outline: none;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        .form-group input:focus {
            border-color: #7c3aed;
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2);
        }

        .form-group input::placeholder {
            color: #6b7280;
        }

        .save-btn {
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(124, 58, 237, 0.3);
        }

        .save-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 25px rgba(124, 58, 237, 0.4);
        }

        /* LIGHTNING LEADS PAGE */
        .leads-container {
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }

        .leads-card {
            background: rgba(124, 58, 237, 0.1);
            border: 2px solid #7c3aed;
            border-radius: 25px;
            padding: 3rem;
            margin-bottom: 2rem;
            backdrop-filter: blur(20px);
        }

        .leads-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .leads-header h1 {
            font-size: 2.5rem;
            font-weight: 800;
            color: white;
        }

        .leads-subtitle {
            color: #9ca3af;
            font-size: 1.2rem;
            margin-bottom: 2rem;
            font-weight: 500;
        }

        .leads-video {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 15px;
            height: 300px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-bottom: 2rem;
            border: 1px solid rgba(124, 58, 237, 0.3);
            backdrop-filter: blur(10px);
        }

        .signup-section h2 {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            color: white;
            font-weight: 600;
        }

        .signup-section p {
            color: #9ca3af;
            margin-bottom: 1.5rem;
            font-size: 1rem;
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
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(124, 58, 237, 0.3);
        }

        .price-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(124, 58, 237, 0.4);
            background: #6d28d9;
        }

        /* Modal System */
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            backdrop-filter: blur(10px);
        }

        .modal-content {
            background: linear-gradient(135deg, #1a0033 0%, #2d1b4e 100%);
            border-radius: 20px;
            padding: 0;
            max-width: 900px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            border: 2px solid #7c3aed;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
        }

        .modal-header {
            background: rgba(124, 58, 237, 0.2);
            padding: 1.5rem 2rem;
            border-bottom: 1px solid rgba(124, 58, 237, 0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 18px 18px 0 0;
        }

        .modal-header h2 {
            margin: 0;
            color: white;
            font-size: 1.5rem;
            font-weight: 700;
        }

        .close-modal {
            font-size: 1.8rem;
            color: #9ca3af;
            cursor: pointer;
            transition: color 0.3s ease;
        }

        .close-modal:hover {
            color: white;
        }

        .modal-body {
            padding: 2rem;
        }

        .property-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .info-card {
            background: rgba(0, 0, 0, 0.4);
            padding: 1.5rem;
            border-radius: 15px;
            border: 1px solid rgba(124, 58, 237, 0.3);
            backdrop-filter: blur(10px);
        }

        .info-card h3 {
            margin-bottom: 1rem;
            color: #7c3aed;
            font-size: 1.1rem;
            font-weight: 600;
        }

        .info-card p {
            margin-bottom: 0.5rem;
            color: #e5e7eb;
            font-size: 0.9rem;
        }

        .info-card strong {
            color: white;
            font-weight: 600;
        }

        .grade-a, .grade-b {
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.8rem;
        }

        .grade-a {
            background: #10b981;
            color: white;
        }

        .grade-b {
            background: #f59e0b;
            color: white;
        }

        .buyer-list {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .buyer-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem;
            background: rgba(124, 58, 237, 0.1);
            border-radius: 8px;
            border: 1px solid rgba(124, 58, 237, 0.3);
        }

        .buyer-type {
            color: white;
            font-weight: 500;
            font-size: 0.9rem;
        }

        .buyer-count {
            background: #7c3aed;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 12px