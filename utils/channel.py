import numpy as np


def emulate_channel(P, x):
    # P - матрица P(y/x)
    # на выход строка x, на выход строка y
    assert check_matrix_p(P), 'Измените матрицу P(x/y)'

    y = ''
    for i in x:
        if int(i) == 0:
            y += str(np.random.choice(2, 1, p=P[0])[0])
        else:
            y += str(np.random.choice(2, 1, p=P[1])[0])
    return y


def check_matrix_p(P):
    """
    Проверяем корректность поданой матрицы P. Для этого она должна удовлетворять
    двум свойствам:
    - Сумма элементов в строке = 1
    - Любой элемент принадлежит отрезку [0;1]
    """
    for line in P:
        sum = 0

        for i in line:
            sum += i

            # проверим, что элемент принадлежит [0;1]
            if (i > 1) or (i < 0):
                print(f"Элемент {i} в строке {line} не принадлежит отрезку [0;1]")
                return False

        # проверим, что сумма в строке равна единице
        if sum != 1:
            print(f"Сумма элементов в строке {line} не равняется единице")
            return False

    return True
