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

#include <time.h>
#include "methods/methods.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

/*
 *----------------------------------------------
 * Functions for processing objects from Python.
 *----------------------------------------------
 */

/*
 * SWIGwrapper for glp_prob * (see https://wiki.python.org/moin/boost.python/HowTo#SWIG_exposed_C.2B-.2B-_object_from_Python ).
 */

struct PySwigprobObject{
    PyObject_HEAD
    glp_prob *ptr;
    const char *desc;
};

/*
 *-----------------------------------
 * Functions to be exposed to Python.
 *-----------------------------------
 */

/*
 * Simulate individual dfba model.
 */

std::vector< std::vector<double> > simulate_dfba_model(py::object dfba_model, std::string functionlib)
{
    ///PYTHON INTERFACE TO GET MODEL
    ////////////////////////////////
    std::vector< std::vector<double> > results; //create results array
    
    ///Here we get SWIGLPK wrapped glp_prob * attribute of model, rationale: ((PySwigprobObject*) PyObject* )->ptr
    glp_prob *lp = ((PySwigprobObject*) dfba_model.attr("lp_problem")().ptr() )->ptr;
    glp_smcp parm; //TODO: obtain copy of LP configuration from Python

    ///Here we extract copy of wrapped UserData and SolverData attributes
    UserData user_data = dfba_model.attr("user_data").cast<UserData>(); //cast UserData attribute
    SolverData solver_data = dfba_model.attr("solver_data").cast<SolverData>(); //cast SolverData attribute

    ///Here we confirm sunmatrix and sunlinearsolve combination supported
    if(solver_data.sunlinsolver != "dense"){
        std::cout << "SUNMatrix and SUNLinearSolver combination not supported! See SUNDIALS documentation for details." << std::endl;
        return results;
    }

    ///Here hide glpk display if requested
    glp_init_smcp(&parm);
    if(!(solver_data.display == "full" || solver_data.display == "glpk_only")){
        parm.msg_lev = GLP_MSG_OFF;
    }

    ///CREATE MODEL AND RUN SIMULATION
    //////////////////////////////////
    clock_t t1, t2; //time tracking
    t1 = clock(); //set start time
    if(solver_data.algorithm == "Harwood"){
        EMBLP_HARWOOD model(lp,parm,user_data, functionlib); //init emblp Harwood model from pointer to LP problem in Python and user data
        PrintOutput(model,results); //store initial conditions to file
        integrateHarwood(model,results,solver_data); //run simulation on model
        model.clear(); //clear model memory
    }
    else if(solver_data.algorithm == "direct"){
        EMBLP_DIRECT model(lp,parm,user_data, functionlib); //init emblp direct model from pointer to LP problem in Python and user data
        PrintOutput(model,results); //store initial conditions to file
        integrateDirect(model,results,solver_data); //run simulation on model
        model.clear(); //clear model memory
    }
    else{
        std::cout << "Algorithm currently not supported!" << std::endl;
        return results;
    }
    t2 = clock(); //set end time
    std::cout << std::endl << "Total simulation time was " << ((float)t2-(float)t1)/CLOCKS_PER_SEC << " seconds" << std::endl << std::endl;
    return results;
}

/*
 *----------------
 * Python wrapper.
 *----------------
 */

PYBIND11_MODULE(dfba_utils, m)
{
    m.doc() = "pybind11 wrap dfba_utils module";
    
    ///Here we expose simulate dfba model method
    m.def("simulate_dfba_model", simulate_dfba_model);

    ///Here we expose UserData
    py::class_<UserData>(m,"UserData")
        .def(py::init<>())
        .def("set_name", &UserData::set_name)
        .def("set_kinetic_dimensions", &UserData::set_kinetic_dimensions)
        .def("set_output_times", &UserData::set_output_times)
        .def("set_initial_conditions", &UserData::set_initial_conditions)
        .def("set_exchange_indices", &UserData::set_exchange_indices)
        .def("set_required_indices", &UserData::set_required_indices)
        .def("set_current_indices", &UserData::set_current_indices)
        .def("add_objective", &UserData::add_objective)
        .def("set_directions", &UserData::set_directions)
        .def("set_change_points", &UserData::set_change_points)
        ;

    ///Here we expose SolverData
    py::class_<SolverData>(m,"SolverData")
        .def(py::init<>())
        .def("set_rel_tolerance", &SolverData::set_rel_tolerance)
        .def("set_abs_tolerance", &SolverData::set_abs_tolerance)
        .def("set_sunmatrix", &SolverData::set_sunmatrix)
        .def("set_sunlinsolver", &SolverData::set_sunlinsolver)
        .def("set_ode_method", &SolverData::set_ode_method)
        .def("set_algorithm", &SolverData::set_algorithm)
        .def("set_display", &SolverData::set_display)
        ;
}

