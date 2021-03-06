import numpy as np
import decimal as dec

class NewNumber:

    """
        NewNumber(x, dx) 
        where dx is the error associated with x
        Overloads the sum/subtraction/multiplication/division operations 
        for correct error propagation
    """

    def __init__(self, x, dx = 0.0, prec = None):
        self.prec = prec
        if isinstance(x, (tuple, list)) and len(x) == 2:
            self.x = x[0]
            self.dx = x[1]
        else:
            self.x = float(x)
            self.dx = float(dx)

    def _retrieve_first_digit(self, nonzero = False):
        """
        Retrieves first digit of the number and the stat error on the number
        if nonzero = True, returns the first number which is non 0
        """
        str_x = str(self.x).replace(".", "").replace("-","")
        str_dx = str(self.dx).replace(".", "").replace("-","")
        
        if nonzero:
            if self.x != 0.0:
                str_x = str_x.replace("0", "")
            if self.dx != 0.0:
                str_dx = str_dx.replace("0", "")

        f_x = int(str_x[0])
        f_dx = int(str_dx[0])

        return f_x, f_x
        
    def _autogenerate_precision(self):
        if self.prec:
            # Precision has been set from outside
            return 
        precision = np.floor(np.log10(self.dx))

        # If the error's first number is 1, get an extra digit!
        _, first_digit = self._retrieve_first_digit(nonzero = True)
        if first_digit == 1:
            precision -= 1

        if precision > 0:
            # Use the full number for self.dx > 1.0
            self.set_precision(0)
        else:
            self.set_precision(-int(precision))

    def power_of_10(self, partition = 1):
        """
            Returns the power of 10 corresponding to 
            scientific notation for self.x
            Partition decides from which number onwards
            we count a new power of 10
            By default: 1 
            (ie, if partition = 2: 152 = 15.2 * 10)
        """
        pow10 = np.floor(np.log10(self.x))
        f, _ = self._retrieve_first_digit(nonzero = True)
        if f < partition:
            pow10 -= 1

        return int(pow10)

    def ceil(self, decimals = 0):
        if decimals == 0:
            new_x = np.ceil(self.x)
            new_dx = np.ceil(self.dx)
        else:
            f_x = dec.Decimal(self.x)
            f_dx = dec.Decimal(self.dx)
            base_n = str(pow(10,-decimals))
            f_n = dec.Decimal(base_n)
            
            new_x = f_x.quantize(f_n, rounding=dec.ROUND_UP)
            new_dx = f_dx.quantize(f_n, rounding=dec.ROUND_UP)

        return NewNumber(new_x, new_dx)

    def floor(self, decimals = 0):
        if decimals == 0:
            new_x = np.floor(self.x)
            new_dx = np.floor(self.dx)
        else:
            f_x = dec.Decimal(self.x)
            f_dx = dec.Decimal(self.dx)
            base_n = str(pow(10,-decimals))
            f_n = dec.Decimal(base_n)
            
            new_x = f_x.quantize(f_n, rounding=dec.ROUND_DOWN)
            new_dx = f_dx.quantize(f_n, rounding=dec.ROUND_DOWN)

        return NewNumber(new_x, new_dx)

    def round(self, decimals = 0):
        new_x = np.round(self.x, decimals = decimals)
        new_dx = np.round(self.dx, decimals = decimals)
        return NewNumber(new_x, new_dx)

    def set_precision(self, precision):
        """  How many decimal places to print or round to
        """
        self.prec = precision

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

    ####### Intrinsic overrides
    def __str__(self):
        if (self.dx == 0.0):
            return str(self.x)
        else:
            self._autogenerate_precision()
            base_string = "{0:.{prec}f} +/- {1:.{prec}f}"
            return base_string.format(self.x, self.dx, prec = self.prec)

    def __ceil__(self):
        if self.prec:
            return self.ceil(self.prec)
        else:
            return self.ceil()

    def __floor__(self):
        if self.prec:
            return self.floor(self.prec)
        else:
            return self.floor()

    def __float__(self):
        return float(self.x)

    def __int__(self):
        return int(self.x)

    # Operations override

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

