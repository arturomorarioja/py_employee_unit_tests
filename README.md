# Employee - Pytest unit tests

## Purpose
Example of Pytest unit tests.

The system under test is an Employee class with the following attributes:
- CPR. 10 numeric digits
- First name. A minimum of 1 and a maximum of 30 characters.The characters can be alphabetic, spaces or a dash
- Last name. A minimum of 1 and a maximum of 30 characters.The characters can be alphabetic, spaces or a dash
- Department. One among the following: `HR`, `Finance`, `IT`, `Sales`, `GeneralServices`
- Base salary. In Danish kroner. A minimum of 20000 and a maximum of 100000
- Educational level. One among the following: `0` (none), `1` (primary), `2` (secondary), `3` (tertiary)
- Date of birth. dd/MM/yyyy. At least 18 years from the present day
- Date of employment. dd/MM/yyyy. Equal or lower than the present day
- Country. Country name as a string

The getter method for the educational level returns the name of said level.

Public methods:
- `get_salary()`. Calculates and returns the actual salary based on the following formula:
`Actual salary = base salary + (educational level * 1220)`
- `get_discount()`. Employees can purchase company products with a discount. `get_discount()` calculates and returns said discount based on the following formula:
`Discount = years of employment * 0,5`
- `get_shipping_costs()` calculates and returns the shipping cost percentage, taking into account that  employees  from  Denmark,  Norway  and  Sweden  do  not  pay  shipping  costs,  employees  from  Iceland  and Finland pay 50%, and employees from other countries pay 100%

## Usage
1. Create a Python virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate`, `.\venv\Scripts\Activate`, `source venv/bin/activate`, depending on OS and CLI
3. Install the dependencies: `pip install -r requirements.txt`
4. Run the tests: `pytest`

## Tools
Pytest / Python

## Author:
Arturo Mora-Rioja