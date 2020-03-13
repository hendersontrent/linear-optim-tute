# Import library required for linear programming

import pulp as p

# Establish a minimisation problem environment

hosp_prob = p.LpProblem('Problem', p.LpMinimize)

# Define problem variables
# In the hospital context, these will represent staffing areas of the hospital
# Minimums are defined by government for each and happen to be 5000 units

the_lowBound = 5000

x = p.LpVariable("x", lowBound = the_lowBound) # Create a variable x >= 5000 to represent medical staff units
y = p.LpVariable("y", lowBound = the_lowBound) # Create a variable y >= 5000 to represent nursing staff units
z = p.LpVariable("z", lowBound = the_lowBound) # Create a variable z >= 5000 to represent admin staff units
a = p.LpVariable("a", lowBound = the_lowBound) # Create a variable a >= 5000 to represent cleaning staff units

# Define cost per unit for each staffing area
# These are set up as named variables so we can enact changes here and flow them through

med_cost = 6175
nurs_cost = 3980
admin_cost = 2935
clean_cost = 2060

# Define Objective Function that governs the problem we are trying to solve

hosp_prob += x*med_cost + y*nurs_cost + z*admin_cost + a*clean_cost

# Define constraints which bound the optimisation solution
# Hypothetical minimum staffing units set by government is 50000

hosp_prob += 2*z + 2*a <= x
hosp_prob += x*1.5 <= y
hosp_prob += 2*z <= a
hosp_prob += x + y + z + a >= 50000

# Display the problem on-screen

print(hosp_prob)

# Display solver and status on-screen

status = hosp_prob.solve()
print(p.LpStatus[status])

# Print the optimisation solution in terms of overall minimised cost output
# as well as the optimised number of units per staffing area

print(p.value(x), p.value(y), p.value(z), p.value(a),
p.value(hosp_prob.objective))
