from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self

from typing import Any, Final, List, Mapping, Optional, Union

from PIL import Image
from deepface import DeepFace
from deepface.extendedmodels import Emotion

from viam.media.video import RawImage
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

import asyncio
import numpy

LOGGER = getLogger(__name__)

demographies = ['age', 'race', 'gender', 'emotion']
dominant_demographies = ['age', 'dominant_race', 'dominant_gender', 'dominant_emotion']
demography_map = dict(zip(demographies, dominant_demographies))

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
              
        demography = config.attributes.fields["demography"].string_value or 'emotion'
        if not demography in demographies:
            raise Exception("demography must be one of the following: 'age', 'race', 'gender', or 'emotion'")

        backends = ['opencv', 'retinaface','mtcnn', 'ssd', 'dlib', 'mediapipe', 'yolov8']
        detector_backend = config.attributes.fields["detector_backend"].string_value or 'opencv'
        if not detector_backend in backends:
            raise Exception("detector_backend must be one of the following: 'opencv', 'retinaface','mtcnn', 'ssd', 'dlib', 'mediapipe', 'yolov8'.")
        
        models =  ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
        model_name = config.attributes.fields["recognition_model"].string_value or 'ArcFace'
        if not model_name in models:
            raise Exception("detector_backend must be one of the following: 'VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib', 'SFace'")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.DEPS = dependencies
        self.detector_backend = config.attributes.fields["detector_backend"].string_value or 'opencv'
        self.model_name = config.attributes.fields["recognition_model"].string_value or 'ArcFace'
        self.demography = config.attributes.fields["demography"].string_value or 'emotion'
        self.dominant_demography = config.attributes.fields["dominant_demography"].string_value or 'dominant_emotion'

    # Methods the Viam RDK defines for the Vision API (rdk:service:vision) 
    async def get_detections_from_camera(
        self, camera_name: str, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Detection]:
        viam_cam = self.DEPS[Camera.get_resource_name(camera_name)]
        cam = cast(Camera, viam_cam)
        cam_image = await cam.get_image(mime_type="image/jpeg")
        return await self.get_detections(cam_image)

    
    async def get_detections(
        self,
        image: Union[Image.Image, RawImage],
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Detection]:
        detections = []

        results = DeepFace.analyze(
            img_path=numpy.array(image.convert('RGB')),
            actions= self.demography,
            detector_backend= self.detector_backend,
            enforce_detection=False,
            align=True,
        )
                                    
        for r in results: 
            dom = r[demography_map[self.demography]]
            if r["face_confidence"] > 0.4: 
                detection = { "confidence": r["face_confidence"]*10, "class_name": str(r[dom]), "x_min": r["region"]["x"], "y_min": r["region"]["y"], 
                "x_max": r["region"]["x"] + r["region"]["w"], "y_max": r["region"]["y"] + r["region"]["h"]}
                detections.append(detection)

        LOGGER.info(detections)
        return detections
    
    async def get_classifications_from_camera(self):
        return
    
    async def get_classifications(self):
        return
    
    async def get_object_point_clouds(self):
        return
    
    async def do_command(self):
        return

