import datetime
import os
from openai import OpenAI

# Load your OpenAI API key (ensure it's set in your environment variables or Replit secrets)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initial setup
states = {"Arizona": 0, "Minnesota": 0}
home_budgets = {
    "Arizona": {"utilities": 200, "insurance": 150, "HOA": 100},
    "Minnesota": {"utilities": 250, "insurance": 170, "HOA": 90}
}
seasonal_cash_flow = {
    "Travel": 300,
    "Healthcare": 400,
    "Supplemental Insurance": 200
}
TAX_THRESHOLD_DAYS = 183  # Common threshold for state tax residency

def count_days(location):
    today = datetime.date.today()
    print(f"\nRecording today's date ({today}) as a day spent in {location}.")
    states[location] += 1

def print_budget(location):
    print(f"\n--- {location} Home Budget ---")
    for k, v in home_budgets[location].items():
        print(f"{k}: ${v}/month")

def print_cash_flow():
    print("\n--- Seasonal Cash Flow Estimates ---")
    for k, v in seasonal_cash_flow.items():
        print(f"{k}: ${v}/month")

def check_tax_residency():
    print("\n--- Tax Residency Status ---")
    for state, days in states.items():
        print(f"{state}: {days} days")
        if days >= TAX_THRESHOLD_DAYS:
            print(f"⚠️ You may now be considered a tax resident of {state}.")

def ask_ai(question):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly AI financial assistant for seasonal residents (snowbirds)."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def main():
    print("❄️ Welcome to Snowbird AI Financial Assistant 🏖️")
    name = input("What’s your name? ")
    print(f"Hi {name}, let's make sure your seasonal lifestyle stays stress-free and tax-smart!")

    while True:
        print("\nMenu:")
        print("1. Log a day in Arizona")
        print("2. Log a day in Minnesota")
        print("3. View home maintenance budget")
        print("4. View seasonal cash flow plan")
        print("5. Check tax residency alerts")
        print("6. Ask a financial question")
        print("7. Exit")

        choice = input("Choose an option (1-7): ")

        if choice == "1":
            count_days("Arizona")
        elif choice == "2":
            count_days("Minnesota")
        elif choice == "3":
            loc = input("View budget for which home? (Arizona/Minnesota): ")
            if loc in home_budgets:
                print_budget(loc)
            else:
                print("Invalid location.")
        elif choice == "4":
            print_cash_flow()
        elif choice == "5":
            check_tax_residency()
        elif choice == "6":
            q = input("Ask your financial question: ")
            print("\nAI Response:")
            print(ask_ai(q))
        elif choice == "7":
            print("Stay warm (or cool), and travel safe, Snowbird!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()