import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import time
import statistics
import matplotlib.image as mpimg
import cv2
from matplotlib.colors import LogNorm
import scipy.sparse


def DFT_slow(inputArray):
    N = inputArray.size
    V = np.array([[np.exp(-2j * np.pi * v * y / N) for v in range(N)] for y in range(N)])
    return inputArray.dot(V)


def IDFT_slow(inputArray):
    N = inputArray.size
    V = np.array([[np.exp(2j * np.pi * v * y / N) for v in range(N)] for y in range(N)])
    return inputArray.dot(V)


def FFT(inputArray):
    inputArray = np.asarray(inputArray, dtype=float)
    N = inputArray.shape[0]

    if N % 2 > 0:
        raise ValueError("size of x must be a power of 2")
    elif N <= 32:  # this cutoff should be optimized
        return DFT_slow(inputArray)
    else:
        X_even = FFT(inputArray[::2])
        X_odd = FFT(inputArray[1::2])
        factor = np.exp(-2j * np.pi * np.arange(N) / N)
        return np.concatenate([X_even + factor[:int(N / 2)] * X_odd, X_even + factor[int(N / 2):] * X_odd])


def FFT_inverse(inputArray):
    inputArray = np.asarray(inputArray, dtype=complex)
    N = inputArray.shape[0]

    if N % 2 > 0:
        raise ValueError("size of x must be a power of 2")
    elif N <= 32:  # this cutoff should be optimized
        return IDFT_slow(inputArray)
    else:
        X_even = FFT_inverse(inputArray[::2])
        X_odd = FFT_inverse(inputArray[1::2])
        factor = np.exp(2j * np.pi * np.arange(N) / N)
        return np.concatenate([X_even + factor[:int(N / 2)] * X_odd, X_even + factor[int(N / 2):] * X_odd])


def FFT_2D(input2DArray):
    N = input2DArray.shape[1]
    if N % 2 > 0:
        raise ValueError("size of x must be a power of 2")
    elif N <= 32:  # this cutoff should be optimized
        return np.array([DFT_slow(input2DArray[i, :]) for i in range(input2DArray.shape[0])])
    else:
        X_even = FFT_2D(input2DArray[:, ::2])
        X_odd = FFT_2D(input2DArray[:, 1::2])
        factor = np.array([np.exp(-2j * np.pi * np.arange(N) / N) for i in range(input2DArray.shape[0])])
        return np.hstack([X_even + np.multiply(factor[:, :int(N / 2)], X_odd),
                          X_even + np.multiply(factor[:, int(N / 2):], X_odd)])


def IFFT_2D(input2DArray):
    N = input2DArray.shape[1]
    if N % 2 > 0:
        raise ValueError("size of x must be a power of 2")
    elif N <= 32:  # this cutoff should be optimized
        return np.array([IDFT_slow(input2DArray[i, :]) for i in range(input2DArray.shape[0])])
    else:
        X_even = IFFT_2D(input2DArray[:, ::2])
        X_odd = IFFT_2D(input2DArray[:, 1::2])
        factor = np.array([np.exp(2j * np.pi * np.arange(N) / N) for i in range(input2DArray.shape[0])])
        return np.hstack([X_even + np.multiply(factor[:, :int(N / 2)], X_odd),
                          X_even + np.multiply(factor[:, int(N / 2):], X_odd)])


def IDFT(inputArray):
    return list(map(lambda a: a / len(inputArray), IDFT_slow(inputArray)))


def IFFT(inputArray):
    return list(map(lambda a: a / len(inputArray), FFT_inverse(inputArray)))


def twoD_FFT(input2DArray):
    input2DArray = np.asarray(input2DArray, dtype=float)
    return FFT_2D(FFT_2D(input2DArray).T).T


def twoD_IFFT(input2DArray):
    input2DArray = np.asarray(input2DArray, dtype=complex)
    return np.array(
        list(map(lambda a: a / (len(input2DArray) * len(input2DArray[0])), IFFT_2D(IFFT_2D(input2DArray).T).T)))


