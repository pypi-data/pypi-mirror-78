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
 *------------------------------
 * EMBLP_MODEL member functions.
 *------------------------------
 */

/*
 * Initialization of emblp model
 */

EMBLP_MODEL::EMBLP_MODEL(glp_prob *lp_in, glp_smcp parm_in, UserData user_data, std::string functionlib)
{
    ///Here we load dynamic library and get symbols
    handle = dlopen(functionlib.c_str(), RTLD_LAZY); //open the library
    if(!handle){ //if library not found
        std::cerr << "Cannot open dynamic library: " << dlerror() << std::endl;
        clear();
        return;
    }
    dlerror(); //init error
    std::string kinetics = "kinetics" + user_data.name; //create kinetics tag
    std::string upper_bounds = "upper_bounds" + user_data.name; //create upper bounds tag
    std::string lower_bounds = "lower_bounds" + user_data.name; //create lower bounds tag
    exchange_upper_bounds = (ExchangeBound) dlsym(handle, upper_bounds.c_str()), exchange_lower_bounds = (ExchangeBound) dlsym(handle, lower_bounds.c_str());  //set symbols for exchange bound functions
    kinetic_expression = (OdeExpression) dlsym(handle, kinetics.c_str()); //set symbol for kinetic expression
    const char *dlsym_error = dlerror(); //set error
    if(dlsym_error){ //if error loading symbols
        std::cerr << "Cannot load symbols: " << dlsym_error << std::endl;
        clear();
        return;
    }

    ///Here we assign pointer to copy of input LP problem
    lp = glp_create_prob(); //create empty problem and assign pointer
    parm = parm_in; //copy value of parm
    glp_copy_prob(lp,lp_in,GLP_OFF); //copy problem from input

    ///Here we set and arrange user data
    set_data(user_data); //set user data
}

/*
 * Set data for model
 */

void EMBLP_MODEL::set_data(UserData user_data)
{
    nkin = user_data.kinetic_dimensions[0], nexc = user_data.kinetic_dimensions[1], nreq = user_data.kinetic_dimensions[2];
    tstop = user_data.output_times[0], tout = user_data.output_times[1];
    obj_dirs = user_data.obj_directions, obj_inds = user_data.obj_indices, obj_coefs = user_data.obj_coefficients;
    nobj = obj_dirs.size();
    ex_ind = user_data.exchange_indices, req_ind = user_data.required_indices, cur_ind = user_data.current_indices;
    nrow = glp_get_num_rows(lp), ncol = glp_get_num_cols(lp), ntot = ncol+nrow;
    ex_stat = std::vector<bool>(ntot,0);
    current_t = user_data.initial_conditions[0];
    current_lpvars = std::vector<double>(cur_ind.size());
    change_pnts = user_data.change_points;
    change_pnts.push_back(tstop);
    neq = nrts = section = 0; //default

    ///Here we set indices and status of exchange lpvariables
    for(int i=0; i<nexc; i++){ //loop over exchange indices
        ex_stat[ex_ind[i]] = 1; //set status of exchange
    }
}

/*
 * Update all structural bounds
 */

void EMBLP_MODEL::update_bounds()
{
    realtype *yval = N_VGetArrayPointer(current_y); //pointer to pass to return_bound

    ///Here we update the bounds of each auxiliary variable
    for(int i = 0; i<nrow; i++){ //loop over all auxiliary lpvariables
        double lb = return_lower_bound(i,current_t,yval), ub = return_upper_bound(i,current_t,yval); //get lb,ub using current yval
        int row_index = i+1; //get row index
        double diff = ub - lb;
        int type = glp_get_row_type(lp,row_index); //get row type
        if(type == 4 && lb == ub){ //if lb = ub then row type is changed to GLP_FX
            type = 5;
        }
        if(type == 5 && lb != ub){ //if lb != ub then row type is changed to GLP_DB
            type = 4;
        }
        glp_set_row_bnds(lp,row_index,type,lb,ub); //update auxiliary lpvariable with new calculated bounds
    }

    ///Here we update the bounds of each structural variable
    for(int i = nrow; i<ntot; i++){ //loop over all structural lpvariables
        double lb = return_lower_bound(i,current_t,yval), ub = return_upper_bound(i,current_t,yval); //get lb,ub using current yval
        int col_index = i-nrow+1; //get column index
        double diff = ub - lb;
        int type = glp_get_col_type(lp,col_index); //get column type
        if(type == 4 && lb == ub){ //if lb = ub then column type is changed to GLP_FX
            type = 5;
        }
        if(type == 5 && lb != ub){ //if lb != ub then column type is changed to GLP_DB
            type = 4;
        }
        glp_set_col_bnds(lp,col_index,type,lb,ub); //update structural lpvariable with new calculated bounds
    }
}

