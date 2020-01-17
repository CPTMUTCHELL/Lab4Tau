import control.matlab as c
from control.matlab import *
import math
import matplotlib.pyplot as plt

#Звенья
num1= [1];den1= [4,1];w1= tf(num1, den1)
num2= [4];den2= [7,1];w2= tf(num2, den2)
num3= [25];den3= [3,1];w3= tf(num3, den3)


def raschet(P, I, D):
    num4 = [D, P, I];den4 = [1, 0];w4 = tf(num4, den4)
    w5 = series(w1, w2, w3,w4)
    W = feedback(w5, 1, -1)

    y1, x1 = step(W)
    steps = x1[2] - x1[1]
    maxy = 0

    #Установившееся значение
    for i in range(0, len(y1)):
        if y1[i] > maxy:
            maxy = y1[i]
    Yyct = y1[len(y1) - 1]

    y2 = []
    x2 = []
    #+5% от уст
    for i in range(0, 50, 1):
        high = 1.05 * Yyct
        y2.append(high)
    for i in range(0, 50, 1):
        x2.append(i)
    y3 = []
    x3 = []
    low = 0.95 * Yyct
    #-5% от уст
    for i in range(0, 50, 1):
        y3.append(low)
    for i in range(0, 50, 1):
        x3.append(i)
    ppx = []
    ppy = []
    ppx1 = []
    ppy1 = []
    ppx2 = []
    ppy2 = []
    pptime = 0
    pptime1=0
    pptime2 = 0
    Treg=[]

    #Время рег.по графику
    for g in range(0, len(y1)):
        if (y1[g] - low) < 0.001:
            pptime = x1[g]
            ppygrek = y1[g]
            ppx, ppy = [pptime, pptime], [y1[g], 0]
            Treg.append(pptime)
    for j in range(0, len(y1)):
        if (high-y1[j]) < 0.001:
            pptime1 = x1[j]
            ppygrek1 = y1[j]
            ppx1, ppy1 = [pptime1, pptime1], [y1[j], 0]
            Treg.append(pptime1)
    treg=max(Treg)

    poles = pole(W)
    peregeg = (maxy - Yyct) / Yyct * 100

    A = []

    stepenkoleb=0
    amin = 0
    for i in range(0, len(poles)):
        if 0 > poles[i].real > poles[i - 1].real:
            amin = poles[i].real
        if 0 > poles[i].real < poles[i - 1].real and poles[i].imag != 0:
            amax = poles[i].real
            jwmax = poles[i].imag
            stepenkoleb = abs(jwmax / amax)

    stepenzatuhania=0
    for y in range(0, len(y1)):
        if x1[y] < treg and y1[y - 1] < y1[y] > y1[y + 1]:

            A.append(y1[y])
    if len(A) > 1:
        stepenzatuhania = 1 - (A[0] / A[1])



    #Квадратич.ошибка epsilon
    epsilon = 0
    for i in range(0, len(y1)):
        epsilon = epsilon + (Yyct - y1[i] * steps) ** 2
    print("Параметры регулятора : ")
    print("Время регулирования : ", treg, ". Требуемое значение : 15c")
    print("Перерегулирование : ", peregeg, " %", ". Требуемое значение : 24%")
    print("Степень затухания : ", stepenzatuhania)
    print("Степень колебательности : ", stepenkoleb)
    print("Значения регулятора:", "\nP = ", P, "\nI = ", I, "\nD = ", D, )
    return treg, peregeg, epsilon

#Функция проверки
def check(t,  per):
    result = False
    if t <= 15:
         if per < 24:
            result = True
    return result

#Функция для ПИД
def PID(P, I, D):
    complete = False
    while not complete:
        P1 = P + 0.001
        P2 = P
        P3 = P
        I1 = I
        I2 = I + 0.001
        I3 = I
        D1 = D
        D2 = D
        D3 = D + 0.001
        tr1, per1, e1, = raschet(P1, I1, D1)
        tr2, per2, e2, = raschet(P2, I2, D2)
        tr3,  per3, e3 = raschet(P3, I3, D3)
        ans1 = check(tr1,  per1)
        ans2 = check(tr2,  per2)
        ans3 = check(tr3,  per3)
        if ans1:
            P = P1
            I = I1
            D = D1
            complete = True
        elif ans2:
            P = P2
            I = I2
            D = D2
            complete = True
        elif ans3:
            P = P3
            I = I3
            D = D3
            complete = True
        else:
            e_min = min(e1, e2, e3)
            if e_min == e1:
                P = P1
                I = I1
                D = D1
            elif e_min == e2:
                P = P2
                I = I2
                D = D2
            elif e_min == e3:
                P = P3
                I = I3
                D = D3
    return P, I, D



Kp, Ki, Kd = PID(0.00001, 0.00001, 0.00001)
print("Финальная Коэф.регулятора:", "\nP = ", Kp, "\nI = ", Ki, "\nD = ", Kd)
num4 = [Kd, Kp, Ki];den4 = [1, 0];w4 = tf(num4, den4)
w5 = series(w1, w2, w3,w4)
w = feedback(w5, 1, -1)
y,x=step(w)
plt.plot(x,y,"r")
plt.plot([0,80],[0.95*y[-1],0.95*y[-1]],"b")
plt.plot([0,80],[1.05*y[-1],1.05*y[-1]],"b")
plt.title('Переходная функция ')
plt.ylabel('Амплитуда h(t)')
plt.xlabel('t(с)')
plt.grid(True)
plt.show()






