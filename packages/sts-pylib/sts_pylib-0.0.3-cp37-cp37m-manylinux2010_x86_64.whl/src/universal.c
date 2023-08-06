#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/cephes.h"
#include "../include/externs.h"
#include "../include/utilities.h"

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                         U N I V E R S A L  T E S T
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

double Universal(unsigned char epsilon[], int n) {
  int i, j, p, L, Q, K;
  double arg, sqrt2, sigma, phi, sum, p_value, c;
  long *T, decRep;
  double expected_value[17] = {
      0,         0,         0,         0,         0,         0,
      5.2177052, 6.1962507, 7.1836656, 8.1764248, 9.1723243, 10.170032,
      11.168765, 12.168070, 13.167693, 14.167488, 15.167379};
  double variance[17] = {0,     0,     0,     0,     0,     0,
                         2.954, 3.125, 3.238, 3.311, 3.356, 3.384,
                         3.401, 3.410, 3.416, 3.419, 3.421};

  /* * * * * * * * * ** * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   * * THE FOLLOWING REDEFINES L, SHOULD THE CONDITION:     n >= 1010*2^L*L *
   * NOT BE MET, FOR THE BLOCK LENGTH L. *
   * * * * * * * * * * ** * * * * * * * * * * * * * * * * * * * * * * * * * * *
   */
  L = 5;
  if (n >= 387840) L = 6;
  if (n >= 904960) L = 7;
  if (n >= 2068480) L = 8;
  if (n >= 4654080) L = 9;
  if (n >= 10342400) L = 10;
  if (n >= 22753280) L = 11;
  if (n >= 49643520) L = 12;
  if (n >= 107560960) L = 13;
  if (n >= 231669760) L = 14;
  if (n >= 496435200) L = 15;
  if (n >= 1059061760) L = 16;

  Q = 10 * (int)pow(2, L);
  K = (int)(floor(n / L) - (double)Q); /* BLOCKS TO TEST */

  p = (int)pow(2, L);
  if ((L < 6) || (L > 16) || ((double)Q < 10 * pow(2, L)) ||
      ((T = (long *)calloc(p, sizeof(long))) == NULL)) {
    printf("UNIVERSAL STATISTICAL TEST\n");
    printf("---------------------------------------------\n");
    printf("ERROR:  L IS OUT OF RANGE.\n");
    printf("-OR- :  Q IS LESS THAN %f.\n", 10 * pow(2, L));
    printf("-OR- :  Unable to allocate T.\n");
    return;
  }

  /* COMPUTE THE EXPECTED:  Formula 16, in Marsaglia's Paper */
  c = 0.7 - 0.8 / (double)L +
      (4 + 32 / (double)L) * pow(K, -3 / (double)L) / 15;
  sigma = c * sqrt(variance[L] / (double)K);
  sqrt2 = sqrt(2);
  sum = 0.0;
  for (i = 0; i < p; i++) T[i] = 0;
  for (i = 1; i <= Q; i++) { /* INITIALIZE TABLE */
    decRep = 0;
    for (j = 0; j < L; j++)
      decRep += epsilon[(i - 1) * L + j] * (long)pow(2, L - 1 - j);
    T[decRep] = i;
  }
  for (i = Q + 1; i <= Q + K; i++) { /* PROCESS BLOCKS */
    decRep = 0;
    for (j = 0; j < L; j++)
      decRep += epsilon[(i - 1) * L + j] * (long)pow(2, L - 1 - j);
    sum += log(i - T[decRep]) / log(2);
    T[decRep] = i;
  }
  phi = (double)(sum / (double)K);

  printf("UNIVERSAL STATISTICAL TEST\n");
  printf("--------------------------------------------\n");
  printf("COMPUTATIONAL INFORMATION:\n");
  printf("--------------------------------------------\n");
  printf("(a) L         = %d\n", L);
  printf("(b) Q         = %d\n", Q);
  printf("(c) K         = %d\n", K);
  printf("(d) sum       = %f\n", sum);
  printf("(e) sigma     = %f\n", sigma);
  printf("(f) variance  = %f\n", variance[L]);
  printf("(g) exp_value = %f\n", expected_value[L]);
  printf("(h) phi       = %f\n", phi);
  printf("(i) WARNING:  %d bits were discarded.\n", n - (Q + K) * L);
  printf("-----------------------------------------\n");

  arg = fabs(phi - expected_value[L]) / (sqrt2 * sigma);
  p_value = erfc(arg);
  if (isNegative(p_value) || isGreaterThanOne(p_value))
    printf("WARNING:  P_VALUE IS OUT OF RANGE\n");

  printf("%p_value = %f\n", p_value);

  free(T);

  return p_value;
}
