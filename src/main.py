import asyncio
import sys

from viam.module.module import Module
from viam.services.vision import VisionClient
from .facialAnalysis import facialAnalysis

async def main():
    module = Module.from_args()
    module.add_model_from_registry(VisionClient.SUBTYPE, facialAnalysis.MODEL)
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())
