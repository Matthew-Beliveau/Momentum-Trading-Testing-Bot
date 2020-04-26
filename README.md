# Momentum-Trading-Testing-Bot

## What is this?
The US stock market is worth about 30 trillion dollars with about 6.43 billion shares traded per day. Different trading strategies can be implemented. Upon researching said strategies we found that trading strategies that use past behavior to predict future behavior generates higher returns, called momentum trading.

Our goal is to create an AI that will test momentum trading with three approaches to prediction: Kalman Filters, Hidden Markov Model, and Dynamic Bayesian Networks.

## Why?
The Idea behind using a trading-bot is to be able to analyize historical data to give investors a upperhand and increase trading volume. We want to find which group of algorithm, initial investment, and historical data range, will produce the highest returns.

*Example grouping:* `{$10,000, 7-13 months prior, Kalman Filter}`

## Setup

### Installations
For data.py:
`pip3 install -r data_requirements.txt`

For get_historical_data.py
`pip3 install -r history_requirements.txt`

### Google Cloud Storage setup
[Link](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python) to
the setup for google cloud storage.


[Link to the project page:](https://github.com/users/Matthew-Beliveau/projects/2)
