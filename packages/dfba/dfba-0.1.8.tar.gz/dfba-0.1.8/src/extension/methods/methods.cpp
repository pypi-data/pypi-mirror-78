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

#include "methods.h"

/*
 *----------------------------------
 * Functions for analyzing SUNDIALS.
 *----------------------------------
 */

/*
 * Print output to file
 */

void PrintOutput(EMBLP_MODEL &model, std::vector< std::vector<double> > &results)
{
    realtype *yval = N_VGetArrayPointer(model.current_yval());
    std::vector<double> lpvars = model.current_lpvariables();
    int num_fluxes = lpvars.size()/2;

    std::vector<double> result(NKIN+num_fluxes+1);
    result[0] = model.current_tval();
    
    ///Here we write kinetic variables to results
    for(int i=0; i<NKIN; i++){
        result[i+1] = yval[i];
    }

    ///Here we write fluxes to results
    for(int i=0; i<num_fluxes; i++){
        result[i+NKIN+1] = lpvars[2*i] - lpvars[2*i+1];
    }
    
    results.push_back(result);
}

/*
 * Print final integrator statistics
 */

void PrintFinalStatsCVode(void *mem, bool display)
{
    if(!display){
        return;
    }
    int retval;
    long int nst, nfe, nsetups, nje, nfeLS, nni, ncfn, netf, nge;

    retval = CVodeGetNumSteps(mem, &nst);
    check_flag(&retval, "CVodeGetNumSteps", 1);
    retval = CVodeGetNumRhsEvals(mem, &nfe);
    check_flag(&retval, "CVodeGetNumRhsEvals", 1);
    retval = CVodeGetNumLinSolvSetups(mem, &nsetups);
    check_flag(&retval, "CVodeGetNumLinSolvSetups", 1);
    retval = CVodeGetNumErrTestFails(mem, &netf);
    check_flag(&retval, "CVodeGetNumErrTestFails", 1);
    retval = CVodeGetNumNonlinSolvIters(mem, &nni);
    check_flag(&retval, "CVodeGetNumNonlinSolvIters", 1);
    retval = CVodeGetNumNonlinSolvConvFails(mem, &ncfn);
    check_flag(&retval, "CVodeGetNumNonlinSolvConvFails", 1);
    retval = CVodeGetNumJacEvals(mem, &nje);
    check_flag(&retval, "CVodeGetNumJacEvals", 1);
    retval = CVodeGetNumRhsEvals(mem, &nfeLS);
    check_flag(&retval, "CVodeGetNumRhsEvals", 1);
    retval = CVodeGetNumGEvals(mem, &nge);
    check_flag(&retval, "CVodeGetNumGEvals", 1);

    printf("\nFinal Statistics:\n");
    printf("Steps = %-6ld RhsEvals  = %-6ld LinSolvSetups = %-6ld lsRhsEvals = %-6ld JacEvals = %ld\n",
           nst, nfe, nsetups, nfeLS, nje);
    printf("NonlinSolvIters = %-6ld NonlinSolvConvFails = %-6ld ErrTestFails = %-6ld GEvals = %ld\n \n",
           nni, ncfn, netf, nge);
}

void PrintFinalStatsIDA(void *mem, bool display)
{
    if(!display){
        return;
    }
    int retval;
    long int nst, nni, nje, nre, nreLS, netf, ncfn, nge;

    retval = IDAGetNumSteps(mem, &nst);
    check_flag(&retval, "IDAGetNumSteps", 1);
    retval = IDAGetNumResEvals(mem, &nre);
    check_flag(&retval, "IDAGetNumResEvals", 1);
    retval = IDAGetNumJacEvals(mem, &nje);
    check_flag(&retval, "IDAGetNumJacEvals", 1);
    retval = IDAGetNumNonlinSolvIters(mem, &nni);
    check_flag(&retval, "IDAGetNumNonlinSolvIters", 1);
    retval = IDAGetNumErrTestFails(mem, &netf);
    check_flag(&retval, "IDAGetNumErrTestFails", 1);
    retval = IDAGetNumNonlinSolvConvFails(mem, &ncfn);
    check_flag(&retval, "IDAGetNumNonlinSolvConvFails", 1);
    retval = IDAGetNumResEvals(mem, &nreLS);
    check_flag(&retval, "IDAGetNumResEvals", 1);
    retval = IDAGetNumGEvals(mem, &nge);
    check_flag(&retval, "IDAGetNumGEvals", 1);
    printf("\nFinal Run Statistics: \n\n");
    printf("Number of steps                    = %ld\n", nst);
    printf("Number of residual evaluations     = %ld\n", nre+nreLS);
    printf("Number of Jacobian evaluations     = %ld\n", nje);
    printf("Number of nonlinear iterations     = %ld\n", nni);
    printf("Number of error test failures      = %ld\n", netf);
    printf("Number of nonlinear conv. failures = %ld\n", ncfn);
    printf("Number of root fn. evaluations     = %ld\n", nge);
}

/*
 * Check function return value...
 *   opt == 0 means SUNDIALS function allocates memory so check if
 *            returned NULL pointer
 *   opt == 1 means SUNDIALS function returns a flag so check if
 *            flag >= 0
 *   opt == 2 means function allocates memory so check if returned
 *            NULL pointer
 */

int check_flag(void *flagvalue, const char *funcname, int opt)
{
    int *errflag;
    if(opt == 0 && flagvalue == NULL){ //check if SUNDIALS function returned NULL pointer - no memory allocated
        fprintf(stderr,"\nSUNDIALS_ERROR: %s() failed - returned NULL pointer\n\n",funcname);
        return(1);
    }
    else if(opt == 1){
        errflag = (int *) flagvalue; //check if flag < 0
        if(*errflag<0){
            fprintf(stderr,"\nSUNDIALS_ERROR: %s() failed with flag = %d\n\n",funcname, *errflag);
            return(1);
        }
    }
    else if(opt == 2 && flagvalue == NULL){ //check if function returned NULL pointer - no memory allocated
        fprintf(stderr,"\nMEMORY_ERROR: %s() failed - returned NULL pointer\n\n",funcname);
        return(1);
    }
    return(0);
}

/*
 *--------------------
 * Functions for CVode
 *--------------------
 */

/*
 * Define the system rhs for CVode.
 */

int f(realtype t, N_Vector yy, N_Vector yp, void *user_data)
{
    ((EMBLP_MODEL*)user_data)->rhs(t, N_VGetArrayPointer(yy), N_VGetArrayPointer(yp));
    return(0);
}

/*
 *------------------
 * Functions for IDA
 *------------------
 */

/*
 * Define the system residual function for IDA.
 */

int resrob(realtype t, N_Vector yy, N_Vector yp, N_Vector rr, void *user_data)
{
    ((EMBLP_MODEL*)user_data)->drhs(t, N_VGetArrayPointer(yy), N_VGetArrayPointer(yp), N_VGetArrayPointer(rr));
    return(0);
}

/*
 * Root function routine for IDA.
 */

int grob(realtype t, N_Vector yy, N_Vector yp, realtype *gout, void *user_data)
{
    ((EMBLP_MODEL*)user_data)->event(t, N_VGetArrayPointer(yy), gout);
    return(0);
}
