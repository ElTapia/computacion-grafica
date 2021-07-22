
# Calculo de la componente K1 del método de RK4
def K1(f, t_n, z_n):
    k1 = f(t_n, z_n)
    return k1

# Calculo de la componente K2 del método de RK4
def K2(f, h, t_n, z_n):
    k2 = f(t_n + h/2, z_n + (h/2)*K1(f, t_n, z_n))
    return k2

# Calculo de la componente K3 del método de RK4
def K3(f, h, t_n, z_n):
    k3 = f(t_n + h/2, z_n + (h/2)*K2(f, h, t_n, z_n))
    return k3

# Calculo de la componente K4 del método de RK4
def K4(f, h, t_n, z_n):
    k4 = f(t_n + h, z_n + h*K3(f, h, t_n, z_n))
    return k4

# Calculo un paso de la aproximación con el método de RK4
def RK4_step(f, h, t_n, z_n):
    k1 = K1(f, t_n, z_n)
    k2 = K2(f, h, t_n, z_n)
    k3 = K3(f, h, t_n, z_n)
    k4 = K4(f, h, t_n, z_n)
    return z_n + (h/6)*(k1 + 2*k2 + 2*k3 + k4)


# Calculo un paso de la aproximacion con Euler modificado
def modified_euler_step(f, h, t_n, z_n):
    f_n = f(t_n, z_n)
    next_z = z_n + h*f(t_n + h/2, z_n + h/2 * f_n)
    return next_z


# Calculo un paso de la aproximacion con Euler mejorado
def improved_euler_step(f, h, t_n, z_n):
    f_n = f(t_n, z_n)
    next_z = z_n + h/2 *(f_n + f(t_n + h, z_n + h*f_n))
    return next_z


# Calculo un paso de la aproximacion con el método de euler
def euler_step(f, h, t_n, z_n):
    next_z = z_n + h*f(t_n, z_n)
    return next_z

