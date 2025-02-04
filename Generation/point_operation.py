# -*- coding: utf-8 -*-
# @Time        : 16/1/2019 5:26 PM
# @Description :
# @Author      : li rui hui
# @Email       : ruihuili@gmail.com
# @File        : point_operation.py

import numpy as np
from numpy.linalg import norm
import matplotlib.pylab  as plt
#plt.switch_backend('TkAgg')
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.text as mtext
import open3d as o3d
######################################Drawing Tools#########################################################
def plot_pcd_multi_rows(filename, pcds, titles, suptitle='', sizes=None, cmap='Greys', zdir='y',
                         xlim=(-0.4, 0.4), ylim=(-0.4, 0.4), zlim=(-0.4, 0.4)):
    if sizes is None:
        sizes = [0.2 for i in range(len(pcds[0]))]

    #print(len(pcds),len(pcds[0]))
    fig = plt.figure(figsize=(len(pcds[0]) * 3, len(pcds)*3)) # W,H
    for i in range(len(pcds)):
        elev = 30
        azim = -45
        for j, (pcd, size) in enumerate(zip(pcds[i], sizes)):
            color = np.zeros(pcd.shape[0])
            ax = fig.add_subplot(len(pcds), len(pcds[i]), i * len(pcds[i]) + j + 1, projection='3d')
            #print(len(pcds), len(pcds[i]), i * len(pcds[i]) + j + 1)
            ax.view_init(elev, azim)
            ax.scatter(pcd[:, 0], pcd[:, 1], pcd[:, 2], zdir=zdir, c=color, s=size, cmap=cmap, vmin=-1, vmax=0.5)
            pcd_cloud = o3d.geometry.PointCloud()
            pcd_cloud.points = o3d.utility.Vector3dVector(pcd)
            o3d.io.write_point_cloud(filename+"output.ply" , pcd_cloud, write_ascii=False, compressed=False, print_progress=True)
            print("save")
            ax.set_title(titles[i][j])
            #ax.text(0, 0, titles[i][j], color="green")
            ax.set_axis_off()
            #ax.set_xlabel(titles[i][j])

            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            ax.set_zlim(zlim)

    #plt.xticks(np.arange(len(pcds)), titles[:len(pcds)])

    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9, wspace=0.1, hspace=0.1)
    plt.suptitle(suptitle)
    fig.savefig(filename)
    plt.close(fig)


def plot_pcd_multi_rows_single_color(filename, pcds, titles, suptitle='', sizes=None, cmap=cm.get_cmap("jet"), zdir='y',
                                     xlim=(-0.4, 0.4), ylim=(-0.4, 0.4), zlim=(-0.4, 0.4), colors=None):
    if sizes is None:
        sizes = [0.2 for i in range(len(pcds[0]))]

    #print(len(pcds),len(pcds[0]))
    fig = plt.figure(figsize=(len(pcds[0]) * 3, len(pcds)*3)) # W,H
    for i in range(len(pcds)):
        elev = 30
        azim = -45
        for j, (pcd, size) in enumerate(zip(pcds[i], sizes)):
            #color = np.zeros(pcd.shape[0])
            color = colors[j] if colors is not None else np.zeros(pcd.shape[0])
            ax = fig.add_subplot(len(pcds), len(pcds[i]), i * len(pcds[i]) + j + 1, projection='3d')
            #print(len(pcds), len(pcds[i]), i * len(pcds[i]) + j + 1)
            ax.view_init(elev, azim)
            ax.scatter(pcd[:, 0], pcd[:, 1], pcd[:, 2], zdir=zdir, c=color, s=size, cmap=cmap, vmin=-1, vmax=0.5)
            ax.set_title(titles[i][j])
            #ax.text(0, 0, titles[i][j], color="green")
            ax.set_axis_off()
            #ax.set_xlabel(titles[i][j])

            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            ax.set_zlim(zlim)

    #plt.xticks(np.arange(len(pcds)), titles[:len(pcds)])

    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9, wspace=0.1, hspace=0.1)
    plt.suptitle(suptitle)
    fig.savefig(filename)
    plt.close(fig)


def plot_pcd_multi_rows_color(filename, pcds, titles, suptitle='', sizes=None, cmap=cm.get_cmap("jet"), zdir='y',
                                     xlim=(-0.4, 0.4), ylim=(-0.4, 0.4), zlim=(-0.4, 0.4), colors=None):
    if sizes is None:
        sizes = [0.2 for i in range(len(pcds[0]))]

    #print(len(pcds),len(pcds[0]))
    fig = plt.figure(figsize=(len(pcds[0]) * 3, len(pcds)*3)) # W,H
    for i in range(len(pcds)):
        elev = 30
        azim = -45
        for j, (pcd, size) in enumerate(zip(pcds[i], sizes)):
            #color = np.zeros(pcd.shape[0])
            color = colors[i][j] if colors is not None else np.zeros(pcd.shape[0])
            ax = fig.add_subplot(len(pcds), len(pcds[i]), i * len(pcds[i]) + j + 1, projection='3d')
            #print(len(pcds), len(pcds[i]), i * len(pcds[i]) + j + 1)
            ax.view_init(elev, azim)
            ax.scatter(pcd[:, 0], pcd[:, 1], pcd[:, 2], zdir=zdir, c=color, s=size, cmap=cmap, vmin=-1, vmax=0.5)
            ax.set_title(titles[i][j])
            #ax.text(0, 0, titles[i][j], color="green")
            ax.set_axis_off()
            #ax.set_xlabel(titles[i][j])

            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            ax.set_zlim(zlim)

    #plt.xticks(np.arange(len(pcds)), titles[:len(pcds)])

    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9, wspace=0.1, hspace=0.1)
    plt.suptitle(suptitle)
    fig.savefig(filename)
    plt.close(fig)

