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
 *--------------------------------
 * EMBLP_HARWOOD member functions.
 *--------------------------------
 */

EMBLP_HARWOOD::EMBLP_HARWOOD(glp_prob *lp_in, glp_smcp parm_in, UserData user_data, std::string functionlib) : EMBLP_MODEL(lp_in, parm_in, user_data, functionlib)
{
    neq = nkin+nrow, nrts = 2*nrow;
    basic_ind = std::vector<int>(nrow,0);
    basic_stat = std::vector<int>(ntot,0);
    basic_const = std::vector<double>(nrow,0);
    simplex_tableau = std::vector< std::vector<double> >(nrow, std::vector<double>(nexc,0.0));
    current_y = N_VNew_Serial(neq), current_yp = N_VNew_Serial(neq); //create current y and yp
    for(int i=0; i<nkin; i++){ //loop over kinetic variables
        Ith(current_y,i) = user_data.initial_conditions[i+1]; //set initial condition for kinetic variable
    }
}

/*
 * Update current kinetic values
 */

void EMBLP_HARWOOD::update_kinetics(realtype tval, N_Vector yval, N_Vector ypval)
{
    ///Here we update current time
    current_t = tval; //update current time

    ///Here we update current y and y'
    for(int i=0; i<neq; i++){
        Ith(current_y,i) = Ith(yval,i), Ith(current_yp,i) = Ith(ypval,i); //update current y,y' components
    }

    ///Here we update current lpvariables
    realtype *yy = N_VGetArrayPointer(yval);
    for(int i=0; i<cur_ind.size(); i++){
        current_lpvars[i] = get_lpvariable(cur_ind[i],tval,yy);
    }
}


/*
 * Set starting values for integration
 */

void EMBLP_HARWOOD::starting_values(realtype &tval, realtype *yval, realtype *ypval)
{
    tval = current_tval(); //set t
    for(int i=0; i<neq; i++){ //loop over y,y' components
        yval[i] = Ith(current_y,i), ypval[i] = Ith(current_yp,i); //set y,y'
    }
}

/*
 * Update bounds, optimize, and set starting values for next round of integration
 */

int EMBLP_HARWOOD::initialize()
{
    ///Here we update bounds then optimize to obtain current values for non-kinetic SUNDIALS variables
    remove_constraints(); //removing additional constraints from LP if problem lexicographic
    update_bounds(); //update bounds of LP using current kinetic values
    int solver = optimize(); //call optimize
    if(solver != 0){ //if optimize not successful
        return solver; //return unsuccessful optimize
    }

    ///Here we represent optimal basis using simplex tableau
    calculate_tableau(); //calculate simplex tableau for representing current basis

    ///Here we set current values for all SUNDIALS variables
    realtype *y = N_VGetArrayPointer(current_y);
    for(int i=0; i<nrow; i++){ //loop over basic lpvariables
        Ith(current_y,i+nkin) = get_lpvariable(basic_ind[i],current_t,y); //set non-kinetic starting value to basic lpvariable
    }

    ///Here we use drhs combined with zero vector (blank) to set current y' variables
    N_Vector blank = N_VNew_Serial(neq); //create blank vector
    N_VConst(RCONST(0.0),blank); //set blank to zero vector
    realtype *yp = N_VGetArrayPointer(current_yp), *bl = N_VGetArrayPointer(blank); //get pointers
    drhs(current_t,y,bl,yp); //use drhs to calculate yp using blank in place of ypval and yp in place of rval for normal use
    N_VDestroy(blank); //destroy blank vector
    return 0;
}

/*
 * Calculate simplex tableau for current basis
 */

