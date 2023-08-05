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
 *----------------------------------------------------
 * Integrate model using algorithm from Harwood et al.
 *----------------------------------------------------
 */

int integrateHarwood(EMBLP_HARWOOD &model, std::vector< std::vector<double> > &results, SolverData solver_data)
{
    ///Here we declare and initialize required objects for IDA
    std::string sunmatrix = solver_data.sunmatrix; //get sunmatrix string
    std::string sunlinsolver = solver_data.sunlinsolver; //get sunlinsolver string
    bool display = 0;
    if(solver_data.display == "full" || solver_data.display == "sundials_only"){
        display = 1;
    }
    void *mem;
    N_Vector yy, yp, avtol, vid;
    realtype rtol, *yval, *ypval, *atval, *idval;
    realtype t0, tout, tret;
    int retval, retvalr;
    int rootsfound[NRTS];
    SUNMatrix A;
    SUNLinearSolver LS;
    sunindextype nnz;

    mem = NULL;
    yy = yp = avtol = vid = NULL;
    yval = ypval = atval = idval = NULL;
    A = NULL;
    LS = NULL;

    ///Here we allocate N-vectors
    yy = N_VNew_Serial(NEQ);
    if(check_flag((void *)yy, "N_VNew_Serial", 0)) return(1);
    yp = N_VNew_Serial(NEQ);
    if(check_flag((void *)yp, "N_VNew_Serial", 0)) return(1);
    avtol = N_VNew_Serial(NEQ);
    if(check_flag((void *)avtol, "N_VNew_Serial", 0)) return(1);
    vid = N_VNew_Serial(NEQ);
    if(check_flag((void *)vid, "N_VNew_Serial", 0)) return(1);

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

    /// Here we set vector ids
    idval = N_VGetArrayPointer(vid);
    for(int i=0; i<NKIN; i++){
        idval[i] = 1.0;
    }
    for(int i=NKIN; i<NEQ; i++){
        idval[i] = 0.0;
    }

    /// Here we create and initialize y, y', and set integration limits, using model
    yval  = N_VGetArrayPointer(yy);
    ypval = N_VGetArrayPointer(yp);
    int solver = model.initialize(); //update bounds and optimize lp (simplex method, set basis info and store tableau)
    if(solver != 0){ //if simplex method fails or lp not feasible
        IDAFree(&mem);
        SUNLinSolFree(LS);
        SUNMatDestroy(A);
        N_VDestroy(avtol);
        N_VDestroy(yy);
        N_VDestroy(yp);
        N_VDestroy(vid);
        return 1; //break out of algorithm1
    }
    if(display){
        std::cout << std::endl;
    }
    model.starting_values(t0,yval,ypval);
    tout = t0 + TOUT;

    ///Here we set up the IDA memory object and check flags at each step
    mem = IDACreate(); //create IDA object
    if(check_flag((void *)mem, "IDACreate", 0)) return(1);
    EMBLP_MODEL *user_data = &model; //create user data (reference to model)
    retval = IDASetUserData(mem, user_data); //set reference to model as user data
    if(check_flag(&retval, "IDASetUserData", 1)) return(1);
    retval = IDAInit(mem, resrob, t0, yy, yp); //initialize IDA memory
    if(check_flag(&retval, "IDAInit", 1)) return(1);
    retval = IDASVtolerances(mem, rtol, avtol); //set tolerances
    if(check_flag(&retval, "IDASVtolerances", 1)) return(1);
    retval = IDASetId(mem, vid); //set vector ids
    if(check_flag(&retval, "IDASetId", 1)) return(1);
    retval = IDARootInit(mem, NRTS, grob); //specify the root function grob with NRTS components
    if (check_flag(&retval, "IDARootInit", 1)) return(1);
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
        IDAFree(&mem);
        SUNLinSolFree(LS);
        SUNMatDestroy(A);
        N_VDestroy(avtol);
        N_VDestroy(yy);
        N_VDestroy(yp);
        N_VDestroy(vid);
        return 1;
    }
    if(sunlinsolver == "dense"){
        LS = SUNDenseLinearSolver(yy, A); //create dense SUNLinearSolver object
        if(check_flag((void *)LS, "SUNDenseLinearSolver", 0)) return(1);
    }
    else{
        std::cout << "SUNLinearSolver type not supported!" << std::endl;
        IDAFree(&mem);
        SUNLinSolFree(LS);
        SUNMatDestroy(A);
        N_VDestroy(avtol);
        N_VDestroy(yy);
        N_VDestroy(yp);
        N_VDestroy(vid);
        return 1;
    }
    retval = IDASetLinearSolver(mem, LS, A); //attach the matrix and linear solver
    if(check_flag(&retval, "IDASetLinearSolver", 1)) return(1);
    retval = IDASetJacFn(mem, NULL); //set the default Jacobian routine
    if(check_flag(&retval, "IDASetJacFn", 1)) return(1);

    ///Here we loop over change points and integrate between them
    int num_cps = model.change_points().size(); //get number of change points
    bool solver_valid = 1; //keep track of solver validity
    for(int cp_idx = 0; cp_idx<num_cps; cp_idx++){ //loop over change points
        double change_pnt = model.change_points()[cp_idx]; //get change point
        model.set_section(cp_idx); //set section
        retval = IDACalcIC(mem,IDA_YA_YDP_INIT,tout); //calculate consistent initial conditions
        if(check_flag(&retval, "IDACalcIC", 1)) return(1);
        retval = IDASetStopTime(mem, change_pnt); //set change point as stop time
        if(check_flag(&retval, "IDASetStopTime", 1)) return(1);
        while(model.current_tval()<change_pnt){ //while within limits of change point
            retval = IDASolve(mem, tout, &tret, yy, yp, IDA_NORMAL); //call IDA solver
            model.update_kinetics(tret,yy,yp); //update kinetic values
            if(check_flag(&retval, "IDASolve", 1)) return(1); //check status of IDA solver
            if (retval == IDA_ROOT_RETURN) { //if root was found
                retvalr = IDAGetRootInfo(mem, rootsfound); //get root info
                check_flag(&retvalr, "IDAGetRootInfo", 1); //check status of roots
                PrintFinalStatsIDA(mem,display); //print final stats of intergation loop
                if(display){
                    std::cout << std::endl;
                }
                int solver = model.initialize(); //update bounds and optimize lp (simplex method, set basis info and store tableau)
                if(solver != 0){ //if simplex method fails or lp not feasible
                    solver_valid = 0; //solver invalid
                    break; //break out of while loop
                }
                model.starting_values(t0,yval,ypval); //update starting values
                retval = IDAReInit(mem, t0, yy, yp); //re-initialize IDA memory
                if(check_flag(&retval, "IDAInit", 1)) return(1);
            }
            else if(retval == IDA_SUCCESS){ //if IDA solver reached tout
                PrintOutput(model,results); //store result at tout
                tout += TOUT; //increment tout by TOUT
            }
            else if(retval == IDA_TSTOP_RETURN){ //if IDA solver reached change point
                model.starting_values(t0,yval,ypval); //update starting values
                retval = IDAReInit(mem, t0, yy, yp); //re-initialize IDA memory
                if(check_flag(&retval, "IDAInit", 1)) return(1);
                break; //break out of while loop
            }
        }
        if(!solver_valid){ //if solver invalid
            break; //break out of algorithm
        }
    }

    ///Here we print final stats and free memory
    PrintFinalStatsIDA(mem,display); //print final stats of intergation loop
    IDAFree(&mem);
    SUNLinSolFree(LS);
    SUNMatDestroy(A);
    N_VDestroy(avtol);
    N_VDestroy(yy);
    N_VDestroy(yp);
    N_VDestroy(vid);
    return retval;
}
