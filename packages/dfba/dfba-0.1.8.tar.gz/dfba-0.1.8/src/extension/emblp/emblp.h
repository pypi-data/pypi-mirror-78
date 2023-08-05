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

#include "../user_data.h"

#include <dlfcn.h>
#include <glpk.h>
#include <nvector/nvector_serial.h>    //access to serial N_Vector
#include <sundials/sundials_types.h>   //defs of realtype, sunindextype

///Macro for N vector elements
#define Ith(v,i)    NV_Ith_S(v,i)

///Typedefs for user-supplied function pointers
typedef double (*ExchangeBound)(int, realtype, realtype *, int);
typedef void (*OdeExpression)(realtype, realtype *, realtype *, realtype *, std::vector<double>, int); //TODO: change once implemented in python

class EMBLP_MODEL
{
protected:
    ///Model data
    ///----------
    int nkin, nrow, ncol, nexc, nreq, ntot, neq, nrts, nobj; //int data
    std::vector<int> obj_dirs; //objective directions (1 = GLP_MIN, 2 = GLP_MAX)
    std::vector< std::vector<int> > obj_inds; //column indices of non-zero objective coefficients
    std::vector< std::vector<double> > obj_coefs; //values of non-zero objective coefficients
    realtype tstop, tout; //realtypes data
    glp_prob *lp; //pointer to current formulation of LP problem
    glp_smcp parm; //parameters of LP problem
    std::vector<bool> ex_stat; //exchange status of structural lpvariables
    std::vector<int> ex_ind, req_ind, cur_ind; //indices of exchange, required, and current lpvariables
    ExchangeBound exchange_upper_bounds, exchange_lower_bounds; //user-supplied function pointers for exchange bounds
    OdeExpression kinetic_expression; //user-supplied function pointer for rhs of ode
    realtype current_t; //current time
    N_Vector current_y, current_yp; //current y,y' kinetics
    std::vector<double> current_lpvars; //current values of lpvariables desired by user
    std::vector<double> change_pnts; //list of change points for any control parameters in model
    int section; //flag for keeping track of current section between change points
    void *handle; //handle for keeping status of functionlib shared library

public:
    ///Member functions for model
    ///--------------------------
    ///Constructor
    EMBLP_MODEL(glp_prob *, glp_smcp, UserData, std::string);
    ///Updating model data
    void set_data(UserData), update_bounds(), set_section(int);
    ///Return bounds
    double return_upper_bound(int, realtype, realtype *), return_lower_bound(int, realtype, realtype *), ex_bound(int, realtype, realtype *, bool);
    ///Optimize
    int optimize();
    void remove_constraints(), set_objective(int), add_constraint(int, int);
    int red_costs();
    ///Return model data
    int get_nkin(), get_nrow(), get_ncol(), get_nexc(), get_ntot(), get_neq(), get_nrts(), get_nobj();
    realtype get_tstop(), get_tout();
    realtype current_tval();
    N_Vector current_yval(), current_ypval();
    std::vector<double> current_lpvariables();
    std::vector<double> change_points();
    int get_section();
    ///Virtual templates for CVODE and IDA
    virtual int initialize(){ return 1; };
    virtual void rhs(realtype, realtype *, realtype *){};
    virtual void drhs(realtype, realtype *, realtype *, realtype *){};
    virtual void event(realtype, realtype *, realtype *){};
    ///Clear model memory (N_Vectors and LP problem)
    void clear();
    ///Display
    void print_lpresults();
};

class EMBLP_DIRECT : public EMBLP_MODEL
{
private:
    ///Data for direct method
    ///----------------------
    realtype *ypval; //pointer to zero vector current_yp
    std::vector<double> required_lpvariables; //values of required lpvariables

public:
    ///Member functions for direct method
    ///----------------------------------
    ///Constructor
    EMBLP_DIRECT(glp_prob *, glp_smcp, UserData, std::string);
    ///Updating model data
    void update_kinetics(realtype, N_Vector), starting_values(realtype &, realtype *);
    ///Algorithm
    int initialize();
    double get_lpvariable(int);
    ///CVODE
    void rhs(realtype, realtype *, realtype *);

};

class EMBLP_HARWOOD : public EMBLP_MODEL
{
private:
    ///Data for Harwood et al.
    ///-----------------------
    std::vector<int> basic_ind; //stores lpindices of basis
    std::vector<int> basic_stat; //lpvariable basic status (-1 = non-basic)
    std::vector<double> basic_const; //current constant portion of basic lpvariables
    std::vector< std::vector<double> > simplex_tableau; //current remaining portion of simplex tableau

public:
    ///Member functions for Harwood et al.
    ///-----------------------------------
    ///Constructor
    EMBLP_HARWOOD(glp_prob *, glp_smcp, UserData, std::string);
    ///Updating model data
    void update_kinetics(realtype, N_Vector, N_Vector), starting_values(realtype &, realtype *, realtype *);
    ///Algorithm
    int initialize();
    void calculate_tableau();
    double get_lpvariable(int, realtype, realtype *);
    ///IDA
    void drhs(realtype, realtype *, realtype *, realtype *), event(realtype, realtype *, realtype *);
};

class EMBLP_SCOTT : public EMBLP_MODEL
{
public:
    ///Member functions for Scott et al.
    ///---------------------------------
    ///Constructor
    EMBLP_SCOTT(glp_prob *, glp_smcp, UserData, std::string);
    ///Algorithm
    int initialize();
    ///IDA
    void drhs(realtype, realtype *, realtype *, realtype *);
};
