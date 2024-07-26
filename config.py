# velocity of each joint and also the length of the probe
probe = {
	"v0": 100,
	"v1": 100,
	"l1": 2000,
}

joystick_offset_time = {
    "up": 0,
    "down": 0,
    "left": 0,
    "right": 0
}

detection = {
	"direction": "height",
	"start": 0.5,
	"end": 0.5,
	"width": 20,
	"height":20,
	"thr_distance": 2000,
	"z_min": 100,
	"z_max": 10000,
	"model_path": "xxx.xyz"
}

home = {
	"up":{
		"step": 90,
		"value": 45,
		"standby": 45
	},
	"left":{
		"step": 240,
		"value": 120,
		"standby": 0,
	},
	"p0":{
		"direction": "left",
		"step": 30,
		"value": 120,
		"amp": 6,
		"f0": 60,
		"hf": 30,
		"hf_thr":10,
		"standby": 0
	},
	"p1":{
		"direction": "up",
		"step": 30,
		"value": 30,
		"amp": 6,
		"f0": 60,
		"hf": 30,
		"hf_thr":10,
		"standby": 30
	},
}

search = {
	"p0": [0, 45, -45]
}


######################
######################
######################
"""
robot
"""
robot_model= "dorna_ta"
robot_ip = "192.168.254.18"
emergency=["in0",[0, 1]] # [pin_index, [off_state, on_state]]

"""
startup routine
"""
startup_routine = [
    {"cmd": "motor", "motor": 1},
    {"cmd": "sleep", "time": 1},
    {"cmd":"jmove","rel":0, "j1":125, "vel": 50, "accel": 800, "jerk":1000},
    {"cmd":"jmove","rel":0,"j0":0},
    {"cmd":"jmove","rel":0, "j2":-125},
    {"cmd":"jmove","rel":0, "j3":0,"j4":0,"j5":0},
]


"""
joystick
"""
# joystick engage
joystick_engage = [
    {"cmd":"jmove","rel":0,"j0":-8.129883,"j1":40.979004,"j2":-99.09668,"j3":-0.153809,"j4":-31.92627,"j5":0, "vel": 200, "accel": 2000, "jerk":4000},
    {"cmd":"jmove","rel":0,"j0":-7.77832,"j1":32.255859,"j2":-97.404785,"j3":-0.197754,"j4":-24.851074,"j5":0},
]

# up after engage
joystick_up = [
    {**joystick_engage[1], **{"vel": 80, "accel": 600, "jerk":1600}},
    {"cmd":"jmove","rel":0,"j0":-10.327148,"j1":32.233887,"j2":-97.294922,"j3":-0.197754,"j4":-24.916992,"j5":0},
    joystick_engage[1]
]

# down after engage
joystick_down = [
    {**joystick_engage[1], **{"vel": 80, "accel": 600, "jerk":1600}},
    {"cmd":"jmove","rel":0,"j0":-5.185547,"j1":32.211914,"j2":-97.229004,"j3":-0.197754,"j4":-24.98291,"j5":0},
    joystick_engage[1]
]

# left after engage
joystick_left = [
    {**joystick_engage[1], **{"vel": 170, "accel": 1700, "jerk":2000}},
    {"cmd":"jmove","rel":0,"j0":-7.77832,"j1":30.52002,"j2":-91.713867,"j3":-0.175781,"j4":-28.806152,"j5":0},
    joystick_engage[1]
]

# right after engage
joystick_right = [
    {**joystick_engage[1], **{"vel": 170, "accel": 1700, "jerk":2000}},
    {"cmd":"jmove","rel":0,"j0":-8.569336,"j1":34.057617,"j2":-104.018555,"j3":-0.241699,"j4":-20.061035,"j5":0},
    joystick_engage[1]
]

# hover after engage
joystick_disengage = [
    joystick_engage[1],
    joystick_engage[0]
]

"""
switch alarm
"""
# switch alarm engage
switch_alarm_engage = [
    {"cmd":"jmove","rel":0, "j0":-14.787598,"j1":36.496582,"j2":-87.385254,"j3":-0.109863,"j4":-39.111328, "j5":0, "vel": 75, "accel": 500, "jerk":1200},
    {"cmd":"jmove","rel":0, "j0":-14.787598,"j1":22.17041,"j2":-83.188477,"j3":-0.153809,"j4":-28.981934,"j5":0}  
]

