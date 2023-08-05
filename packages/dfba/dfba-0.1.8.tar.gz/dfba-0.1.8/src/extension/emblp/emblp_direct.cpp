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

#include "emblp.h"

/*
 *-------------------------------
 * EMBLP_DIRECT member functions.
 *-------------------------------
 */

EMBLP_DIRECT::EMBLP_DIRECT(glp_prob *lp_in, glp_smcp parm_in, UserData user_data, std::string functionlib) : EMBLP_MODEL(lp_in, parm_in, user_data, functionlib)
{
    neq = nkin;
    required_lpvariables = std::vector<double>(nreq,0.0); //init required lpvariables
    current_y = N_VNew_Serial(neq), current_yp = N_VNew_Serial(neq);
    for(int i=0; i<nkin; i++){ //loop over kinetic variables
        Ith(current_y,i) = user_data.initial_conditions[i+1]; //set initial condition for kinetic variable
    }
    N_VConst(RCONST(0.0), current_yp); //blank current yp
    ypval = N_VGetArrayPointer(current_yp); //set blank pointer
}

/*
 * Update current kinetic values
 */

void EMBLP_DIRECT::update_kinetics(realtype tval, N_Vector yval)
{
    ///Here we update current time
    current_t = tval; //update current time

    ///Here we update current y
    for(int i=0; i<neq; i++){
        Ith(current_y,i) = Ith(yval,i); //update current y components
    }

    ///Here we update current lpvariables
    for(int i=0; i<cur_ind.size(); i++){
        current_lpvars[i] = get_lpvariable(cur_ind[i]); //update current lpvariables
    }
}

/*
 * Set starting values for integration
 */

void EMBLP_DIRECT::starting_values(realtype &tval, realtype *yval)
{
    tval = current_tval(); //set t
    for(int i=0; i<neq; i++){ //loop over y components
        yval[i] = Ith(current_y,i); //set y
    }
}

/*
 * Update bounds, optimize, and set starting values for next round of integration
 */

int EMBLP_DIRECT::initialize()
{
    ///Here we update bounds then optimize
    update_bounds(); //update bounds of LP using current kinetic values
    int solver = optimize(); //call optimize
    if(solver != 0){ //if optimize not successful
        return solver; //return unsuccessful optimize
    }

    ///Here we extract values of required lpvariables
    for(int i=0; i<nreq; i++){ //loop over required lpvariables
        required_lpvariables[i] = get_lpvariable(req_ind[i]); //calculate required lpvariable
    }
    return 0;
}

/*
 * Return value of lpvariable with provided index
 */

double EMBLP_DIRECT::get_lpvariable(int i)
{
    if(i>=nrow){ //if structural
        return glp_get_col_prim(lp,i-nrow+1); //get primal value of structural lpvariable
    }
    else{ //if auxiliary
        return glp_get_row_prim(lp,i+1); //get primal value of auxiliary lpvariable
    }
}

/*
 * Calculate ODE right-hand side
 */

void EMBLP_DIRECT::rhs(realtype tval, realtype *yval, realtype *ydot)
{
    ///Here we calculate ydot of kinetic SUNDIALS variables using user-supplied function pointer
    kinetic_expression(tval,yval,ypval,ydot,required_lpvariables,section); //call kinetic function, passing required lpvariables and section flag
}
