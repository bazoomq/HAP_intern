# Natural Shape Balloon

This code calculates the shape of natural shape balloon for heights from 15000 to 25000m (one calculation for each 500m). The solution is based on differential equations derived from physics laws, which derivation can be found in:

[Baginski, F. On the Design and Analysis of Inflated Membranes: Natural and Pumpkin shaped balloons,](https://www.jstor.org/stable/4096199)\
[P H Wen, G E Dorrington Simple method to predict balloon shape](https://sci-hub.se/10.1243/09544100JAERO690)

### Differential equations
$\theta'(s) = {-2 \pi(r_p w_p \sin\theta + p r) \over T}$ \
$T'(s) = 2 \pi r_p w_p \cos\theta$ \
$z'(s) = \cos\theta$ \
$r'(s) = \sin\theta$ 

Besides the equations above balloon should have $a$ and initial $\theta_0$ chosen such that after solving the differential equations the last $\theta$ will be $-pi/2$ and $r = 0$.

Fo find a solution to the differential equations and combine the two given conditions we have defined a function F, which reaches its minimum exactly at a point where the conditions take place. The more clear explanation can be found in the second article provided above.

We have used gradient descent algorithm (fmin_cg in python) to find the minimum point. At first we have found a reasonable initial guess from where the algorithm can work for the height 25000. After finding the solution for any height we use its values of $a$ and $\theta_0$ as an initial guess for the next height.

### Files
The project consists of several parts:\
  constants.py - Keeps all the constants used in project\
  bouyancy.py - calculates the buoyancy at any height $h$\
  interp_s0.py - does an interpolation from r to s\
  optimization.py - gradient algorithm realization\
  natural_shape_balloon.py - Class for a natural shape balloon is created\
  main.py\

### Output
Output of program is saved on a file called theta_a.csv which contains information about $\theta_0$, $a$, $V$ - volume of balloon etc. The file is created (if not created) or modified in the same directory where the program is.
  
