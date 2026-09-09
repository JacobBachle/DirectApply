# If you were to make x in x state
# how much would be required to make
# to live at the same living standard in y state.

# Cost of living index per US state (national average = 100).
# Higher means more expensive. Values are approximate and can be
# swapped for a live data source later without changing the functions below.
COST_OF_LIVING_INDEX = {
    "alabama": 88.0,
    "alaska": 125.0,
    "arizona": 108.0,
    "arkansas": 89.0,
    "california": 138.0,
    "colorado": 105.0,
    "connecticut": 113.0,
    "delaware": 101.0,
    "district of columbia": 146.0,
    "florida": 103.0,
    "georgia": 91.0,
    "hawaii": 186.0,
    "idaho": 98.0,
    "illinois": 92.0,
    "indiana": 91.0,
    "iowa": 90.0,
    "kansas": 87.0,
    "kentucky": 94.0,
    "louisiana": 91.0,
    "maine": 112.0,
    "maryland": 116.0,
    "massachusetts": 146.0,
    "michigan": 91.0,
    "minnesota": 95.0,
    "mississippi": 85.0,
    "missouri": 89.0,
    "montana": 103.0,
    "nebraska": 91.0,
    "nevada": 101.0,
    "new hampshire": 115.0,
    "new jersey": 114.0,
    "new mexico": 94.0,
    "new york": 125.0,
    "north carolina": 96.0,
    "north dakota": 95.0,
    "ohio": 94.0,
    "oklahoma": 86.0,
    "oregon": 114.0,
    "pennsylvania": 102.0,
    "rhode island": 111.0,
    "south carolina": 96.0,
    "south dakota": 93.0,
    "tennessee": 90.0,
    "texas": 93.0,
    "utah": 103.0,
    "vermont": 114.0,
    "virginia": 101.0,
    "washington": 116.0,
    "west virginia": 90.0,
    "wisconsin": 95.0,
    "wyoming": 92.0,
}

# Approximate state income tax rate (fraction of income paid).
# A flat estimate per state; real tax is progressive, so swap this for a
# bracket lookup later if more precision is needed. States with no income
# tax are 0.0.
STATE_INCOME_TAX = {
    "alabama": 0.05,
    "alaska": 0.0,
    "arizona": 0.025,
    "arkansas": 0.049,
    "california": 0.093,
    "colorado": 0.044,
    "connecticut": 0.055,
    "delaware": 0.066,
    "district of columbia": 0.085,
    "florida": 0.0,
    "georgia": 0.055,
    "hawaii": 0.079,
    "idaho": 0.058,
    "illinois": 0.0495,
    "indiana": 0.032,
    "iowa": 0.057,
    "kansas": 0.057,
    "kentucky": 0.045,
    "louisiana": 0.0425,
    "maine": 0.0715,
    "maryland": 0.0575,
    "massachusetts": 0.05,
    "michigan": 0.0425,
    "minnesota": 0.0785,
    "mississippi": 0.05,
    "missouri": 0.048,
    "montana": 0.059,
    "nebraska": 0.0584,
    "nevada": 0.0,
    "new hampshire": 0.0,
    "new jersey": 0.0637,
    "new mexico": 0.049,
    "new york": 0.0685,
    "north carolina": 0.045,
    "north dakota": 0.025,
    "ohio": 0.035,
    "oklahoma": 0.0475,
    "oregon": 0.099,
    "pennsylvania": 0.0307,
    "rhode island": 0.0599,
    "south carolina": 0.064,
    "south dakota": 0.0,
    "tennessee": 0.0,
    "texas": 0.0,
    "utah": 0.0465,
    "vermont": 0.076,
    "virginia": 0.0575,
    "washington": 0.0,
    "west virginia": 0.0512,
    "wisconsin": 0.053,
    "wyoming": 0.0,
}

#
# Returns the cost of living index for a state, or None if the state is unknown.
#
def get_index(state):
    return COST_OF_LIVING_INDEX.get(state.strip().lower())

#
# Returns the income tax rate for a state, or None if the state is unknown.
#
def get_tax_rate(state):
    return STATE_INCOME_TAX.get(state.strip().lower())

#
# Given a salary in source_state, returns the equivalent salary needed in
# target_state to maintain the same living standard.
# Accounts for both cost of living and state income tax by default; set
# account_for_tax=False to compare gross cost of living only.
# Raises ValueError if either state is unknown.
#
def convert_salary(salary, source_state, target_state, account_for_tax=True):
    source_index = get_index(source_state)
    target_index = get_index(target_state)
    if source_index is None:
        raise ValueError(f"Unknown state: {source_state}")
    if target_index is None:
        raise ValueError(f"Unknown state: {target_state}")

    equivalent = salary * (target_index / source_index)

    if account_for_tax:
        source_tax = get_tax_rate(source_state)
        target_tax = get_tax_rate(target_state)
        equivalent *= (1 - source_tax) / (1 - target_tax)

    return equivalent

# Simple terminal input and output for standalone use
if __name__ == "__main__":
    salary = float(input("Salary: "))
    source_state = input("Current state: ")
    target_state = input("Target state: ")

    try:
        equivalent = convert_salary(salary, source_state, target_state)
        print(f"To live the same in {target_state}, you would need: {equivalent:,.2f}")
    except ValueError as error:
        print(error)
