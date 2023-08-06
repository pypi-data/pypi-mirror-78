from os import path as osp, chdir
import numpy as np
import matplotlib.pyplot as plt
from co2mpas_driver import dsp as driver

my_dir = osp.dirname(osp.abspath(__file__))
chdir(my_dir)


def simple_run():
    """
     This example computes and plots the fuel consumption in grams for a
     simulated trajectory.

    """
    # A sample car id from the database = {
    car_id_db = {
        'fuel_engine': [35135, 39393, 27748, 8188, 40516, 35452, 40225, 7897, 7972, 41388, 5766, 9645, 9639, 5798, 8280,
                        34271, 34265, 6378, 39723, 34092, 2592, 5635, 5630, 7661, 7683, 8709, 9769, 1872, 10328, 35476,
                        41989, 26799, 26851, 27189, 23801, 3079, 36525, 47766, 6386, 33958, 33986, 5725, 5718, 36591,
                        4350, 39396, 40595, 5909, 5897, 5928, 5915, 40130, 42363, 34760, 34766, 1835, 36101, 42886,
                        1431, 46547, 44799, 41045, 39820, 34183, 34186, 20612, 20605, 1324, 9882, 4957, 5595, 18831,
                        18833, 9575, 5380, 9936, 7995, 6331, 18173, 34286, 34279, 20706, 34058, 34057, 24268, 19028,
                        19058, 7979, 22591, 34202, 40170, 44599, 5358, 5338, 34015, 9872, 9856, 6446, 8866, 9001, 9551,
                        6222],
        'electric_engine': [47844]
    }
    car_id = 39393

    # The desired speed
    vdes = 124 / 3.6

    # Current speed
    v_start = 0

    # The simulation step in seconds
    sim_step = 0.1

    # The driving style as described in the TRR paper.
    driver_style = 0.8

    # Duration of the simulation in seconds.
    duration = 100

    # sample time series
    times = np.arange(0, duration + sim_step, sim_step)

    # core model, this will select and execute the proper functions for the given inputs and returns the output
    # You can also pass vehicle database path db_path='path to vehicle db'
    if car_id in car_id_db['electric_engine']:
        sol = driver(dict(vehicle_id=47844, inputs=dict(inputs=dict(
            desired_velocity=vdes, starting_velocity=v_start, driver_style=driver_style,
            sim_start=0, sim_step=sim_step, duration=duration, use_linear_gs=True,
            use_cubic=False))))['outputs']
    else:
        # The gear shifting style as described in the TRR paper.
        gs_style = 0.8
        sol = driver(dict(vehicle_id=car_id, inputs=dict(inputs=dict(
            gear_shifting_style=gs_style, desired_velocity=vdes,
            starting_velocity=v_start, driver_style=driver_style,
            sim_start=0, sim_step=sim_step, duration=duration, degree=4, use_linear_gs=True,
            use_cubic=False))))['outputs']
    # Plots workflow of the core model, this will automatically open an internet browser and show the work flow
    # of the core model. you can click all the rectangular boxes to see in detail sub models like load, model,
    # write and plot.
    # you can uncomment to plot the work flow of the model
    # driver.plot(1)  # Note: run your IDE as Administrator if file permission error.

    fig = plt.figure('Time-Speed')
    plt.plot(times, sol['velocities'][1:], label=f'Simulation car:{car_id}, DS: {driver_style}')
    plt.plot(times, np.ones(len(times)) * vdes, label=f'Desired speed (m/s)')
    plt.legend()
    fig.suptitle('Speed over time', x=0.54, y=1, fontsize=12)
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Speed (m/s)', fontsize=12)
    plt.grid()

    fig = plt.figure('Time-Acceleration')
    plt.plot(times, sol['accelerations'][1:], label=f'Simulation car:{car_id}, DS: {driver_style}')
    plt.legend()
    fig.suptitle('Acceleration over time', x=0.54, y=1, fontsize=12)
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Acceleration (m/s2)', fontsize=12)
    plt.grid()

    fig = plt.figure('Speed-Acceleration')
    plt.plot(sol['velocities'][1:], sol['accelerations'][1:], label=f'Simulation car:{car_id}, DS: {driver_style}')
    plt.legend()
    fig.suptitle('Acceleration over speed', x=0.54, y=1, fontsize=12)
    plt.xlabel('Speed (m/s)', fontsize=14)
    plt.ylabel('Acceleration (m/s2)', fontsize=12)
    plt.grid()

    if car_id not in car_id_db['electric_engine']:
        fig = plt.figure('Time-Fuel consumption')
        plt.plot(times, sol['fp'], label=f'Simulation car:{car_id}, DS: {driver_style}')
        plt.legend()
        fig.suptitle('Fuel Consumption over time', x=0.54, y=1, fontsize=12)
        plt.xlabel('Time (s)', fontsize=14)
        plt.ylabel('Fuel Consumption (g)', fontsize=12)
        plt.grid()

    plt.show()


if __name__ == '__main__':
    simple_run()
