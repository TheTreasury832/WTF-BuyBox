# Wholesale2Flip API Documentation

## Overview

The Wholesale2Flip API provides developers with programmatic access to our real estate investment platform. This RESTful API allows you to integrate property matching, buyer management, and deal analysis into your applications.

**Base URL:** `https://api.wholesale2flip.com/v1`

**Authentication:** Bearer Token (JWT)

---

## Authentication

### Get Access Token

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "subscription_tier": "professional"
  }
}
```

### Refresh Token

```http
POST /auth/refresh
Content-Type: application/json
Authorization: Bearer {refresh_token}

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## Properties

### List Properties

```http
GET /properties?page=1&limit=20&market=atlanta&min_price=50000&max_price=200000
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20, max: 100)
- `market` (string): Market/city filter
- `min_price` (integer): Minimum price filter
- `max_price` (integer): Maximum price filter
- `property_type` (string): Single-family, multi-family, commercial
- `status` (string): available, under_contract, sold

**Response:**
```json
{
  "properties": [
    {
      "id": "prop_123",
      "address": "123 Main St, Atlanta, GA 30309",
      "price": 125000,
      "arv": 185000,
      "estimated_repairs": 35000,
      "bedrooms": 3,
      "bathrooms": 2,
      "sqft": 1250,
      "lot_size": 0.25,
      "year_built": 1985,
      "property_type": "single-family",
      "market": "atlanta",
      "neighborhood": "Midtown",
      "days_on_market": 15,
      "status": "available",
      "photos": [
        "https://cdn.wholesale2flip.com/photos/prop_123_1.jpg"
      ],
      "matched_buyers": 5,
      "profit_potential": 25000,
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-20T14:45:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 145,
    "total_pages": 8
  }
}
```

### Get Property Details

```http
GET /properties/{property_id}
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": "prop_123",
  "address": "123 Main St, Atlanta, GA 30309",
  "price": 125000,
  "arv": 185000,
  "estimated_repairs": 35000,
  "property_details": {
    "bedrooms": 3,
    "bathrooms": 2,
    "sqft": 1250,
    "lot_size": 0.25,
    "year_built": 1985,
    "garage": true,
    "basement": false,
    "pool": false
  },
  "financial_analysis": {
    "purchase_price": 125000,
    "repair_costs": 35000,
    "holding_costs": 8000,
    "closing_costs": 5000,
    "total_investment": 173000,
    "arv": 185000,
    "profit_potential": 12000,
    "roi_percentage": 6.9
  },
  "market_data": {
    "neighborhood": "Midtown",
    "median_home_price": 275000,
    "price_per_sqft": 220,
    "days_on_market_avg": 25,
    "appreciation_rate": 4.2
  },
  "seller_info": {
    "motivation_level": "high",
    "reason_for_selling": "relocation",
    "timeline": "30_days"
  }
}
```

### Create Property

```http
POST /properties
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "address": "456 Oak St, Birmingham, AL 35203",
  "price": 85000,
  "arv": 135000,
  "estimated_repairs": 25000,
  "bedrooms": 3,
  "bathrooms": 1,
  "sqft": 1100,
  "property_type": "single-family",
  "description": "Fixer-upper in up-and-coming neighborhood"
}
```

---

## Buyers

### List Buyers

```http
GET /buyers?page=1&limit=20&market=atlanta&strategy=fix-flip
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `market` (string): Geographic market filter
- `strategy` (string): Investment strategy (fix-flip, rental, section8, etc.)
- `min_budget` (integer): Minimum budget filter
- `max_budget` (integer): Maximum budget filter
- `funding_type` (string): cash, conventional, hard-money, etc.
- `verified` (boolean): Only verified buyers

**Response:**
```json
{
  "buyers": [
    {
      "id": "buyer_456",
      "name": "John Smith",
      "email": "john@smithinvestments.com",
      "phone": "+1-555-0123",
      "markets": ["atlanta", "birmingham", "nashville"],
      "strategies": ["fix-flip", "rental"],
      "budget_range": {
        "min": 75000,
        "max": 300000
      },
      "funding_type": "cash",
      "proof_of_funds": true,
      "verification_status": "verified",
      "close_timeline": "14_days",
      "deals_completed": 23,
      "total_volume": 2850000,
      "rating": 4.8,
      "last_active": "2025-01-20T09:15:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 89,
    "total_pages": 5
  }
}
```

### Get Buyer Profile

```http
GET /buyers/{buyer_id}
Authorization: Bearer {access_token}
```

### Create Buyer

```http
POST /buyers
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@doerealty.com",
  "phone": "+1-555-0456",
  "markets": ["atlanta"],
  "strategies": ["rental"],
  "budget_min": 100000,
  "budget_max": 250000,
  "funding_type": "conventional"
}
```

---

## Deal Matching

### Match Property to Buyers

```http
POST /matching/properties/{property_id}/match
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "property_id": "prop_123",
  "matched_buyers": [
    {
      "buyer_id": "buyer_456",
      "match_score": 95,
      "match_reasons": [
        "Budget range matches (75k-300k)",
        "Primary market is Atlanta",
        "Fix & flip strategy aligns",
        "Cash buyer with fast close"
      ],
      "buyer": {
        "name": "John Smith",
        "rating": 4.8,
        "deals_completed": 23
      }
    }
  ],
  "total_matches": 5,
  "best_match_score": 95
}
```

