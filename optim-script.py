# Import libraries

import pulp as p
import plotly.graph_objects as go

#-------------------------------OPTIMISATION------------------------------------

# Establish a minimisation problem environment

hosp_prob = p.LpProblem('Problem', p.LpMinimize)

# Define problem variables
# In the hospital context, these will represent staffing areas of the hospital
# Minimums are defined by government for each and happen to be 5000 units

the_lowBound = 5000

x = p.LpVariable("x", lowBound = the_lowBound) # Medical staff units variable
y = p.LpVariable("y", lowBound = the_lowBound) # Nursing staff units variable
z = p.LpVariable("z", lowBound = the_lowBound) # Admin staff units variable
a = p.LpVariable("a", lowBound = the_lowBound) # Cleaning staff units variable

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

#-------------------------------VISUALISATION-----------------------------------

fig = go.Figure(go.Waterfall(
    name = "20", orientation = "v",
    measure = ['relative', 'relative', 'relative', 'relative', 'total'],
    x = ['Medical Staff', 'Nursing Staff', 'Admin Staff', 'Cleaning Staff', 'Total Cost'],
    textposition = "outside",
    text = [(p.value(x)*med_cost), (p.value(y)*nurs_cost),
    (p.value(z)*admin_cost), (p.value(a)*clean_cost),
    p.value(hosp_prob.objective)],
    y = [(p.value(x)*med_cost), (p.value(y)*nurs_cost),
    (p.value(z)*admin_cost), (p.value(a)*clean_cost),
    p.value(hosp_prob.objective)],
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))

fig.update_layout(
        title = "Optimised hospital staffing expenditure",
        showlegend = False
)

fig.show()