def DFT_2(f, N):
    '''
    :param f: 2_dim marix
    :param N: even; denote number of rows
    :param M: even; denote number of cols
    :return: DFT results without shifting(complex number)
    '''
    if N % 2 != 0:
        raise ValueError("size of x must be a power of 2")
    f = f.astype('float64')
    rows = f.shape[0]
    cols = f.shape[1]
    n = np.arange(0, N, 1).reshape((N, 1))
    row = np.arange(0, rows, 1).reshape((1, rows))
    left = np.exp(-1j*2*np.pi/N*(n @ row))
    col = np.arange(0, cols, 1).reshape((cols, 1))
    m = np.arange(0, N, 1).reshape((1, N))
    right = np.exp(-1j*2*np.pi/N*(col @ m))
    F = left @ f @ right
    return F


def next_power_of_2(x):
    return 1 if x == 0 else 2 ** (x - 1).bit_length()


# mode manipulation
def modeOutput(mode, address):
    # img is a 2-d array
    img_original = cv2.imread(address, cv2.IMREAD_UNCHANGED)
    # img_original = mpimg.imread(address)
    vertical = img_original.shape[0]
    horizontal = img_original.shape[1]
    changed_vertical = next_power_of_2(vertical)
    changed_horizontal = next_power_of_2(horizontal)

    dsize = (changed_horizontal, changed_vertical)
    img_original = cv2.resize(img_original, dsize, interpolation=cv2.INTER_AREA)

    if mode == 1:
        print("mode 1 is triggered")

        # my function
        img_FFT = twoD_FFT(img_original)

        # built-in function
        # img_FFT = np.fft.fft2(img_original)

        plt.figure("Mode_1")
        plt.subplot(121)
        plt.imshow(img_original)

        plt.subplot(122)
        plt.imshow(np.abs(img_FFT), norm=LogNorm(vmin=5))
        plt.show()

    if mode == 2:
        print("mode 2 is triggered")
        keep_fraction = 0.1

        # Call ff a copy of the original transform. Numpy arrays have a copy
        # method for this purpose.

        # my function
        im_fft2 = twoD_FFT(img_original)

        # built-in function
        # im_fft2 = np.fft.fft2(img_original)

        r, c = im_fft2.shape
        print(im_fft2[10, 10])

        im_fft2[10, 10] = 0.0

        print(im_fft2[10, 10])
        print("checkpoint1")
        im_fft2[int(r * keep_fraction):int(r * (1 - keep_fraction)), :] = 0.0
        im_fft2[:, int(c * keep_fraction):int(c * (1 - keep_fraction))] = 0.0

        img_new = twoD_IFFT(im_fft2).real

        plt.figure("Mode_2")
        plt.subplot(121)
        plt.imshow(img_original)

        plt.subplot(122)
        plt.imshow(img_new)
        plt.show()

    if (mode == 3):
        print("mode 3 is triggered")
        threshold_19 = 1
        threshold_38 = 10
        threshold_57 = 100
        threshold_76 = 1000
        threshold_95 = 10000

        im_fft2 = twoD_FFT(img_original)

        h, w = im_fft2.shape
        # print(im_fft2.shape)

        # print(im_fft2[10, 10])

        # im_fft2[10,10] = 0.0

        # print(im_fft2[10, 10])
        # print("checkpoint2")

        im_19 = im_fft2
        im_38 = im_fft2
        im_57 = im_fft2
        im_76 = im_fft2
        im_95 = im_fft2

        for j in range(w):
            for i in range(h):
                if int(abs(im_19[i, j])) < threshold_19:
                    im_19[i, j] = 0.0
                if int(abs(im_38[i, j])) < threshold_38:
                    im_38[i, j] = 0.0
                if int(abs(im_57[i, j])) < threshold_57:
                    im_57[i, j] = 0.0
                if int(abs(im_76[i, j])) < threshold_76:
                    im_76[i, j] = 0.0
                if int(abs(im_95[i, j])) < threshold_95:
                    im_95[i, j] = 0.0

        scipy.sparse.save_npz('/matrix/sparse_matrix_im_fft2.npz', im_fft2)
        scipy.sparse.save_npz('/matrix/sparse_matrix_im_19.npz', im_19)
        scipy.sparse.save_npz('/matrix/sparse_matrix_im_38.npz', im_38)
        scipy.sparse.save_npz('/matrix/sparse_matrix_im_57.npz', im_57)
        scipy.sparse.save_npz('/matrix/sparse_matrix_im_76.npz', im_76)
        scipy.sparse.save_npz('/matrix/sparse_matrix_im_95.npz', im_95)

        im_i19 = twoD_IFFT(im_19).real
        im_i38 = twoD_IFFT(im_38).real
        im_i57 = twoD_IFFT(im_57).real
        im_i76 = twoD_IFFT(im_76).real
        im_i95 = twoD_IFFT(im_95).real

        # out_original = np.count_nonzero(im_fft2)

        # out_19 = np.count_nonzero(im_i19)
        # out_38 = np.count_nonzero(im_i38)
        # out_57 = np.count_nonzero(im_i57)
        # out_76 = np.count_nonzero(im_i76)
        # out_95 = np.count_nonzero(im_i95)

        # print("19%:", out_19/out_original)
        # print("38%:", out_38/out_original)
        # print("57%:", out_57/out_original)
        # print("76%:", out_76/out_original)
        # print("95%:", out_95/out_original)

        print("19%:", np.count_nonzero(im_i19))
        print("38%:", np.count_nonzero(im_i38))
        print("57%:", np.count_nonzero(im_i57))
        print("76%:", np.count_nonzero(im_i76))
        print("95%:", np.count_nonzero(im_i95))

        plt.figure("Mode_3")

        plt.subplot(231)
        plt.imshow(img_original)

        plt.subplot(232)
        plt.imshow(im_i19)

        plt.subplot(233)
        plt.imshow(im_i38)

        plt.subplot(234)
        plt.imshow(im_i57)

        plt.subplot(235)
        plt.imshow(im_i76)

        plt.subplot(236)
        plt.imshow(im_i95)

        plt.show()

    if mode == 4:
        print("mode 4 is triggered")
        x = 256
        y = np.random.rand(x, x)
        startTime = time.perf_counter()
        a = DFT_2(y, x)
        endTime = time.perf_counter()
        startTime2 = time.perf_counter()
        a2 = twoD_FFT(y)
        endTime2 = time.perf_counter()
        print(str(endTime-startTime) + " " + str(endTime2-startTime2))
        # with open("result2.txt", "w") as fp:
        #     for j in range(5):
        #         fp.write(str(x) + '\n')
        #         for i in range(15):
        #             y = np.random.rand(x, x)
        #             startTime = time.perf_counter()
        #             my = DFT_2(y, x)
        #             endTime = time.perf_counter()
        #             print(np.allclose(my, np.fft.fft2(y)))
        #             diffTime = endTime - startTime
        #             fp.write(str(diffTime) + '\n')
        #         fp.write('\n')
        #         x *= 2
        #         print(x)
        #
        # fp.close()