def plot_pcd_three_views_color(filename, pcds, titles, suptitle='', sizes=None, cmap=cm.get_cmap("jet"), zdir='y',
                         xlim=(-0.4, 0.4), ylim=(-0.4, 0.4), zlim=(-0.4, 0.4),colors=None):
    if sizes is None:
        sizes = [0.2 for i in range(len(pcds))]
    fig = plt.figure(figsize=(len(pcds) * 3, 9))
    for i in range(3):
        elev = 30
        azim = -45 + 90 * i
        for j, (pcd, size) in enumerate(zip(pcds, sizes)):
            color = colors[j,:,0] if colors is not None else np.zeros(pcd.shape[0])
            #color = pcd[:, -1]
            ax = fig.add_subplot(3, len(pcds), i * len(pcds) + j + 1, projection='3d')
            ax.view_init(elev, azim)
            ax.scatter(pcd[:, 0], pcd[:, 1], pcd[:, 2], zdir=zdir, c=color, s=size, cmap=cmap, vmin=-1, vmax=0.5)
            #print(j,titles[j])
            if i == 0:
                ax.set_title(titles[j])
            ax.set_axis_off()
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            ax.set_zlim(zlim)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9, wspace=0.1, hspace=0.1)
    plt.suptitle(suptitle)
    fig.savefig(filename)
    plt.close(fig)

######################################Transformation Tools#########################################################
def normalize_point_cloud(inputs):
    """
    input: pc [N, P, 3]
    output: pc, centroid, furthest_distance
    """
    #print("shape",input.shape)
    C = inputs.shape[-1]
    pc = inputs[:,:,:3]
    if C > 3:
        nor = inputs[:,:,3:]

    centroid = np.mean(pc, axis=1, keepdims=True)
    pc = inputs[:,:,:3] - centroid
    furthest_distance = np.amax(
        np.sqrt(np.sum(pc ** 2, axis=-1, keepdims=True)), axis=1, keepdims=True)
    pc = pc / furthest_distance
    if C > 3:
        return np.concatenate([pc,nor],axis=-1)
    else:
        return pc

def shuffle_point_cloud_and_gt(batch_data,batch_gt=None):
    B,N,C = batch_data.shape

    idx = np.arange(N)
    np.random.shuffle(idx)
    batch_data = batch_data[:,idx,:]
    if batch_gt is not None:
        np.random.shuffle(idx)
        batch_gt = batch_gt[:,idx,:]
    return batch_data,batch_gt

def shuffle_data(data, labels):
    """ Shuffle data and labels.
        Input:
          data: B,N,... numpy array
          label: B,... numpy array
        Return:
          shuffled data, label and shuffle indices
    """
    idx = np.arange(len(labels))
    np.random.shuffle(idx)
    return data[idx, ...], labels[idx]

def rotate_point_cloud_by_angle_batch(batch_data, rotation_angle):
  """ Rotate the point cloud along up direction with certain angle.
    Input:
      BxNx3 array, original batch of point clouds
    Return:
      BxNx3 array, rotated batch of point clouds
  """
  rotated_data = np.zeros(batch_data.shape, dtype=np.float32)
  for k in range(batch_data.shape[0]):
    #rotation_angle = np.random.uniform() * 2 * np.pi
    cosval = np.cos(rotation_angle)
    sinval = np.sin(rotation_angle)
    rotation_matrix = np.array([[cosval, 0, sinval],
                  [0, 1, 0],
                  [-sinval, 0, cosval]])
    shape_pc = batch_data[k, ...]
    rotated_data[k, ...] = np.dot(shape_pc.reshape((-1, 3)), rotation_matrix)
  return rotated_data

def rotate_point_cloud_and_gt(pc,gt=None,y_rotated=True):
    """ Randomly rotate the point clouds to augument the dataset
        rotation is per shape based along up direction
        Input:
          BxNx3 array, original batch of point clouds
        Return:
          BxNx3 array, rotated batch of point clouds
    """
    angles = np.random.uniform(size=(3)) * 2 * np.pi
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(angles[0]), -np.sin(angles[0])],
                   [0, np.sin(angles[0]), np.cos(angles[0])]])
    Ry = np.array([[np.cos(angles[1]), 0, np.sin(angles[1])],
                   [0, 1, 0],
                   [-np.sin(angles[1]), 0, np.cos(angles[1])]])
    Rz = np.array([[np.cos(angles[2]), -np.sin(angles[2]), 0],
                   [np.sin(angles[2]), np.cos(angles[2]), 0],
                   [0, 0, 1]])
    if y_rotated:
        rotation_matrix = Ry
    else:
        rotation_matrix = np.dot(Rz, np.dot(Ry, Rx))

    pc = np.dot(pc, rotation_matrix)
    if gt is not None:
        gt = np.dot(gt, rotation_matrix)
        return pc, gt

    return pc

