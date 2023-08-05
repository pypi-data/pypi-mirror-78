// Copyright (C) 2018, 2019 Columbia University Irving Medical Center,
//     New York, USA

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

#include "../emblp/emblp.h"
#include "../solver_data.h"

#include <nvector/nvector_manyvector.h>    //access to manyvector N_Vector
#include <sundials/sundials_math.h>    //access to SUNDIALS

#include <cvode/cvode.h>                //prototypes for CVODE fcts, consts
#include <ida/ida.h>                    //prototypes for IDA fcts., consts
#include <cvode/cvode_direct.h>         //access to CVode interface
#include <ida/ida_direct.h>             //access to IDA interface
#include <sunmatrix/sunmatrix_dense.h>  //access to dense SUNMatrix
#include <sunmatrix/sunmatrix_sparse.h> //access to sparse SUNMatrix
#include <sunlinsol/sunlinsol_dense.h>  //access to dense SUNLinearSolver

/*
 *----------------------------------
 * Macros and function declarations.
 *----------------------------------
 */

///Macros for member functions
//////////////////////////////
#define NKIN  model.get_nkin()
#define TSTOP model.get_tstop()
#define TOUT  model.get_tout()
#define NEQ   model.get_neq()
#define NRTS  model.get_nrts()

///SUNDIALS ANALYZE
void PrintFinalStatsCVode(void *mem, bool), PrintFinalStatsIDA(void *mem, bool), PrintOutput(EMBLP_MODEL &, std::vector< std::vector<double> > &);
int check_flag(void *, const char *, int);

///SUNDIALS CVode and IDA
int f(realtype, N_Vector, N_Vector, void *), resrob(realtype, N_Vector, N_Vector, N_Vector, void *), grob(realtype, N_Vector, N_Vector, realtype *, void *);

///Integration using direct method
int integrateDirect(EMBLP_DIRECT &, std::vector< std::vector<double> > &, SolverData);

///Integration using Harwood et al.
int integrateHarwood(EMBLP_HARWOOD &, std::vector< std::vector<double> > &, SolverData);

///Integration using Scott et al.