# up after engage
switch_alarm_up = [
    {**switch_alarm_engage[1], **{"vel": 75, "accel": 500, "jerk":1200}},
    {"cmd":"jmove","rel":0,"j0":-16.479492,"j1":21.950684,"j2":-82.507324,"j3":-0.153809,"j4":-29.487305,"j5":0},
]

# down after engage
switch_alarm_down = [
    {**switch_alarm_engage[1], **{"vel": 75, "accel": 500, "jerk":1200}},
    {"cmd":"jmove","rel":0,"j0":-12.766113,"j1":22.346191,"j2":-83.803711,"j3":-0.153809,"j4":-28.564453,"j5":0},
]

"""
switch in_out
"""
# engage
switch_in_out_engage = [
    {"cmd":"jmove","rel":0, "j0":-16.984863,"j1":43.571777,"j2":-106.325684,"j3":-0.153809,"j4":-27.246094, "j5":0, "vel": 75, "accel": 500, "jerk":1200},
    {"cmd":"jmove","rel":0, "j0":-16.984863,"j1":26.938477,"j2":-101.953125,"j3":-0.285645,"j4":-15.007324,"j5":0}
]

# after engage
switch_in_out_in = [
    {**switch_in_out_engage[1], **{"vel": 75, "accel": 500, "jerk":1200}},
    {"cmd":"jmove","rel":0,"j0":-18.896484,"j1":26.806641,"j2":-101.293945,"j3":-0.263672,"j4":-15.534668,"j5":0},
]

# after engage
switch_in_out_out = [
    {**switch_in_out_engage[1], **{"vel": 75, "accel": 500, "jerk":1200}},
    {"cmd":"jmove","rel":0,"j0":-14.501953,"j1":27.070312,"j2":-102.612305,"j3":-0.263672,"j4":-14.47998,"j5":0},
]

"""
switch vac
"""
# engage
switch_vac_engage = [
    {"cmd":"jmove","rel":0, "j0":-0.395508,"j1":43.59375,"j2":-106.391602,"j3":-0.153809,"j4":-27.246094, "j5":0, "vel": 75, "accel": 500, "jerk":1200},
    {"cmd":"jmove","rel":0, "j0":-0.395508,"j1":26.960449,"j2":-102.019043,"j3":-0.263672,"j4":-14.963379,"j5":0}
]

# after engage
switch_vac_on = [
    {"cmd":"jmove","rel":0,  "j0":-2.219238,"j1":27.04834,"j2":-102.502441,"j3":-0.263672,"j4":-14.589844,"j5":0},
]

# after engage
switch_vac_off = [
    {"cmd":"jmove","rel":0, "j0":1.801758,"j1":26.828613,"j2":-101.315918,"j3":-0.241699,"j4":-15.534668,"j5":0},
]

"""
switch on_off
"""
# engage
switch_on_off_engage = [
    {"cmd":"jmove","rel":0, "j0":-0.351562,"j1":36.518555,"j2":-87.473145,"j3":-0.109863,"j4":-39.089355, "j5":0, "vel": 75, "accel": 500, "jerk":1200},
    {"cmd":"jmove","rel":0, "j0":-0.351562,"j1":22.192383,"j2":-83.254395,"j3":-0.131836,"j4":-28.959961,"j5":0}
]

# after engage
switch_on_off_on = [
    {"cmd":"jmove","rel":0,  "j0":-1.955566,"j1":22.346191,"j2":-83.737793,"j3":-0.131836,"j4":-28.630371,"j5":0},
]

# after engage
switch_on_off_off = [
    {"cmd":"jmove","rel":0, "j0":1.252441,"j1":21.994629,"j2":-82.63916,"j3":-0.131836,"j4":-29.399414,"j5":0},
]

"""
startup routine
"""
estop = [
    {"cmd":"jmove","rel":0,"j0":-8.129883,"j1":40.979004,"j2":-99.09668,"j3":-0.153809,"j4":-31.92627,"j5":0, "vel": 100, "accel": 800, "jerk":1000},
    {"cmd":"jmove","rel":0,"j0":-76.201172, "j1":76.201172, "j2":-138.054199, "j3":2.746582, "j4":-34.057617, "j5":0}
]