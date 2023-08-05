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
 * EMBLP_SCOTT member functions.
 *------------------------------
 */

EMBLP_SCOTT::EMBLP_SCOTT(glp_prob *lp_in, glp_smcp parm_in, UserData user_data, std::string functionlib) : EMBLP_MODEL(lp_in, parm_in, user_data, functionlib)
{
    current_y = N_VNew_Serial(neq), current_yp = N_VNew_Serial(neq);
}

int EMBLP_SCOTT::initialize()
{
    int solver = optimize(); //call optimize
    if(solver != 0){ //if optimize not succesful
        return solver; //return unsuccesful optimize
    }
    return 0;
}

/*
 * Calculate DAE right-hand side
 */

void EMBLP_SCOTT::drhs(realtype tval, realtype *yval, realtype *ypval, realtype *rval)
{

}
