# Facial Analysis DeepFace Viam Module 

![emotions](https://github.com/ariellemella/facial-analysis/assets/105662831/f15b9772-4dbe-4012-8d74-48c5b8de0518)


_facial-analysis_ is a Viam modular vision service that uses the [DeepFace](https://github.com/serengil/deepface/) library to perform facial analysis. 

DeepFace is a lightweight facial attribute analysis and recognition framework for Python, and this Viam module allows you to deploy the Deepface module directly onto your robots and smart machines with Viam's Computer Vision service. 

The following attributes can be passed into this module: **age, gender, facial expression (emotion), and race**. The default mode for this module is **emotion**, but you can set other attributes in the Viam JSON config. 

## Prerequisites 

Python3 >= 3.11.7 


## Viam Service Configuration

The following attributes may be configured as facial-detector config attributes, one at a time: 
**demography**: "gender", "race", "emotion", or "age" 
**dominant_demography**: "dominant_gender", "dominant_race", "dominant_emotion", or "age"
<img width="615" alt="visionmodule" src="https://github.com/ariellemella/facial-analysis/assets/105662831/9d799482-19d4-44ee-8e39-b64da80553f9">

For example, 

```
{
  "demography": "emotion",
  "dominant_demography": "dominant_emotion"
}
```
### Demography 
DeepFace returns a full list of facial analysis output, however you can define which demography you would like to see on your detection bounding boxes. The Viam vision service module returns the dominant value specified, which takes the highest value of a certain output and determines that as the emotion/age/gender/race of the person.

#### Returns:
results: A list of dictionaries, where each dictionary represents the analysis results for a detected face. Example:
```
{
     "age": 27.66,
     "dominant_emotion": "neutral",
     "emotion": {
                'sad': 37.65260875225067,
                'angry': 0.15512987738475204,
                'surprise': 0.0022171278033056296,
                'fear': 1.2489334680140018,
                'happy': 4.609785228967667,
                'disgust': 9.698561953541684e-07,
                'neutral': 56.33133053779602
                 }
     "dominant_gender": "woman",
     "gender": {
                'woman': 99.99407529830933,
                'man': 0.005928758764639497,
               }
     "dominant_race": "latino hispanic",
     "race": {
                'indian': 0.5480832420289516,
                'asian': 0.7830780930817127,
                'latino hispanic': 93.0677512511610985,
                'black': 0.06337375962175429,
                'middle eastern': 3.088453598320484,
                'white': 2.44925880432129
              }
```
