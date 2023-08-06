from sacramathengine import *
from State import State, StateError

class Movement: #Will add fixed values for specific keys, a,d,w,s.


    def __init__(self, Vector, MeshObject = None):
        if not isinstance(Vector, (vec3d, vec4d)):
            raise TypeError("[System]: Vector has to be of type vec3d, or vec4d.")
        self.Vector = Vector
        if MeshObject == None:
            print("[System]: Call the _setter method to add a MeshObject to the class.")

    def _setter(self, MeshObject):
        self.Mesh = MeshObject.Mesh()

    def _Move(self, Vector):
        return Movement(self.Vector, MeshObject)
