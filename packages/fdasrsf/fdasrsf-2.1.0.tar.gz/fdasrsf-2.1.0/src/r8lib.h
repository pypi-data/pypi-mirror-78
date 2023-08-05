void gamma_values ( int *n_data, double *x, double *fx );
void gamma_log_values ( int *n_data, double *x, double *fx );
int i4_log_10 ( int i );
int i4_max ( int i1, int i2 );
int i4_min ( int i1, int i2 );
int i4_modp ( int i, int j );
int i4_power ( int i, int j );
int i4_sign ( int i );
int i4_uniform_ab ( int a, int b, int *seed );
int i4_wrap ( int ival, int ilo, int ihi );
double i4int_to_r8int ( int imin, int imax, int i, double rmin, double rmax );
void i4vec_copy ( int n, int a1[], int a2[] );
int *i4vec_indicator_new ( int n );
void i4vec_permute ( int n, int p[], int base, int a[] );
void i4vec_print ( int n, int a[], char *title );
void i4vec_zero ( int n, int a[] );
int *i4vec_zero_new ( int n );
double *legendre_zeros ( int order );
int perm_check ( int n, int p[], int base );
int *perm_uniform_new ( int n, int base, int *seed );
int r4_nint ( float x );
double r8_abs ( double x );
double r8_acos ( double c );
double r8_acosh ( double x );
double r8_add ( double x, double y );
double r8_aint ( double x );
double r8_asin ( double c );
double r8_asinh ( double x );
double r8_atan ( double y, double x );
double r8_atanh ( double x );
double r8_cas ( double x );
double r8_ceiling ( double x );
double r8_choose ( int n, int k );
double r8_chop ( int place, double x );
double r8_csc ( double theta );
double r8_cube_root ( double x );
double r8_degrees ( double radians );
double r8_diff ( double x, double y, int n );
int r8_digit ( double x, int idigit );
double r8_divide_i4 ( int i, int j );
double r8_epsilon ( );
double r8_epsilon_compute ( );
double r8_exp ( double x );
double r8_factorial ( int n );
double r8_factorial2 ( int n );
double r8_fall ( double x, int n );
double r8_floor ( double x );
double r8_fraction ( int i, int j );
double r8_fractional ( double x );
double r8_gamma ( double x );
double r8_gamma_log ( double x );
double r8_huge ( );
double r8_hypot ( double a, double b );
int r8_in_01 ( double a );
int r8_insignificant ( double r, double s );
int r8_is_int ( double r );
double r8_log_10 ( double x );
double r8_log_2 ( double x );
double r8_log_b ( double x, double b );
void r8_mant ( double x, int *s, double *r, int *l );
double r8_max ( double x, double y );
double r8_min ( double x, double y );
double r8_mod ( double x, double y );
double r8_modp ( double x, double y );
double r8_mop ( int i );
int r8_nint ( double x );
double r8_normal_01 ( int *seed );
double r8_normal_ab ( double a, double b, int *seed );
double r8_pi ( );
double r8_pi_sqrt ( );
double r8_power ( double r, int p );
double r8_power_fast ( double r, int p, int *mults );
double r8_pythag ( double a, double b );
double r8_radians ( double degrees );
double r8_reverse_bytes ( double x );
double r8_rise ( double x, int n );
double r8_round ( double x );
int r8_round_i4 ( double x );
double r8_round2 ( int nplace, double x );
double r8_roundb ( int base, int nplace, double x );
double r8_roundx ( int nplace, double x );
double r8_sech ( double x );
double r8_sign ( double x );
char r8_sign_char ( double x );
int r8_sign_match ( double r1, double r2 );
int r8_sign_match_strict ( double r1, double r2 );
int r8_sign_opposite ( double r1, double r2 );
int r8_sign_opposite_strict ( double r1, double r2 );
double r8_sign2 ( double x, double y );
double r8_sqrt_i4 ( int i );
double r8_sum ( double x, double y );
void r8_swap ( double *x, double *y );
void r8_swap3 ( double *x, double *y, double *z );
double r8_tiny ( );
void r8_to_dhms ( double r, int *d, int *h, int *m, int *s );
int r8_to_i4 ( double x, double xmin, double xmax, int ixmin, int ixmax );
double r8_to_r8_discrete ( double r, double rmin, double rmax, int nr );
double r8_uniform_ab ( double b, double c, int *seed );
double r8_uniform_01 ( int *seed );
void r8_unswap3 ( double *x, double *y, double *z );
double r8_walsh_1d ( double x, int digit );
double r8_wrap ( double r, double rlo, double rhi );
double r82_dist_l2 ( double a1[2], double a2[2] );
void r82_print ( double a[2], char *title );
void r82_uniform_ab ( double b, double c, int *seed, double r[] );
void r82poly2_print ( double a, double b, double c, double d, double e, double f );
int r82poly2_type ( double a, double b, double c, double d, double e, double f );
void r82poly2_type_print ( int type );
double *r82vec_max ( int n, double a[] );
double *r82vec_min ( int n, double a[] );
int r82vec_order_type ( int n, double a[] );
void r82vec_part_quick_a ( int n, double a[], int *l, int *r );
void r82vec_permute ( int n, int p[], int base, double a[] );
void r82vec_print ( int n, double a[], char *title );
void r82vec_print_part ( int n, double a[], int max_print, char *title );
int *r82vec_sort_heap_index_a ( int n, int base, double a[] );
void r82vec_sort_quick_a ( int n, double a[] );
double r83_norm ( double x, double y, double z );
double *r83vec_max ( int n, double a[] );
double *r83vec_min ( int n, double a[] );
void r83vec_part_quick_a ( int n, double a[], int *l, int *r );
void r83vec_print_part ( int n, double a[], int max_print, char *title );
void r83vec_sort_quick_a ( int n, double a[] );
void r8block_delete ( int l, int m, int n, double ***a );
double *r8block_expand_linear ( int l, int m, int n, double x[], int lfat,
  int mfat, int nfat );
