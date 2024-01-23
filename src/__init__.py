

from viam.services.vision import VisionClient
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .facialAnalysis import facialAnalysis

Registry.register_resource_creator(VisionClient.SUBTYPE, facialAnalysis.MODEL, ResourceCreatorRegistration(facialAnalysis.new, facialAnalysis.validate))
