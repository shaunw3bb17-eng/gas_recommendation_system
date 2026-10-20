# Jamaican Gas Station Recommendation System

A full-stack web application that helps users identify suitable gas stations in Jamaica by considering fuel prices, distance, and estimated traffic conditions.

## Overview

Finding a suitable gas station involves more than comparing fuel prices. Distance and traffic conditions can also influence which station is the most convenient choice.

This project combines a Python backend with a React frontend to provide gas station recommendations, retrieve historical fuel prices, analyze price trends, and estimate upcoming prices.

## Features

- **Gas Station Recommendations:** Ranks stations based on fuel prices, distance, and estimated traffic.
- **Fuel Price History:** Stores and retrieves historical fuel price records using SQLite.
- **Price Trend Analysis:** Examines historical prices to identify price trends.
- **Price Prediction:** Estimates upcoming fuel prices using available historical data.
- **Station Reports:** Provides information and price reports for individual stations.
- **Location-Based Ranking:** Uses latitude and longitude to compare stations relative to a user's location.
- **REST API:** Exposes backend functionality through FastAPI endpoints.

## Technologies Used

**Backend**
- Python
- FastAPI
- SQLite
- Uvicorn

**Frontend**
- React
- JavaScript
- Vite
- CSS

**Tools**
- Git and GitHub
- Visual Studio Code

## Project Structure

```text
gas_recommendation_system/
├── gas_code/
│   ├── main.py
│   ├── gas_logic.py
│   ├── gas_data.py
│   ├── station_location.py
│   ├── load_data.py
│   └── test.py
├── gas-frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

Install the following before running the application:

- Python
- Node.js and npm
- Git (optional, if cloning the repository)

### 1. Clone the Repository

```bash
git clone https://github.com/shaunw3bb17-eng/gas_recommendation_system.git
cd gas_recommendation_system
```

### 2. Set Up the Backend

Open a terminal and run:

```bash
cd gas_code
py -m pip install fastapi uvicorn requests
```

Start the backend server:

```bash
py -m uvicorn main:app --reload
```

The API should be available at:

`http://127.0.0.1:8000`

Interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

### 3. Set Up the Frontend

Open a second terminal from the project root and run:

```bash
cd gas-frontend
npm install
npm run dev
```

Open the local address displayed in the terminal, usually:

`http://localhost:5173`

Keep both the backend and frontend servers running while using the application.

## How Recommendations Work

The backend calculates a score for each station using fuel price, distance, and estimated traffic.

The current scoring formula is:

`Score = Price + (Distance × 0.7) + (Traffic × 0.2)`

A lower score represents a more favourable recommendation according to this formula.

The recommendation considers multiple factors rather than selecting a station based on price alone.

## Limitations

- Recommendations depend on the station locations and fuel-price data available to the application.
- Traffic estimates may be simulated rather than based on live traffic information.
- Distance calculations may use straight-line distance rather than actual driving routes.
- Price predictions are estimates and depend on the available historical data.
- The application currently supports a limited set of gas stations.

## Future Improvements

- Expand the number of supported gas stations across Jamaica.
- Integrate interactive maps and actual driving routes.
- Improve fuel-price prediction accuracy with additional historical data and evaluation.
- Incorporate regularly updated fuel prices and verified traffic information.
- Improve the interface with additional visualizations and station comparisons.

## Author
-Shaun Webb

Developed as a full-stack software development project focused on location-based recommendations and fuel-price analysis.