double ***r8block_new ( int l, int m, int n );
void r8block_print ( int l, int m, int n, double a[], char *title );
void r8cmat_delete ( int m, int n, double **a );
double **r8cmat_new ( int m, int n );
void r8cmat_print ( int m, int n, double **a, char *title );
double *r8cmat_to_r8mat ( int m, int n, double **a );
double *r8block_zero_new ( int l, int m, int n );
int r8col_compare ( int m, int n, double a[], int i, int j );
double *r8col_duplicates ( int m, int n, int n_unique, int *seed );
int r8col_find ( int m, int n, double a[], double x[] );
int *r8col_first_index ( int m, int n, double a[], double tol );
int r8col_insert ( int n_max, int m, int n, double a[], double x[] );
double *r8col_max ( int m, int n, double a[] );
int *r8col_max_index ( int m, int n, double a[] );
void r8col_max_one ( int m, int n, double a[] );
double *r8col_mean ( int m, int n, double a[] );
double *r8col_min ( int m, int n, double a[] );
int *r8col_min_index ( int m, int n, double a[] );
void r8col_normalize_li ( int m, int n, double a[] );
void r8col_part_quick_a ( int m, int n, double a[], int *l, int *r );
void r8col_permute ( int m, int n, int p[], int base, double a[] );
void r8col_reverse ( int m, int n, double a[] );
void r8col_separation ( int m, int n, double a[], double *d_min, double *d_max );
void r8col_sort_heap_a ( int m, int n, double a[] );
int *r8col_sort_heap_index_a ( int m, int n, int base, double a[] );
void r8col_sort_quick_a ( int m, int n, double a[] );
void r8col_sorted_tol_undex ( int m, int n, double a[], int unique_num,
  double tol, int undx[], int xdnu[] );
int r8col_sorted_tol_unique ( int m, int n, double a[], double tol );
int r8col_sorted_tol_unique_count ( int m, int n, double a[], double tol );
void r8col_sorted_undex ( int m, int n, double a[], int unique_num,
  int undx[], int xdnu[] );
int r8col_sorted_unique ( int m, int n, double a[] );
int r8col_sorted_unique_count ( int m, int n, double a[] );
void r8col_sortr_a ( int m, int n, double a[], int key );
double *r8col_sum ( int m, int n, double a[] );
void r8col_swap ( int m, int n, double a[], int j1, int j2 );
double *r8col_to_r8vec ( int m, int n, double a[] );
void r8col_tol_undex ( int x_dim, int x_num, double x_val[], int x_unique_num,
  double tol, int undx[], int xdnu[] );
int r8col_tol_unique_count ( int m, int n, double a[], double tol );
int *r8col_tol_unique_index ( int m, int n, double a[], double tol );
void r8col_undex ( int x_dim, int x_num, double x_val[], int x_unique_num,
  int undx[], int xdnu[] );
double *r8col_uniform_abvec_new ( int m, int n, double a[], double b[], int *seed );
int r8col_unique_count ( int m, int n, double a[] );
int *r8col_unique_index ( int m, int n, double a[] );
double *r8col_variance ( int m, int n, double a[] );
double r8int_to_r8int ( double rmin, double rmax, double r, double r2min,
  double r2max );
