from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self

from typing import Any, Final, List, Mapping, Optional, Union

from PIL import Image
from deepface import DeepFace
from deepface.extendedmodels import Emotion

from viam.media.video import RawImage
from viam.proto.common import PointCloudObject
from viam.proto.service.vision import Classification, Detection
from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype
from viam.utils import ValueTypes

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.service.vision import Detection
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.services.vision import Vision
from viam.components.camera import Camera

from viam.logging import getLogger

import time
import asyncio
import numpy

LOGGER = getLogger(__name__)

class facialAnalysis(Vision, Reconfigurable):
    
    MODEL: ClassVar[Model] = Model(ModelFamily("arielle", "detector"), "facial-analysis")
    
    # Class Variables
    img_path: str           #The exact path to the image, a numpy array in BGR format,
                            #or a base64 encoded image. If the source image contains multiple faces, the result will
                            #include information for each detected face.
    
    actions: tuple          #Attributes to analyze. The default is ('age', 'gender', 'emotion', 'race').
                            #You can exclude some of these attributes from the analysis if needed.
    
    enforce_detection: bool #If no face is detected in an image, raise an exception.
                            #Default is True. Set to False to avoid the exception for low-resolution images.
    
    detector_backend: str   #face detector backend. Options: 'opencv', 'retinaface',
                            #'mtcnn', 'ssd', 'dlib', 'mediapipe', 'yolov8'.

    distance_metric: str    #Metric for measuring similarity. Options: 'cosine',
                            #'euclidean', 'euclidean_l2'.
    
    align: bool             #Perform alignment based on the eye positions.            
    silent: bool            #Suppress or allow some log messages for a quieter analysis process.


    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        backends = ['opencv']
        detector_backend = config.attributes.fields["detector_backend"].string_value or 'opencv'
        if not detector_backend in backends:
            raise Exception("detector_backend must be 'opencv'")
        models =  ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
        model_name = config.attributes.fields["recognition_model"].string_value or 'ArcFace'
        if not model_name in models:
            raise Exception("detector_backend must be one of 'VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib', 'SFace'")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        # here we initialize the resource instance, the following is just an example and should be updated as needed
        self.DEPS = dependencies
        self.detector_backend = config.attributes.fields["detector_backend"].string_value or 'ssd'
        self.model_name = config.attributes.fields["recognition_model"].string_value or 'ArcFace'
       

    # Methods the Viam RDK defines for the Vision API (rdk:service:vision)
    
    async def get_detections_from_camera(
        self, camera_name: str, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Detection]:
        actual_cam = self.DEPS[Camera.get_resource_name(camera_name)]
        cam = cast(Camera, actual_cam)
        cam_image = await cam.get_image(mime_type="image/jpeg")
        return await self.get_detections(cam_image)

    
    async def get_detections(
        self,
        image: Union[Image.Image, RawImage],
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Detection]:
        return
            ################################# analyze methods

    
    async def get_classifications_from_camera(self):
        return
    
    async def get_classifications(self):
        return
    
    async def get_object_point_clouds(self):
        return
    
    async def do_command(self):
        return

