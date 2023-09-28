#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.nn.parameter import Parameter
from torch.optim import SGD, LBFGS

class CircleFitting2(nn.Module):
    def __init__(self):
        super().__init__()
        self.center = Parameter(torch.randn((1,2)))
        self.radius = Parameter(torch.randn(1))

    def forward(self, ps):
        v = ps - self.center # N x 2
        return torch.norm(v, dim=1) - self.radius


class CircleFitting(object):
    '''Bullock, R. (2017). Least-Squares Circle Fit. October, 22–24. Retrieved from https://dtcenter.org/met/users/docs/write_ups/circle_fit.pdf'''

    def __init__(self):
        pass

    def fit(self, points):
        '''
        points: two-dimension(N x 2) data points to be fitted.

        return: circle center `x' and `y', circle radius `r'

        least square error problem:
        \min_{x,y,r} \sum_{j=1}^N{((x_j-x)^2+(y_j-y)^2-r^2)^2}
        '''

        m = np.mean(points, axis=0)
        p = points - m
        sxx, syy = np.sum(p*p,axis=0)
        sxxx,syyy = np.sum(p*p*p, axis=0)
        sxy = np.sum(p[:,0]*p[:,1])
        sxxy = np.sum(p[:,0]*p[:,0]*p[:,1])
        sxyy = np.sum(p[:,0]*p[:,1]*p[:,1])

        y = 0.5*((sxxx+sxyy)*sxy-(syyy+sxxy)*sxx)/(sxy*sxy-sxx*syy)
        x = (0.5*(sxxx+sxyy)-y*sxy)/sxx

        r = (x*x + y*y + (sxx+syy)/p.shape[0])**0.5
        x += m[0]
        y += m[1]
        return x,y,r


if __name__ == '__main__':
    n = 30
    # x_ground_truth = 1.5
    # y_ground_truth = 2.0
    # r_ground_truth = 5
    x_ground_truth = np.random.uniform(-100, 100)
    y_ground_truth = np.random.uniform(-100, 100)
    r_ground_truth = np.random.uniform(1, 10)
    print("GROUND TRUTH(x,y,r): ", x_ground_truth, y_ground_truth, r_ground_truth)
    angle = np.random.uniform(0, 2*np.pi, (n, 1))
    points = np.hstack([np.cos(angle), np.sin(angle)])*r_ground_truth + np.hstack([np.ones((n,1))*x_ground_truth, np.ones((n,1))*y_ground_truth])
    noise = np.random.normal(0.0, 0.2, (n, 2))
    points += noise
    c = CircleFitting()
    x ,y , r = c.fit(points)
    print("ESTIMATION1(x,y,r): ", x, y, r)

    # ax = plt.gca()
    # ax.cla()
    # ax.scatter(points[:,0], points[:,1], color='b')
    # ax.add_artist(plt.Circle((x,y), r, fill=False, color='g'))


    c2 = CircleFitting2()
    # optimizer = SGD(c2.parameters(), lr=1.0e-3, momentum=0.9)
    optimizer = LBFGS(c2.parameters(), lr=1.0e-1)
    point_tensors = torch.tensor(points)
    for i in range(100):
        def closure():
            optimizer.zero_grad()
            res = c2(point_tensors)
            loss = torch.mean(res*res)
            # if i % 1000 == 0:
            #     print(f"iteration {i}: loss={loss.item()}")
            loss.backward()
            return loss
        optimizer.step(closure)
    print("ESTIMATION2(x,y,r): ", c2.center.tolist(), c2.radius.item())


    # ax.add_artist(plt.Circle(c2.center.tolist()[0], c2.radius.item(), fill=False, color='r'))
    # plt.show()