int r8int_to_i4int ( double rmin, double rmax, double r, int imin, int imax );
void r8mat_add ( int m, int n, double alpha, double a[], double beta,
  double b[], double c[] );
double *r8mat_add_new ( int m, int n, double alpha, double a[], double beta,
  double b[] );
double r8mat_amax ( int m, int n, double a[] );
double *r8mat_border_add ( int m, int n, double table[] );
double *r8mat_border_cut ( int m, int n, double table[] );
double *r8mat_cholesky_factor ( int n, double a[], int *flag );
double *r8mat_cholesky_factor_upper ( int n, double a[], int *flag );
void r8mat_cholesky_inverse ( int n, double a[] );
double *r8mat_cholesky_solve ( int n, double a[], double b[] );
double *r8mat_cholesky_solve_upper ( int n, double r[], double b[] );
void r8mat_copy ( int m, int n, double a1[], double a2[] );
double *r8mat_copy_new ( int m, int n, double a1[] );
double *r8mat_covariance ( int m, int n, double x[] );
double r8mat_det ( int n, double a[] );
double r8mat_det_2d ( double a[] );
double r8mat_det_3d ( double a[] );
double r8mat_det_4d ( double a[] );
double r8mat_det_5d ( double a[] );
void r8mat_diag_add_scalar ( int n, double a[], double s );
void r8mat_diag_add_vector ( int n, double a[], double v[] );
void r8mat_diag_get_vector ( int n, double a[], double v[] );
double *r8mat_diag_get_vector_new ( int n, double a[] );
void r8mat_diag_set_scalar ( int n, double a[], double s );
void r8mat_diag_set_vector ( int n, double a[], double v[] );
double *r8mat_diagonal_new ( int n, double diag[] );
double r8mat_dif_fro ( int m, int n, double a[], double b[] );
double *r8mat_expand_linear ( int m, int n, double x[], int mfat, int nfat );
double *r8mat_expand_linear2 ( int m, int n, double a[], int m2, int n2 );
double *r8mat_flip_cols_new ( int m, int n, double a[] );
double *r8mat_flip_rows_new ( int m, int n, double a[] );
void r8mat_fs ( int n, double a[], double x[] );
double *r8mat_fs_new ( int n, double a[], double b[] );
void r8mat_fss ( int n, double a[], int nb, double x[] );
double *r8mat_fss_new ( int n, double a[], int nb, double b[] );
double *r8mat_givens_post ( int n, double a[], int row, int col );
double *r8mat_givens_pre ( int n, double a[], int row, int col );
double *r8mat_hess ( double (*fx )( int n, double x[] ), int n, double x[] );
void r8mat_house_axh ( int n, double a[], double v[] );
double *r8mat_house_axh_new ( int n, double a[], double v[] );
double *r8mat_house_form ( int n, double v[] );
double *r8mat_house_hxa ( int n, double a[], double v[] );
double *r8mat_house_post ( int n, double a[], int row, int col );
double *r8mat_house_pre ( int n, double a[], int row, int col );
void r8mat_identity ( int n, double a[] );
double *r8mat_identity_new ( int n );
int r8mat_in_01 ( int m, int n, double a[] );
double *r8mat_indicator_new ( int m, int n );
int r8mat_insignificant ( int m, int n, double r[], double s[] );
double *r8mat_inverse_2d ( double a[] );
double *r8mat_inverse_3d ( double a[] );
double *r8mat_inverse_4d ( double a[] );
double r8mat_is_identity ( int n, double a[] );
double r8mat_is_symmetric ( int m, int n, double a[] );
double *r8mat_jac ( int m, int n, double eps,
  double *(*fx) ( int m, int n, double x[] ), double x[] );
double *r8mat_kronecker ( int m1, int n1, double a[], int m2, int n2,
  double b[] );
