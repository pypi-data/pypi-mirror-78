from libcpp cimport bool
cdef extern from "gropt/incl/ElasticCurvesReparam.h":
    void optimum_reparam(double *C1, double *C2, int n, int d, double w,
                     bool onlyDP, bool rotated, bool isclosed, int skipm,
                     int autoselectC, double *opt, bool swap, double *fopts,
                     double *comtime);
