from sympy import symbols
from sympy import Eq
from sympy import solve
from sympy import diff
from sympy import integrate
from sympy import latex
from sympy import lambdify
from sympy import *



class Equation:

    def __init__(self, equation: str, variable='x'):
        """
        Initializes an equation from a string, with the option to specify the variable.
        
        Parameters:
        - equation (str): The equation in string form, e.g., 'x**2 + 3*x + 2 = 0'
        - variable (str): The variable in the equation (default is 'x')
        """
        self.equation_string = equation

        equation.replace(variable, 'x')
        left_eq, right_eq = equation.split('=')
        x = symbols(variable)

        self.variable = symbols(variable)
        self.equation = Eq(eval(left_eq), eval(right_eq))

    def __str__(self):
        return self.equation_string
    
    def __repr__(self):
        return f'${latex(self.equation)}$'
    
    
    #def display(self):
    #    """
    #    Displays the equation using LaTeX rendering in Jupyter Notebook.
    #    """
    #    display(Latex(f"${latex(self.equation)}$"))

    @property
    def as_lambda(self):
        """
        Returns a lambda function representing the equation (LHS - RHS).
        
        The result is a function f(x) such that f(x) == 0 is equivalent to the equation.
        """
        expr = self.equation.lhs - self.equation.rhs
        return lambdify(self.variable, expr, modules='math')

    @classmethod
    def from_simpy_eq(cls, simpy_eq, variable):
        string_eq = f'{simpy_eq.lhs} = {simpy_eq.rhs}'
        equation = Equation(string_eq, str(variable))
        return equation




    def solve(self):
        """
        Solves the equation for the variable.

        Returns:
        - solutions: The solutions of the equation.
        """
        solutions = solve(self.equation, self.variable)
        return solutions



    def differentiate(self):
        """
        Differentiates the equation with respect to the variable.

        Returns:
        - derivative: The symbolic derivative of the equation.
        """
        # Differentiate both sides of the equation with respect to the variable
        left_diff = diff(self.equation.lhs, self.variable)
        right_diff = diff(self.equation.rhs, self.variable)
        
        # Return the differentiated equation
        equation = Eq(left_diff, right_diff)
        equation = Equation.from_simpy_eq(equation, self.variable)
        return equation
    

    def integrate(self):
        """
        Integrates the equation with respect to the variable.

        Returns:
        - Equation: The symbolic integral of the equation as a new Equation instance.
        """
        left_integral = integrate(self.equation.lhs, self.variable)
        right_integral = integrate(self.equation.rhs, self.variable)
        return Equation.from_simpy_eq(Eq(left_integral, right_integral), self.variable)









def is_prime(n: int) -> bool:
    """
    Determines whether a number is prime.

    A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.

    Parameters:
        n (int): The number to check for primality.

    Returns:
        bool: True if the number is prime, False otherwise.

    Example:
        >>> is_prime(5)
        True
        >>> is_prime(10)
        False

    Note:
        The function returns False for numbers less than or equal to 1, as they are not prime.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True




def find_prime_factors(n: int) -> list[tuple[int, int]]:
    """
    Finds the prime factors of a number along with their exponents.

    Parameters:
        n (int): The number to find the prime factors of.

    Returns:
        list[tuple[int, int]]: A list of tuples, where each tuple contains 
        a prime factor and its corresponding exponent in the factorization of n.

    Example:
        >>> find_prime_factors(18)
        [(2, 1), (3, 2)]

    Note:
        The function returns an empty list for n <= 1 since there are no prime factors.
    """
    factors = []
    # Check for factor of 2
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    if count > 0:
        factors.append((2, count))

    # Check for odd factors from 3 upwards
    factor = 3
    while factor * factor <= n:
        count = 0
        while n % factor == 0:
            n //= factor
            count += 1
        if count > 0:
            factors.append((factor, count))
        factor += 2
    
    # If n is still greater than 2, it is prime
    if n > 2:
        factors.append((n, 1))

    return factors



def divisors(n: int) -> list[int]:
    """
    Returns a list of divisors of a given integer n.

    A divisor of n is any integer that divides n without leaving a remainder.

    Parameters:
        n (int): The number to find the divisors of.

    Returns:
        list[int]: A list of divisors of n.

    Example:
        >>> divisors(12)
        [1, 2, 3, 4, 6, 12]

    Note:
        The function includes both 1 and n as divisors.
    """
    divs = []
    for i in range(1, n + 1):
        if n % i == 0:
            divs.append(i)
    return divs