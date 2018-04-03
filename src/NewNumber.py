import numpy as np

class NewNumber:

    """
        NewNumber(x, dx) 
        where dx is the error associated with x
        Overloads the sum/subtraction/multiplication/division operations 
        for correct error propagation
    """

    def __init__(self, x, dx = 0.0):
        self.prec = None
        if isinstance(x, (tuple, list)) and len(x) == 2:
            self.x = x[0]
            self.dx = x[1]
        else:
            self.x = float(x)
            self.dx = float(dx)

    def _autogenerate_precision(self):
        if self.prec:
            # Precision has been set from outside
            return 
        precision = int(np.log10(self.dx)) - 1
        if precision > 0:
            self.set_precision(0)
        else:
            self.set_precision(-precision)
            
        
    def set_precision(self, precision):
        """  How many decimal places to print
        """
        self.prec = precision

    def __str__(self):
        if (self.dx == 0.0):
            return str(self.x)
        else:
            self._autogenerate_precision()
            base_string = "{0:.{prec}f} +/- {1:.{prec}f}"
            return base_string.format(self.x, self.dx, prec = self.prec)

    def _parse_number(self, number):
        """ 
        Checks type of number and returns 
        x and dx
        if type(x) == float or int, dx = 0.0
        """
        if isinstance(number, type(self)):
            x = number.x
            dx = number.dx
        elif isinstance(number, (float, int)):
            x = float(number)
            dx = 0.0
        else:
            raise Exception("Sum with type {0} not implemented".format(type(number)))
        return x, dx

    def _sum_n(self, number, factor = 1.0):
        """
        Overloads the addition and subtraction operations
        returns a new instance of NewNumber
        """
        x, dx = self._parse_number(number)
        new_x = self.x + factor*x
        new_dx = np.sqrt(pow(self.dx, 2) + pow(dx, 2))
        return NewNumber(new_x, new_dx)


    def __add__(self, number):
        return self._sum_n(number, factor = 1.0)
    def __sub__(self, number):
        return self._sum_n(number, factor = -1.0)

    def __truediv__(self, number):
        x, dx = self._parse_number(number)
        new_x = self.x / x
        a = pow( self.dx/x , 2)
        b = pow( dx*self.x/x/x, 2)
        new_dx = np.sqrt(a + b)
        return NewNumber(new_x, new_dx)

    def __mul__(self, number):
        x, dx = self._parse_number(number)
        new_x = self.x * x
        new_dx = np.sqrt( pow(x*self.dx,2) + pow(self.x*dx,2) )
        return NewNumber(new_x, new_dx)





        


