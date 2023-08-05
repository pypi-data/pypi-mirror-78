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
 *-----------------
 * UserData struct.
 *-----------------
 */

struct UserData{

    void set_name(std::string text){
        name = text;
    }

    void set_kinetic_dimensions(int nkin, int nexc, int nreq){
        kinetic_dimensions[0] = nkin;
        kinetic_dimensions[1] = nexc;
        kinetic_dimensions[2] = nreq;
        initial_conditions = std::vector<double>(nkin+1);
        exchange_indices = std::vector<int>(nexc);
        required_indices = std::vector<int>(nreq);
    }

    void set_output_times(double tstop, double tout){
        output_times[0] = tstop;
        output_times[1] = tout;
    }

    void set_initial_conditions(std::vector<double> init_cond){
        int n = init_cond.size();
        if(n != kinetic_dimensions[0]+1){
            std::cout << "Initial conditions of wrong length (" << n << " when expected " << kinetic_dimensions[0]+1 << ")!" << std::endl;
            return;
        }
        for(int i=0; i<(kinetic_dimensions[0]+1); i++){
            initial_conditions[i] = init_cond[i];
        }
    }

    void set_exchange_indices(std::vector<int> exc_idx){
        int n = exc_idx.size();
        if(n != kinetic_dimensions[1]){
            std::cout << "Exchange indices of wrong length (" << n << " when expected " << kinetic_dimensions[1] << ")!" << std::endl;
            return;
        }
        for(int i=0; i<kinetic_dimensions[1]; i++){
            exchange_indices[i] = exc_idx[i];
        }
    }

    void set_required_indices(std::vector<int> req_idx){
        int n = req_idx.size();
        if(n != kinetic_dimensions[2]){
            std::cout << "Required indices of wrong length (" << n << " when expected " << kinetic_dimensions[2] << ")!" << std::endl;
            return;
        }
        for(int i=0; i<kinetic_dimensions[2]; i++){
            required_indices[i] = req_idx[i];
        }
    }

    void set_current_indices(std::vector<int> cur_idx){
        current_indices = cur_idx;
    }

    void add_objective(std::vector<int> obj_inds, std::vector<double> obj_coefs){
        int length = obj_inds.size();
        int n = obj_coefs.size();
        if(length != n){
            std::cout << "Lengths of objective indices and coefficients do not match! (" << length << " vs " << n <<  ", respectively)" << std::endl;
            return;
        }
        std::vector<int> indices(length);
        std::vector<double> coefficients(length);
        for(int i=0; i<length; i++){
            indices[i] = obj_inds[i] + 1;
            coefficients[i] = obj_coefs[i];
        }
        obj_indices.push_back(indices);
        obj_coefficients.push_back(coefficients);
    }

    void set_directions(std::vector<std::string> directions){
        int nobj = obj_indices.size();
        int n = directions.size();
        if(n != nobj){
            std::cout << "Objective directions of wrong length (" << n << " when expected " << nobj << ")!" << std::endl;
            return;
        }
        for(int i=0; i<nobj; i++){
            std::string dir = directions[i];
            if(dir == "max"){
                obj_directions.push_back(2);
            }
            else if(dir == "min"){
                obj_directions.push_back(1);
            }
            else{
                std::cout << "Direction " << dir << " unexpected!" << std::endl;
                return;
            }
        }
    }

    void set_change_points(std::vector<double> change_pnts){
        for(int i=0; i<change_pnts.size(); i++){
            change_points.push_back(change_pnts[i]);
        }
    }

    std::string name;
    std::vector<int> kinetic_dimensions = std::vector<int>(3,0);
    std::vector<double> output_times = std::vector<double>(2);
    std::vector<double> initial_conditions;
    std::vector<int> exchange_indices;
    std::vector<int> required_indices;
    std::vector<int> current_indices;
    std::vector< std::vector<int> > obj_indices;
    std::vector< std::vector<double> > obj_coefficients;
    std::vector<int> obj_directions;
    std::vector<double> change_points;
};