/*
 * Return upper bound for lpvariable with provided index
 */

double EMBLP_MODEL::return_upper_bound(int i, realtype tval, realtype *yval)
{
    if(ex_stat[i]){ //if an exchange lpvariable
        return ex_bound(i,tval,yval,1); //calculate and return variable upper bound of exchange lpvariable
    }
    else{ //if not an exchange lpvariable
        if(i>=nrow){ //if structural variable
            return glp_get_col_ub(lp,i+1-nrow); //return fixed upper bound of structural lpvariable
        }
        else{ //if auxiliary variable
            return glp_get_row_ub(lp,i+1); //return fixed upper bound of auxiliary lpvariable
        }
    }
    return 0.0;
}

/*
 * Return lower bound for lpvariable with provided index
 */

double EMBLP_MODEL::return_lower_bound(int i, realtype tval, realtype *yval)
{
    if(ex_stat[i]){ //if an exchange lpvariable
        return ex_bound(i,tval,yval,0); //calculate and return variable lower bound of exchange lpvariable
    }
    else{ //if not an exchange lpvariable
        if(i>=nrow){ //if structural variable
            return glp_get_col_lb(lp,i+1-nrow); //return fixed lower bound of structural lpvariable
        }
        else{ //if auxiliary variable
            return glp_get_row_lb(lp,i+1); //return fixed lower bound of auxiliary lpvariable
        }
    }
    return 0.0;
}

/*
 * Return bound for exchange lpvariable with provided index
 */

double EMBLP_MODEL::ex_bound(int i, realtype tval, realtype *yval, bool boundtype)
{
    double bound = 0.0;
    if(boundtype){ //upper bound for exchange structural lpvariable using user-supplied function pointer
        bound = exchange_upper_bounds(i,tval,yval,section);
    }
    else{ //lower bound for exchange structural lpvariable using user-supplied function pointer
        bound = exchange_lower_bounds(i,tval,yval,section);
    }
    return bound;
}

/*
 * Perform LP iteration and print results
 */

int EMBLP_MODEL::optimize()
{
    ///Here we blank previous objective and reset if multiple objectives supplied for lexicographic optimization
    if(nobj > 0){
        for(int index=1; index<=ncol; index++){ //loop over all structural variables
            glp_set_obj_coef(lp,index,0.0); //set all objective coefficients to zero
        }
        set_objective(0); //set initial objective
    }

    ///Here we solve intial LP and check primal solution exists
    int solver = glp_simplex(lp,&parm); //optimization using dual simplex method
    if(solver != 0){ //if simplex method irregular
        return solver;
    }
    int primal = glp_get_prim_stat(lp); //get primal status
    if(primal != 2){ //if other than feasible
        std::cout << "Basis not feasible with primal status " << primal << std::endl;
        return 1;
    }
    int obj_constraint = 0; //objective to be used as possible constraint

    ///Solve projected LPs using simplex method
    for(int obj=1; obj<nobj; obj++){
        int j = red_costs(); //calculate max reduced cost of non-basic variables

        ///Here we re-optimize to obtain alternative solution if not unique
        if(j>-1){ //if solution not unique
            if(j>0){ //if constraint not redundant
                add_constraint(obj_constraint,j); //add constraint to LP
            }
            set_objective(obj); //set new objective

            ///Here we solve new LP and check primal solution exists
            int sub_solver = glp_simplex(lp,&parm); //optimization using dual simplex method
            if(sub_solver != 0){ //if simplex method irregular
                return sub_solver;
            }
            int sub_primal = glp_get_prim_stat(lp); //get primal status
            if(sub_primal != 2){ //if other than feasible
                std::cout << "Basis not feasible with primal status " << sub_primal << std::endl;
                return 1;
            }
            obj_constraint = obj; //objective to be used as possible constraint
        }
    }
    return 0;
}

