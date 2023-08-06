import matplotlib
from co2mpas_driver import dsp as driver
import matplotlib.pyplot as plt
import numpy as np
import math as m

matplotlib.use('qt4agg')


def idm_calc_vel(af_mfc, fol_v, lead_v, vn, dist, bn, an, sim_step, **kwargs):
    if 'ds' in kwargs:  # intervehicle spacing at a stop
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
    return max(0, fol_v + (af_mfc + \
                           -an * (pow(
                max(0, (ds + fol_v * th) / dist + (fol_v * (fol_v - lead_v)) / (2 * m.sqrt(an * bn_idm) * dist)),
                2))) * sim_step)


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

# v_des = 100 / 3.6
v_start = 0
dt = 0.1

sim_duration = 230.1  # sec

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
cnt = 0

v_des_p = []
my_veh = models[0]
my_veh.reset(v_start)
res[my_veh] = {'accel': [0], 'speed': [v_start], 'pos': [0]}
for idx, myt in enumerate(times):
        dd = 700
        if 0 <= res[my_veh]['pos'][idx] <= 0.3 * dd:
            v_des = 20
        elif 0.3 * dd < res[my_veh]['pos'][idx] <= 1 * dd:
            v_des = 30
        elif 1 * dd < res[my_veh]['pos'][idx] <= 1.5 * dd:
            v_des = 5
        elif 1.5 * dd < res[my_veh]['pos'][idx] <= 2 * dd:
            v_des = 25
        elif 2 * dd < res[my_veh]['pos'][idx] <= 4.5 * dd:
            v_des = 45
        elif 4.5 * dd < res[my_veh]['pos'][idx] <= 6.5 * dd:
            v_des = 15
        elif 6.5 * dd < res[my_veh]['pos'][idx] <= 7.5 * dd:
            v_des = 0

        v_des_p.append(v_des)
        # Compute MFC gear, next_velocity, acceleration - The positing is not needed
        gear, gear_count, next_velocity, acc = my_veh(dt, v_des)

        final_acc = acc

        # So the next velocity will be based on the cf acceleration (not the MFC one)
        next_velocity = res[my_veh]['speed'][-1] + final_acc * dt

        ####
        if next_velocity < 0:
            next_velocity = 0
        if v_des - 0.001 < next_velocity < v_des + 0.001:
            next_velocity = v_des
        # if next_velocity > v_des:
        #     next_velocity = v_des
        ####

        # I save my results. Again here positing is of no use
        res[my_veh]['accel'].append(final_acc)
        res[my_veh]['speed'].append(next_velocity)
        res[my_veh]['pos'].append(res[my_veh]['pos'][idx]+ (res[my_veh]['speed'][idx]+res[my_veh]['speed'][-1])*0.5*dt)

        # if res[models[vidx]]['pos'][idx - 1] + next_velocity * (dt) + 0.5 * acc * dt ** 2 <0:
        #     print('check')
        # dtf = res[models[vidx]]['pos'][idx - 1] + next_velocity * (dt) + 0.5 * acc * dt ** 2
        # res[models[vidx]]['pos'].append(dtf)

        # update the vehicle for the next MFC
        gear, gear_count = my_veh.update(next_velocity, gear, gear_count, dt)
        cnt += 1
        if cnt == 1651:
            print('check')
        print(cnt)

fig = plt.figure('Trajectory (distance-speed)')
ax = fig.add_subplot(111)
ax.plot(res[my_veh]['pos'][1:], v_des_p, label='Reference speed')
ax.plot(res[my_veh]['pos'][1:], res[my_veh]['speed'][1:], label='Reference speed')
plt.show()
