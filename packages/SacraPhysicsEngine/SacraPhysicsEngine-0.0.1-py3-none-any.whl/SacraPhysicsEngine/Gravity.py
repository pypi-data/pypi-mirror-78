from .State import State
from SacraMathEngine import * #Do not use this in final version. Need it right now for the mesh, and vector definitions.
from .State import State, StateError

global FPS

class GravityIssue(Exception):
    pass

class Gravity:
    GravityPull = 9.82

    GravityVector = vec3d(0, -self.GravityPull, 0)

    def __init__(self):
        pass

    def _setter(self, Object = None):
        if Object == None:
            raise TypeError("[System]: Gravity must have an object")
        elif is not isinstance(Object, State):
            raise TypeError("[System]: Gravity must have an State-object")
        else:
            try:
                self.Object = Object
                self.MeshObject = Object.Mesh
            except:
                raise TypeError("[System]: Cannot give attribute mesh from the state.")
        try:
            _Update()
        except:
            pass

    def _Update(self):#Add so that it can't go below the ground. Simple fix.
        NewMesh = self.MeshObject + self.GravityVector
        State = self.Object.state
        NewObject = State()
        return NewObject._setter(State, NewMesh)
