

# 4th Order Runge Kutta Calculation
def RK4(f, x, u, dt):
    # Inputs: f(x[k],u[k]), x[k], u[k], dt (time step, seconds)
    # Returns: x[k+1]
    
    # Calculate slope estimates
    K1 = f(x, u)
    K2 = f(x + K1 * dt / 2, u)
    K3 = f(x + K2 * dt / 2, u)
    K4 = f(x + K3 * dt, u)
    
    # Calculate x[k+1] estimate using combination of slope estimates
    x_next = x + 1/6 * (K1 + 2*K2 + 2*K3 + K4) * dt
    
    return x_next