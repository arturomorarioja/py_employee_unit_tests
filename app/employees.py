from dataclasses import dataclass
import re
import math
from datetime import date
from dateutil.relativedelta import relativedelta

@dataclass(frozen=True)
class EmployeeConstants:
    EDU_LEVELS = ('None', 'Primary', 'Secondary', 'Tertiary')
    DEPARTMENTS = ('HR', 'Finance', 'IT', 'Sales', 'General Services')
    DATE_FORMAT = '%d/%m/%Y'
    COUNTRIES_NO_SHIPPING_COSTS = ('Denmark', 'Norway', 'Sweden')
    COUNTRIES_HALF_SHIPPING_COSTS = ('Iceland', 'Finland')

class Employee(EmployeeConstants):

    def __name_is_valid(self, name: str) -> bool:
        return len(name) > 0 and len(name) <= 30 \
            and bool(re.match(r'^[a-zA-ZæøåñçáéíóúàèìòùäëïöüâêîôûÆØÅÑÇÁÉÍÓÚÀÈÌÒÙÄËÏÖÜÂÊÎÔÛ \-]+$', name))

    def __validate_date(self, date_string: str) -> str | bool:
        try:
            day, month, year = map(int, date_string.split('/'))
            return date(year, month, day)
        except ValueError:
            return False

    @property
    def cpr(self) -> str | bool:
        try:
            return self.__cpr
        except AttributeError:
            return ''

    @cpr.setter    
    def cpr(self, cpr_no: str) -> bool:
        if not bool(re.match(r'^\d{10}$', cpr_no)):
            return False
        self.__cpr = cpr_no
        return True
    
    @property
    def first_name(self) -> str | bool:
        try:
            return self.__first_name
        except AttributeError:
            return ''

    @first_name.setter
    def first_name(self, first_name: str) -> bool:
        if not self.__name_is_valid(first_name):
            return False
        self.__first_name = first_name
        return True

    @property
    def last_name(self) -> str | bool:
        try:
            return self.__last_name
        except AttributeError:
            return ''

    @last_name.setter    
    def last_name(self, last_name: str) -> bool:
        if not self.__name_is_valid(last_name):
            return False
        self.__last_name = last_name
        return True
    
    @property
    def department(self) -> str | bool:
        try:
            return self.__department
        except AttributeError:
            return ''

    @department.setter    
    def department(self, department: str) -> bool:
        if not department in self.DEPARTMENTS:
            return False
        self.__department = department
        return True
    
    @property
    def base_salary(self) -> float | bool:
        try:
            return self.__base_salary
        except AttributeError:
            return 0

    @base_salary.setter
    def base_salary(self, base_salary: float) -> bool:
        if base_salary < 20000 or base_salary > 100000:
            return False
        self.__base_salary = math.floor(round(base_salary * 100)) / 100
        return True
    
    @property
    def educational_level(self) -> int | bool:
        try:
            return self.EDU_LEVELS[self.__educational_level]
        except AttributeError:
            return ''
    
    @educational_level.setter
    def educational_level(self, educational_level: int) -> bool:
        if educational_level < 0 or educational_level > 3:
            return False
        self.__educational_level = educational_level
        return True
        
    @property
    def date_of_birth(self) -> date | bool:
        try:
            return self.__date_of_birth
        except AttributeError:
            return ''
    
    @date_of_birth.setter
    def date_of_birth(self, date_of_birth: str) -> bool:
        dob = self.__validate_date(date_of_birth)
        if not dob:
            return False

        # The date of birth must be at least 18 years before now
        if dob + relativedelta(years=18) > date.today():
            return False
        self.__date_of_birth = dob
        return True

    @property
    def date_of_employment(self) -> date | bool:
        try:
            return self.__date_of_employment
        except AttributeError:
            return ''
    
    @date_of_employment.setter
    def date_of_employment(self, date_of_employment: str) -> bool:
        doe = self.__validate_date(date_of_employment)
        if not doe:
            return False
        
        # The date of employment must be equal or lower than today
        if doe > date.today():
            return False
        self.__date_of_employment = doe
        return True
    
    @property
    def country(self) -> str | bool:
        try:
            return self.__country
        except AttributeError:
            return ''

    @country.setter
    def country(self, country: str) -> bool:
        self.__country = country
        return True
    
    # Calculation of actual salary based on educational level
    def get_salary(self) -> float | bool:
        try:
            return self.__base_salary + (self.__educational_level * 1220)
        except AttributeError:
            return 0

    # Calculation of employee discount based on years of employment    
    def get_discount(self) -> float | bool:
        try:
            return relativedelta(date.today(), self.__date_of_employment).years * 0.5
        except AttributeError:
            return 0
    
    # Calculation of shipping costs based on employee country
    def get_shipping_costs(self) -> float | bool:
        try:
            if self.__country in self.COUNTRIES_NO_SHIPPING_COSTS:
                return 0
            elif self.__country in self.COUNTRIES_HALF_SHIPPING_COSTS:
                return 50
            return 100
        except AttributeError:
            return 100