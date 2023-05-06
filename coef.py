import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

class Fourier():

    def __init__(self, x_low, x_high, n_max, strike_price=100.0):
        '''
        [x_low, strike_price, x_high)
        '''
        assert isinstance(x_low, float)
        assert isinstance(x_high, float)
        assert isinstance(n_max, int)
        assert isinstance(strike_price, float)
        assert strike_price>0
        assert n_max>0
        assert x_low<strike_price
        assert x_high>strike_price
        self.x_low = x_low
        self.x_high = x_high
        self.n_max = n_max
        self.strike_price = strike_price
        self.T = x_high-x_low
        self.omega = 2*np.pi/(x_high-x_low)

    def f(self, x):
        if isinstance(x, float):
            assert self.x_low<=x
            assert x<=self.x_high
            if x==self.x_high:
                x = self.x_low
            return max(0, x-self.strike_price)
        elif isinstance(x, np.ndarray):
            assert np.all(self.x_low<=x)
            assert np.all(x<=self.x_high)
            x[x==self.x_high] = self.x_low
            return np.clip(a=x-self.strike_price, a_min=0, a_max=None)
        else:
            raise ValueError('x should be float or np.ndarray!')
    

    def f_periodic(self, x):
        x_shifted = (x-self.x_low)%self.T + self.x_low
        return self.f(x_shifted)
    
    def create_coef(self):
        self.c = 1.0/self.T*quad(func=self.f, a=self.x_low, b=self.x_high)[0]
        self.a = np.zeros(self.n_max, dtype=float)
        self.b = np.zeros(self.n_max, dtype=float)
        pre_factor = 2.0/self.T
        for n in range(self.n_max):
            nw = (n+1)*self.omega
            self.a[n] = quad(
                func=self.f, a=self.x_low, b=self.x_high, weight='cos', wvar=nw
            )[0]*pre_factor
            self.b[n] = quad(
                func=self.f, a=self.x_low, b=self.x_high, weight='sin', wvar=nw
            )[0]*pre_factor
        
    def f_series(self, x):
        if isinstance(x, float):
            ans = self.c
        elif isinstance(x, np.ndarray):
            ans = self.c*np.ones_like(x, dtype=float)
        else:
            raise ValueError('x should be float or np.ndarray!')
        for n in range(self.n_max):
            nw = (n+1)*self.omega
            ans += self.a[n]*np.cos(nw*x)
            ans += self.b[n]*np.sin(nw*x)
        return ans

if __name__=="__main__":
    XLOW = 0.0
    XHIGH = 421.0
    NMAX = (1, 10, 100, 1000, 10000)
    x = np.linspace(-100, 1000, num=500)
    colors = ('r', 'g', 'b', 'y', 'k')

    fig, ax = plt.subplots()
    mycoef = Fourier(x_low=XLOW, x_high=XHIGH, n_max=1, strike_price=100.0)
    y_ref = mycoef.f_periodic(x)
    ax.plot(x, y_ref)
    for (i, nm) in enumerate(NMAX):
        mycoef = Fourier(x_low=XLOW, x_high=XHIGH, n_max=nm, strike_price=100.0)
        mycoef.create_coef()
        y_this = mycoef.f_series(x)
        rerr = np.max(np.abs(y_ref-y_this))/XHIGH
        print('nmax={0:e}, rerr={1:e} c={2:.2f}'.format(nm, rerr, mycoef.c))
        ax.plot(
            x, y_this, color=colors[i], label='nmax={0:.0e}, rerr={1:.2e}'.format(nm,rerr)
        )
    fig.legend()
    fig.savefig('test.png', dpi=1200)