double *r8mat_l_inverse ( int n, double a[] );
void r8mat_l_print ( int m, int n, double a[], char *title );
double *r8mat_l_solve ( int n, double a[], double b[] );
double *r8mat_l1_inverse ( int n, double a[] );
double *r8mat_lt_solve ( int n, double a[], double b[] );
void r8mat_lu ( int m, int n, double a[], double l[], double p[], double u[] );
double r8mat_max ( int m, int n, double a[] );
void r8mat_max_index ( int m, int n, double a[], int *i_max, int *j_max );
double r8mat_maxcol_minrow ( int m, int n, double a[] );
double r8mat_maxrow_mincol ( int m, int n, double a[] );
double r8mat_mean ( int m, int n, double a[] );
double r8mat_min ( int m, int n, double a[] );
void r8mat_min_index ( int m, int n, double a[], int *i_min, int *j_min );
double r8mat_mincol_maxrow ( int m, int n, double a[] );
double r8mat_minrow_maxcol ( int m, int n, double a[] );
void r8mat_minvm ( int n1, int n2, double a[], double b[], double c[] );
double *r8mat_minvm_new ( int n1, int n2, double a[], double b[] );
void r8mat_mm ( int n1, int n2, int n3, double a[], double b[], double c[] );
double *r8mat_mm_new ( int n1, int n2, int n3, double a[], double b[] );
double *r8mat_mmt_new ( int n1, int n2, int n3, double a[], double b[] );
double *r8mat_mtm_new ( int n1, int n2, int n3, double a[], double b[] );
void r8mat_mtv ( int m, int n, double a[], double x[], double atx[] );
double *r8mat_mtv_new ( int m, int n, double a[], double x[] );
void r8mat_mv ( int m, int n, double a[], double x[], double ax[] );
double *r8mat_mv_new ( int m, int n, double a[], double x[] );
void r8mat_mxm ( int n1, int n2, int n3, double a[], double b[], double c[] );
double *r8mat_mxm_new ( int n1, int n2, int n3, double a[], double b[] );
void r8mat_nint ( int m, int n, double a[] );
double r8mat_norm_eis ( int m, int n, double a[] );
double r8mat_norm_fro ( int m, int n, double a[] );
double r8mat_norm_fro_affine ( int m, int n, double a1[], double a2[] );
double r8mat_norm_l1 ( int m, int n, double a[] );
double r8mat_norm_l2 ( int m, int n, double a[] );
double r8mat_norm_li ( int m, int n, double a[] );
double *r8mat_normal_01_new ( int m, int n, int *seed );
double *r8mat_nullspace ( int m, int n, double a[], int nullspace_size );
int r8mat_nullspace_size ( int m, int n, double a[] );
void r8mat_orth_uniform ( int n, int *seed, double a[] );
double *r8mat_orth_uniform_new ( int n, int *seed );
void r8mat_plot ( int m, int n, double a[], char *title );
char r8mat_plot_symbol ( double r );
double *r8mat_poly_char ( int n, double a[] );
double *r8mat_power ( int n, double a[], int npow );
void r8mat_power_method ( int n, double a[], double *r, double v[] );
void r8mat_print ( int m, int n, double a[], char *title );
void r8mat_print_some ( int m, int n, double a[], int ilo, int jlo, int ihi,
  int jhi, char *title );
void r8mat_ref ( int m, int n, double a[] );
double r8mat_rms ( int m, int n, double a[] );
void r8mat_rref ( int m, int n, double a[] );
void r8mat_scale ( int m, int n, double s, double a[] );
int r8mat_significant ( int m, int n, double r[], double s[] );
int r8mat_solve ( int n, int rhs_num, double a[] );
double *r8mat_solve_2d ( double a[], double b[], double *det );
double *r8mat_solve_3d ( double a[], double b[], double *det );
double *r8mat_solve2 ( int n, double a[], double b[], int *ierror );
double *r8mat_sub_new ( int m, int n, double a[], double b[] );
double r8mat_sum ( int m, int n, double a[] );
double *r8mat_symm_eigen ( int n, double x[], double q[] );
void r8mat_symm_jacobi ( int n, double a[] );
double **r8mat_to_r8cmat ( int m, int n, double a[] );
int r8mat_to_r8plu ( int n, double a[], int pivot[], double lu[] );
double **r8mat_to_r8rmat ( int m, int n, double a[] );
double r8mat_trace ( int n, double a[] );
void r8mat_transpose_in_place ( int n, double a[] );
double *r8mat_transpose_new ( int m, int n, double a[] );
void r8mat_transpose_print ( int m, int n, double a[], char *title );
void r8mat_transpose_print_some ( int m, int n, double a[], int ilo, int jlo,
  int ihi, int jhi, char *title );
