from app.employees import Employee
import pytest
from datetime import date
from dateutil.relativedelta import relativedelta

@pytest.fixture
def employee():
    employee = Employee()
    yield employee

@pytest.mark.parametrize('cpr_passes', [
    '1234567890',   # Valid upper and lower boundary
    '0000000000',
    '9999999999',
    '0999999999'
])
def test_cpr_passes(cpr_passes, employee):
    employee.cpr = cpr_passes
    assert cpr_passes == employee.cpr

# This negative test cannot be included in the negative tests
#  parameterised test, as the assertion would fail
def test_empty_cpr_fails(employee):
    employee.cpr = ''
    assert employee.cpr == ''

@pytest.mark.parametrize('cpr_fails', [
    '10000000000',  # Invalid upper boundary
    '999999999',    # Invalid lower boundary
    'ABCDEFGHIJ',
    '          ',
])
def test_cpr_fails(cpr_fails, employee):
    employee.cpr = cpr_fails
    assert not cpr_fails == employee.cpr

NAMES_PASS = ('name_passes', [
    'A',                                # Valid lower boundary
    'AB',                               # Valid lower boundary + 1 (3-value approach)
    'ABCDEFGHIJKLMNOPQRSTUVWXYZABCD',   # Valid upper boundary
    'ABCDEFGHIJKLMNOPQRSTUVWXYZABC',    # Valid upper boundary - 1 (3-value approach)
    'ABCDEFGHIJKLMN',                   # Middle partition value
    'abcdefghijklmn',                   # Middle partition value
    'æøåñç',
    'áéíóúàèìòùäëïöü',
    'âêîôû',
    'ÆØÅÑÇ',
    'ÁÉÍÓÚÀÈÌÒÙÄËÏÖÜ',
    'ÂÊÎÔÛ',
    'a a a a a a a',
    'a-a-a-a-a-a-a',
    '-',
    ' ',
    ''                                  # Invalid lower boundary, but the method must return an empty string
])

@pytest.mark.parametrize(*NAMES_PASS)
def test_first_name_passes(name_passes, employee):
    employee.first_name = name_passes
    assert name_passes == employee.first_name

@pytest.mark.parametrize(*NAMES_PASS)
def test_last_name_passes(name_passes, employee):
    employee.last_name = name_passes
    assert name_passes == employee.last_name

NAMES_FAIL = ('name_fails', [
    'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDE',  # Invalid upper boundary
    'abcdef1',
    'abcdef/',
    'abcdef,'
])

@pytest.mark.parametrize(*NAMES_FAIL)
def test_first_name_fails(name_fails, employee):
    employee.first_name = name_fails
    assert not name_fails == employee.first_name

@pytest.mark.parametrize(*NAMES_FAIL)
def test_last_name_fails(name_fails, employee):
    employee.last_name = name_fails
    assert not name_fails == employee.last_name

@pytest.mark.parametrize('department_passes', [
    'HR', 'Finance', 'IT', 'Sales', 'General Services', ''
])
def test_department_passes(department_passes, employee):
    employee.department = department_passes
    assert department_passes == employee.department

def test_department_fails(employee):
    fake_department = 'Bonds'
    employee.department = fake_department
    assert not fake_department == employee.department

@pytest.mark.parametrize('base_salary_passes', [
    20000,          # Valid lower boundary
    20000.01,       # Valid lower boundary + 1 (3-value approach)
    60000,          # Middle value for the valid input partition
    100000,         # Valid upper boundary
    99999.99,       # Valid upper boundary - 1 (3-value approach)
    0,              # Invalid value, but the method must return a zero in this case
])
def test_base_salary_passes(base_salary_passes, employee):
    employee.base_salary = base_salary_passes
    assert base_salary_passes == employee.base_salary

@pytest.mark.parametrize('base_salary_fails', [
    19999.99,       # Invalid lower boundary
    100000.01,      # Invalid upper boundary
    10000,          # Middle value for the invalid lower partition
    110000,         # Middle value for the invalid upper partition
    -0.01,          # Invalid lower boundary for the zero partition
    -10000
])
def test_base_salary_fails(base_salary_fails, employee):
    employee.base_salary = base_salary_fails
    assert not base_salary_fails == employee.base_salary

@pytest.mark.parametrize('educational_level_passes, educational_level_name', [
    (0, 'None'),
    (1, 'Primary'),
    (2, 'Secondary'),
    (3, 'Tertiary')
])
def test_educational_level_passes(educational_level_passes, educational_level_name, employee):
    employee.educational_level = educational_level_passes
    assert educational_level_name == employee.educational_level

@pytest.mark.parametrize('educational_level_fails', [
    -1, 4, 10, -10
])
def test_educational_level_fails(educational_level_fails, employee):
    employee.educational_level = educational_level_fails
    assert employee.educational_level == ''

# Date of birth passes
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

# Date of birth fails
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

# Date of employment passes
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

# Date of employment fails
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
    ('ABCDEFG', 100)
])
def test_shipping_costs(country, expected_shipping_costs, employee):
    employee.country = country
    assert employee.get_shipping_costs() == expected_shipping_costs