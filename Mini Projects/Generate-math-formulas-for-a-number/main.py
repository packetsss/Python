"""
This project is under development
"""

import math
import random
# import numpy as np
from scipy.integrate import quad
# from pylatex.utils import italic, NoEscape
# from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
#     Plot, Figure, Matrix, Alignat
import matplotlib.pyplot as plt

formulas = {
    "e^{i\pi }": ("math.e**(1j*math.pi)", -1), 
    "\pi": ("math.pi", math.pi), 
    "e": ("math.e", math.e),
    "1": ("1", 1),
    "0": ("0", 0),
    "\int _{\:-\infty }^{\infty }e^{-x^2}dx": ("quad(lambda x: math.e**(-x**2), -np.inf, np.inf)[0]", math.sqrt(math.pi)),
}

# doc = Document()

# for x in list(formulas.items()):
#     func = x[0]
#     ans = round(x[1][1], 3)
#     print(func, ans)
#     doc.append(Math(data=[NoEscape(func), '=', ans]))

# doc.generate_pdf('formula', compiler='pdflatex')

plt.plot()
# plt.ion()
for x in list(formulas.items()):
    func = x[0]
    ans = round(x[1][1], 3)
plt.text(0.5, 0.5, f'${list(formulas.items())[0][0]}$')
    # plt.pause(0.01)

plt.show()


# formulas_list = list(formulas.items())
# a = eval(formulas_list[5][0])
# print(a, formulas_list[5][1])
# a = complex(round(a.real),round(a.imag))
# a = a.real if a.imag == 0 else a

# print(a)
