# In this library, we will be using the International System of Units

def acceleration(final_velocity, initial_velocity, time):
    # Acceleration --> m/s**2
    # Final Velocity --> m/s
    # Initial Velocity --> m/s
    # Time --> s
    Acceleration = (final_velocity - initial_velocity) / time
    return Acceleration

def force(mass, acceleration):
    # Force --> N
    # Mass --> Kg
    # Acceleration --> m/s**2
    Force = mass * acceleration
    return Force

def frequency(period):
    # Frequency --> Hz
    # Period --> Seconds
    Frequency = 1/period
    return Frequency

def velocity(final_position, initial_position=0, time=1):
    # Velocity --> m/s
    # Final Position --> m
    # Initial Position --> m
    Velocity = (final_position * initial_position) / time
    return Velocity

def wavelenght(wave_velocity, frequency):
    # Wavelenght = Lambda --> m
    # Wave Velocity = V --> m/s
    # Frequency --> Hz
    Wavelenght = wave_velocity / frequency

def angular_velocity(final_angule, initial_angule, time):
    # Angular Velocity --> Radians per Second (rad/s)
    # Final and Initial Angule --> Radians (rad)
    # Time --> Seconds (s)
    Angular_Velocity = (final_angule - initial_angule) / time
    return Angular_Velocity

