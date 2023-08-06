try:
   from prettytable import PrettyTable
   import numpy as np
except ImportError as error:
   print(f"Error, Module {error.__class__.__name__}  is required")


def graphTableResultsXY(x_list,y_list):
    mytable = PrettyTable()
    for x,y in zip(x_list,y_list):
        mytable.add_row(["{:0.2f}".format(x),"{:0.6f}".format(y)])
    print(mytable)

def graphTableResults(y_list):
    mytable = PrettyTable()
    x_list = np.linspace(0,len(y_list),len(y_list))
    for x,y in zip(x_list,y_list):
        mytable.add_row(["{:0.2f}".format(x),"{:0.6f}".format(y)])
    print(mytable)

