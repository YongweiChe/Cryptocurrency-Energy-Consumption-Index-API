# Cryptocurrency-Energy-Consumption-Index-API
API for getting raw data in order to calculate energy consumption for the Top 20 Proof-of-Work (PoW) cryptocurrencies in the market.

## Web Scraping
Used Selenium to scrape Mining Pool data and Mining Hardware data for the twenty largest PoW cryptocurrencies in terms of market capitalization.

## Database
Uses SQLAlchemy to to store the scraped data in a mySQL database

## API
Flask API where you can GET:
- Coin name
- Price
- Network hashrate
- Algorithm
- The large majority of known mining pools for the specified coin along with the pool hashrate and their countries of operation
- The most popular mining hardware for each algorithm and its individual hashrate and power consumption (W)
