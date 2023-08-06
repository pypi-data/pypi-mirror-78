import math
from math import inf
import dtaidistance.dtw as dtw


class LBEnhanced:

    @staticmethod
    def distance(A: [], B: [], U: [], L: [], W, v, cutoffvalue=None):
        dists = list()
        n = len(A)
        m = len(B)
        l = n - 1
        n_bands = min(l / 2, v)
        last_index = l - n_bands
        d_inicial = A[0] - B[0]
        d_final = A[l] - B[m - 1]
        res = d_inicial * d_inicial + d_final * d_final

        i = 1
        while i < n_bands:
            right_end = l - i
            minL = A[i] - B[i]
            minL = minL * minL
            minR = A[right_end] - B[right_end]
            minR = minR * minR
            j = int(max(0, i - W))
            while j < i:
                right_start = l - j
                tmp = A[j] - B[j]
                minL = min(minL, tmp * tmp)
                tmp = A[j] - B[j]
                minL = min(minL, tmp * tmp)
                tmp = A[right_end] - B[right_start]
                minR = min(minR, tmp * tmp)
                tmp = A[right_start] - B[right_end]
                minR = min(minR, tmp * tmp)
                j = j + 1
            relative_res = minL + minR
            dists.append(relative_res)
            res = res + minL + minR
            i = i + 1
        if cutoffvalue is not None:
            if res >= cutoffvalue:
                return dtw.lb_keogh(A, B, window=W)
                #return dtw.distance_fast(A, B)

        i = int(n_bands)
        while i <= last_index:
            a_val = A[i]
            if a_val > U[i]:
                tmp = a_val - U[i]
                res = res + tmp * tmp
            elif a_val < L[i]:
                tmp = L[i] - a_val
                res = res + tmp * tmp
            i = i + 1
        return res

    @staticmethod
    def distance_without_keogh(A, B, W, n_bands, keogh_distance):
        array_A = A.get_array_serie()
        array_B = B.get_array_serie()
        n = len(array_A)
        m = len(array_B)
        l = n - 1
        d_inicial = array_A[0] - array_B[0]
        d_final = array_A[n - 1] - array_B[m - 1]
        res = d_inicial * d_inicial + d_final * d_final + keogh_distance

        for i in range(1, n_bands):
            right_end = l - i
            minL = array_A[i] - array_B[i]
            minL = minL * minL
            minR = array_A[right_end] - array_B[right_end]
            minR = minR * minR
            j = max(0, i - W)
            while j < i:
                right_start = l - j
                tmp = array_A[i] - array_B[j]
                minL = min(minL, tmp * tmp)
                tmp = array_A[j] - array_B[i]
                minL = min(minL, tmp * tmp)

                tmp = array_A[right_end] - array_B[right_start]
                minR = min(minR, tmp * tmp)
                tmp = array_A[right_start] - array_B[right_end]
                minR = min(minR, tmp * tmp)
                j = j + 1
            res = res + minL + minR
        return res
