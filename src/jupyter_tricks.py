class DataTable:
    """
    Fill this class with arrays where each array is a row of the table
    the content of the array will be parsed to str
    Afterwards print it as latex or html
    Initialise the class with a header (an array) or the number of columns
     >>>>> In construction
    """
    def __init__(self, ncols = None, header = None, horizontal_sep = "", vertical_sep = ""):
        if header:
            try:
                self.ncols = len(header)
                self.rows = [header]
            except:
                print("TODO: catch when header does not implement len...")
        elif ncols:
            self.ncols = ncols
            self.rows = []
        else:
            raise Exception("This class needs either the header of the table or the number of columns")
        self.h_sep = horizontal_sep
        self.v_sep = vertical_sep
        
    def add_row(self, fields_raw, row_header = None):
        if row_header:
            fields = [row_header]
        else:
            fields = []
        for field in fields_raw:
            fields.append(str(field))
        if len(fields) != self.ncols:
            raise Exception("The number of fields provided do not match the current table size")
        self.rows.append(fields)
    
    def str_latex(self, align = "c"):
        if "-" in self.h_sep or "_" in self.h_sep:
            latex_sep = "    \\\\ \hline\n"
        else:
            latex_sep = "     \\\\ {0}\n".format(self.h_sep)  
        positioning_sp = " {0} ".format(align)
        columns = "{" + self.v_sep + self.v_sep.join( self.ncols*[positioning_sp] ) + self.v_sep + "}"
        lines = ["\\begin{tabular}" + columns]
        for row in self.rows:
            new_str = " & ".join(row)
            lines.append(new_str)
        lines.append("\end{tabular}")
        return latex_sep.join(lines)
        
    def str_html(self, align = "center"):
        # Create the style
        style_table = "border-collapse: separate; border-spacing: 1px; width:95%; margin-left:auto; margin-right:auto;"     
        cell_style = "text-align: {0};".format(align)

        cell_start = '<td style="{0}">'.format(cell_style)
        cell_separator = "</td>" + cell_start

        # Build the table
        lines = ['<table style="{0}">'.format(style_table)]
        for row in self.rows:
            lines.append("    <tr>")
            new_str = "        " + cell_start
            new_str += cell_separator.join(row)
            new_str += "</td>"
            lines.append(new_str)
            lines.append("    </tr>")
        lines.append("</table>")
        lines.append("</div>")
        return "\n".join(lines)
    
    def jupyter_print(self):
        get_ipython().run_cell_magic(u'HTML', u'', self.str_html())
