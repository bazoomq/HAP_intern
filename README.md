# Natural Shape Balloon

This code calculates the shape of natural shape balloon for heights from 15000 to 25000m (one calculation for each 500m). The solution is based on differential equations derived from physics laws, which derivation can be found in:
[Baginski, F. On the Design and Analysis of Inflated Membranes: Natural and Pumpkin shaped balloons,] \
[P H Wen, G E Dorrington Simple method to predict balloon shape] \

### Differential equations
$\theta'(s) = {-2 \pi(r_p w_p \sin\theta + p r) \over T}$ \
$T'(s) = 2 \pi r_p w_p \cos\theta$ \
$z'(s) = \cos\theta$ \
$r'(s) = \sin\theta$ 

Besides the equations above balloon should have $a \ and initial $theta_0 \ chosen such that after solving the differential equations the last $theta \ will be $ -pi/2 \ and $ r = 0 \.