def jitter_perturbation_point_cloud(pc, sigma=0.01, clip=0.02):
    """ Randomly jitter points. jittering is per point.
        Input:
          BxNx3 array, original batch of point clouds
        Return:
          BxNx3 array, jittered batch of point clouds
    """
    N, C = pc.shape
    assert(clip > 0)
    jittered_data = np.clip(sigma * np.random.randn(N, C), -1*clip, clip)
    jittered_data += pc
    return jittered_data

def jitter_perturbation_point_cloud_bt(batch_data, sigma=0.01, clip=0.02):
    """ Randomly jitter points. jittering is per point.
        Input:
          BxNx3 array, original batch of point clouds
        Return:
          BxNx3 array, jittered batch of point clouds
    """
    jittered_data = np.zeros(batch_data.shape, dtype=np.float32)
    _, N, C = batch_data.shape

    for k in range(batch_data.shape[0]):
        # rotation_angle = np.random.uniform() * 2 * np.pi
        noise = np.clip(sigma * np.random.randn(N, C), -1 * clip, clip)
        shape_pc = batch_data[k, ...]
        jittered_data[k, ...] = shape_pc + noise
    return jittered_data

def shift_point_cloud_and_gt(pc, gt = None, shift_range=0.1):
    """ Randomly shift point cloud. Shift is per point cloud.
        Input:
          BxNx3 array, original batch of point clouds
        Return:
          BxNx3 array, shifted batch of point clouds
    """
    N, C = pc.shape
    shifts = np.random.uniform(-shift_range, shift_range, (3))
    pc = pc + shifts

    if gt is not None:
        gt = gt + shifts
        return pc, gt

    return pc


def translate_pointcloud(pointcloud):
    xyz1 = np.random.uniform(low=2. / 3., high=3. / 2., size=[3])
    xyz2 = np.random.uniform(low=-0.2, high=0.2, size=[3])

    translated_pointcloud = np.add(np.multiply(pointcloud, xyz1), xyz2).astype('float32')
    return translated_pointcloud

def random_scale_point_cloud_and_gt(pc, gt = None, scale_low=0.8, scale_high=1.25):
    """ Randomly scale the point cloud. Scale is per point cloud.
        Input:
            BxNx3 array, original batch of point clouds
        Return:
            BxNx3 array, scaled batch of point clouds
    """
    N, C = pc.shape
    scale = np.random.uniform(scale_low, scale_high, 1)
    pc = pc * scale

    if gt is not None:
        gt = gt * scale
        return pc, gt, scale

    return pc


def rotate_perturbation_point_cloud(pc, angle_sigma=0.06, angle_clip=0.18):
    """ Randomly perturb the point clouds by small rotations
        Input:
          BxNx3 array, original batch of point clouds
        Return:
          BxNx3 array, rotated batch of point clouds
    """
    N, C = pc.shape

    angles = np.clip(angle_sigma*np.random.randn(3), -angle_clip, angle_clip)
    Rx = np.array([[1,0,0],
                   [0,np.cos(angles[0]),-np.sin(angles[0])],
                   [0,np.sin(angles[0]),np.cos(angles[0])]])
    Ry = np.array([[np.cos(angles[1]),0,np.sin(angles[1])],
                   [0,1,0],
                   [-np.sin(angles[1]),0,np.cos(angles[1])]])
    Rz = np.array([[np.cos(angles[2]),-np.sin(angles[2]),0],
                   [np.sin(angles[2]),np.cos(angles[2]),0],
                   [0,0,1]])
    R = np.dot(Rz, np.dot(Ry,Rx))
    pc = np.dot(pc, R)

    return pc

def guass_noise_point_cloud(batch_data, sigma=0.005, mu=0.00):
    """ Add guassian noise in per point.
        Input:
          BxNx3 array, original batch of point clouds
        Return:
          BxNx3 array, jittered batch of point clouds
    """
    batch_data += np.random.normal(mu, sigma, batch_data.shape)
    return batch_data

def rotate_point_cloud_by_angle(self, data, rotation_angle):
    """
    Rotate the point cloud along up direction with certain angle.
    :param batch_data: Nx3 array, original batch of point clouds
    :param rotation_angle: range of rotation
    :return:  Nx3 array, rotated batch of point clouds
    """
    cosval = np.cos(rotation_angle)
    sinval = np.sin(rotation_angle)
    rotation_matrix = np.array([[cosval, 0, sinval],
                                [0, 1, 0],
                                [-sinval, 0, cosval]])
    rotated_data = np.dot(data, rotation_matrix)

    return rotated_data


