import numpy as np

def computeH(t1, t2):

    matrix_list = []

    for i in range(len(t1)):

        p1 = np.matrix([t1[i, 0], t1[i, 1], 1])
        p2 = np.matrix([t2[i, 0], t2[i, 1], 1])

        a2 = [0, 0, 0, -p2.item(2) * p1.item(0), -p2.item(2) * p1.item(1), -p2.item(2) * p1.item(2),
              p2.item(1) * p1.item(0), p2.item(1) * p1.item(1), p2.item(1) * p1.item(2)]
        a1 = [-p2.item(2) * p1.item(0), -p2.item(2) * p1.item(1), -p2.item(2) * p1.item(2), 0, 0, 0,
              p2.item(0) * p1.item(0), p2.item(0) * p1.item(1), p2.item(0) * p1.item(2)]

        matrix_list.append(a1)
        matrix_list.append(a2)

    matrix = np.matrix(matrix_list, dtype='float')

    _, _, v = np.linalg.svd(matrix)

    h = np.reshape(v[8], (3, 3))

    h /= h[2, 2]
    print(h)

    return h