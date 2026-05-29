from app.employees import Employee
import sys
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta

@pytest.fixture
def employee():
    employee = Employee()
    yield employee

#   CPR                                Middle value  Boundary values
#   ---------------------------------- ------------- --------------------------------------------------------
#   Invalid partition: empty           empty         empty | 1 character 
#   Invalid partition: 1-9 characters  5 characters  empty | 1 character | 2 characters
#                                                    8 characters | 9 characters | 10 characters
#   Valid partition:   10 characters   10 characters 9 characters | 10 characters | 11 characters
#   Invalid partition: > 10 characters 15 characters 10 characters | 11 characters | 12 characters

# CPR positive tests
@pytest.mark.parametrize('cpr_passes', [
    '1234567890',   # 10 characters
    '0000000000',
    '9999999999',
    '0999999999'
])
def test_cpr_passes(cpr_passes, employee):
    employee.cpr = cpr_passes
    assert cpr_passes == employee.cpr

# CPR negative tests
@pytest.mark.parametrize('cpr_fails', [
    '1',            # 1 character
    '12',           # 2 characters
    '12345678',     # 8 characters
    '123456789',    # 9 characters
    '10000000000',  # 11 characters
    '100000000000', # 12 characters
    'ABCDEFGHIJ',   # Format / Edge case
    '          ',   # Format / Edge case
])
def test_cpr_fails(cpr_fails, employee):
    employee.cpr = cpr_fails
    assert not cpr_fails == employee.cpr

# This negative test cannot be included in the negative tests'
# parameterised test, as the assertion would fail
def test_empty_cpr_fails(employee):
    employee.cpr = ''
    assert employee.cpr == ''


#   First and last name                Middle value  Boundary values
#   ---------------------------------- ------------- --------------------------------------------------------
#   Invalid partition: empty           empty         empty | 1 character 
#   Valid partition: 1-30 characters   15 characters empty | 1 character | 2 characters
#                                      29 characters | 30 characters | 31 characters 
#   Invalid partition: > 30 characters 45 characters | 31 characters | 32 characters

# First and last name positive tests
NAMES_PASS = ('name_passes', [
    'A',                                # 1 character
    'AB',                               # 2 characters
    'ABCDEFGHIJKLMNO',                  # 15 characters
    'abcdefghijklmno',                  # 15 characters
    'ABCDEFGHIJKLMNOPQRSTUVWXYZABC',    # 29 characters
    'ABCDEFGHIJKLMNOPQRSTUVWXYZABCD',   # 30 characters
    'æøåñç',                            # Format
    'áéíóúàèìòùäëïöü',                  # Format
    'âêîôû',                            # Format
    'ÆØÅÑÇ',                            # Format
    'ÁÉÍÓÚÀÈÌÒÙÄËÏÖÜ',                  # Format
    'ÂÊÎÔÛ',                            # Format
    # The following cases are unlikely to be valid, but they are according to requirements.
    # In a real company scenario, the person(s) in charge of writing requirements should be contacted to clarify the situation
    'a a a a a a a',                    # Format
    'a-a-a-a-a-a-a',                    # Format
    '-',                                # Format
    ' ',                                # Format
])

@pytest.mark.parametrize(*NAMES_PASS)
def test_first_name_passes(name_passes, employee):
    employee.first_name = name_passes
    assert name_passes == employee.first_name

@pytest.mark.parametrize(*NAMES_PASS)
def test_last_name_passes(name_passes, employee):
    employee.last_name = name_passes
    assert name_passes == employee.last_name

# First and last name negative tests
NAMES_FAIL = ('name_fails', [
    'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDE',                  # 31 characters
    'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRS',    # 45 characters
    'abcdef1',                                          # Format / Edge case
    'abcdef/',                                          # Format / Edge case
    'abcdef,'                                           # Format / Edge case
])

@pytest.mark.parametrize(*NAMES_FAIL)
def test_first_name_fails(name_fails, employee):
    employee.first_name = name_fails
    assert not name_fails == employee.first_name

@pytest.mark.parametrize(*NAMES_FAIL)
def test_last_name_fails(name_fails, employee):
    employee.last_name = name_fails
    assert not name_fails == employee.last_name

# The next two negative tests cannot be included in the 
# negative tests' parameterised test, as the assertion would fail
def test_empty_first_name_fails(employee):
    employee.first_name = ''
    assert employee.first_name == ''

def test_empty_last_name_fails(employee):
    employee.last_name = ''
    assert employee.last_name == ''


#   Department
#   There are so few that testing all of them is not costly

# Department positive tests
@pytest.mark.parametrize('department_passes', [
    'HR', 'Finance', 'IT', 'Sales', 'General Services'
])
def test_department_passes(department_passes, employee):
    employee.department = department_passes
    assert department_passes == employee.department

# Department negative tests
def test_department_fails(employee):
    employee.department = ''
    assert employee.department == ''

