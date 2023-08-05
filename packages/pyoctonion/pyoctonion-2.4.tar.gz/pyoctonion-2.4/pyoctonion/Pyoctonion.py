import numpy as np
import sympy as sym
import math
import pyquaternion as pqu


class Octonion:
    def __init__(self, x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7):
        self.x_0 = x_0
        self.x_1 = x_1
        self.x_2 = x_2
        self.x_3 = x_3
        self.x_4 = x_4
        self.x_5 = x_5
        self.x_6 = x_6
        self.x_7 = x_7
        self.norm = self.cal_norm()
        # self.conjugate = self.cal_conjugate()

    # self.inverse = self.cal_inverse()

    def Octon(self, x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7):  # define Octonion
        r_1 = [x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7]
        a_1 = np.array(r_1, float)
        return a_1

    def cal_norm(self):  # define norm
        b_1 = math.sqrt(
            self.x_0 ** 2
            + self.x_1 ** 2
            + self.x_2 ** 2
            + self.x_3 ** 2
            + self.x_4 ** 2
            + self.x_5 ** 2
            + self.x_6 ** 2
            + self.x_7 ** 2
        )
        return b_1

    def cal_conjugate(self):
        r_2 = [
            self.x_0,
            -(self.x_1),
            -(self.x_2),
            -(self.x_3),
            -(self.x_4),
            -(self.x_5),
            -(self.x_6),
            -(self.x_7),
        ]
        a_2 = np.array(r_2, float)
        return a_2

    @property
    def conjugate(self):
        """r_2 = [
            self.x_0,
            -(self.x_1),
            -(self.x_2),
            -(self.x_3),
            -(self.x_4),
            -(self.x_5),
            -(self.x_6),
            -(self.x_7),
        ]
        a_2 = np.array(r_2, float)"""
        conj = Octonion(
            self.x_0,
            -(self.x_1),
            -(self.x_2),
            -(self.x_3),
            -(self.x_4),
            -(self.x_5),
            -(self.x_6),
            -(self.x_7),
        )
        return conj

    def cal_multiply(self, x, y):  # define octonion multiplication
        # from pyquaternion import Quaternion
        a = pqu.Quaternion(x.x_0, x.x_1, x.x_2, x.x_3)
        b = pqu.Quaternion(x.x_4, x.x_5, x.x_6, x.x_7)
        c = pqu.Quaternion(y.x_0, y.x_1, y.x_2, y.x_3)
        d = pqu.Quaternion(y.x_4, y.x_5, y.x_6, y.x_7)
        a_1 = a * c - (d.conjugate) * b
        b_1 = (d * a) + (b * (c.conjugate))
        # print(np.array(a_1, float))
        # print(np.array(b_1, float))
        print(
            self.Octon(a_1[0], a_1[1], a_1[2], a_1[3], b_1[0], b_1[1], b_1[2], b_1[3])
        )
        xy = [a_1[0], a_1[1], a_1[2], a_1[3], b_1[0], b_1[1], b_1[2], b_1[3]]
        xyz = np.array(xy, float)
        return xyz

    @property
    def inverse(self):  # define inverse
        # from pyquaternion import Quaternion
        b = self.cal_conjugate()
        # print("conjugate:{}".format(b))
        c = self.norm
        d = c ** 2
        e = [
            b[0] / d,
            b[1] / d,
            b[2] / d,
            b[3] / d,
            b[4] / d,
            b[5] / d,
            b[6] / d,
            b[7] / d,
        ]
        # x = np.array(e, float)
        x = Octonion(
            b[0] / d,
            b[1] / d,
            b[2] / d,
            b[3] / d,
            b[4] / d,
            b[5] / d,
            b[6] / d,
            b[7] / d,
        )
        return x

    def __mul__(x, y):
        if isinstance(y, Octonion):
            a = pqu.Quaternion(x.x_0, x.x_1, x.x_2, x.x_3)
            b = pqu.Quaternion(x.x_4, x.x_5, x.x_6, x.x_7)
            c = pqu.Quaternion(y.x_0, y.x_1, y.x_2, y.x_3)
            d = pqu.Quaternion(y.x_4, y.x_5, y.x_6, y.x_7)
            a_1 = a * c - (d.conjugate) * b
            b_1 = (d * a) + (b * (c.conjugate))
            # xy = [a_1[0], a_1[1], a_1[2], a_1[3], b_1[0], b_1[1], b_1[2], b_1[3]]
            # xyz = np.array(xy, float)
            mul = Octonion(
                a_1[0], a_1[1], a_1[2], a_1[3], b_1[0], b_1[1], b_1[2], b_1[3]
            )
            return mul
        raise NotImplementedError

    def __add__(x, y):
        if isinstance(y, Octonion) and isinstance(x, Octonion):
            total = [
                x.x_0 + y.x_0,
                x.x_1 + y.x_1,
                x.x_2 + y.x_2,
                x.x_3 + y.x_3,
                x.x_4 + y.x_4,
                x.x_5 + y.x_5,
                x.x_6 + y.x_6,
                x.x_7 + y.x_7,
            ]
            addition = Octonion(
                total[0],
                total[1],
                total[2],
                total[3],
                total[4],
                total[5],
                total[6],
                total[7],
            )
            return addition
        elif isinstance(x, Octonion) and not isinstance(y, Octonion):
            total = [x.x_0 + y, x.x_1, x.x_2, x.x_3, x.x_4, x.x_5, x.x_6, x.x_7]
            addition = Octonion(
                total[0],
                total[1],
                total[2],
                total[3],
                total[4],
                total[5],
                total[6],
                total[7],
            )
            return addition
        raise NotImplementedError

    def __radd__(y, x):
        # print(x)
        # print(y)
        if isinstance(y, Octonion):
            total = [x + y.x_0, y.x_1, y.x_2, y.x_3, y.x_4, y.x_5, y.x_6, y.x_7]
            addition = Octonion(
                total[0],
                total[1],
                total[2],
                total[3],
                total[4],
                total[5],
                total[6],
                total[7],
            )
            return addition
        raise NotImplementedError

    def __sub__(x, y):
        if isinstance(y, Octonion):
            total = [
                x.x_0 - y.x_0,
                x.x_1 - y.x_1,
                x.x_2 - y.x_2,
                x.x_3 - y.x_3,
                x.x_4 - y.x_4,
                x.x_5 - y.x_5,
                x.x_6 - y.x_6,
                x.x_7 - y.x_7,
            ]
            addition = Octonion(
                total[0],
                total[1],
                total[2],
                total[3],
                total[4],
                total[5],
                total[6],
                total[7],
            )
            return addition
        elif isinstance(x, Octonion) and not isinstance(y, Octonion):
            total = [x.x_0 - y, x.x_1, x.x_2, x.x_3, x.x_4, x.x_5, x.x_6, x.x_7]
            addition = Octonion(
                total[0],
                total[1],
                total[2],
                total[3],
                total[4],
                total[5],
                total[6],
                total[7],
            )
            return addition
        raise NotImplementedError

    def __rsub__(y, x):
        # print(x)
        # print(y)
        if isinstance(y, Octonion):
            total = [x - y.x_0, y.x_1, y.x_2, y.x_3, y.x_4, y.x_5, y.x_6, y.x_7]
            addition = Octonion(
                total[0],
                total[1],
                total[2],
                total[3],
                total[4],
                total[5],
                total[6],
                total[7],
            )
            return addition
        raise NotImplementedError

    def __repr__(self):
        return "%+.2f %+0.2fi %+0.2fj %+0.2fk %+0.2fl %+0.2fil %+0.2fjl %+0.2fkl" % (
            self.x_0,
            self.x_1,
            self.x_2,
            self.x_3,
            self.x_4,
            self.x_5,
            self.x_6,
            self.x_7,
        )


# b = Octonion(1, 0, 0, 0, 0, 0, 1, 1)
# c = Octonion(1, 0, 0, 0, 0, 0, 1, 1)
# print(b)
# print(c)
# print(b.conjugate)
# print(b.inverse)
# print(b * c)
# print(b + c)
# print(b - c)
# print(2 + b)
# print(b + 2)
# print(b - 2)
# print(2 - b)


# octonion.oct_quad(0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0)

# octonion.oct_quad(2/3,0,0,-1/3,-1/3,0,0,0,-1/3,0,0,2/3,2/3,0,0,0)

# octonion.oct_quad(0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0)

# octonion.oct_quad(0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,8)

# octonion.oct_quad(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)

