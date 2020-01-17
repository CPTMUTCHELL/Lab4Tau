#ПИ регулятор:
import control.matlab as c
from control.matlab import *
import math
num1= [1];den1= [4,1];w1= tf(num1, den1)
num2= [4];den2= [7,1];w2= tf(num2, den2)
num3= [25];den3= [3,1];w3= tf(num3, den3)


def raschet(P, I):
    num4 = [P, I]
    den4 = [1, 0]
    w4 = tf(num4, den4)
    w5 = series(w1, w2, w3, w4)
    W = feedback(w5, 1, -1)
    y1, x1 = step(W)
    #Шаг по иксу(для нахождения квадратичной ошибки)
    steps = x1[2] - x1[1]
    maxy = 0
    for i in range(0, len(y1)):
        if y1[i] > maxy:
            maxy = y1[i]
    #Установившиеся значение
    Yyct = y1[len(y1) - 1]
    y2 = []
    x2 = []
    #+5%
    for i in range(0, 50, 1):
        high = 1.05 * Yyct
        y2.append(high)
    for i in range(0, 50, 1):
        x2.append(i)
    y3 = []
    x3 = []
    low = 0.95 * Yyct
    #-5%
    for i in range(0, 50, 1):
        y3.append(low)
    for i in range(0, 50, 1):
        x3.append(i)
    ppx = []
    ppy = []
    treg = 0
    #Для времени регулирования по графику
    for g in range(0, len(y1)):
        if (y1[g] - low) < 0.001:
            treg = x1[g]
            ppygrek = y1[g]
            ppx, ppy = [treg, treg], [y1[g], 0]
    poles = pole(W)
    mag, phase, omega = bode(W, dB=False)
    peregeg = (maxy - Yyct) / Yyct * 100
    stepenzatuhania=0
    A = []
    #Считаем степень затухания по графику
    for y in range(0, len(y1)):
        if x1[y] < treg and y1[y - 1] < y1[y] > y1[y + 1]:
            A.append(y1[y])
    if len(A) > 1:
        stepenzatuhania = 1 - (A[1] / A[0])

    amin = 0
    # Считаем степень колебаний по корням
    for i in range(0, len(poles)):
        if 0 > poles[i].real > poles[i - 1].real:
            amin = poles[i].real
        if 0 > poles[i].real < poles[i - 1].real and poles[i].imag != 0:
            amax = poles[i].real
            jwmax = poles[i].imag
            stepenkolebania = abs(jwmax / amax)

    # Считаем колебательность по АЧХ
    Amax = 0
    for i in range(0, len(mag)):
        if abs(mag[i] - mag[0]) < 0.05:
            omegasr = omega[i]
        if mag[i] > Amax:
            Amax = mag[i]
    kolebatelnost = Amax / (mag[0] + 0.000000000001)
    epsilon = 0
    #Считаем среднеквадратическую ошибку
    for i in range(0, len(y1)):
        epsilon = epsilon + (Yyct - y1[i] * steps) ** 2
    print("\033[35;1mПараметры регулятора : ")
    print("Время регулирования : ", treg, ". Требуемое значение : 15 c")
    print("Показатель колебательности : ", kolebatelnost, ". Требуемое значение : 1.2")
    print("Перерегулирование : ", peregeg, " %", ". Требуемое значение : 24 %")
    print("Значения регулятора:", "\nP = ", P, "\nI = ", I, "\n\033[30;1m")
    return treg, kolebatelnost, peregeg, epsilon

# Функция проверки по критериям(Не удалось подобрать ПИ регулятор с treg=15)
def check(t, M, per):
    result = False
    if t < 18:
        if M < 1.2:
            if abs(per) <= 40:
                result = True
    return result

#Функция град.спуска
def PI(P, I):
    complete = False
    while not complete:
        P1 = P + 0.00001
        P3 = P
        I1 = I
        I3 = I + 0.00001
        tr1, M1, per1, e1 = raschet(P1, I1)
        tr3, M3, per3, e3 = raschet(P3, I3)
        ans1 = check(tr1, M1, per1)
        ans3 = check(tr3, M3, per3)
        if ans1:
            P = P1
            I = I1
            complete = True
        elif ans3:
            P = P3
            I = I3
            complete = True
        else:
            e_min = min(e1, e3)
            if e_min == e1:
                P = P1
                I = I1
            elif e_min == e3:
                P = P3
                I = I3
    print(P, I)
    return P, I
Kp, Ki = PI(0.000001, 0.000001)
print("Коэф.регулятора:", "\nP = ", Kp, "\nI = ", Ki)