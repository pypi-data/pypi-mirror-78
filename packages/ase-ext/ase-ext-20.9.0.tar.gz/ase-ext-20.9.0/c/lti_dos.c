#include "_ase_ext.h"
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif
#include <stdlib.h>
#include <math.h>

#define MAX(x, y) ((x) > (y) ? (x) : (y))
#define MIN(x, y) ((x) < (y) ? (x) : (y))


int lti_compare(const void* a, const void* b, void* f)
{
    double fa = ((double*)f)[*((const int*)a)];
    double fb = ((double*)f)[*((const int*)b)];
    return (fa > fb) - (fa < fb);
}


void lti_dos1(double* E,
              double** W,
              double* energies, double* dos,
              int nweights, int nenergies)
{
    int indices[4] = {0, 1, 2, 3};
    qsort_r(indices, 4, sizeof(int), lti_compare, E);
    double e0 = E[indices[0]];
    double e1 = E[indices[1]];
    double e2 = E[indices[2]];
    double e3 = E[indices[3]];

    double* W0 = W[indices[0]];
    double* W1 = W[indices[1]];
    double* W2 = W[indices[2]];
    double* W3 = W[indices[3]];

    double zero = energies[0];
    int n0, n1, n2, n3;
    if (nenergies > 1) {
        double de = energies[1] - zero;
        n0 = MAX(0, MIN((floor((e0 - zero) / de)) + 1, nenergies));
        n1 = MAX(0, MIN((floor((e1 - zero) / de)) + 1, nenergies));
        n2 = MAX(0, MIN((floor((e2 - zero) / de)) + 1, nenergies));
        n3 = MAX(0, MIN((floor((e3 - zero) / de)) + 1, nenergies));
    }
    else {
        n0 = (int)(e0 > zero);
        n1 = (int)(e1 > zero);
        n2 = (int)(e2 > zero);
        n3 = (int)(e3 > zero);
    }

    for (int n = n0; n < n1; n++) {
        double x = energies[n] - e0;
        double f10 = x / (e1 - e0);
        double f20 = x / (e2 - e0);
        double f30 = x / (e3 - e0);
        double f01 = 1 - f10;
        double f02 = 1 - f20;
        double f03 = 1 - f30;
        double gw = f20 * f30 / (e1 - e0);
        for (int w = 0; w < nweights; w++)
            dos[w * nenergies + n] += (
                W0[w] * (f01 + f02 + f03) +
                W1[w] * f10 +
                W2[w] * f20 +
                W3[w] * f30) * gw;
    }
    for (int n = n1; n < n2; n++) {
        double delta = e3 - e0;
        double x = energies[n];
        double f20 = (x - e0) / (e2 - e0);
        double f30 = (x - e0) / (e3 - e0);
        double f21 = (x - e1) / (e2 - e1);
        double f31 = (x - e1) / (e3 - e1);
        double f02 = 1 - f20;
        double f03 = 1 - f30;
        double f12 = 1 - f21;
        double f13 = 1 - f31;
        double gw = 1 / delta * (f12 * f20 + f21 * f13);
        for (int w = 0; w < nweights; w++)
            dos[w * nenergies + n] += (
                W0[w] *
                (gw * f03 + f02 * f20 * f12 / delta) +
                W1[w] *
                (gw * f12 + f13 * f13 * f21 / delta) +
                W2[w] *
                (gw * f21 + f20 * f20 * f12 / delta) +
                W3[w] *
                (gw * f30 + f31 * f13 * f21 / delta));
        }
    for (int n = n2; n < n3; n++) {
        double x = energies[n] - e3;
        double f03 = x / (e0 - e3);
        double f13 = x / (e1 - e3);
        double f23 = x / (e2 - e3);
        double f30 = 1 - f03;
        double f31 = 1 - f13;
        double f32 = 1 - f23;
        double gw = f03 * f13 / (e3 - e2);
        for (int w = 0; w < nweights; w++)
            dos[w * nenergies + n] += (
                W0[w] * f03 +
                W1[w] * f13 +
                W2[w] * f23 +
                W3[w] * (f30 + f31 + f32)) * gw;
    }
}


void lti_dos(long* simplices,
             double* eigs,
             double* weights,
             double* energies,
             double* dos,
             int ni, int nj, int nk,
             int neigs,
             int nweights,
             int nenergies,
             int rank, int size)
{
    int q = -1;
    for (int i = 0; i < ni; i++)
        for (int j = 0; j < nj; j++)
            for (int k = 0; k < nk; k++) {
                q += 1;
                if (q % size != rank)
                    continue;
                for (int s = 0; s < 6; s++) {
                    long* simplex = simplices + s * 4 * 3;
                    int i1[4];
                    int j1[4];
                    int k1[4];
                    for (int c = 0; c < 4; c++) {  // four corners
                        i1[c] = (i + simplex[c * 3]) % ni;
                        j1[c] = (j + simplex[c * 3 + 1]) % nj;
                        k1[c] = (k + simplex[c * 3 + 2]) % nk;
                    }
                    for (int e = 0; e < neigs; e++) {
                        int m0 = e + neigs * (
                            k1[0] + nk * (j1[0] + nj * i1[0]));
                        int m1 = e + neigs * (
                            k1[1] + nk * (j1[1] + nj * i1[1]));
                        int m2 = e + neigs * (
                            k1[2] + nk * (j1[2] + nj * i1[2]));
                        int m3 = e + neigs * (
                            k1[3] + nk * (j1[3] + nj * i1[3]));
                        double E[4] = {eigs[m0], eigs[m1], eigs[m2], eigs[m3]};
                        double* W[4] = {weights + nweights * m0,
                                        weights + nweights * m1,
                                        weights + nweights * m2,
                                        weights + nweights * m3};
                        lti_dos1(E,
                                 W,
                                 energies,
                                 dos,
                                 nweights, nenergies);
                    }
                }
            }
}
