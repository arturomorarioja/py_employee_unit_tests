from app.employees import Employee

lene = Employee()
lene.cpr = '5555555555'
lene.first_name = 'Lene Rye'
lene.last_name = 'Johansen'
lene.department = 'HR'
lene.base_salary = 35045.98
lene.educational_level = 2
lene.date_of_birth = '23/8/2006'
lene.date_of_employment = '26/7/2022'
lene.country = 'Iceland'
print(f'''
    CPR: {lene.cpr}
    First name: {lene.first_name}
    Last name: {lene.last_name}
    Department: {lene.department}
    Base salary: {lene.base_salary}
    Education: {lene.educational_level}
    Date of birth: {lene.date_of_birth}
    Date of employment: {lene.date_of_employment}
    Country: {lene.country}
''')
print(f'Salary: {lene.get_salary()}')
print(f'Discount: {lene.get_discount()}')
print(f'Shipping costs: {lene.get_shipping_costs()}')