def test_department_fails(employee):
    fake_department = 'Bonds'
    employee.department = fake_department
    assert not fake_department == employee.department


#   Base salary                                Middle value  Boundary values
#   ------------------------------------------ ------------- --------------------------------------------------------
#   Invalid partition: -MAX FLOAT- -0.01           -10000 kr  -MAX FLOAT - 0.01 | -MAX FLOAT | -MAX FLOAT + 0.01
#                                                             -0.02 | -0.01 | 0
#   Invalid partition: 0                                0     -0.01 | 0 | 0.01
#   Invalid partition: 0.01-19999.99 kr             10000 kr  0 | 0.01 | 0.02
#                                                             19999.98 | 19999.99 | 20000
#   Valid partition: 20000-100000 kr                60000 kr  19999.99 | 20000 | 20000.01
#                                                             999999.99 | 100000 | 100000.01
#   Invalid partition: 100000.01-MAX FLOAT kr      120000 kr  100000 | 100000.01 | 100000.02
#                                                             MAX FLOAT - 0.01 | MAX FLOAT | MAX FLOAT + 0.01

# Base salary positive tests
@pytest.mark.parametrize('base_salary_passes', [
    20000,          # Valid partition: Valid lower boundary
    20000.01,       # Valid partition: Valid lower boundary + 1 (3-value approach)
    60000,          # Valid partition: Middle value
    100000,         # Valid partition: Valid upper boundary
    99999.99,       # Valid partition: Valid upper boundary - 1 (3-value approach)
])
def test_base_salary_passes(base_salary_passes, employee):
    employee.base_salary = base_salary_passes
    assert base_salary_passes == employee.base_salary

# Base salary negative tests
@pytest.mark.parametrize('base_salary_fails', [
    -sys.float_info.max - 0.01,
    -sys.float_info.max,
    -sys.float_info.max + 0.01,
    -10000
    -0.02,          
    -0.01,          
    0.01,
    0.02,
    10000,          
    19999.98,
    19999.99,
    100000.01,      
    100000.02,      
    120000,
    sys.float_info.max - 0.01,
    sys.float_info.max,
    sys.float_info.max + 0.01,
])
def test_base_salary_fails(base_salary_fails, employee):
    employee.base_salary = base_salary_fails
    assert not base_salary_fails == employee.base_salary

# This negative test cannot be included in the negative tests'
# parameterised test, as the assertion would fail
def test_base_salary_zero_fails(employee):
    employee.base_salary = 0
    assert employee.base_salary == 0


#   Educational level
#   There are so few that testing all of them is not costly

# Educational level positive tests
@pytest.mark.parametrize('educational_level_passes, educational_level_name', [
    (0, 'None'),
    (1, 'Primary'),
    (2, 'Secondary'),
    (3, 'Tertiary')
])
def test_educational_level_passes(educational_level_passes, educational_level_name, employee):
    employee.educational_level = educational_level_passes
    assert educational_level_name == employee.educational_level

# Educational level positive tests
@pytest.mark.parametrize('educational_level_fails', [    
    # Random invalid values covering boundary values (-1, 4) and middle partition values (-10, 10)
    -1, 4, 10, -10  
])
def test_educational_level_fails(educational_level_fails, employee):
    employee.educational_level = educational_level_fails
    assert employee.educational_level == ''

#   Date of birth
#   Testing non-deterministic data is complicated. Here the date of birth must be compared to the present date, which changes daily.
#   One approach is to calculate several dates relative to today 
#   (in the past, in the future, 18 years ago, right before 18 years ago, right after 18 years ago).
#   Unfortunately, it enforces an anti-pattern: calculations taking place in a unit test

# Date of birth positive tests
dobs = []
eighteen_years_ago = date.today() - relativedelta(years=18) # AMR: This test caught a bug. I was using >= instead of >
dobs.append(f'{eighteen_years_ago.day}/{eighteen_years_ago.month}/{eighteen_years_ago.year}')
eya_minus_one_day = eighteen_years_ago - relativedelta(days=1)
dobs.append(f'{eya_minus_one_day.day}/{eya_minus_one_day.month}/{eya_minus_one_day.year}')
eya_minus_ten_days = eighteen_years_ago - relativedelta(days=10)
dobs.append(f'{eya_minus_ten_days.day}/{eya_minus_ten_days.month}/{eya_minus_ten_days.year}')
eya_minus_eight_years = eighteen_years_ago - relativedelta(years=8)
dobs.append(f'{eya_minus_eight_years.day}/{eya_minus_eight_years.month}/{eya_minus_eight_years.year}')

@pytest.mark.parametrize('date_of_birth_passes', dobs)
def test_date_of_birth_passes(date_of_birth_passes, employee):
    employee.date_of_birth = date_of_birth_passes
    day, month, year = map(int, date_of_birth_passes.split('/'))
    assert employee.date_of_birth == date(year, month, day)

