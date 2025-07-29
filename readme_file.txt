# Wholesale2Flip - Real Estate Platform

A modern web application for real estate wholesaling and flipping, built with Flask and featuring a responsive design with advanced animations and user interactions.

## Features

- **AI-Powered Deal Matching**: Connect properties with qualified buyers
- **Verified Cash Buyers Network**: Access to 15K+ pre-qualified investors
- **Instant Deal Analysis**: Advanced calculators for ARV, repair costs, and ROI
- **User Authentication**: Secure login and registration system
- **Buyer Qualification System**: Comprehensive form for investor onboarding
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI/UX**: Premium design with smooth animations and interactions

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern gradients and animations
- **Icons**: Emoji-based icons for better cross-platform compatibility

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/wholesale2flip.git
   cd wholesale2flip
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Project Structure

```
wholesale2flip/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── wholesale2flip.db     # SQLite database (created automatically)
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── style.css         # CSS styles
    └── script.js         # JavaScript functionality
```

## Features Overview

### User Management
- User registration and authentication
- Secure password hashing
- Session management

### Buyer Qualification System
- Comprehensive investor profiling
- Investment strategy selection
- Financial capacity assessment
- Experience level tracking

### Database Schema

**Users Table**
- id, name, email, password_hash, created_at

**Buyer Qualifications Table**
- Complete investor profiles with preferences and requirements

## API Endpoints

- `POST /api/login` - User authentication
- `POST /api/signup` - User registration  
- `POST /api/buyer-qualification` - Submit buyer qualification form
- `POST /api/select-plan` - Plan selection for pricing tiers

## Deployment

### Heroku Deployment

1. **Install Heroku CLI**
2. **Create a Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Deploy to Heroku**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

### Environment Variables

For production, set these environment variables:
- `SECRET_KEY`: Your Flask secret key
- `DATABASE_URL`: Database connection string (if using PostgreSQL)

## Database

The application uses SQLite for local development. For production, consider upgrading to PostgreSQL:

1. Install psycopg2: `pip install psycopg2-binary`
2. Update database connection in `app.py`
3. Set `DATABASE_URL` environment variable

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security Features

- Password hashing with Werkzeug
- CSRF protection ready (add Flask-WTF for production)
- SQL injection prevention with parameterized queries
- Session-based authentication

## Performance Optimizations

- Optimized CSS with custom properties
- Efficient JavaScript with event delegation
- Lazy loading animations
- Minimal external dependencies

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact:
- Email: hello@wholesale2flip.com
- Phone: (555) 123-FLIP

## Roadmap

- [ ] Payment integration (Stripe)
- [ ] Email notifications
- [ ] Advanced search and filtering
- [ ] Mobile app (React Native)
- [ ] Real-time chat system
- [ ] Property management tools
- [ ] Advanced analytics dashboard