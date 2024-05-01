joystick = {
	"up": [0, 0, 0, 0, 0, 0],
	"down": [0, 0, 0, 0, 0, 0],
	"left": [0, 0, 0, 0, 0, 0],
	"right": [0, 0, 0, 0, 0, 0],
	"standby": [0, 0, 0, 0, 0, 0],
	"standby_middle_joint": [0, 0, 0, 0, 0, 0],
	"disengage_joint": [0, 0, 0, 0, 0, 0]
	"vel_joint": 100,
	"accel_joint": 100,
	"jerk_joint": 100,
	"vel": 100,
	"accel": 100,
	"jerk": 100,
}
probe = {
	"v0": 100,
	"v1": 100,
	"l1": 2000,
}

detection = {
	"direction": "height"
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

robot = {
	"ip": "192.168.254.1"
}