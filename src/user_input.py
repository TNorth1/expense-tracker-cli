from datetime import datetime
import re


class UserInput:

    @staticmethod
    def prompt_for_max_claimable_amount():
        """Prompt the user for daily maximum amount allowed to be claimed in the expense report"""
        while True:
            max_claimable_amount = input(
                "Enter the daily maximum amount allowed to be claimed in expense reports: ")
            if UserInput.is_valid_monetary_value(max_claimable_amount):
                return float(max_claimable_amount)
            print("Enter a valid monetary value i.e. '10' or '10.01' NOT '10.1'")

    @staticmethod
    def is_valid_date(date_str):
        """Validate user input for date in the format dd/mm/yyyy"""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_monetary_value(value_str):
        """Checks if a string is a valid monetary value (integer or float with up two decimal places)"""
        return re.match(r'^\d+(\.\d{2})?$', value_str) is not None

    @staticmethod
    def prompt_for_meal_cost(meal):
        """
        Prompt the user to input the cost of a specified meal.
        The input is validated to ensure it is either an integer or a float with exactly 2 decimal places.
        """
        while True:
            meal_cost = input(f"Enter the cost of {meal}: ")
            if UserInput.is_valid_monetary_value(meal_cost):
                meal_cost = float(meal_cost)
                break
            else:
                print("Enter a valid monetary value i.e. '10' or '10.01' NOT '10.1'")

        return meal_cost

    @staticmethod
    def get_date_for_report():
        """
        Prompts the user for the date of an expense entry and formats it to DD/MM/YYYY
        """
        while True:
            date = input(
                "Enter the date of the expense DD/MM/YYYY (Leave blank to select today's date): ").strip()
            # If user input is left blank, use today's date
            if not date:
                date = datetime.today().strftime('%d/%m/%Y')
                break
            if UserInput.is_valid_date(date):
                break
            print("Enter a valid date - DD/MM/YYYY")

        return date

    @staticmethod
    def get_report_data(max_claimable_amount):
        """Get the expense report data from user input"""
        date = UserInput.get_date_for_report()
        breakfast_cost = UserInput.prompt_for_meal_cost("breakfast")
        lunch_cost = UserInput.prompt_for_meal_cost("lunch")
        dinner_cost = UserInput.prompt_for_meal_cost("dinner")
        # Use round to eliminate floating point error
        total = round(breakfast_cost + lunch_cost + dinner_cost, 2)
        claimable_total = min(total, max_claimable_amount)

        return date, breakfast_cost, lunch_cost, dinner_cost, total, claimable_total