if __name__ == '__main__':
    mode = 1
    address = "moonlanding.png"

    # If there are more than two inputs, exit
    if len(sys.argv) > 3:
        print("Invalid inputs!\tpython fft.py [-m mode] [-i image]")
        exit(1)

    # Case 1: no input: default mode and address
    elif len(sys.argv) == 1:
        pass

    # Case 2: Two inputs: mode and address
    elif len(sys.argv) == 3:
        try:  # Is this a number?
            mode = int(sys.argv[1])
        except ValueError:
            print("Invalid mode input! Mode should be inputted 1, 2, 3, or 4!\tYour input: " + sys.argv[1])
            exit(1)
        else:  # Check if mode is in range of [1, 4]
            if not 1 <= mode <= 4:
                print("Invalid mode input! Mode should be inputted 1, 2, 3, or 4!\tYour input: " + sys.argv[1])
                exit(1)

        # Is this a valid address?
        if not os.path.isfile(sys.argv[2]):
            print("Invalid image input! Filename does not exist!\tYour input: " + sys.argv[2])
            exit(1)
        else:
            address = sys.argv[2]

        # Case 3: One input: either mode or address
    else:
        try:  # Is this a number?
            mode = int(sys.argv[1])
        except ValueError:  # If not, is this a valid address?
            if not os.path.isfile(sys.argv[1]):
                print("Invalid image input! Filename does not exist!\tYour input: " + sys.argv[1])
                exit(1)
            else:
                address = sys.argv[1]
        else:
            # Check if mode is in range of [1, 4]
            if not 1 <= mode <= 4:
                print("Invalid mode input! Mode should be inputted 1, 2, 3, or 4!\tYour input: " + sys.argv[1])
                exit(1)

    modeOutput(mode, address)
