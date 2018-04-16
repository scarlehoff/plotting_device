import numpy as np
import collections

def jupyter_html_print(string):
    get_ipython().run_cell_magic(u'HTML', u'', string)

class DataTable:
    """
    This class takes as input and stores a table in the form of an array of arrays 
    with the following structure:
    self.data_raw[row][column]
    """

    # Initialiser functions
    def __init__(self, ncols = None, header = None, data = None):
        self.header = None
        self.data_raw = []
        if not ncols and not header and not data:
            raise Exception("Need either ncols, header or data to initialise")
        if data:
            self._init_from_data(data, header = header)
        elif header:
            self._init_from_header(header)
        if ncols and (header or data):
            if ncols != self.ncols:
                raise Exception("Number of columns and header provided are not compatible")
        elif ncols:
            self.ncols = ncols

    def _init_from_data(self, data, header = None):
        if header:
            self.header = header
            data_raw = data
        else:
            self.header = data[0]
            self.data_raw = data[1:]

    def _init_from_header(self, header):
        if isinstance(header, (tuple, list, np.array)):
            self.ncols = len(header)
            self.header = header
        elif isinstance(header, (str)):
            header_sp = header.split('&')
            self.header = header_sp
            self.ncols = len(header_sp)
        else:
            raise Exception("DataTable doesn't implement type {0} yet".format(type(header)))

    # Add extra content 
    def add_row(self, fields_raw, row_header = None):
        """
        Add an extra row to the DataTable
        Exposes row_header, being the first column of the row, to be filled separately
        """
        if row_header:
            fields = [row_header]
        else:
            fields = []

        if isinstance(fields_raw, str) or not isinstance(fields_raw, collections.Iterable):
            fields.append(fields_raw)
        else:
            for field in fields_raw:
                fields.append(field)

        if len(fields) != self.ncols:
            raise Exception("The number of fields provided do not match the current table size")
        self.data_raw.append(fields)

    # Printing functions
    def _str_row(self, row, escape = None):
        """ Parse the content to a row
        to a row of str()
        """
        out_row = []
        for item in row:
            new_st = str(item)
            if escape == "latex":
                new_st = new_st.replace("%", "\\%")
            out_row.append(new_st)
        return out_row

    def str_latex(self, align = "c", v_sep = "", h_sep = "", environment = "tabular"):
        """
        Print table as a latex tabular (by default) environment
        """
        environment_c = "{" + environment + "}"
        # Preprocess the table
        if "-" in h_sep or "_" in h_sep:
            latex_sep = "    \\\\ \hline\n"
        else:
            latex_sep = "     \\\\ {0}\n".format(h_sep)  
        positioning_sp = " {0} ".format(align)
        # Header always have a separator
        if self.header and h_sep == "":
            header_sep = "    \\\\ \hline\n"
        else:
            header_sep = latex_sep
        amp = " & "

        # Generate the column structure and the first few lines
        columns = "{" + v_sep + v_sep.join( self.ncols*[positioning_sp] ) + v_sep + "}"
        latex_begin = "\\begin{0}{1}".format(environment_c, columns) + "\n"
        latex_end = "\end{0}".format(environment_c)

        # Generate a list of strings
        latex_out = latex_begin 
        if self.header:
            latex_out += "\hline " + amp.join(self._str_row(self.header, escape = "latex")) + header_sep

        lines = []
        for row in self.data_raw:
            lines.append( amp.join(self._str_row(row, escape = "latex")) )
        lines.append(latex_end)

        latex_out += latex_sep.join(lines)
        return latex_out

    def str_html(self, align = "center"):
        # Create the CSS style
        table_style = "border-collapse: separate; border-spacing: 1px; width:95%; margin-left:auto; margin-right:auto;"
        cell_style = "text-align: {0};".format(align)

        # Define the html commands
        table_start = '<table style="{0}">'.format(table_style)
        table_end = "</table>"

        cell_start = '<td style="{0}">'.format(cell_style)
        cell_end = "</td>"
        cell_separator = cell_end + "\n\t\t" + cell_start # </td><td>

        row_start = "\t<tr>\n\t\t" + cell_start
        row_end = cell_end + "\n\t</tr>"

        # Build the table
        lines = [table_start]
        # Write header if it exists
        if self.header:
            bold_header = ["<strong>{0}</strong>".format(i) for i in self.header]
            new_str = row_start + cell_separator.join(bold_header) + row_end
            lines.append(new_str)
        for row in self.data_raw:
            new_str = row_start 
            new_str += cell_separator.join(self._str_row(row))
            new_str += row_end
            lines.append(new_str)
        lines.append(table_end)
        return "\n".join(lines)


    # Wrappers
    def jupyter_print(self, mode = 'html'):
        if mode == 'html':
            jupyter_html_print(self.str_html())