# Date of birth negative tests
dobs = []
eya_plus_one_day = eighteen_years_ago + relativedelta(days=1)
dobs.append(f'{eya_plus_one_day.day}/{eya_plus_one_day.month}/{eya_plus_one_day.year}')
eya_plus_ten_days = eighteen_years_ago + relativedelta(days=10)
dobs.append(f'{eya_plus_ten_days.day}/{eya_plus_ten_days.month}/{eya_plus_ten_days.year}')
eya_plus_eight_years = eighteen_years_ago + relativedelta(years=8)
dobs.append(f'{eya_plus_eight_years.day}/{eya_plus_eight_years.month}/{eya_plus_eight_years.year}')
dobs.append('30/2/1914')
dobs.append('')
dobs.append('999')

@pytest.mark.parametrize('date_of_birth_fails', dobs)
def test_date_of_birth_fails(date_of_birth_fails, employee):
    employee.date_of_birth = date_of_birth_fails
    assert employee.date_of_birth == ''

#   Date of employment
#   Same problematic as in the date of birth

# Date of employment positive tests
does = []
today = date.today()
does.append(f'{today.day}/{today.month}/{today.year}')
yesterday = today - relativedelta(days=1)
does.append(f'{yesterday.day}/{yesterday.month}/{yesterday.year}')
t_minus_ten_days = today - relativedelta(days=10)
does.append(f'{t_minus_ten_days.day}/{t_minus_ten_days.month}/{t_minus_ten_days.year}')
t_minus_eight_years = today - relativedelta(years=8)
does.append(f'{t_minus_eight_years.day}/{t_minus_eight_years.month}/{t_minus_eight_years.year}')

@pytest.mark.parametrize('date_of_employment_passes', does)
def test_date_of_employment_passes(date_of_employment_passes, employee):
    employee.date_of_employment = date_of_employment_passes
    day, month, year = map(int, date_of_employment_passes.split('/'))
    assert employee.date_of_employment == date(year, month, day)

# Date of employment negative tests
does = []
tomorrow = today + relativedelta(days=1)
does.append(f'{tomorrow.day}/{tomorrow.month}/{tomorrow.year}')
t_plus_ten_days = today + relativedelta(days=10)
does.append(f'{t_plus_ten_days.day}/{t_plus_ten_days.month}/{t_plus_ten_days.year}')
t_plus_eight_years = today + relativedelta(years=8)
does.append(f'{t_plus_eight_years.day}/{t_plus_eight_years.month}/{t_plus_eight_years.year}')
does.append('30/2/1914')
does.append('')
does.append('999')

@pytest.mark.parametrize('date_of_employment_fails', does)
def test_date_of_employment_fails(date_of_employment_fails, employee):
    employee.date_of_employment = date_of_employment_fails
    assert employee.date_of_employment == ''


@pytest.mark.parametrize('base_salary,educational_level,expected_salary', [
    (30000, 0, 30000),
    (30000, 1, 31220),
    (30000, 2, 32440),
    (30000, 3, 33660),
    (10000, 0, 0),
    (110000, 0, 0),
])    
def test_salary(base_salary, educational_level, expected_salary, employee):
    employee.base_salary = base_salary
    employee.educational_level = educational_level
    assert employee.get_salary() == expected_salary

# Discount calculation
does = []
does.append((f'{today.day}/{today.month}/{today.year}', 0))
t_minus_one_year = today - relativedelta(years=1)
does.append((f'{t_minus_one_year.day}/{t_minus_one_year.month}/{t_minus_one_year.year}', 0.5))
t_minus_ten_years = today - relativedelta(years=10)
does.append((f'{t_minus_ten_years.day}/{t_minus_ten_years.month}/{t_minus_ten_years.year}', 5))
t_minus_fifteen_years = today - relativedelta(years=15)
does.append((f'{t_minus_fifteen_years.day}/{t_minus_fifteen_years.month}/{t_minus_fifteen_years.year}', 7.5))
t_minus_twenty_three_years = today - relativedelta(years=23)
does.append((f'{t_minus_twenty_three_years.day}/{t_minus_twenty_three_years.month}/{t_minus_twenty_three_years.year}', 11.5))

@pytest.mark.parametrize('date_of_employment,expected_discount', does)
def test_discount(date_of_employment, expected_discount, employee):
    employee.date_of_employment = date_of_employment
    assert employee.get_discount() == expected_discount

@pytest.mark.parametrize('country, expected_shipping_costs', [
    ('Denmark', 0),
    ('Norway', 0),
    ('Sweden', 0),
    ('Iceland', 50),
    ('Finland', 50),
    ('DENMARK', 100),
    ('Spain', 100),
    ('ABCDEFG', 100),
    ('', 100),
])
def test_shipping_costs(country, expected_shipping_costs, employee):
    employee.country = country
    assert employee.get_shipping_costs() == expected_shipping_costs