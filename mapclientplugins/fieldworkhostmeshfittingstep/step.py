"""
MAP Client Plugin Step
"""
import json

from PySide2 import QtGui

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.fieldworkhostmeshfittingstep.configuredialog import ConfigureDialog
from mapclientplugins.fieldworkhostmeshfittingstep.mayavihostmeshfittingviewerwidget import \
    MayaviHostMeshFittingViewerWidget

import copy
from gias2.fieldwork.field.tools import fitting_tools
from gias2.fieldwork.field import geometric_field_fitter as GFF
import numpy as np


class FieldworkHostMeshFittingStep(WorkflowStepMountPoint):
    """
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    """

    _configDefaults = {}
    _configDefaults['GUI'] = 'True'
    _configDefaults['fit mode'] = 'DPEP'
    _configDefaults['host element type'] = 'quad444'
    _configDefaults['slave mesh discretisation'] = '[10,10]'
    _configDefaults['slave sobelov discretisation'] = '[8,8]'
    _configDefaults['slave sobelov weight'] = '[1e-6, 1e-6, 1e-6, 1e-6, 2e-6]'
    _configDefaults['slave normal discretisation'] = '8'
    _configDefaults['slave normal weight'] = '50.0'
    _configDefaults['max iterations'] = '10'
    _configDefaults['host sobelov discretisation'] = '[8,8,8]'
    _configDefaults['host sobelov weight'] = '1e-5'
    _configDefaults['n closest points'] = '1'
    _configDefaults['kdtree args'] = '{}'
    _configDefaults['verbose'] = 'True'

    def __init__(self, location):
        super(FieldworkHostMeshFittingStep, self).__init__('Fieldwork Host Mesh Fitting', location)
        self._configured = True  # A step cannot be executed until it has been configured.
        self._category = 'Fitting'
        self._identifier = ''
        # Add any other initialisation code here:
        self._icon = QtGui.QImage(':/fieldworkhostmeshfittingstep/images/fieldworkhostmeshfittingicon.png')
        # Ports:

        # target data clouds
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#pointcloud'))

        # slave mesh to fit
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmodel'))

        # data weights (optional)
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'numpy#array1d'))

        # host mesh (optional)
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmodel'))

        # fitted slave mesh
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'ju#fieldworkmodel'))

        # fitted slave mesh parameters
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'ju#fieldworkmodelparameters'))

        # fitted RMS error
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'python#float'))

        # fitted error distance for each data point
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'numpy#array1d'))

        # fitted host mesh
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'ju#fieldworkmodel'))

        self._config = {}
        for k, v in list(self._configDefaults.items()):
            self._config[k] = v

        self.data = None
        self.dataWeights = None
        self.slaveGFUnfitted = None
        self.slaveGF = None
        self.slaveGFFitted = None
        self.RMSEFitted = None
        self.slaveGFParamsFitted = None
        self.fitErrors = None
        self.hostGFUnfitted = None
        self.hostGF = None
        self.hostGFFitted = None
        self._genHostGF = True
        self._hostGFType = None

        self._widget = None

    def execute(self):
        """
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        """
        # Put your execute step code here before calling the '_doneExecution' method.

        if self._config['GUI'] == 'True':
            self._initHostGF(self._config['host element type'])
            self._widget = MayaviHostMeshFittingViewerWidget(self.data, self.slaveGFUnfitted,
                                                             self.hostGFUnfitted, self._config, self._fit, self._reset)
            # self._widget._ui.registerButton.clicked.connect(self._register)
            self._widget._ui.acceptButton.clicked.connect(self._doneExecution)
            self._widget._ui.abortButton.clicked.connect(self._abort)
            self._widget._ui.resetButton.clicked.connect(self._reset)
            self._setCurrentWidget(self._widget)

        elif self._config['GUI'] == 'False':
            self._fit()
            self.slaveGFFitted = copy.deepcopy(self.slaveGF)
            self._doneExecution()

    def _parseFitConfigs(self):
        """
        sanitisation should be done here
        """
        args = {}
        args['fit mode'] = self._config['fit mode']
        args['verbose'] = self._config['verbose']
        args['host element type'] = self._config['host element type']
        args['slave mesh discretisation'] = eval(self._config['slave mesh discretisation'])
        args['slave sobelov discretisation'] = eval(self._config['slave sobelov discretisation'])
        args['slave sobelov weight'] = eval(self._config['slave sobelov weight'])
        args['slave normal discretisation'] = eval(self._config['slave normal discretisation'])
        args['slave normal weight'] = float(self._config['slave normal weight'])
        args['host sobelov discretisation'] = eval(self._config['host sobelov discretisation'])
        args['host sobelov weight'] = float(self._config['host sobelov weight'])
        args['max iterations'] = int(self._config['max iterations'])
        args['slave mesh discretisation'] = eval(self._config['slave mesh discretisation'])
        args['n closest points'] = int(self._config['n closest points'])
        args['kdtree args'] = eval(self._config['kdtree args'])

        return args

    def _initHostGF(self, hostElementType):
        # make host GF if one is not provided
        if self._genHostGF:
            print('creating host mesh of type', hostElementType)
            self.hostGF = GFF.makeHostMesh(self.slaveGFUnfitted.get_field_parameters(), \
                                           5.0, hostElementType)
            self.hostGFUnfitted = copy.deepcopy(self.hostGF)

    def _fit(self, callback=None):

        args = self._parseFitConfigs()
        self._initHostGF(args['host element type'])
        # make slave obj
        if args['fit mode'] == 'DPEP':
            slaveGObj = GFF.makeObjDPEP(self.slaveGF, self.data, args['slave mesh discretisation'],
                                        nClosestPoints=args['n closest points'],
                                        treeArgs=args['kdtree args'])
        elif args['fit mode'] == 'EPDP':
            slaveGObj = GFF.makeObjEPDP(self.slaveGF, self.data, args['slave mesh discretisation'],
                                        nClosestPoints=args['n closest points'],
                                        treeArgs=args['kdtree args'])
        elif args['fit mode'] == '2way':
            slaveGObj = GFF.makeObj2Way(self.slaveGF, self.data, args['slave mesh discretisation'],
                                        nClosestPoints=args['n closest points'],
                                        treeArgs=args['kdtree args'])

        slaveSobObj = GFF.makeSobelovPenalty2D(self.slaveGF, args['slave sobelov discretisation'],
                                               args['slave sobelov weight'])
        slaveNormalSmoother = GFF.normalSmoother2(self.slaveGF.ensemble_field_function.flatten()[0])
        slaveNormObj = slaveNormalSmoother.makeObj(args['slave normal discretisation'])

        def slaveObj(x):
            errSurface = slaveGObj(x)
            errSob = slaveSobObj(x)
            errNorm = slaveNormObj(x) * args['slave normal weight']
            return np.hstack([errSurface, errSob, errNorm])

        # run HMF
        hostParamsOpt, slaveParamsOpt, \
        slaveXi, RMSEFitted = fitting_tools.hostMeshFitMulti(
            self.hostGF, self.slaveGF, slaveObj,
            maxIt=args['max iterations'],
            sobD=args['host sobelov discretisation'],
            sobW=args['host sobelov weight'],
            verbose=args['verbose'],
            xtol=1e-6,
        )

        # prepare outputs
        self.slaveGF.set_field_parameters(slaveParamsOpt)
        self.hostGF.set_field_parameters(hostParamsOpt)

        self.slaveGFFitted = copy.deepcopy(self.slaveGF)
        self.slaveGFParamsFitted = slaveParamsOpt.copy()
        self.fitErrors = np.sqrt(slaveGObj(slaveParamsOpt))
        self.RMSEFitted = np.sqrt((self.fitErrors ** 2.0).mean())
        self.hostGFFitted = copy.deepcopy(self.hostGF)

        # self._genHostGF = True

        return self.slaveGFFitted, self.slaveGFParamsFitted, self.RMSEFitted, \
               self.fitErrors, self.hostGFFitted

    def _abort(self):
        # self._doneExecution()
        raise RuntimeError('host mesh fitting aborted')

    def _reset(self):
        self.slaveGFFitted = None
        self.slaveGFParamsFitted = None
        self.RMSEFitted = None
        self.FitErrors = None
        self.slaveGF = copy.deepcopy(self.slaveGFUnfitted)
        self.hostGFFitted = None
        self.hostGF = copy.deepcopy(self.hostGFUnfitted)
        # self._genHostGF = True

    def setPortData(self, index, dataIn):
        '''
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        '''

        if index == 0:
            self.data = np.array(dataIn, dtype=float)  # ju#pointcoordinates
        elif index == 1:
            self.slaveGF = dataIn  # ju#fieldworkmodel
            self.slaveGFUnfitted = copy.deepcopy(self.slaveGF)
        elif index == 2:
            self.dataWeights = np.array(dataIn, dtype=float)  # numpyarray1d - dataWeights
        else:
            self.hostGF = dataIn
            self.hostGFUnfitted = copy.deepcopy(self.hostGF)
            self._genHostGF = False

    def getPortData(self, index):
        '''
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.
        '''
        if index == 4:
            return self.slaveGFFitted  # ju#fieldworkmodel
        elif index == 5:
            return self.slaveGFParamsFitted  # ju#fieldworkmodelparameters
        elif index == 6:
            return self.RMSEFitted  # float
        elif index == 7:
            return self.fitErrors  # numpyarray1d
        else:
            return self.hostGFFitted  # ju#fieldworkmodel

    def configure(self):
        '''
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        '''
        dlg = ConfigureDialog(self._main_window)
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        '''
        The identifier is a string that must be unique within a workflow.
        '''
        return self._identifier

    def setIdentifier(self, identifier):
        '''
        The framework will set the identifier for this step when it is loaded.
        '''
        self._identifier = identifier

    def serialize(self):
        '''
        Add code to serialize this step to disk. Returns a json string for
        mapclient to serialise.
        '''
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        '''
        Add code to deserialize this step from disk. Parses a json string
        given by mapclient
        '''
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.setConfig(self._config)
        self._configured = d.validate()
