from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database setup
def init_db():
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    conn = sqlite3.connect('wholesale2flip.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, password_hash FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        return jsonify({'success': True, 'message': 'Login successful!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not all([name, email, password]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    password_hash = generate_password_hash(password)
    
    conn = sqlite3.connect('wholesale2flip.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)', 
                      (name, email, password_hash))
        conn.commit()
        user_id = cursor.lastrowid
        session['user_id'] = user_id
        session['user_name'] = name
        conn.close()
        return jsonify({'success': True, 'message': 'Account created successfully!'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Email already exists'}), 400

@app.route('/api/buyer-qualification', methods=['POST'])
def buyer_qualification():
    data = request.get_json()
    
    # Extract form data
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    location = data.get('location')
    strategy = json.dumps(data.get('strategy', []))  # Store as JSON string
    budget_min = data.get('budgetMin')
    budget_max = data.get('budgetMax')
    funding_type = data.get('fundingType')
    proof_of_funds = data.get('proofOfFunds')
    experience = data.get('experience')
    timeline = data.get('timeline')
    monthly_deals = data.get('monthlyDeals')
    special_requirements = data.get('specialRequirements', '')
    newsletter = 1 if data.get('newsletter') else 0
    discord = 1 if data.get('discord') else 0
    mentorship = 1 if data.get('mentorship') else 0
    
    if not all([name, email, phone, location]):
        return jsonify({'success': False, 'message': 'Required fields are missing'}), 400
    
    conn = sqlite3.connect('wholesale2flip.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO buyer_qualifications (
            name, email, phone, location, strategy, budget_min, budget_max,
            funding_type, proof_of_funds, experience, timeline, monthly_deals,
            special_requirements, newsletter, discord, mentorship
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, phone, location, strategy, budget_min, budget_max,
          funding_type, proof_of_funds, experience, timeline, monthly_deals,
          special_requirements, newsletter, discord, mentorship))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Successfully added to buyer network!'})

@app.route('/api/select-plan', methods=['POST'])
def select_plan():
    data = request.get_json()
    plan_type = data.get('planType')
    
    # Here you would integrate with a payment processor like Stripe
    # For now, we'll just return a success message
    
    return jsonify({
        'success': True, 
        'message': f'You\'ve selected the {plan_type} plan. Redirecting to secure checkout...',
        'redirect_url': f'/checkout/{plan_type}'
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    return render_template('dashboard.html', user_name=session.get('user_name'))

@app.route('/admin/buyers')
def admin_buyers():
    # Simple admin route to view buyer qualifications
    conn = sqlite3.connect('wholesale2flip.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM buyer_qualifications ORDER BY created_at DESC')
    buyers = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries for easier template rendering
    buyers_list = []
    columns = ['id', 'name', 'email', 'phone', 'location', 'strategy', 'budget_min', 'budget_max',
              'funding_type', 'proof_of_funds', 'experience', 'timeline', 'monthly_deals',
              'special_requirements', 'newsletter', 'discord', 'mentorship', 'created_at']
    
    for buyer in buyers:
        buyer_dict = dict(zip(columns, buyer))
        # Parse strategy JSON
        try:
            buyer_dict['strategy'] = json.loads(buyer_dict['strategy'])
        except:
            buyer_dict['strategy'] = []
        buyers_list.append(buyer_dict)
    
    return render_template('admin_buyers.html', buyers=buyers_list)

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)