/*
 * Evaluate reduced costs of LP
 * returns: index of lp variable with max reduced cost, -1 if solution unique, 0 if all zero
 */

int EMBLP_MODEL::red_costs()
{
    int red_cost = -1; //init return value
    double max_cost = 0.0; //keep track of max reduced cost
    int zeros = 0; //keep track of zeros
    int counter = 0; //keep track of non-basic lpvariables at lower or upper bounds
    for(int index=1; index<=ntot; index++){ //loop over all lpvariables
        int status = 0; //basis status for ith lpvariable
        double cost = 0.0; //cost for ith lpvariable
        if(index<=nrow){ //if auxiliary
            status = glp_get_row_stat(lp,index); //get basic status of row
            cost = glp_get_row_dual(lp,index); //get cost of row
        }
        else{ //if structural
            int col_index = index-nrow;
            status = glp_get_col_stat(lp,col_index); //get basic status of column
            cost = glp_get_col_dual(lp,col_index); //get cost of column
        }
        if(status == 2 || status == 3){ //active lower or upper bound and not fixed type
            counter++; //increment non-basic counter
            if(-1e-6 < cost && cost < 1e-6){ //if reduce cost zero (with tolerance 1e-6)
                zeros++; //increment number of zeros
            }
            else if(cost*cost > max_cost*max_cost){ //else if larger than current max cost
                max_cost = cost; //update max cost
                red_cost = index; //update index of max reduced cost
            }
        }
    }
    if(zeros == 0){ //if no reduced costs are zero
        red_cost = -1; //set return value to unique
    }
    else if(zeros == counter){ //if all reduce costs are zero
        red_cost = 0; //set return value to redundant constraint
    }
    return red_cost;
}

/*
 * Remove previous constraints from LP
 */

void EMBLP_MODEL::remove_constraints()
{
    for(int con=nrow-nobj+2; con<=nrow; con++){ //loop over objectives
        std::cout << "Freeing constraint " << con << " corresponding to objective " << con - nrow + nobj - 2 << std::endl;
        glp_set_row_bnds(lp,con,GLP_FR,-DBL_MAX,DBL_MAX); //free constraint
        if(con == nrow){
            glp_adv_basis(lp,0); //construct advanced basis
        }
    }
}

/*
 * Set objective for next LP iteration
 */

void EMBLP_MODEL::set_objective(int obj)
{
    if(obj>0){ //if not first objective
        std::cout << "Zeroing previous objective" << std::endl;
        for(int i=0; i<obj_inds[obj-1].size(); i++){ //loop over non-zero coefficients of previous objective
            glp_set_obj_coef(lp,obj_inds[obj-1][i],0.0); //set coefficients to zero
        }
    }
    std::cout << "Setting objective " << obj << ": ";
    std::vector<int> inds = obj_inds[obj]; //get indices of non-zero coefficients
    std::vector<double> coefs = obj_coefs[obj]; //get values of non-zero coefficients
    for(int i=0; i<inds.size(); i++){ //loop over non-zero coefficients of current objective
        std::cout << " column " << inds[i] << " coefficient " << coefs[i];
        glp_set_obj_coef(lp,inds[i],coefs[i]); //set coefficient
    }
    std::cout << " direction " << obj_dirs[obj] << std::endl;
    glp_set_obj_dir(lp,obj_dirs[obj]); //set direction of current objective
}

/*
 * Add objective as additional constraint in LP
 */

