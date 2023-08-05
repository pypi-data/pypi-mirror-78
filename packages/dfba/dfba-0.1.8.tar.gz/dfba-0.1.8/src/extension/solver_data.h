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

#include <vector>
#include <iostream>

/*
 *-------------------
 * SolverData struct.
 *-------------------
 */

struct SolverData{

    void set_rel_tolerance(double rel_tol){
        if(rel_tol > 0.0){
            rel_tolerance = rel_tol;
            std::cout << "rel_tolerance set to " << rel_tol << std::endl;
        }
        else{
            std::cout << "rel_tolerance must be positive!" << std::endl;
        }
    }

    void set_abs_tolerance(std::vector<double> abs_tol){
        int n = abs_tol.size();
        std::vector<double> tmp_abs_tolerance(n,1.0e-4);
        for(unsigned int i=0; i<n; i++){
            double abs_tol_val = abs_tol[i];
            if(abs_tol_val > 0.0){
                tmp_abs_tolerance[i] = abs_tol_val;
            }
            else{
                std::cout << "abs_tolerance components must be positive!" << std::endl;
                return;
            }
        }
        abs_tolerance = tmp_abs_tolerance;
        std::cout << "abs_tolerance set to [";
        for(unsigned int i=0; i<n; i++){
            std::cout << abs_tolerance[i];
            if(i != n-1){
                std::cout << ", ";
            }
        }
        std::cout << "]" << std::endl;
    }

    void set_sunmatrix(std::string sunmat){
        if(sunmat == "dense" || sunmat == "sparse"){
            sunmatrix = sunmat;
            std::cout << "sunmatrix set to " << sunmat << std::endl;
        }
        else{
            std::cout << "sumatrix must be set to 'dense' or 'sparse'!" << std::endl;
        }
    }

    void set_sunlinsolver(std::string sunlin){
        if(sunlin == "dense"){
            sunlinsolver = sunlin;
            std::cout << "sunlinsolver set to " << sunlin << std::endl;
        }
        else{
            std::cout << "sunlinsolver must be set to 'dense'!" << std::endl;
        }
    }

    void set_ode_method(std::string method){
        if(method == "BDF" || method == "ADAMS"){
            ode_method = method;
            std::cout << "ode method set to " << method << std::endl;
        }
        else{
            std::cout << "ode method must be set to 'BDF' or 'ADAMS'!" << std::endl;
        }
    }

    void set_algorithm(std::string alg){
        if(alg == "direct" || alg == "Harwood"){
            algorithm = alg;
            std::cout << "algorithm set to " << alg << std::endl;
        }
        else{
            std::cout << "algorithm must be set to 'direct' or 'Harwood'!" << std::endl;
        }
    }

    void set_display(std::string disp){
        if(disp == "full" || disp == "glpk_only" || disp == "sundials_only" || disp == "none"){
            display = disp;
            std::cout << "display set to " << disp << std::endl;
        }
        else{
            std::cout << "display must be set to 'full', 'glpk_only', 'sundials_only', or 'none'!" << std::endl;
        }
    }

    ///Default values
    double rel_tolerance = 1.0e-4;
    std::vector<double> abs_tolerance = std::vector<double>(1,1.0e-4);
    std::string sunmatrix = "dense";
    std::string sunlinsolver = "dense";
    std::string ode_method = "ADAMS";
    std::string algorithm = "Harwood";
    std::string display = "full";
};
