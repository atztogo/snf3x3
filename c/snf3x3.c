#ifndef SNF3x3CONST
#define SNF3x3CONST
#endif

typedef struct {
  int A[3][3];
  int P[3][3];
  int Q[3][3];
  int D[3][3];
} SNF3x3;

SNF3x3 core_run(SNF3x3CONST int A[3][3])
{
  int i, j;
  SNF3x3 mats;

  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      mats.A[i][j] = A[i][j];
      mats.P[i][j] = 0;
      mats.Q[i][j] = 0;
      mats.D[i][j] = 0;
    }
  }
}


static void first(SNF3x3 mats)
{
}

static void first_one_loop(SNF3x3 mats)
{
}

static void first_column(SNF3x3 mats)
{
}

static void zero_first_column(SNF3x3 mats)
{
}

static void search_first_pivot(SNF3x3 mats)
{
}

static void first_finalize(SNF3x3 mats)
{
}

static void second(SNF3x3 mats)
{
}

static void second_one_loop(SNF3x3 mats)
{
}

static void second_column(SNF3x3 mats)
{
}

static void zero_second_column(SNF3x3 mats)
{
}

static void second_finalize(SNF3x3 mats)
{
}

static void swap_rows(SNF3x3 mats)
{
}

static void flip_sign_row(SNF3x3 mats)
{
}

static void set_zero(SNF3x3 mats)
{
}

/* gcd */
static void bezout_gcd(int retvals[3], const int r0, const int r1)
{
  int i;
  int vals[6];

  vals[0] = r0;
  vals[1] = r1;
  vals[2] = 1;  /* s0 */
  vals[3] = 0;  /* s1 */
  vals[4] = 0;  /* t0 */
  vals[5] = 1;  /* t1 */

  for (i = 0; i < 1000; i++) {
    gcd_step(vals);
    if (vals[1] == 0) {
      break;
    }
  }

  retvals[0] = vals[0];  /* r0 */
  retvals[1]
}

static void bezout_gcd_step(int vals[6])
{
}