double *r8mat_u_inverse ( int n, double a[] );
double *r8mat_u_solve ( int n, double a[], double b[] );
double *r8mat_u1_inverse ( int n, double a[] );
void r8mat_uniform_01 ( int m, int n, int *seed, double r[] );
double *r8mat_uniform_01_new ( int m, int n, int *seed );
void r8mat_uniform_ab ( int m, int n, double a, double b, int *seed, double r[] );
double *r8mat_uniform_ab_new ( int m, int n, double a, double b, int *seed );
void r8mat_uniform_abvec ( int m, int n, double a[], double b[], int *seed, double r[] );
double *r8mat_uniform_abvec_new ( int m, int n, double a[], double b[], int *seed );
double *r8mat_ut_solve ( int n, double a[], double b[] );
double *r8mat_vand2 ( int n, double x[] );
double r8mat_vtmv ( int m, int n, double x[], double a[], double y[] );
void r8mat_zero ( int m, int n, double a[] );
double *r8mat_zero_new ( int m, int n );
double r8plu_det ( int n, int pivot[], double lu[] );
void r8plu_inverse ( int n, int pivot[], double lu[], double a_inverse[] );
void r8plu_mul ( int n, int pivot[], double lu[], double x[], double b[] );
void r8plu_sol ( int n, int pivot[], double lu[], double b[], double x[] );
void r8plu_to_r8mat ( int n, int pivot[], double lu[], double a[] );
int r8poly_degree ( int na, double a[] );
double *r8poly_deriv ( int n, double c[], int p );
double r8poly_lagrange_0 ( int npol, double xpol[], double xval );
double r8poly_lagrange_1 ( int npol, double xpol[], double xval );
double r8poly_lagrange_2 ( int npol, double xpol[], double xval );
double *r8poly_lagrange_coef ( int npol, int ipol, double xpol[] );
void r8poly_lagrange_factor ( int npol, double xpol[], double xval,
  double *wval, double *dwdx );
int r8poly_lagrange_val ( int npol, int ipol, double xpol[], double xval,
  double *pval, double *dpdx );
int r8poly_order ( int na, double a[] );
void r8poly_print ( int n, double a[], char *title );
void r8poly_shift ( double scale, double shift, int n, double poly_cof[] );
double *r8poly_value ( int m, double c[], int n, double x[] );
double *r8poly_value_2d ( int m, double c[], int n, double x[], double y[] );
int r8poly2_ex ( double x1, double y1, double x2, double y2, double x3, double y3,
  double *x, double *y );
int r8poly2_ex2 ( double x1, double y1, double x2, double y2, double x3, double y3,
  double *x, double *y, double *a, double *b, double *c );
void r8poly2_rroot ( double a, double b, double c, double *r1, double *r2 );
void r8poly2_val ( double x1, double y1, double x2, double y2,
  double x3, double y3, double x, double *y, double *yp, double *ypp );
void r8poly2_val2 ( int ndata, double tdata[],
  double ydata[], int left, double tval, double *yval );
int r8r8_compare ( double x1, double y1, double x2, double y2 );
void r8r8_print ( double a1, double a2, char *title );
int r8r8r8_compare ( double x1, double y1, double z1, double x2, double y2,
  double z2 );
void r8r8r8vec_index_insert_unique ( int maxn, int *n, double x[], double y[],
  double z[], int indx[], double xval, double yval, double zval, int *ival,
  int *ierror );
void r8r8r8vec_index_search ( int n, double x[], double y[], double z[],
  int indx[], double xval, double yval, double zval, int *less, int *equal,
  int *more );
void r8r8vec_index_insert_unique ( int maxn, int *n, double x[], double y[],
  int indx[], double xval, double yval, int *ival, int *ierror );
void r8r8vec_index_search ( int n, double x[], double y[], int indx[],
  double xval, double yval, int *less, int *equal, int *more );
void r8rmat_delete ( int m, int n, double **a );
double **r8rmat_new ( int m, int n );
void r8rmat_print ( int m, int n, double **a, char *title );
void r8rmat_print_some ( int m, int n, double **a, int ilo, int jlo, int ihi,
  int jhi, char *title );
double *r8rmat_to_r8mat ( int m, int n, double **a );
int r8row_compare ( int m, int n, double a[], int i, int j );
double *r8row_max ( int m, int n, double a[] );
double *r8row_mean ( int m, int n, double a[] );
double *r8row_min ( int m, int n, double a[] );
void r8row_reverse ( int m, int n, double a[] );
void r8row_sort_heap_a ( int m, int n, double a[] );
double *r8row_sum ( int m, int n, double a[] );
void r8row_swap ( int m, int n, double a[], int irow1, int irow2 );
double *r8row_to_r8vec ( int m, int n, double a[] );
double *r8row_variance ( int m, int n, double a[] );
void r8slmat_print ( int m, int n, double a[], char *title );
void r8vec_01_to_ab ( int n, double a[], double amax, double amin );
void r8vec_ab_to_01 ( int n, double a[] );
double *r8vec_ab_to_cd ( int n, double a[], double bmin, double bmax );
void r8vec_add ( int n, double a1[], double a2[] );
int r8vec_all_nonpositive ( int n, double a[] );
double r8vec_amax ( int n, double a[] );
int r8vec_amax_index ( int n, double a[] );
double r8vec_amin ( int n, double a[] );
int r8vec_amin_index ( int n, double a[] );
int r8vec_any_negative ( int n, double a[] );
int r8vec_any_nonzero ( int n, double a[] );
double *r8vec_any_normal ( int dim_num, double v1[] );
int r8vec_ascends ( int n, double x[] );
int r8vec_ascends_strictly ( int n, double x[] );
void r8vec_bin ( int n, double x[], int bin_num, double bin_min, double bin_max,
  int bin[], double bin_limit[] );
