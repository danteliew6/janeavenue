from webbrowser import get
import database

def add_investment(investment_details):
    toAdd = {
        investment_details.name: {
            "Currency": [currency for currency in investment_details.currencies],
            "Interest": investment_details.interest,
            "Ticker": investment_details.ticker,
            "TotalDeposits": 0,
            "Type": investment_details.type
            }
        }
    database.db.child("Investments").update(toAdd)
    return True
