from app.employees import Employee
import pytest
from pytest import approx

@pytest.fixture
def employee():
    employee = Employee()
    yield employee

@pytest.mark.parametrize('cpr_passes', [
    '1234567890',   # Valid upper and lower boundary
    '0000000000',
    '9999999999',
    '0999999999',
    ''
])
def test_cpr_passes(cpr_passes, employee):
    employee.cpr = cpr_passes
    assert cpr_passes == employee.cpr

@pytest.mark.parametrize('cpr_fails', [
    '99999999999',  # Invalid upper boundary
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
    -1,
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