void EMBLP_HARWOOD::calculate_tableau()
{
    ///Here we calculate rows of the simplex tableau and set basic info
    std::fill(basic_stat.begin(),basic_stat.end(),-1); //set all lpvariable basic statuses to non-basic
    std::fill(basic_ind.begin(),basic_ind.end(),0); //zero all basic lpindices
    std::vector< std::vector<double> > simplex_tableau_val(ntot, std::vector<double>(ntot,0.0)); //tmp simplex tableau
    int basic_index = 0; //to provide lpvariable basic status
    for(int index = 1; index<=ntot; index++){
        int status = 0; //glp basis status for ith lpvariable
        if(index<=nrow){ //if auxiliary lpvariable
            status = glp_get_row_stat(lp,index); //get glp basic status of row
        }
        else{ //if structural lpvariable
            status = glp_get_col_stat(lp,index-nrow); //get glp basic status of column
        }
        if(status == 1){ //if glp basic then save row of simplex tableau and set basic info
            //basic info
            int i = index - 1; //lpindex
            basic_stat[i] = basic_index; //set basic status of ith lpvariable
            basic_ind[basic_index] = i; //set basic lpindex
            basic_index++; //increment lpvariable basic status
            //simplex tableau
            int ind[ncol+1]; //temp index
            double val[ncol+1]; //temp value
            int len = glp_eval_tab_row(lp,index,ind,val); //evaluate ith row of simplex tableau
            for(int row_index = 1; row_index<=len; row_index++){ //update all column values for ith row
                int col_index = ind[row_index] - 1;
                simplex_tableau_val[i][col_index] = val[row_index]; //value in ith row, jth column of simplex tableau
            }
        }
    }

    ///Here we calculate current constant portion of all lpvariables in two stages
    std::fill(basic_const.begin(),basic_const.end(),0.0);
    /// 1) Here we calculate the values of non-exchange, non-basic lpvariables
    std::vector<double> non_basic(ntot,0); //temp vector for storing values of non-basic lpvariables
    for(int i=0; i<ntot; i++){ //loop over all lpvariables
        if(basic_stat[i]<0){ //if non-basic (so that basic remain zero)
            if(!(ex_stat[i])){ //if non-exchange (so that exchange remain zero)
                realtype t; //dummy t
                realtype *yval; //dummy yval
                non_basic[i] = get_lpvariable(i,t,yval); //calculate value of a non-exchange, non-basic lpvariable
            }
        }
    }
    /// 2) Here we calculate the constant portion of basic lpvariables and save the unused portion of simplex tableau
    for(int i=0; i<nrow; i++){ //loop over basic lpvariables
        int lpindex = basic_ind[i]; //get lpindex of ith basic lpvariable
        double basic_value = 0.0;
        int exchange_index = 0;
        for(int j=0; j<ntot; j++){ //loop over lpvariables (recall contributions from basic are zero)
            if(ex_stat[j]){ //if exchange lpvariable
                simplex_tableau[i][exchange_index] = simplex_tableau_val[lpindex][j]; //set remaining portion of simplex tableau
                exchange_index++;
            }
            else{ //if non-exchange lpvariable
                basic_value += simplex_tableau_val[lpindex][j]*non_basic[j]; //add jth component of sum for ith basic variable
            }
        }
        basic_const[i] = basic_value; //set constant portion of ith basic structural lpvariable
    }
}

/*
 * Return value of lpvariable with provided index
 */

double EMBLP_HARWOOD::get_lpvariable(int i, realtype tval, realtype *yval)
{
    double lpvariable = 0.0;
    if(basic_stat[i]<0){ //if non-basic
        int status = 0;
        if(i>=nrow){ //if structural
            status = glp_get_col_stat(lp,i-nrow+1); //get status of structural lpvariable
        }
        else{ //if auxiliary
            status = glp_get_row_stat(lp,i+1); //get status of auxiliary lpvariable
        }
        switch(status){
            case 2: {
                lpvariable = return_lower_bound(i,tval,yval); //lower bound of non-basic variable at lower bound
                break;
            }
            case 3: {
                lpvariable = return_upper_bound(i,tval,yval); //upper bound of non-basic variable at upper bound
                break;
            }
            case 5: {
                lpvariable = return_lower_bound(i,tval,yval); //lower bound of fixed non-basic variable
                break;
            }
            default: {
                std::cout << "Error: there was an uncoventional (free non-basic) lpvariable." << std::endl; //if free non-basic variable
                clear();
                exit(-1);
            }
        }
    }
    else{ //if basic
        int basic_index = basic_stat[i]; //get basic index of lpvariable i
        lpvariable = basic_const[basic_index]; //get constant portion of (basic) lpvariable i
        for(int j=0; j<nexc; j++){ //loop over exchange lpvariables
            int exchange_lpindex = ex_ind[j]; //get exchange lpindex
            if(basic_stat[exchange_lpindex]<0){ //if exchange lpvariable is non-basic
                lpvariable += simplex_tableau[basic_index][j]*get_lpvariable(exchange_lpindex,tval,yval); //add non-basic exchange contribution
            }
        }
    }
    return lpvariable;
}

/*
 * Calculate DAE right-hand side
 */

void EMBLP_HARWOOD::drhs(realtype tval, realtype *yval, realtype *ypval, realtype *rval)
{
    ///Here we calculate values of required lpvariables
    std::vector<double> required_lpvariables(nreq,0.0); //declare temp storage vector
    for(int i=0; i<nreq; i++){ //loop over required lpvariables
        required_lpvariables[i] = get_lpvariable(req_ind[i],tval,yval); //calculate required lpvariable
    }

    ///Here we calculate residuals of kinetic SUNDIALS variables using user-supplied function pointer
    kinetic_expression(tval,yval,ypval,rval,required_lpvariables,section); //call kinetic function, passing required lpvariables and section flag

    ///Here we calculate resdiuals of non-kinetic SUNDIALS variables using basic lpvariables
    for(int i=nkin; i<neq; i++){
        rval[i]  = yval[i] - get_lpvariable(basic_ind[i-nkin],tval,yval);
    }
}

/*
 * Event detection
 */

void EMBLP_HARWOOD::event(realtype tval, realtype *yval, realtype *gout)
{
    double epsilon = 1e-6; //set regularity of rootfinding

    ///Here we create a rootfinding function for the upper and lower bound of each basic lpvariable
    for(int i=0; i<nrow; i++){
        realtype y = yval[nkin+i];
        int lpindex = basic_ind[i];
        gout[2*i] = return_upper_bound(lpindex,tval,yval) - y + epsilon; //root function for upper bound
        gout[2*i+1] = y - return_lower_bound(lpindex,tval,yval) + epsilon; //root function for lower bound
    }
}
