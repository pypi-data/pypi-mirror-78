import gym
from gym import error, spaces, utils
from gym.utils import seeding

import os
import pybullet as p
import pybullet_data
import math
import numpy as np
import random

MAX_EPISODE_LEN = 5000
JOINTS=[0,1,2,5,6,7]
MAX_TORQUE=500
FORCE_ACTION={
    #1: 0,
    #2: 0,
    #4: 0,
    #5: 0,
}

class NFEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    _max_episode_steps=MAX_EPISODE_LEN

    def __init__(self):
        self.step_counter = 0
        if os.path.exists("/Users/dj/stuff/bot/urdf/bot6.urdf"):
            p.connect(p.GUI)
        else:
            p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.action_space = spaces.Box(np.array([-1]*6), np.array([1]*6))
        self.observation_space = spaces.Box(np.array([-1]*28), np.array([1]*28)) # XXX: range

    def reset(self):
        self.step_counter = 0
        p.resetSimulation()
        p.setGravity(0,0,-10)
        self.plane_id = p.loadURDF("plane.urdf")
        #self.wall1_id = p.loadURDF("plane.urdf",[-0.7,0,0],p.getQuaternionFromEuler([0,math.pi/2,0]))
        #self.wall2_id = p.loadURDF("plane.urdf",[0.7,0,0],p.getQuaternionFromEuler([0,-math.pi/2,0]))
        cubeStartPos = [0,0,2.8]
        cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
        try:
            self.bot_id = p.loadURDF("/Users/dj/stuff/bot/urdf/bot6.urdf", cubeStartPos, cubeStartOrientation)
        except:
            self.bot_id = p.loadURDF("/content/drive/My Drive/bot/bot6.urdf", cubeStartPos, cubeStartOrientation)

        maxForce = 0
        mode = p.VELOCITY_CONTROL
        for i in range(10):
            p.setJointMotorControl2(self.bot_id, i, controlMode=mode, force=maxForce)

        c = p.createConstraint(self.bot_id, 2, self.bot_id, 4, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=-1, maxForce=10000)

        c = p.createConstraint(self.bot_id, 2, self.bot_id, 3, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=1, maxForce=10000)

        c = p.createConstraint(self.bot_id, 7, self.bot_id, 9, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=-1, maxForce=10000)

        c = p.createConstraint(self.bot_id, 7, self.bot_id, 8, jointType=p.JOINT_GEAR,jointAxis =[1,0,0],parentFramePosition=[0,0,0],childFramePosition=[0,0,0])
        p.changeConstraint(c, gearRatio=1, maxForce=10000)

        res=p.getBasePositionAndOrientation(self.bot_id)
        pos=res[0]
        rot=p.getEulerFromQuaternion(res[1])

        obs=[]
        for i in range(6):
            joint_no=JOINTS[i]
            res=p.getJointState(self.bot_id, joint_no)
            obs.append(res[0]) # pos
            obs.append(res[1]) # vel
            obs.append(res[3]) # torque
        res=p.getBaseVelocity(self.bot_id)
        obs+=rot # orient (3)
        obs+=res[0] # lin vel (3)
        obs+=res[1] # ang vel (3)
        obs.append(pos[2]) # z
        self.observation = obs 
        return np.array(self.observation).astype(np.float32)

    def step(self, action):
        show_log=self.step_counter%100==0
        if show_log:
            print("step #%s action=%s"%(self.step_counter,action))
        mode = p.POSITION_CONTROL
        for i in range(6):
            a=action[i]
            if i in FORCE_ACTION:
                a=FORCE_ACTION[i]
            pos=a*math.pi
            joint_no=JOINTS[i]
            p.setJointMotorControl2(self.bot_id, joint_no, controlMode=mode, targetPosition=pos, force=MAX_TORQUE)

        p.stepSimulation()

        res=p.getBasePositionAndOrientation(self.bot_id)
        pos=res[0]
        rot=p.getEulerFromQuaternion(res[1])

        obs=[]
        power=0
        for i in range(6):
            joint_no=JOINTS[i]
            res=p.getJointState(self.bot_id, joint_no)
            obs.append(res[0]) # pos
            obs.append(res[1]) # vel
            obs.append(res[3]) # torque
            power+=res[3]**2
        res=p.getBaseVelocity(self.bot_id)
        obs+=rot # orient (3)
        obs+=res[0] # lin vel (3)
        obs+=res[1] # ang vel (3)
        obs.append(pos[2]) # z
        self.observation = obs 

        #print("rot=%s"%str(rot))
        if pos[2]<=0.9 or abs(rot[0])>=0.78 or abs(rot[1])>=0.78:
            reward = -10
            done = True
        else:
            reward = 1-power/(6*MAX_TORQUE**2)
            done = False

        self.step_counter += 1
        if self.step_counter > MAX_EPISODE_LEN:
            reward = 0
            done = True

        info = {}

        if show_log:
            print("=> reward=%s obs=%s"%(reward,obs))
        return np.array(self.observation).astype(np.float32), reward, done, info

    def render(self):
        pass

    def _get_state(self):
        return self.observation

    def close(self):
        p.disconnect()
