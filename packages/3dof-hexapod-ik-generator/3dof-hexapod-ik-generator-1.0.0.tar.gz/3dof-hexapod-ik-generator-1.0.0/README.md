This is a simple Python package for hexapod IK calculations.

Commands:

To be imported as ikengine

class IKEngine # initialises the class object. Takes 4 arguments in mm - coxaLength, femurLength, tibiaLength and bodySideLength. Optionally can take a 5th argument that can either be a list or a tuple. Please pass the servos that need to be reversed into this tuple/list. They will be reversed (angle = 180 - angle) for the whole runtime of your program that utilises this library.

shift_lean(posX, posY, posZ, rotX, rotY, rotZ) # returns an array of 18 servo angles that are calculated using IK from the given variables that correspond to the translation and tilt of the body of the hexapod. The order goes from tibia to coxa, from left to right and then from front to back

Any questions or suggestions? Please feel free to contact me at macaquedev@gmail.com
