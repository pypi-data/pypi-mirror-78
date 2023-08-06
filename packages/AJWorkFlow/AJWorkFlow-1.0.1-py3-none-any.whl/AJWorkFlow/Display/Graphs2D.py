try:
   import matplotlib.pyplot as plt
   import numpy as np
except ImportError as error:
   print(f"Error, Module {error.__class__.__name__}  is required")


def Graph2D(x_list,y_list,_description_list):
    plt.style.use("default")
    plt.figure(figsize=(6,6))
    plt.plot(x_list,y_list)
    plt.title(_description_list[0])
    plt.xlabel(_description_list[1])
    plt.ylabel(_description_list[2])
    plt.tight_layout()
    plt.show()
def Graph2DS2(x_list1,y_list1,x_list2,y_list2,_description_list,_description_list2):
    plt.figure(figsize=(8,3))
    plt.subplot(1,2,1)
    plt.plot(x_list1,y_list1)
    plt.title(_description_list[0])
    plt.xlabel(_description_list[1])
    plt.ylabel(_description_list[2])

    plt.subplot(1,2,2)
    plt.plot(x_list2,y_list2)
    plt.title(_description_list2[0])
    plt.xlabel(_description_list2[1])
    plt.ylabel(_description_list2[2])
    plt.tight_layout()
    plt.show()

def Graph2DS3(x_list1,y_list1,x_list2,y_list2,x_list3,y_list3,_description_list,_description_list2,_description_list3):
    plt.figure(figsize=(12,3))
    plt.subplot(1,3,1)
    plt.plot(x_list1,y_list1)
    plt.title(_description_list[0])
    plt.xlabel(_description_list[1])
    plt.ylabel(_description_list[2])

    plt.subplot(1,3,2)
    plt.plot(x_list2,y_list2)
    plt.title(_description_list2[0])
    plt.xlabel(_description_list2[1])
    plt.ylabel(_description_list2[2])

    plt.subplot(1,3,3)
    plt.plot(x_list3,y_list3)
    plt.title(_description_list3[0])
    plt.xlabel(_description_list3[1])
    plt.ylabel(_description_list3[2])

    plt.tight_layout()
    plt.show()

def Graph2DVector(x_list,y_list,_description_list):
    x = np.linspace(min(x_list),max(x_list),len(x_list))
    y = np.linspace(min(y_list),max(y_list),len(y_list))
    X,Y = np.meshgrid(x,y)
    x_list = np.ndarray(x_list)
    y_list = np.ndarray(y_list)
    mag = np.sqrt(x_list**2+y_list**2)
    x_list_unit = x_list/mag
    y_list_unit = y_list/mag
    plt.figure(figsize=(6,6))
    plt.quiver(X,Y,x_list_unit,y_list_unit)
    plt.title(_description_list[0])
    plt.xlabel(_description_list[1])
    plt.ylabel(_description_list[2])
    plt.tight_layout()
    plt.show()