### Get Match History

```http
GET /matching/history?property_id=prop_123
Authorization: Bearer {access_token}
```

---

## Analytics

### Deal Analysis

```http
POST /analytics/deal-analysis
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "purchase_price": 125000,
  "arv": 185000,
  "repair_costs": 35000,
  "holding_period_months": 6,
  "market": "atlanta"
}
```

**Response:**
```json
{
  "analysis": {
    "purchase_price": 125000,
    "repair_costs": 35000,
    "holding_costs": 8000,
    "closing_costs": 5000,
    "selling_costs": 11100,
    "total_costs": 184100,
    "arv": 185000,
    "gross_profit": 60000,
    "net_profit": 900,
    "roi_percentage": 0.5,
    "annualized_roi": 1.0,
    "recommendation": "marginal_deal",
    "risk_factors": [
      "Low profit margin",
      "Extended holding period risk"
    ]
  }
}
```

### Market Reports

```http
GET /analytics/market-report/{market}?period=30d
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "market": "atlanta",
  "period": "30d",
  "report": {
    "total_properties": 156,
    "avg_price": 145000,
    "avg_arv": 215000,
    "avg_profit_margin": 18.5,
    "avg_days_on_market": 22,
    "top_neighborhoods": [
      {
        "name": "Midtown",
        "avg_price": 275000,
        "growth_rate": 4.2
      }
    ],
    "buyer_activity": {
      "total_active_buyers": 89,
      "avg_close_time": "18_days",
      "most_popular_strategy": "fix-flip"
    }
  }
}
```

---

## Webhooks

### Setup Webhook

```http
POST /webhooks
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "url": "https://your-app.com/webhooks/wholesale2flip",
  "events": ["property.created", "match.found", "deal.closed"],
  "secret": "your_webhook_secret"
}
```

### Webhook Events

**property.created**
```json
{
  "event": "property.created",
  "data": {
    "property_id": "prop_123",
    "address": "123 Main St, Atlanta, GA",
    "price": 125000
  },
  "timestamp": "2025-01-20T15:30:00Z"
}
```

**match.found**
```json
{
  "event": "match.found",
  "data": {
    "property_id": "prop_123",
    "buyer_id": "buyer_456",
    "match_score": 95
  },
  "timestamp": "2025-01-20T15:35:00Z"
}
```

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": [
      {
        "field": "price",
        "message": "Price must be greater than 0"
      }
    ]
  },
  "request_id": "req_abc123"
}
```

### Common Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `UNAUTHORIZED` | 401 | Invalid or expired access token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 422 | Invalid input data |
| `RATE_LIMITED` | 429 | Too many requests |
| `SERVER_ERROR` | 500 | Internal server error |

---

## Rate Limits

| Tier | Requests/Hour | Burst Limit |
|------|---------------|-------------|
| Starter | 1,000 | 50 |
| Professional | 5,000 | 100 |
| Elite | 10,000 | 200 |

---

## SDKs and Libraries

### JavaScript/Node.js

```bash
npm install @wholesale2flip/api-client
```

```javascript
const Wholesale2Flip = require('@wholesale2flip/api-client');

const client = new Wholesale2Flip({
  apiKey: 'your_api_key',
  environment: 'production' // or 'sandbox'
});

// List properties
const properties = await client.properties.list({
  market: 'atlanta',
  min_price: 50000,
  max_price: 200000
});

// Match property to buyers
const matches = await client.matching.matchProperty('prop_123');
```

### Python

```bash
pip install wholesale2flip-python
```

```python
from wholesale2flip import Client

client = Client(api_key='your_api_key')

# List properties
properties = client.properties.list(
    market='atlanta',
    min_price=50000,
    max_price=200000
)

# Analyze deal
analysis = client.analytics.analyze_deal(
    purchase_price=125000,
    arv=185000,
    repair_costs=35000
)
```

### PHP

```bash
composer require wholesale2flip/php-sdk
```

```php
<?php
require_once 'vendor/autoload.php';

use Wholesale2Flip\Client;

$client = new Client(['api_key' => 'your_api_key']);

// List buyers
$buyers = $client->buyers->list([
    'market' => 'atlanta',
    'strategy' => 'fix-flip'
]);
```

---

## Testing

### Sandbox Environment

Use the sandbox environment for testing:

**Base URL:** `https://api-sandbox.wholesale2flip.com/v1`

### Test Data

The sandbox includes realistic test data:
- 500+ sample properties
- 200+ test buyers
- Market data for major cities

### Test API Keys

Sandbox API keys are prefixed with `sk_test_`

---

## Support

- **Documentation:** https://docs.wholesale2flip.com
- **Discord Community:** https://discord.gg/wholesale2flip
- **Email Support:** api@wholesale2flip.com
- **Status Page:** https://status.wholesale2flip.com

---

## Changelog

### v1.2.0 (2025-01-20)
- Added market analytics endpoints
- Improved matching algorithm
- New webhook events

### v1.1.0 (2025-01-15)
- Added deal analysis endpoints
- Enhanced buyer filtering
- Performance improvements

### v1.0.0 (2025-01-01)
- Initial API release
- Core property and buyer management
- Basic matching functionality