void EMBLP_MODEL::add_constraint(int obj, int j)
{
    double obj_val = glp_get_obj_val(lp); //get previous objective value
    int cons = obj + nrow - nobj + 2;
    std::cout << "Adding objective " << obj << " as constraint " << cons  << " with value " << obj_val << std::endl;
    glp_set_row_bnds(lp,cons,GLP_FX,obj_val,obj_val); //change bounds to fixed on objective value
    glp_set_row_stat(lp,cons,GLP_NF); //change status to non-basic
    if(j<=nrow){ //if j auxiliary
        glp_set_row_stat(lp,j,GLP_BS); //set status to basic
    }
    else{ //if j structural
        glp_set_col_stat(lp,j-nrow,GLP_BS); //set status to basic
    }
}

/*
 * Return model data
 */

int EMBLP_MODEL::get_nkin(){ return nkin; }
int EMBLP_MODEL::get_nrow(){ return nrow; }
int EMBLP_MODEL::get_ncol(){ return ncol; }
int EMBLP_MODEL::get_nexc(){ return nexc; }
int EMBLP_MODEL::get_ntot(){ return ntot; }
int EMBLP_MODEL::get_neq(){ return neq; }
int EMBLP_MODEL::get_nrts(){ return nrts; }
int EMBLP_MODEL::get_nobj(){ return nobj; }
realtype EMBLP_MODEL::get_tstop(){ return tstop; }
realtype EMBLP_MODEL::get_tout(){ return tout; }

realtype EMBLP_MODEL::current_tval()
{
    return current_t;
}

N_Vector EMBLP_MODEL::current_yval()
{
    return current_y;
}

N_Vector EMBLP_MODEL::current_ypval()
{
    return current_yp;
}

std::vector<double> EMBLP_MODEL::current_lpvariables()
{
    return current_lpvars;
}

std::vector<double> EMBLP_MODEL::change_points()
{
    return change_pnts;
}

int EMBLP_MODEL::get_section()
{
    return section;
}

void  EMBLP_MODEL::set_section(int flag)
{
    section = flag;
}

/*
 * Clear model memory
 */

void EMBLP_MODEL::clear()
{
    N_VDestroy(current_y);
    N_VDestroy(current_yp);
    glp_delete_prob(lp);
    dlclose(handle);
}

/*
 * Print results of LP solver
 */

void EMBLP_MODEL::print_lpresults()
{
    double z = glp_get_obj_val(lp);
    std:: cout << "Soultion value = " << z << std::endl;
    std::cout << "Values = [";
    for(int i=1; i<=ncol; i++){
        double x = glp_get_col_prim(lp, i);
        if(i < ncol){
            std::cout << x << ", ";
        }
        else{
            std::cout << x << "]" << std::endl;
        }
    }
    std::cout << "Auxiliaries = [";
    for(int i=1; i<=nrow; i++){
        double x = glp_get_row_prim(lp, i);
        if(i < nrow){
            std::cout << x << ", ";
        }
        else{
            std::cout << x << "]" << std::endl;
        }
    }
    std::cout << "Basis indices (structural) = [";
    for(int i=1; i<=ncol; i++){
        int x = glp_get_col_bind(lp, i);
        if(i < ncol){
            std::cout << x << ", ";
        }
        else{
            std::cout << x << "]" << std::endl;
        }
    }
    std::cout << "Basis indices (auxiliaries) = [";
    for(int i=1; i<=nrow; i++){
        int x = glp_get_row_bind(lp, i);
        if(i < nrow){
            std::cout << x << ", ";
        }
        else{
            std::cout << x << "]" << std::endl;
        }
    }
    std::cout << "Basis status (structural) = [";
    for(int i=1; i<=ncol; i++){
        int x = glp_get_col_stat(lp, i);
        if(i < ncol){
            std::cout << x << ", ";
        }
        else{
            std::cout << x << "]" << std::endl;
        }
    }
    std::cout << "Basis status (auxiliaries) = [";
    for(int i=1; i<=nrow; i++){
        int x = glp_get_row_stat(lp, i);
        if(i < nrow){
            std::cout << x << ", ";
        }
        else{
            std::cout << x << "]" << std::endl;
        }
    }
}
