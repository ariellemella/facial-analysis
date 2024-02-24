# Facial Analysis DeepFace Viam Module 

![emotions](https://github.com/ariellemella/facial-analysis/assets/105662831/f15b9772-4dbe-4012-8d74-48c5b8de0518)


_facial-analysis_ is a Viam modular vision service that uses the [DeepFace](https://github.com/serengil/deepface/) library to perform facial analysis. 

DeepFace is a lightweight facial attribute analysis and recognition framework for Python, and this Viam module allows you to deploy the Deepface module directly onto your robots and smart machines with Viam's Computer Vision service. 

## Prerequisites 

Python3 >= 3.11.7 

## API
The facial-analysis resource provides the following methods from Viam's built-in rdk:service:vision API

### get_detections(image=binary)

### get_detections_from_camera(camera_name=string)

### Demography 
DeepFace returns a full list of facial analysis output and you can define which demography you would like to see on your detection bounding boxes. The Viam vision service module returns the dominant value specified. The default is 'emotion', but you may configure additioinal attributes according to the DeepFace Facial Attributes Analysis documentation. See more [here](https://github.com/serengil/deepface/). 

## Viam Service Configuration

Different demographies may be configured as facial-analysis config attributes, as according to the DeepFace doumentation.  

```
{
  "demography": "emotion"
}
```

