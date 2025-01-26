# DPD - Dental Preparation Deformation 
> A deformation model of a dental crown shell to generate a series of preparations by teeth number based on SP-GAN by Li. et al.
> 
By Imane Chafi



## Software Implementation 
This code builds onto code from the [SP GAN](https://liruihui.github.io/publication/SP-GAN/) paper by Li et al. 

Our labs have provided a list of public dataset (78 cases) of dies and margin lines you can use in this paper and other papers, please make sure to cite our lab when using our data: 
[Public Dataset Intellident](https://github.com/intellident-ai/public-datasets)

This dataset above is a small part of the dataset used to train our model. Due to privacy laws concerning dentistry shape material, we cannot share the original data here. Please email imane.chafi@polymtl.ca for data. 

## Installation

You can download the code from this github page. Refer [here](https://github.com/ImaneChafi/DPD.git) to 

```
git clone https://github.com/ImaneChafi/DPD.git
```

## Training
The code is separated into two: Training and visualization 

The file `train.py` has all the important information for training the code, as well as a log file setup to have a log for every training.

This is an unsupervised method, and doesn't need ground truth. We use COV-CD and MMD-CD from [latent 3D points](https://github.com/optas/latent_3d_points.git) to evaluate the output. 

To train on your own data, you need to make an h5 file of point clouds. These point clouds can have a certain number of points. 

Use `h5/convert_dataset.py` to make your training dataset (.stl) into a h5 file. It needs to have at least a couple shapes (more than 50) for the training to run. Each shape can have as many points as wanted. It can also be used to downsample your meshes. 

Once the training dataset has been converted, you can use `h5/check_h5.py` to make sure the downsampling has been well executed into the h5 file.  

The output h5 file (titled prep.h5 for example) needs to be added to the folder 2048, or a folder with the name being the number of points for meshes inside the h5 file. (ie. if your file has a series of point clouds for 3 points each, your folder with the h5 file inside should be called 3, and be placed in the root.) 

### Files for compute canada

You can choose to train locally or remotely, using the code provided (train.py and train.sh).

The train.sh has all the information to train, since you need to setup CD and EMD before training. 

Here is an example:
```
python train.py --choice preps --np 2048 --max_epoch 300 
```
1. `--choice` means that it is the category choice, or the name of your h5 file 
2. `--np` this is the number of points in each mesh, or the name of your folder where the h5 file lies
3. `--max epoch` is the maximum number of epochs you want to have for the run. It can be changed directly on training, along with a number of other `config` options. 


## Visualization
```
python  visual.py --np 2048
```
For the visualization, you also need to have the name of the folder (or number of points) for your run. 

In the file `visual.py`, you need to change the lines: 
```
opts.pretrain_model_G = "300_preps_G.pth"
opts.log_dir = "log/20240629-2221"
```  
With the name of the pretrained model (it will be outputted as a log) and the directory (also outputted as a log) of your run. 

## Evaluation

The code `hausdorff_dist` is available for you to use, to calculate the hausdorff distance between two meshes or pointclouds. 
And example output for the hausdorff distance code evaluation is:
```
{'RMS': 0.05054453760385513, 'diag_mesh_0': 11.399076461791992, 'diag_mesh_1': 11.315515084423572, 'max': 0.1677803099155426, 'mean': 0.039864495396614075, 'min': 6.468382451885191e-08, 'n_samples': 7619}
```
More information about this function [here](https://pymeshlab.readthedocs.io/en/latest/filter_list.html) 

## Thickness Analysis Script
On a python environment, you can run the file found in `scripts/thickness_interactive.py` with
`python3 thickness_interactive.py`
and the application should show up on http://127.0.0.1:8050/

## Undercut Evaluation Script
On a python environment, you can run the file found in `scripts/undercut_evaluation.py` with
`python3 undercut_evaluation.py`
and the application should show up on http://127.0.0.1:8050/

There is a path for a die file and a prep file. This can be updated to allow for entire folder. There is also in the application a slidedown for two types of direction. A PCA Based direction and a Z-axis direction, such that the undercut points in red show up for the direction of extrusion which is more adequate. This can be updated to only one type of direction if needed. 

## Licence
The code is available under `MIT` licence. Please list authors if this code has been of help to you!


