# pylint: disable = invalid-name
import os
import sys
from pathlib import Path
from typing import Tuple
from databricksbundle.pipeline.decorator.duplicateColumnsChecker import checkDuplicateColumns
from databricksbundle.pipeline.function.ServiceResolver import ServiceResolver
from databricksbundle.pipeline.function.ServicesResolver import ServicesResolver
from pyfonybundles.appContainerInit import initAppContainer
from databricksbundle.pipeline.decorator.static_init import static_init
from databricksbundle.pipeline.decorator.argsChecker import checkArgs
from databricksbundle.pipeline.decorator.executor.dataFrameLoader import loadDataFrame
from databricksbundle.pipeline.decorator.executor.transformation import transform
from databricksbundle.pipeline.decorator.executor.dataFrameSaver import saveDataFrame
from injecta.dtype.DType import DType

@static_init
class PipelineDecorator:

    _servicesResolver: ServicesResolver

    @classmethod
    def static_init(cls):
        container = initAppContainer(os.environ['APP_ENV'])

        cls._pipelinePath = Path(sys.argv[0])
        cls._servicesResolver = container.get(ServicesResolver)
        cls._serviceResolver = container.get(ServiceResolver)

class pipelineFunction(PipelineDecorator):

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        checkArgs(args, self.__class__.__name__)

    def __call__(self, fun, *args, **kwargs):
        services = self._servicesResolver.resolve(fun, 0, self._pipelinePath) # pylint: disable = no-member
        fun(*services)

        return fun

class dataFrameLoader(PipelineDecorator):

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        checkArgs(args, self.__class__.__name__)

    def __call__(self, fun, *args, **kwargs):
        services = self._servicesResolver.resolve(fun, 0, self._pipelinePath) # pylint: disable = no-member
        loadDataFrame(fun, services)

        return fun

class transformation(PipelineDecorator):

    def __init__(self, *args, **kwargs): # pylint: disable = unused-argument
        self._sources = args # type: Tuple[callable]
        self._checkDuplicateColumns = kwargs.get('checkDuplicateColumns', True)

    def __call__(self, fun, *args, **kwargs):
        startIndex = len(self._sources)
        services = self._servicesResolver.resolve(fun, startIndex, self._pipelinePath) # pylint: disable = no-member
        df = transform(fun, self._sources, services)

        if self._checkDuplicateColumns:
            logger = self._serviceResolver.resolve(DType('logging', 'Logger'), self._pipelinePath)
            checkDuplicateColumns(df, fun, self._sources, logger)

        return fun

class dataFrameSaver(PipelineDecorator):

    def __init__(self, *args):
        self._sources = args # type: Tuple[callable]

    def __call__(self, fun, *args, **kwargs):
        services = self._servicesResolver.resolve(fun, 1, self._pipelinePath) # pylint: disable = no-member
        saveDataFrame(fun, self._sources, services)

        return fun