void r8vec_bracket ( int n, double x[], double xval, int *left,
  int *right );
void r8vec_bracket2 ( int n, double x[], double xval, int start, int *left,
  int *right );
void r8vec_bracket3 ( int n, double t[], double tval, int *left );
void r8vec_bracket4 ( int nt, double t[], int ns, double s[], int left[] );
int r8vec_bracket5 ( int nd, double xd[], double xi );
int *r8vec_bracket6 ( int nd, double xd[], int ni, double xi[] );
double *r8vec_chebyspace_new ( int n, double a, double b );
double *r8vec_cheby1space_new ( int n, double a, double b );
double *r8vec_cheby2space_new ( int n, double a, double b );
double r8vec_circular_variance ( int n, double x[] );
int r8vec_compare ( int n, double a[], double b[] );
void r8vec_concatenate ( int n1, double a[], int n2, double b[], double c[] );
double *r8vec_concatenate_new ( int n1, double a[], int n2, double b[] );
double *r8vec_convolution ( int m, double x[], int n, double y[] );
double *r8vec_convolution_circ ( int n, double x[], double y[] );
void r8vec_copy ( int n, double a1[], double a2[] );
double *r8vec_copy_new ( int n, double a1[] );
double r8vec_correlation ( int n, double x[], double y[] );
double r8vec_covar ( int n, double x[], double y[] );
double r8vec_cross_product_2d ( double v1[2], double v2[2] );
double r8vec_cross_product_2d_affine ( double v0[2], double v1[2], double v2[2] );
double *r8vec_cross_product_3d ( double v1[3], double v2[3] );
double *r8vec_cross_product_3d_affine ( double v0[3], double v1[3], double v2[3] );
double *r8vec_cum_new ( int n, double a[] );
double *r8vec_cum0_new ( int n, double a[] );
double *r8vec_dif ( int n, double h );
double r8vec_diff_norm ( int n, double a[], double b[] );
double r8vec_diff_norm_l1 ( int n, double a[], double b[] );
double r8vec_diff_norm_l2 ( int n, double a[], double b[] );
double r8vec_diff_norm_li ( int n, double a[], double b[] );
double r8vec_diff_norm_squared ( int n, double a[], double b[] );
void r8vec_direct_product ( int factor_index, int factor_order,
  double factor_value[], int factor_num, int point_num, double x[] );
void r8vec_direct_product2 ( int factor_index, int factor_order,
  double factor_value[], int factor_num, int point_num, double w[] );
double r8vec_distance ( int dim_num, double v1[], double v2[] );
int r8vec_distinct ( int n, double x[] );
void r8vec_divide ( int n, double a[], double s );
double r8vec_dot_product ( int n, double a1[], double a2[] );
double r8vec_dot_product_affine ( int n, double v0[], double v1[], double v2[] );
double r8vec_entropy ( int n, double x[] );
int r8vec_eq ( int n, double a1[], double a2[] );
void r8vec_even ( int n, double alo, double ahi, double a[] );
double *r8vec_even_new ( int n, double alo, double ahi );
double r8vec_even_select ( int n, double xlo, double xhi, int ival );
void r8vec_even2 ( int maxval, int nfill[], int nold, double xold[],
  int *nval, double xval[] );
double r8vec_even2_select ( int n, double xlo, double xhi, int ival );
void r8vec_even3 ( int nold, int nval, double xold[], double xval[] );
double *r8vec_expand_linear ( int n, double x[], int fat );
double *r8vec_expand_linear2 ( int n, double x[], int before, int fat,
  int after );
int *r8vec_first_index ( int n, double a[], double tol );
double r8vec_frac ( int n, double a[], int k );
double *r8vec_fraction ( int n, double x[] );
int r8vec_gt ( int n, double a1[], double a2[] );
void r8vec_heap_a ( int n, double a[] );
void r8vec_heap_d ( int n, double a[] );
int *r8vec_histogram ( int n, double a[], double a_lo, double a_hi, int histo_num );
double *r8vec_house_column ( int n, double a[], int k );
double r8vec_i4vec_dot_product ( int n, double r8vec[], int i4vec[] );
int r8vec_in_01 ( int n, double x[] );
int r8vec_in_ab ( int n, double x[], double a, double b );
void r8vec_index_delete_all ( int n, double x[], int indx[], double xval,
  int *n2, double x2[], int indx2[] );
