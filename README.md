Fieldwork Host-mesh Fitting Step
================================
MAP Client plugin for non-rigid registration of a Fieldwork mesh to a target pointcloud using host-mesh fitting.

The input mesh (slave mesh) is embedded in a 1-element high-order 3-D Lagrange host mesh that deforms the slave mesh to minimise the least-squares distance between target points and points sampled on the slave mesh.

Information about the host-mesh fitting method can be found in
Fernandez, J. W., Mithraratne, P., Thrupp, S. F., Tawhai, M. H., & Hunter, P. J.
(2004). Anatomically based geometric modelling of the musculo-skeletal system
and other organs. Biomech Model Mechanobiol, 2(3), 139-155.

Requires
--------
- GIAS3 - Fieldwork : https://github.com/musculoskeletal/gias3.fieldwork
- GIAS3 - MAP Client Plugin Utilities : https://github.com/musculoskeletal/gias3.mapclientpluginutilities

Inputs
------
- **pointcloud** [nx3 NumPy Array] : The target point cloud.
- **fieldworkmodel** [GIAS3 GeometricField instance] : The source Fieldwork mesh to be registered.
- **array1d** [1-D NumPy Array] : An array of weights for each target point.
- **fieldworkmodel** [GIAS3 GeometricField instance][Optional] : The host-mesh to use in the registration. If not provided, a  global-axis-aligned host-mesh of the configured type is automatically generated around the input slave mesh.

Outputs
-------
- **fieldworkmodel** [GIAS3 GeometricField instance] : The registered slave mesh.
- **fieldworkmodelparameters** [NumPy Array] : An array of the registered slave mesh parameters.
- **float** [float] : The registration error in terms of the root-mean-squared Euclidean distance between the target points and the registered slave mesh.
- **array1d** [1-D NumPy Array] : An array of the Euclidean distance between each target point and its closest point on the registered slave mesh.
- **fieldworkmodel** [GIAS3 GeometricField instance] : The registered host mesh.

Configuration
-------------
- **identifier** : Unique name for the step.
- **GUI** : If the step GUI should be lauched on execution. Disable if running workflow in batch mode.
- **Fit Mode** : How distance is calculated in the registration objective function.
	- DPEP : Distance between each target point and its closest point on the slave mesh. Points on the slave mesh are sampled according to the "slave mesh discretisation" parameter.
	- EPDP : Distance between each point on the slave mesh and its closest target point. Points on the slave mesh are sampled according to the "slave mesh discretisation" parameter.
- **host element type** : The host element shape and order. Recommended values:
	- quad222 - tri-linear hexahedral
	- quad333 - tri-quadratic hexahedral
	- quad444 - tri-cubic hexahedral
- **slave mesh discretisation** : How densely the slave mesh is to be sampled when calculating distance to or from the target points. Should of the format "[d1, d2]" where d1 and d2 are the discretisation for each element in each element coordinate direction. E.g. [5,5] means each 2-D quadralateral element will be discretised into 25 points. High values give a more accurate discretisation and a more accurate fit.
- **slave sobelov discretisation** : Slave mesh discretisation when calculating the Sobelov norm of the slave mesh which penalises against regions of high curvature. Should of the format "[d1, d2]" where d1 and d2 are the discretisation for each element in each element coordinate direction. Recommended values for different slave mesh orders:
	- 3 (cubic) : [4,4]
	- 4 (quartic) : [5,5]
- **slave sobelov weight** : Weights for each of the 5 terms of the slave mesh Sobelov norm. Typical values: [1e-5, 1e-5, 1e-5, 1e-5, 2e-6].
- **slave normal discretistaion** : Number of points to sample along a slave mesh element edge when calculating the element normal penalty term. Recommended values for different slave mesh orders:
	- 3 (cubic) : 4
	- 4 (quartic) : 5
- **slave normal weight** : Weight on the slave mesh element normal penalty term.
- **max iterations** : Max number of fitting iterations before termination.
- **host sobelov discretisation** : Host mesh discretisation when calculating the Sobelov norm of the host mesh which penalises against regions of high curvature. Should of the format "[d1, d2, d3]" where d1, d2, and d3 are the discretisation for the host mesh in each element coordinate direction. Recommended values for different host mesh orders:
	- 3 (cubic) : [4,4,4]
	- 4 (quartic) : [5,5,5]
- **host sobelov weight** : Weight for each term of the host mesh Sobelov norm. Typical value: 1e-5.
- **n closest points** : Number of closest points to find when calculating distances between slave mesh and target points.
- **kdtree args** : optional arguments for the SciPy cKDTree.query function when searching for closest target and slave mesh points.
- **verbose** : [True|False] print extra messages to commandline.

Step GUI
--------
- **3D Scene** : Interactive viewer for the target point cloud, the unregistered slave mesh, and the registered slave mesh.
- **Visibles box** : Show or hide objects in the 3D scene.
- **Fitting Parameters** : Parameters for the registration optimisation. See the Configuration section for an explanation of the parameters.
- **Fit** : Run the registration using the given parameters.
- **Reset** : Removes the registered slave mesh.
- **Abort** : Abort the workflow.
- **Accept**: Finish the step and send outputs.
- **Fitting Errors** : Displays registration errors.
	- **RMS** : The root-mean-squared distance between target and slave mesh points.
	- **Mean** : The mean distance between target and slave mesh points.
	- **S.D.** : The standard deviation of distances between target and slave mesh points.
- **Screeshot** : Save a screenshot of the current 3-D scene to file.
	- **Pixels X** : Width in pixels of the output image.
	- **Pixels Y** : Height in pixels of the output image.
	- **Filename** : Path of the output image file. File format is defined by the suffix of the given filename.
	- **Save Screenshot** : Take screenshot and write to file.
	
Usage
-----
This step provides coarse non-rigid registration of a Fieldwork mesh to a target pointcloud (e.g. surface vertices from a segmented STL file). This step is typically used in between rigid-body registration and a more local mesh fitting step. Deformations applied to the mesh are constrained by a host mesh which typically has far fewer degrees of freedom than this input mesh.

The registration is performed by an iterative least-squares optimisation of the host mesh nodal coordinates P that mininimises

e = e_d(P) + w_ss\*e_ss(P) + w_n\*e_n(P) + w_hs\*e_hs(P)

where e_d is the squared distance between points sampled on the slave mesh and target points; e_ss is the Sobelov penalty term that penalises against high curvature in the slave mesh; e_hs is the Sobelov penalty term that penalises against high curvature in the host mesh; and e_n is the element normal penalty term that penalises against non-continuous normals across element boundaries in the slave mesh. Relaxing the weightings of the penalty terms will produce a closer fit of the slave mesh at the expense of mesh quality.

