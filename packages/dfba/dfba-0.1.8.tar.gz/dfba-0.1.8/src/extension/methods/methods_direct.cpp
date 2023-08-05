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
 *------------------------------------
 * Integrate model using direct method
 *------------------------------------
 */

int integrateDirect(EMBLP_DIRECT &model, std::vector< std::vector<double> > &results, SolverData solver_data)
{
    ///Here we declare and initialize required objects for CVode
    std::string sunmatrix = solver_data.sunmatrix; //get sunmatrix string
    std::string sunlinsolver = solver_data.sunlinsolver; //get sunlinsolver string
    std::string ode_method = solver_data.ode_method; //get ode_method string
    bool display = 0;
    if(solver_data.display == "full" || solver_data.display == "sundials_only"){
        display = 1;
    }
    void *mem;
    N_Vector yy, avtol;
    realtype rtol, *yval, *atval;
    realtype t0, tout, tret;
    int retval;
    SUNMatrix A;
    SUNLinearSolver LS;
    sunindextype nnz;

    mem = NULL;
    yy = avtol = NULL;
    yval = atval = NULL;
    A = NULL;
    LS = NULL;

    ///Here we allocate N-vectors
    yy = N_VNew_Serial(NEQ);
    if (check_flag((void *)yy, "N_VNew_Serial", 0)) return(1);
    avtol = N_VNew_Serial(NEQ);
    if (check_flag((void *)avtol, "N_VNew_Serial", 0)) return(1);

    /// Here we set tolerance vectors
    rtol = RCONST(solver_data.rel_tolerance);
    atval = N_VGetArrayPointer(avtol);
    unsigned int tol_index = 0;
    for(int i=0; i<NEQ; i++){
        atval[i] = RCONST(solver_data.abs_tolerance[tol_index]);
        if(tol_index < solver_data.abs_tolerance.size() - 1){
            tol_index++;
        }
    }

    /// Here we create and initialize y and set integration limits, using model
    yval  = N_VGetArrayPointer(yy);
    int solver = model.initialize(); //update bounds and optimize lp (simplex method)
    if(solver != 0){ //if simplex method fails or lp not feasible
        CVodeFree(&mem);
        SUNLinSolFree(LS);
        SUNMatDestroy(A);
        N_VDestroy(avtol);
        N_VDestroy(yy);
        return 1; //break out of algorithm
    }
    if(display){
        std::cout << std::endl;
    }
    model.starting_values(t0,yval);
    tout = t0 + TOUT;

    ///Here we set up the CVODE memory object and check flags at each step
    if(ode_method == "BDF"){
        mem = CVodeCreate(CV_BDF); //create CVode object with BDF
    }
    else{
        mem = CVodeCreate(CV_ADAMS); //create CVode object with ADAMS
    }
    if(check_flag((void *)mem, "CVodeCreate", 0)) return(1);
    EMBLP_MODEL *user_data = &model; //create user data (reference to model)
    retval = CVodeSetUserData(mem, user_data); //set reference to model as user data
    if(check_flag(&retval, "CVodeSetUserData", 1)) return(1);
    retval = CVodeInit(mem, f, t0, yy); //initialize CVode memory
    if(check_flag(&retval, "CVodeInit", 1)) return(1);
    retval = CVodeSVtolerances(mem, rtol, avtol); //set tolerances
    if(check_flag(&retval, "CVodeSVtolerances", 1)) return(1);
    if(sunmatrix == "dense"){
        A = SUNDenseMatrix(NEQ, NEQ); //create dense SUNMatrix for use in linear solves
        if(check_flag((void *)A, "SUNDenseMatrix", 0)) return(1);
    }
    else if(sunmatrix == "sparse"){
        nnz = NEQ * NEQ;
        A = SUNSparseMatrix(NEQ, NEQ, nnz, CSR_MAT); //create sparse SUNMatrix for use in linear solves
        if(check_flag((void *)A, "SUNSparseMatrix", 0)) return(1);
    }
    else{
        std::cout << "SUNMatrix type not supported!" << std::endl;
        CVodeFree(&mem);
        SUNLinSolFree(LS);
        SUNMatDestroy(A);
        N_VDestroy(avtol);
        N_VDestroy(yy);
        return 1;
    }
    if(sunlinsolver == "dense"){
        LS = SUNDenseLinearSolver(yy, A); //create dense SUNLinearSolver object
        if(check_flag((void *)LS, "SUNDenseLinearSolver", 0)) return(1);
    }
    else{
        std::cout << "SUNLinearSolver type not supported!" << std::endl;
        CVodeFree(&mem);
        SUNLinSolFree(LS);
        SUNMatDestroy(A);
        N_VDestroy(avtol);
        N_VDestroy(yy);
        return 1;
    }
    retval = CVodeSetLinearSolver(mem, LS, A); //attach the matrix and linear solver
    if(check_flag(&retval, "CVodeSetLinearSolver", 1)) return(1);
    retval = CVodeSetJacFn(mem, NULL); //set the default Jacobian routine
    if(check_flag(&retval, "CVodeSetJacFn", 1)) return(1);

    ///Here we loop over change points and integrate between them
    int num_cps = model.change_points().size(); //get number of change points
    bool solver_valid = 1; //keep track of solver validity
    for(int cp_idx = 0; cp_idx<num_cps; cp_idx++){ //loop over change points
        double change_pnt = model.change_points()[cp_idx]; //get change point
        model.set_section(cp_idx); //set section
        retval = CVodeSetStopTime(mem, change_pnt); //set change point as stop time
        if(check_flag(&retval, "CVodeSetStopTime", 1)) return(1);
        while(model.current_tval()<change_pnt){ //while within limits of change point
            retval = CVode(mem, tout, yy, &tret, CV_NORMAL); //call CVODE solver
            model.update_kinetics(tret,yy); //update kinetic values
            if(check_flag(&retval, "CVode", 1)) return(1); //check status of CVode solver
            if(retval == CV_SUCCESS){ //if CVode solver reached tout
                PrintOutput(model,results); //store results at tout
                PrintFinalStatsCVode(mem,display); //print final stats of intergation loop
                if(display){
                    std::cout << std::endl;
                }
                int solver = model.initialize(); //update bounds and optimize lp (simplex method)
                if(solver != 0){ //if simplex method fails or lp not feasible
                    solver_valid = 0; //solver invalid
                    break; //break out of while loop
                }
                model.starting_values(t0,yval); //set new values
                retval = CVodeReInit(mem, t0, yy); //re-initialize CVode memory
                if(check_flag(&retval, "CVodeReInit", 1)) return(1);
                tout += TOUT; //increment tout by TOUT
            }
            else if(retval == CV_TSTOP_RETURN){ //if CVode solver reached change point
                model.starting_values(t0,yval); //set new values
                retval = CVodeReInit(mem, t0, yy); //re-initialize CVode memory
                if(check_flag(&retval, "CVodeReInit", 1)) return(1);
                break; //break out of while loop
            }
        }
        if(!solver_valid){ //if solver invalid
            break; //break out of algorithm
        }
    }

    ///Here we print final stats and free memory
    PrintFinalStatsCVode(mem,display);  //print final stats of intergation loop
    CVodeFree(&mem);
    SUNLinSolFree(LS);
    SUNMatDestroy(A);
    N_VDestroy(avtol);
    N_VDestroy(yy);
    return retval;
}
