# regressionpack

A library of higher level regression functions that also include errorbars computed using a provided confidence interval. 
Available regressions so far include  
* [Linear](https://en.wikipedia.org/wiki/Linear_regression)
    * [Polynomial](https://en.wikipedia.org/wiki/Polynomial_regression)
* GenericCurveFit
    * CosineFit
    * Exponential


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This package was developped using:  
* python 3.8.3
* numpy 1.18.1
* scipy 1.4.1

While it may still work with older versions, I did not take the time to verify. 

### Installing

```
pip install regressionpack
```

Note that this will also install numpy 1.18.1 and scipy 1.4.1 if they are not already present. 
Once installation is done, you may use the package by importing it this way:  
```python
import regressionpack
```

## Example applications

Everything below needs these imports to work:
```python
from regressionpack import Linear, Polynomial, GenericCurveFit, CosineFit, Exponential
import numpy as np
from matplotlib import pyplot as plt
```

### Using the classes
All the classes are meant to be used the same way (with sometimes minor changes). The most differences come during instanciation, as some models require more input parameters than others. Refer to the relevant models example for this.  
```python
L = Linear(xdata, ydata)
L.Fit() # Performs the fitting
L.Eval(x) # Evaluates the model using provided x data. The shape must be identical to the xdata, except along the FitDim. 
```
### Linear regression
This is the most generic multivariate linear regression. You can use it to fit any data with any base functions you choose fit. This was built from the [wikipedia](https://en.wikipedia.org/wiki/Linear_regression) page. You may notice some similarity in the nomenclature/variable names used in the source code. 

```python
x = np.linspace(-7,6,1000)
_x1 = x.reshape((-1,1)) # A plain linear base
_x2 = np.cos(_x1) # A cosine with frequency 1 base
_x3 = np.exp(_x1) # An exponential base

X = np.hstack((_x1, _x2, _x3)) # Put the base vectors together
Y = 3*_x1 + 10*_x2 + .1*_x3 # Create the result
Y += np.random.randn(*Y.shape)*2 # Add some noise

L = Linear(X, Y)
L.Fit()

YF = L.Eval(X).flatten()
dYF = L.EvalFitError(X).flatten()
dYFp = L.EvalPredictionError(X).flatten()

fig = plt.figure()
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.plot(x, Y, '.k', label='data')
plt.plot(x, YF,'--b', label='fit')
plt.fill_between(x, YF-dYF, YF+dYF,color='k', alpha=.3, label='Fit error')
plt.fill_between(x, YF-dYFp, YF+dYFp,color='b', alpha=.3, label='Prediction error')
plt.legend()

#Check that the fraction of points inside the prediction interval match the confidence interval (should be around 0.95)

frac = np.mean((Y.flatten() >= YF-dYFp) & (Y.flatten() <= YF + dYFp))
print(frac)
```

#### Polynomial regression
Using the previously shown Linear class, the specific case of the polynomial regression was implemented. This is done by creating a Vandermonde matrix of the input data before using the Linear class. Here we will show an example where we measure the photocurrent of a photodiode over the whole C-band (1525-1575 nm) at multiple optical powers. The goal is then to obtain the wavelength-dependant responsivity. 

```python
wavelengths = np.linspace(1525,1575,5001).reshape((-1,1))
power = np.linspace(1e-6,1e-3,30).reshape((1,-1))

#Generate a photocurrent curve with wavelength dependance (5 nm ripples) and nonlinear behavior, also a dark current of 2 nA
photocurrents = (0.1*power - 2*power**2) * (1 + 0.1 * np.cos(2*np.pi/5 * wavelengths)) + 2e-9

#Generate the data for fitting
#Add 1% of relative noise stdev
#And 10 pA of stdev absolute noise
Y = photocurrents*(1 + np.random.randn(*photocurrents.shape)*0.01) + np.random.randn(*photocurrents.shape) * 10e-12

# Repeat the power axis
X = np.repeat(power, Y.shape[0],axis=0) 
X *= (1 + .01*np.random.randn(*X.shape)) # 1% relative noise stdev
X += np.random.randn(*X.shape)*100e-9 # 100 nW noise

#Fit using a second order polynomial
P = Polynomial(X, Y, 2, 1)
P.Fit()

plt.figure()
plt.grid(True)
plt.xlabel('Wavelength [nm]')
plt.ylabel('Responsivity [A/W]')
plt.plot(wavelengths, P.Beta[:,1],'k')
plt.fill_between(wavelengths.flatten(), P.Beta[:,1] - P.BetaFitError[:,1], P.Beta[:,1] + P.BetaFitError[:,1], color='blue', alpha=0.7)

# Check that the fraction of points inside the prediction interval match the confidence interval (should be around 0.95)
YF = P.Eval(X)
dYFp = P.EvalPredictionError(X)
frac = np.mean((Y >= YF-dYFp) & (Y <= YF + dYFp))
print(frac)
print(np.min(P.AdjR2))
```

### GenericCurveFit
A simple way of wrapping up a custom fit function and its error bars calculations, all based on scipy.curve_fit. 

Example using a custom class with inherirance:  

```python
class myCustomFit(GenericCurveFit):

    def FitFunc(self, x:np.ndarray, a:float, b:float, c:float) -> np.ndarray:
        return a * x + np.exp(-b*x**2) + np.sin(c*x)

    def Jacobian(self, x:np.ndarray, a:float, b:float, c:float) -> np.ndarray:
        out = np.zeros((x.shape[0],) + (3,))

        out[:,0] = x
        out[:,1] = -x**2 * np.exp(-b*x**2)
        out[:,2] = x*np.cos(c*x)

        return out

    def __init__(self, x:np.ndarray, y:np.ndarray, p0:np.ndarray=None, bounds=(-np.inf, np.inf), confidenceInterval:float=0.95, simult:bool=False, **kwargs):
        super(myCustomFit, self).__init__(x, y, self.FitFunc, self.Jacobian, p0, bounds, confidenceInterval, simult, **kwargs )

# Example using standalone functions directly in the GenericCurveFit:  
def func(x:np.ndarray, a:float, b:float, c:float) -> np.ndarray:
    return a * x + np.exp(-b*x**2) + np.sin(c*x)

def jac( x:np.ndarray, a:float, b:float, c:float) -> np.ndarray:
        out = np.zeros((x.shape[0],) + (3,))

        out[:,0] = x
        out[:,1] = -x**2 * np.exp(-b*x**2)
        out[:,2] = x*np.cos(c*x)

        return out

"""
Change this value to use the custom class or 
the standalone functions. The result should be the same. 
"""
useClass = True

# Generate some data
x = np.linspace(-3,5,3000)
p = (.1,.2,6.2)
y = func(x, *p)
y += np.random.randn(*y.shape) * 0.3

# Pick between the class and the standalone functions
if useClass:
    GCF = myCustomFit(x, y, (1,1,7))
else:
    GCF = GenericCurveFit(x, y, func, jac, (1,1,7))

# Perform the fitting
GCF.Fit()

# Evaluate at a greater resolution
xx = np.linspace(x.min(),x.max(),1000)
yy = GCF.Eval(xx)
dyy = GCF.EvalPredictionError(xx)

# Show results and compare
plt.plot(x,y,'.', label='data')
plt.plot(xx,yy,'--', label='Fit')
plt.fill_between(xx, yy-dyy, yy+dyy, alpha=0.3)

# Check what fraction of the data is within the prediction interval
yf = GCF.Eval(x)
dyf = GCF.EvalPredictionError(x)

print("Check that the fraction of points inside the prediction interval match the confidence interval (should be around 0.95)")
frac = np.mean((y <= yf + dyf) & (y >= yf - dyf))
print(frac)

print("Compare parameters with results")
print(p)
print(GCF.Beta)
print(GCF.BetaFitError)
print(GCF.AdjR2)
```

#### Cosine fit
This cosine fit inherits from GenericCurveFit. It also uses the Fourier transform of the data to do the initial guess of the fit parameters. The amplitude $A$ is approximated by the highest amplitude peak (that is not the DC offset) of the FFT. The frequency $\omega$ is the one associated with that highest peak. The phase shift $\phi$ is the angle of the complex FFT component and the constant is the DC offset. Using those as initial guesses, we proceed with least squares fitting on that objective function:

$$\hat{y} = A \cos{\left( \omega x + \phi \right)} + b$$

To increase the speed, improve the results as well as enabling the computation of the errorbars, one must provide the Jacobian. Inheriting from the GenericCurveFit allows us to easily implement the cosine fit in a few lines of code (feel free to look in CosineFit.py). 

Ok, I cheated a little bit: a key component here involved the educated guess of the initial fit parameters. The function that does this (FFTGuess) actually takes more lines than this entire class. Also, since the FFT can be efficiently ran over large multidimensional datasets and provides a quite good estimate, I judged it deserved its own spot among the utilities function of this package. 

```python
x = np.linspace(-3,8,100)
y = 3*np.cos(4*x + .66) - 2
y += np.random.randn(*y.shape)*0.3

CF = CosineFit(x, y)
CF.Fit()
yf = CF.Eval(x)
dyf = CF.EvalPredictionError(x)

print("Parameters vs fit results:")
print((3, 4, .66, -2))
print(CF.Beta)
print(CF.BetaFitError)

plt.figure()
plt.plot(x, y, '.k')
plt.plot(x,yf,'--r')
plt.fill_between(x, yf-dyf, yf+dyf, color='b', alpha=0.3)

print("Check that the fraction of points inside the prediction interval match the confidence interval (should be around 0.95)")
factor = np.mean((y <= yf + dyf) & (y >= yf - dyf))
print(factor)
```

#### Exponential
```python
x = np.linspace(-3,5)
y = 2 * np.exp(2.4*x) + 3
y += np.random.randn(*y.shape)*3

plt.plot(x,y,'.')

E = Exponential(x, y)
E.Fit()

xx = np.linspace(x.min(), x.max(), 1000)
yy = E.Eval(xx)
dyy = E.EvalPredictionError(xx)

plt.plot(xx, yy,'--')
plt.fill_between(xx, yy-dyy, yy+dyy,alpha=0.3)
plt.yscale('log')
print(E.Beta)
print(E.BetaFitError)
```

## Built With
* [Python](https://www.python.org/) - The language
* [numpy](https://numpy.org/) - the numeric library
* [scipy](https://docs.scipy.org/) - the scientific library

## Contributing
Contact me and discuss your ideas and ambitions. 

## Authors

* **FusedSilica** - *Initial work*

## License

This project is licensed under the GNU LGPLv3 License - see the [LICENSE.md](LICENSE.md) file for details

