import SacraMathEngine
from math import sin, cos, tan, pi
from random import randint

class StateError(Exception):
    pass


#Make a decorator that adds gravity as attribute...


class State:
    #This can actually be a dictonary and then lists inside, so each instance is stored in a list within a dictionary.
    ActiveMeshes = []
    AllSolid = []
    AllPlayers = []
    AllMovableObjects = []
    AllProjectiles = []
    Ground = []
    Detail = 10

    def __init__(self):
        self.States = {
        "Solid" : "Solid",
        "NonSolid": "NonSolid",
        "Projectile": "Projectile",
        "MovableObject": "MovableObject",
        "Player" : "Player",
        "Ground": "Ground"}
    #These should be functions...


    def _setter(self, state = None, Mesh = None):
        if state == None:
            raise StateError("[System]: Each object needs a state.")
        elif state == "ground" or "Ground":
            pass
        else:
            try:
                for key in self.States.keys():
                    if state == self.States(key):
                        self.state = self.States(key) #Implement the above mentioned about dictionaries.
                    else:
                        pass
                    #Needs a small remake
            except:
                raise StateError("[System]: Cannot load a state for the object.")
            if Mesh == None:
                raise StateError("[System]: Each State-Object needs a mesh; Refer to SacraMathEngine.Mesh .")
            else:
                if isinstance(Mesh, MeshObject): #Might need to rework that line
                    self.Mesh = Mesh.Mesh
                    self.ActiveMeshes.append(self.Mesh)
                else:
                    raise StateError("[System]: State-Objects need MeshObjects as input in the _setter function.")
            try:
                self._CenterOfMass()
            except:
                raise StateError("[System]: Cannot compute center of mass, fault is in _setter method.")

    def MakeGroundPer(self, Size = (100,100), Name = "PerinGround"):
        """ Size have to be a tuple that describes the size of the terrain. """
        #Can be improved, ran into the issue of having RecursionError($0) when doing it any other way.
        #Tried increasing the recursion depth but didn't fix the issue.
        Mesh = []
        self.state = "Solid"
        for i in range((Size[0])+1):
            FirstSet = []
            for k in range((Size[1])+1):
                FirstSet.append(SacraMathEngine.vec3d(i,0,k))
            Mesh.append(FirstSet)
        for i in range(1, len(Mesh)):
            for k in range(1, len(Mesh[i])):
                value = randint(Mesh[i-1][k].y - 2, Mesh[i][k-1].y + 2)
                Mesh[i][k].y = value
        Ground = SacraMathEngine.MeshObject()
        for i in range(0, len(Mesh)-1):
            for k in range(0, len(Mesh)-1):
                Ground = Ground + SacraMathEngine.Triangle(Mesh[i][k], Mesh[i+1][k], Mesh[i][k+1])
        Ground.SaveToJson(Name)


    def _CenterOfMass(self):
        """A function that is called when using _setter method; Provides the center of mass of that mesh aswell as computing the largest offset."""
        if  isinstance(self.Mesh, (list, tuple)):
            try:
                Colletion = []
                for tri in self.Mesh:
                    CenterOfTriangle = 1/3 * (tri[0] + tri[1] + tri[2])
                    Collection.append(CenterOfTriangle)
                CenterOfMass = vec3d(0, 0, 0)
                for i in range(len(Collection)):
                    CenterOfMass += Collection[i]
                self.CenterOfMass = CenterOfMass / len(Collection)
                try:
                    def Maximum(*args):
                        for i in range(len(args)):
                            if not isinstance(args[i], Triangle):
                                raise TypeError("[System]: The input in Maximum function is not of correct format.")
                        MaxNorms = []
                        for tri in args:
                            vec1 = (self.CenterOfMass - tri[0]).norm()
                            vec2 = (self.CenterOfMass - tri[1]).norm()
                            vec3 = (self.CenterOfMass - tri[2]).norm()
                            NormsOfTri_i = [vec1, vec2, vec3]
                            MaxNorms.append(max(NormsOfTri_i))
                        self.MaxNorm = max(MaxNorms)

                    #compute the largest vector, then apply a rotation to that vector so it covers 360 degress around
                except:
                    raise StateError("[System]: Can't compute the radius")
            except:
                raise StateError("[System]: Can not compute center of mass.")
        else:
            raise TypeError("[System]: Can not load the center of mass, due to Type-Error of the mesh.")



    def _Collision(self, Other):
        try:
            if isinstance(Other, State) and Other.state == "Solid" or isinstance(Other, State) and Other.state == "MovableObject" or isinstance(Other, State) and Other.state == "Player":
                Distance = (self.CenterOfMass - Other.CenterOfMass).norm()
                Radius = self.MaxNorm + Other.MaxNorm
                #Need to add __lq__ to vectors..., Made a temporary fix
                if Distance < Radius: #Might have to invert sign of inequality
                    if Other.State == "Projectile":
                        del Other #This line might not work.
                    return True
                else:
                    return False
            else:
                raise StateError("[System]: Can not compute _Collision method, The object is not of correct 'State'.")
        except:
            raise StateError("[System]: Can not compute _Collision method.")


    def __str__(self):
        return f'{self.state}'

    def __repr__(self):
        return f'{self.state}'

Ground = State().MakeGroundPer(Size = (10,10), Name='TestOfGround')
