import torch
import os
import json

from urllib import request
from .message import pack_experience


class Agent:
    def __init__(self,
                 host='http://localhost',
                 port=8000,
                 dir_path='./',
                 use_gpu=False):
        self.host = host
        self.port = port
        self.base_url = host + ':' + str(port)
        self.dir_path = dir_path

        self.policy = None
        self.device = 'cuda:0' if use_gpu else 'cpu:0'

        # buffer for sending dataset
        self.observations = []
        self.actions = []
        self.rewards = []
        self.terminals = []

    def predict(self, x):
        x = torch.tensor(x, dtype=torch.float32, device=self.device)
        action = self.policy(x)
        return action.cpu().detach().numpy()

    def sync_policy(self):
        # donwload latest policy
        policy_path = os.path.join(self.dir_path, 'policy.pt')
        request.urlretrieve(self.base_url + '/model', policy_path)
        self.policy = torch.jit.load(policy_path, map_location='cpu')

    def store_experience(self, observation, action, reward, terminal):
        self.observations.append(observation)
        self.actions.append(action)
        self.rewards.append(reward)
        self.terminals.append(terminal)

    def send_experience(self):
        message = pack_experience(self.observations, self.actions,
                                  self.rewards, self.terminals)
        headers = {'Content-type': 'application/octet-stream'}
        req = request.Request(self.base_url + '/data',
                              data=message,
                              method='POST',
                              headers=headers)
        self.observations = []
        self.actions = []
        self.rewards = []
        self.terminals = []

    def start_train(self):
        req = request.Request(self.base_url + '/train', method='POST')
        request.urlopen(req)

    def is_training(self):
        res = request.urlopen(self.base_url + '/status')
        status = json.loads(res.read().decode('utf8'))
        return bool(status['training'])
