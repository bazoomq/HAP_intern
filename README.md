# Natural Shape Balloon 

This code provides the shape of a balloon depending on the height (from 15000 to 25000 meters) and set of design parameters. 

### Overview
The basis of this method is the numerical solution of a system of differential equations. The Solve(params) function solves a system of 4 differential equations describing the shape of a balloon depending on the height and parameters $\theta_0$ and $a$.

$\theta'(s) = {-2 \pi(r_p w_p \sin\theta + p r) \over T}$ \
$T'(s) = 2 \pi r_p w_p \cos\theta$ \
$z'(s) = \cos\theta$ \
$r'(s) = \sin\theta$ 

More about this system of differential equations you can find in these papers:

[Baginski, F., Winker, J. The natural shape balloon and related models](https://doi.org/10.1016/j.asr.2003.10.030) \
[Baginski, F., On the Design and Analysis of Inflated Membranes: Natural and Pumpkin Shaped Balloons](https://www.jstor.org/stable/4096199)  

To find the optimal parameters theta and a, we use Grid Search method: set up a grid for both parameters with a fixed step and lounch Solve(params) function for which one. We only consider results for which $\theta_l$ is around -90 degrees and $r_l$ is around 0. Compare the results using a loss function: $loss = \sqrt{({\pi/2 + \theta_l \over \pi/2}) ^2 + r_l ^2}$. For more accurate result, another grid is created around the found approximate result and the process is repeated. We called this algorithm Recursive Grid Search.

To speed up calculations, we use multiprocessing.

### Files 
* `params.py`: setting parameters
* `calculate_rp.py`: calculate rp(s) function - pumpkin shape balloon radius depends on s
* `density.py`: calculate atmosphere and gas density depends on height (h)
* `solve.py`: the whole process to calculate the shape of balloon
* `main.py`: create grid and run the Recursive Grid Search algorithm

### Recursive Grid Search

At first, the grid looks like: from 0 to 90 for $\theta_0$ and from 0 to 16 if $h < 21850$ or from -400 to 0 if $h > 21850$ for $a$. Number of steps per axis $\theta_0$ is 900, per axis $a$ is 64. 

Applying the grid search once, we got the approximate solution $(\theta_{0, 1}, a_1)$. We create a grid around this solution (with the same number of steps) and apply the algorithm again. Thus, we obtain a more accurate solution.

### Multiprocessing
The code uses multiprocessing to speed up calculations. For multiprocessing we use method `ProcessPoolExecutor` from the library `concurrent`. With this method, the function is run on multiple cores and calculations are performed in parallel at the appropriate number of grid points.

### Run the code
To run the code, you need to set the height h (currently in the file `params.py`) and run the `main` function from `main.py` file.

### Output
At the output we get the parameters $\theta_0$ and a; arrays of z and r values that define the shape of the balloon. In addition, the maximum value of r, the last value of r and $\theta$, the value of the loss function, list of $z, r, \theta$ and the volume of the balloon $V$, as well as a plot of r versus z (balloon shape) are displayed for the future analysis and comparison. 
