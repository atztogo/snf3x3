#include <assert.h>
#include <stdio.h>

#ifndef SNF3x3CONST
#define SNF3x3CONST
#endif

typedef struct {
  int A[3][3];
  int P[3][3];
  int Q[3][3];
  int D[3][3];
} SNF3x3;

static SNF3x3 core_run(SNF3x3CONST int A[3][3]);
static void extended_gcd(int retvals[3], const int a, const int b);
static void extended_gcd_step(int vals[6]);
static int first(SNF3x3 *mats);
static void first_one_loop(SNF3x3 *mats);
static void first_column(SNF3x3 *mats);
static void zero_first_column(SNF3x3 *mats);
static int search_first_pivot(SNF3x3CONST int A[3][3]);
static void first_finalize(SNF3x3 *mats);
static void second(SNF3x3 *mats);
static void second_one_loop(SNF3x3 *mats);
static void second_column(SNF3x3 *mats);
static void zero_second_column(SNF3x3 *mats);
static void second_finalize(SNF3x3 *mats);
static void swap_rows(int A[3][3], const int i, const int j);
static void flip_sign_row(SNF3x3 *mats);
static void set_zero(SNF3x3 *mats);
static void transpose(int m[3][3]);
static void matmul(int m[3][3],
                   SNF3x3CONST int a[3][3],
                   SNF3x3CONST int b[3][3]);

static void test_extended_gcd(void);
static void test_transpose(void);
static void test_swap_rows(void);


int main()
{
  test_extended_gcd();
  test_transpose();
  test_swap_rows();
}

static void test_extended_gcd(void)
{
  int vals[3];

  printf("Test extended_gcd\n");
  extended_gcd(vals, 4 , -3);
  printf("%d %d %d\n", vals[0], vals[1], vals[2]);
}

static void test_transpose(void)
{
  int i, j;
  int A[3][3];

  printf("Test transpose\n");

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      A[i][j] = i * 3 + j;
    }
  }

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      printf("%d ", A[i][j]);
    }
    printf("\n");
  }

  transpose(A);

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      printf("%d ", A[i][j]);
    }
    printf("\n");
  }
}

static void test_swap_rows(void)
{
  int i, j;
  int A[3][3];

  printf("Test swap_rows 1 <-> 2\n");

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      A[i][j] = i * 3 + j;
    }
  }

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      printf("%d ", A[i][j]);
    }
    printf("\n");
  }

  swap_rows(A, 0, 1);

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      printf("%d ", A[i][j]);
    }
    printf("\n");
  }
}

static SNF3x3 core_run(SNF3x3CONST int A[3][3])
{
  int i, j;
  SNF3x3 mats;

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      mats.A[i][j] = A[i][j];
      if (i == j) {
        mats.P[i][j] = 1;
        mats.Q[i][j] = 1;
      } else {
        mats.P[i][j] = 0;
        mats.Q[i][j] = 0;
      }
      mats.D[i][j] = 0;
    }
  }
}

/**
 * bool (true: 1, false: 0)
 */
static int first(SNF3x3 *mats)
{
  first_one_loop(mats);
  if ((mats->A[1][0] == 0) && (mats->A[2][0] == 0)) {
    return 1;
  }
  if ((mats->A[1][0] % mats->A[0][0] == 0)
      && (mats->A[2][0] % mats->A[0][0] == 0)) {
    first_finalize(mats);
    return 1;
  }
  return 0;
}

static void first_one_loop(SNF3x3 *mats)
{
  first_column(mats);
  transpose(mats->A);
  first_column(mats);
  transpose(mats->A);
}

static void first_column(SNF3x3 *mats)
{
  int i;

  if (search_first_pivot(mats->A) > 0) {
    swap_rows(mats->A, 0, i);
  }
}

static void zero_first_column(SNF3x3 *mats)
{
}

static int search_first_pivot(SNF3x3CONST int A[3][3])
{
  int i;

  for (i = 0; i < 3; i++) {
    if (A[i][0] != 0) {
      return i;
    }
  }
  return -1;
}

static void first_finalize(SNF3x3 *mats)
{
}

static void second(SNF3x3 *mats)
{
}

static void second_one_loop(SNF3x3 *mats)
{
}

static void second_column(SNF3x3 *mats)
{
}

static void zero_second_column(SNF3x3 *mats)
{
}

static void second_finalize(SNF3x3 *mats)
{
}

static void swap_rows(int A[3][3], const int r1, const int r2)
{
  int i, j;
  int L[3][3];

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      L[i][j] = 0;
    }
    if ((i != r1) && (i != r2)) {
      L[i][i] = 1;
    }
  }
  L[r1][r2] = 1;
  L[r2][r1] = 1;

  matmul(A, L, A);
}

static void flip_sign_row(SNF3x3 *mats)
{
}

static void set_zero(SNF3x3 *mats)
{
}

/**
 * Extended Euclidean algorithm
 * See https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
 */
static void extended_gcd(int retvals[3], const int a, const int b)
{
  int i;
  int vals[6];

  vals[0] = a;  /* r0 */
  vals[1] = b;  /* r1 */
  vals[2] = 1;  /* s0 */
  vals[3] = 0;  /* s1 */
  vals[4] = 0;  /* t0 */
  vals[5] = 1;  /* t1 */

  for (i = 0; i < 1000; i++) {
    extended_gcd_step(vals);
    if (vals[1] == 0) {
      break;
    }
  }

  retvals[0] = vals[0];
  retvals[1] = vals[2];
  retvals[2] = vals[4];

  assert(vals[0] == a * vals[2] + b * vals[4]);
}

static void extended_gcd_step(int vals[6])
{
  int q, r2, s2, t2;

  q = vals[0] / vals[1];
  r2 = vals[0] % vals[1];
  if (r2 < 0) {
    if (vals[1] > 0) {
      r2 += vals[1];
      q -= 1;
    }
    if (vals[1] < 0) {
      r2 -= vals[1];
      q += 1;
    }
  }
  s2 = vals[2] - q * vals[3];
  t2 = vals[4] - q * vals[5];
  vals[0] = vals[1];
  vals[1] = r2;
  vals[2] = vals[3];
  vals[3] = s2;
  vals[4] = vals[5];
  vals[5] = t2;
}

/**
 * Matrix operation utils
 */
static void transpose(int m[3][3])
{
  int tmp, i, j;

  for (i = 0; i < 3; i++) {
    for (j = i; j < 3; j++) {
      tmp = m[i][j];
      m[i][j] = m[j][i];
      m[j][i] = tmp;
    }
  }
}

static void matmul(int m[3][3],
                   SNF3x3CONST int a[3][3],
                   SNF3x3CONST int b[3][3])
{
  int i, j;
  int c[3][3];

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      c[i][j] = a[i][0] * b[0][j] + a[i][1] * b[1][j] + a[i][2] * b[2][j];
    }
  }

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      m[i][j] = c[i][j];
    }
  }
}