void r8vec_index_delete_dupes ( int n, double x[], int indx[],
  int *n2, double x2[], int indx2[] );
void r8vec_index_delete_one ( int n, double x[], int indx[], double xval,
  int *n2, double x2[], int indx2[] );
void r8vec_index_insert ( int *n, double x[], int indx[], double xval );
void r8vec_index_insert_unique ( int *n, double x[], int indx[], double xval );
void r8vec_index_order ( int n, double x[], int indx[] );
void r8vec_index_search ( int n, double x[], int indx[], double xval, int *less,
  int *equal, int *more );
void r8vec_index_sort_unique ( int n, double x[], int *n2, double x2[],
  int indx2[] );
void r8vec_index_sorted_range ( int n, double r[], int indx[], double r_lo,
  double r_hi, int *i_lo, int *i_hi );
void r8vec_indexed_heap_d ( int n, double a[], int indx[] );
int r8vec_indexed_heap_d_extract ( int *n, double a[], int indx[] );
void r8vec_indexed_heap_d_insert ( int *n, double a[], int indx[],
  int indx_insert );
int r8vec_indexed_heap_d_max ( int n, double a[], int indx[] );
void r8vec_indicator ( int n, double a[] );
double *r8vec_indicator_new ( int n );
void r8vec_insert ( int n, double a[], int pos, double value );
int r8vec_insignificant ( int n, double r[], double s[] );
int r8vec_is_int ( int n, double a[] );
int r8vec_is_nonnegative ( int n, double x[] );
int r8vec_is_zero ( int n, double x[] );
double *r8vec_legendre_new ( int n, double a_first, double a_last );
double *r8vec_linspace_new ( int n, double a_lo, double a_hi );
double *r8vec_linspace2_new ( int n, double a_lo, double a_hi );
int r8vec_lt ( int n, double a1[], double a2[] );
void r8vec_mask_print ( int n, double a[], int mask_num, int mask[],
  char *title );
double r8vec_max ( int n, double dvec[] );
int r8vec_max_abs_index ( int n, double a[] );
int r8vec_max_index ( int n, double a[] );
double r8vec_mean ( int n, double x[] );
double r8vec_median ( int n, double a[] );
void r8vec_mesh_2d ( int nx, int ny, double xvec[], double yvec[],
  double xmat[], double ymat[] );
double *r8vec_midspace_new ( int n, double a_lo, double a_hi );
double r8vec_min ( int n, double dvec[] );
int r8vec_min_index ( int n, double a[] );
double r8vec_min_pos ( int n, double a[] );
int r8vec_mirror_next ( int n, double a[] );
int r8vec_negative_strict ( int n, double a[] );
double *r8vec_nint ( int n, double a[] );
double r8vec_norm ( int n, double a[] );
double r8vec_norm_affine ( int n, double v0[], double v1[] );
int r8vec_norm_l0 ( int n, double a[] );
double r8vec_norm_l1 ( int n, double a[] );
double r8vec_norm_l2 ( int n, double a[] );
double r8vec_norm_li ( int n, double a[] );
double r8vec_norm_lp ( int n, double a[], double p );
void r8vec_normal_01 ( int n, int *seed, double x[] );
void r8vec_normal_ab ( int n, double b, double c, int *seed, double x[] );
double *r8vec_normal_01_new ( int n, int *seed );
void r8vec_normalize ( int n, double a[] );
void r8vec_normalize_l1 ( int n, double a[] );
double r8vec_normsq ( int n, double a[] );
double r8vec_normsq_affine ( int n, double v0[], double v1[] );
double *r8vec_ones_new ( int n );
int r8vec_order_type ( int n, double x[] );
void r8vec_part_quick_a ( int n, double a[], int *l, int *r );
void r8vec_permute ( int n, int p[], int base, double a[] );
void r8vec_permute_cyclic ( int n, int k, double a[] );
void r8vec_permute_uniform ( int n, double a[], int *seed );
void r8vec_polarize ( int n, double a[], double p[], double a_normal[],
  double a_parallel[] );
int r8vec_positive_strict ( int n, double a[] );
void r8vec_print ( int n, double a[], char *title );
void r8vec_print_part ( int n, double a[], int max_print, char *title );
void r8vec_print_some ( int n, double a[], int i_lo, int i_hi, char *title );
double r8vec_product ( int n, double a[] );
void r8vec_range ( int n, double x[], double xmin, double xmax, double y[],
  double *ymin, double *ymax );
