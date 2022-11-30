# Natural Shape Balloon 

This code provides the shape of a balloon depending on the altitude (from 15000 to 25000 meters) and set of design parameters.   

### Overview
The basis of this method is the numerical solution of a system of differential equations. The Solve(params) function from `solve.py` solves a system of 4 differential equations describing the shape of a balloon depending on the height and parameters $\theta_0$ and $a$.

$\theta'(s) = {-2 \pi(r_p w_p \sin\theta + p r) \over T}$ \
$T'(s) = 2 \pi r_p w_p \cos\theta$ \
$z'(s) = \cos\theta$ \
$r'(s) = \sin\theta$ 

More about this system of differential equations you can find in these papers:

[Baginski, F., Winker, J. The natural shape balloon and related models](https://doi.org/10.1016/j.asr.2003.10.030) \
[Baginski, F., On the Design and Analysis of Inflated Membranes: Natural and Pumpkin Shaped Balloons](https://www.jstor.org/stable/4096199)  

To find the optimal parameters theta_0 and a, we use Grid Search method: set up a grid for both parameters with a fixed step and lounch Solve(params) function for which one. We only consider results for which $\theta_l$ is around -90 degrees and $r_l$ is around 0. Compare the results using a loss function: $loss = \sqrt{({\pi/2 + \theta_l \over \pi/2}) ^2 + r_l ^2}$. For more accurate result, another grid is created around the found approximate result and the process is repeated. We called this algorithm Recursive Grid Search.

To speed up calculations, we use multiprocessing.

### File System
* `params.py`: setting parameters
* `calculate_rp.py`: calculate rp(s) function - pumpkin shape balloon radius depends on s
* `density.py`: calculate atmosphere and gas density, air pressure and gas temperature depends on height
* `solve.py`: the whole process to calculate the shape of balloon (system's solver)
* `theta0_a.py`: create grid and run the Recursive Grid Search algorithm
* `main.py`: whole process to determine the shape of the balloon (Natural Shape), calculate velocity, maximum radius and volume  

### Recursive Grid Search

At first, the grid looks like: from 0 to 25 for $\theta_0$ and from 5 to 16 for a if $height < 21500$ or from 25 to 90 for $\theta_0$ and from -400 to 4 if $height >= 21500$. Number of steps per axis $\theta_0$ is 900, per axis $a$ is 64 if $h < 21500$ and 100 if $h >= 21500$. 

Applying the grid search once, we got the approximate solution $(\theta_{0, 1}, a_1)$. We create a grid around this solution (with the same number of steps) and apply the algorithm again. Thus, we obtain a more accurate solution.

### Multiprocessing
The code uses multiprocessing to speed up calculations. For multiprocessing we use method `ProcessPoolExecutor` from the library `concurrent`. With this method, the function is run on multiple cores and calculations are performed in parallel at the appropriate number of grid points. The number of cores is entered by the user when the code is run (`number_of_cores` parameter).  

### Run the code
To launch the code you need to run the following: 
`python main.py --number_of_cores [NUMBER OF CORES] --height [HEIGHT]`


### Output
At the output we get the txt file with complete information about the state of the balloon at the given altitude, csv file with lists of z and r (for future calculations) and svg file with a plot of z vs r. 

The following information is written to the text file:
* Parameters $\theta_0$ and a that define the shape of the balloon
* Last values of theta (should be ~-90), r (~0), maximum value of r, loss of this solution (minimize)
* Volume of the balloon
* Difference between input and output mass of the LTA gas (~0)
* Differences between forces
* Input and output values of velocities and difference between them (~0)
* The following information is written to the text file
