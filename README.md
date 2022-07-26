# Case study for KPMG
## Instructions
It’s March 2017. Rob, a (fictional?) KPMG employee living in Berlin, is very fond of his privacy – he lives moving in and out Airbnb’s and never shares his current address. He would like to invite a few D&A colleagues at his place for a dinner evening and decides to share the key features of his current rental: price, room_type, accommodates, bedrooms, bathrooms (see here for more information and to download historical Airbnb data).
The D&A team needs to figure out where Rob is most likely living. The task is therefore to create a model that, given a set of room features(price, room_type, accommodates, bedrooms, bathrooms), for a set of coordinates (latitude, longitude), calculates a score (up to you to define) that quantifies how likely it is that Rob is living at the given latitude-longitude.
We kindly ask you to submit your solution (the code) and a small note explaining the assumptions behind your model.

List of programming languages you are free to use: Python, Java, Scala, R, C#, F#, Go, C, C++, Haskell, Js/Typescript – pretty much anything but LISP dialects

## Solution
The model is rather simple given the limited information available to guess Rob's address. The number of Airbnb properties matching Rob's description within a certain radius around a set of coordinates is compared to the number of all properties matching the description. If this number is relatively high, it is more likely that his address is at these coordinates as if the number is low. It is asusmed that the properties of the apartment he gives are precise, except the price for which some margin is allowed for.

[sandbox.ipynb](./sandbox.ipynb) contains the R&D version of the code including graphs and an example result.

[most_likely_location.py](./most_likely_location.py) contains a simple Python app that runs the logic. The inputs are hardcoded as global variables on top of the file. Further configurables are in [location.py](./location.py) - including with what resolution a solution is searched for.