void r8vec_range_2 ( int n, double a[], double *amin, double *amax );
void r8vec_reverse ( int n, double a[] );
double r8vec_rms ( int n, double a[] );
void r8vec_rotate ( int n, double a[], int m );
double r8vec_scalar_triple_product ( double v1[3], double v2[3], double v3[3] );
void r8vec_scale ( double s, int n, double a[] );
int r8vec_search_binary_a ( int n, double a[], double aval );
void r8vec_shift ( int shift, int n, double x[] );
void r8vec_shift_circular ( int shift, int n, double x[] );
void r8vec_sort_bubble_a ( int n, double a[] );
void r8vec_sort_bubble_d ( int n, double a[] );
void r8vec_sort_heap_a ( int n, double a[] );
void r8vec_sort_heap_d ( int n, double a[] );
void r8vec_sort_heap_index_a ( int n, double a[], int indx[] );
int *r8vec_sort_heap_index_a_new ( int n, double a[] );
void r8vec_sort_heap_index_d ( int n, double a[], int indx[] );
int *r8vec_sort_heap_index_d_new ( int n, double a[] );
int *r8vec_sort_heap_mask_a ( int n, double a[], int mask_num, int mask[] );
void r8vec_sort_insert_a ( int n, double a[] );
int *r8vec_sort_insert_index_a ( int n, double a[] );
void r8vec_sort_quick_a ( int n, double a[] );
void r8vec_sort_shell_a ( int n, double a[] );
double *r8vec_sorted_merge_a ( int na, double a[], int nb, double b[], int *nc );
int r8vec_sorted_nearest ( int n, double a[], double value );
void r8vec_sorted_range ( int n, double r[], double r_lo, double r_hi,
  int *i_lo, int *i_hi );
void r8vec_sorted_split ( int n, double a[], double split, int *i_lt, int *i_gt );
void r8vec_sorted_undex ( int x_num, double x_val[], int x_unique_num,
  double tol, int undx[], int xdnu[] );
double *r8vec_sorted_unique ( int n, double a[], double tol, int *unique_num );
int r8vec_sorted_unique_count ( int n, double a[], double tol );
void r8vec_sorted_unique_hist ( int n, double a[], double tol, int maxuniq,
  int *unique_num, double auniq[], int acount[] );
int r8vec_split ( int n, double a[], double split );
double r8vec_std ( int n, double a[] );
void r8vec_step ( double x0, int n, double x[], double fx[] );
void r8vec_stutter ( int n, double a[], int m, double am[] );
double *r8vec_stutter_new ( int n, double a[], int m );
double r8vec_sum ( int n, double a[] );
void r8vec_swap ( int n, double a1[], double a2[] );
void r8vec_transpose_print ( int n, double a[], char *title );
void r8vec_undex ( int x_num, double x_val[], int x_unique_num, double tol,
  int undx[], int xdnu[] );
void r8vec_uniform_01 ( int n, int *seed, double r[] );
double *r8vec_uniform_01_new ( int n, int *seed );
void r8vec_uniform_ab ( int n, double a, double b, int *seed, double r[] );
double *r8vec_uniform_ab_new ( int n, double a, double b, int *seed );
void r8vec_uniform_abvec ( int n, double a[], double b[], int *seed, double r[] );
double *r8vec_uniform_abvec_new ( int n, double a[], double b[], int *seed );
double *r8vec_uniform_unit_new ( int m, int *seed );
int r8vec_unique_count ( int n, double a[], double tol );
int *r8vec_unique_index ( int n, double a[], double tol );
double r8vec_variance ( int n, double x[] );
double *r8vec_vector_triple_product ( double v1[3], double v2[3], double v3[3] );
void r8vec_write ( int n, double r[], char *output_file );
void r8vec_zero ( int n, double x[] );
double *r8vec_zero_new ( int n );
int r8vec2_compare ( int n, double a1[], double a2[], int i, int j );
void r8vec2_print ( int n, double a1[], double a2[], char *title );
void r8vec2_print_some ( int n, double x1[], double x2[], int max_print,
  char *title );
void r8vec2_sort_a ( int n, double a1[], double a2[] );
void r8vec2_sort_d ( int n, double a1[], double a2[] );
int *r8vec2_sort_heap_index_a ( int n, double x[], double y[] );
void r8vec2_sorted_unique ( int n, double a1[], double a2[], int *unique_num );
void r8vec2_sorted_unique_index ( int n, double a1[], double a2[],
  int *unique_num, int indx[] );
int r8vec2_sum_max_index ( int n, double a[], double b[] );
void r8vec3_print ( int n, double a1[], double a2[], double a3[], char *title );
double *roots_to_r8poly ( int n, double x[] );
void sort_heap_external ( int n, int *indx, int *i, int *j, int isgn );
void timestamp ( );
