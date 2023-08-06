import matplotlib
from co2mpas_driver import dsp as driver
import matplotlib.pyplot as plt
import numpy as np
import math as m

matplotlib.use('qt4agg')


def idm_calc_vel(af_mfc, fol_v, lead_v, vn, dist, bn, an, sim_step, **kwargs):
    if 'ds' in kwargs:  # inter vehicle spacing at a stop
        ds = kwargs['ds']
    else:
        ds = 2
    if 'th' in kwargs:  # the desired time headway to the vehicle in front
        th = kwargs['th']
    else:
        th = 1.5
    if 'delta' in kwargs:  # the desired time headway to the vehicle in front
        delta = kwargs['delta']
    else:
        delta = 4
    bn_idm = abs(bn)  # braking deceleration  b - a positive number
    return max(0, fol_v + (af_mfc + -an * (pow(max(0, (ds + fol_v * th) / dist + (fol_v * (fol_v - lead_v)) /
                                                   (2 * m.sqrt(an * bn_idm) * dist)), 2))) * sim_step)


# IDM params
amax = 3
bn = -2
delta = 4
ds = 2
th = 1.5

np.random.seed(123)

# veh_ids = [27748, 8188]
# veh_ids = [39393, 8188, 40516, 35452, 40225, 7897, 7972, 41388, 5766,
#            9645, 9639, 5798, 8280, 34271, 34265, 6378, 39723, 34092, 2592,
#            5635, 5630, 7661, 7683]
veh_pool = [39393, 8188, 40516, 35452, 40225, 7897, 7972, 41388, 5766,
            9645, 9639, 5798, 8280, 34271, 34265, 6378, 39723, 34092, 2592,
            5635, 5630, 7661, 7683]
num_vehs = 1
veh_ids = [np.random.choice(veh_pool) for i in range(num_vehs)]

v_des = 100 / 3.6
v_start = 20
dt = 0.1

sim_duration = 30  # sec
times = np.arange(0, sim_duration, dt)

vehicles = [driver(dict(vehicle_id=i, inputs=dict(inputs=dict(
    gear_shifting_style=1, driver_style=1,
    use_linear_gs=True,
    use_cubic=False))))['outputs'] for i in
            veh_ids]
models = [veh['driver_simulation_model'] for veh in vehicles]
dcurves = [veh['driver_simulation_model'] for veh in vehicles]

dist = 30  # meters

test_leader_sp_profile = [20 / 3.6] * int(10 * sim_duration / 6) + [50 / 3.6] * int(10 * sim_duration / 6) + [
    120 / 3.6] * int(10 * sim_duration / 6) + [80 / 3.6] * int(10 * sim_duration / 6) + [
                             60 / 3.6] * int(10 * sim_duration / 6) + [100 / 3.6] * int(10 * sim_duration / 6)
leader_dt = np.cumsum([i * dt for i in test_leader_sp_profile]) + dist * (len(models) + 1)

res = {}
for idx, myt in enumerate(times):
    if (len(times) - idx) % 100 == 0:
        print(len(times) - idx)
    for v_idx, my_veh in enumerate(models):
        if myt == times[0]:
            my_veh.reset(v_start)
            res[my_veh] = {'acc': [0], 'speed': [v_start], 'pos': [dist * (len(models) - v_idx)]}
            sl_prev = 20 / 3.6
            continue

        # desired speed in order not to cover the distance to the leader
        # distL is the position of the leader + velocity of leader multiplied by dt
        if v_idx == 0:
            distL = leader_dt[idx] - res[models[v_idx]]['pos'][idx - 1]
        else:
            distL = res[models[v_idx - 1]]['pos'][idx] - res[models[v_idx]]['pos'][idx - 1]
        v_desired_new = min(distL / dt, v_des)

        # Compute MFC gear, next_velocity, acceleration - The positing is not needed
        gear, gear_count, next_velocity, acc = my_veh(dt, v_desired_new)

        # Fuel consumption
        # fc = my_veh.calculate_fuel_consumption(next_velocity, acc, gear, gear_count, dt)

        final_acc = acc

        # So the next velocity will be based on the cf acceleration (not the MFC one)
        next_velocity = res[my_veh]['speed'][-1] + final_acc * dt

        ####
        if next_velocity < 0:
            next_velocity = 0
        if v_desired_new - 0.001 < next_velocity < v_desired_new + 0.001:
            next_velocity = v_desired_new
        if next_velocity > v_desired_new:
            next_velocity = v_desired_new
        ####

        # I save my results. Again here positing is of no use
        res[my_veh]['acc'].append(final_acc)
        res[my_veh]['speed'].append(next_velocity)
        if res[models[v_idx]]['pos'][idx - 1] + next_velocity * (dt) + 0.5 * acc * dt ** 2 <0:
            print('check')
        dtf = res[models[v_idx]]['pos'][idx - 1] + next_velocity * (dt) + 0.5 * acc * dt ** 2
        res[models[v_idx]]['pos'].append(dtf)

        # update the vehicle for the next MFC
        gear, gear_count = my_veh.update(next_velocity, gear, gear_count, dt)
        print(f':{gear_count}')

        # if (gear_count !=0 and v_idx == 0):
        #     fig = plt.figure()
        #     fig.suptitle(gear)
        #     for cgear, curve in enumerate(vehicles[v_idx]['discrete_deceleration_curves']):
        #         sp_bins = list(curve['x'])
        #         acceleration = list(curve['y'])
        #         plt.plot(sp_bins, acceleration, label=f'gear {gear}')
        #     plt.legend()
        #     plt.text(30, 2.5, f'Simulation car:{veh_ids}, GS:{1}')
        #     fig.suptitle('Acceleration over speed', x=0.54, y=1, fontsize=12)
        #     plt.xlabel('Speed (m/s)', fontsize=12)
        #     plt.ylabel('Acceleration (m/s2)', fontsize=12)
        #     plt.show()

fig = plt.figure('Trajectory')
ax = fig.add_subplot(111)
ax.plot(times, leader_dt, label='leader')
for idx, my_veh in enumerate(models):
    # plt.figure('Acceleration-Speed')
    # plt.plot(res[my_veh]['speed'], res[my_veh]['acc'], label=idx)
    # plt.plot(res[my_veh]['speed'], res[my_veh]['acc'], label=idx)
    # plt.legend()
    # plt.show()

    # plt.figure('Speed Profile')
    # plt.plot(times, test_leader_sp_profile, label='leader')
    # plt.plot(times, res[my_veh]['speed'], label=idx)
    # plt.legend()
    # plt.show()

    follower_dt = res[my_veh]['pos']

    ax.plot(times, follower_dt, label=idx)
    # plt.legend()
miny = max(res[models[-1]]['pos'])
maxy = max(res[models[0]]['pos'])
if miny < maxy:
    ax.set_ylim(miny, maxy)
plt.show()
