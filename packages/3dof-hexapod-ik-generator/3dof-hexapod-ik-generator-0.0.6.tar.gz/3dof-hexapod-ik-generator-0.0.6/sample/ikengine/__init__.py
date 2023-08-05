from math import cos, sin, tan, acos, atan, atan2, pi
sqrt = lambda x: x**0.5
class IKEngine:
	def __init__(self, coxaLength, femurLength, tibiaLength, bodySideLength): # Params to be given in millimetres. These equations only work with a hexapod with 3 degrees of freedom and legs spaced equally around the centre of the body.
		self._reversed_servos = [False for _ in range(18)]
		self._coxaLength = coxaLength
		self._femurLength = femurLength
		self._tibiaLength = tibiaLength
		self._bodySideLength = bodySideLength

		self._bodyCenterOffset1 = bodySideLength >> 1
		self._bodyCenterOffset2 = sqrt(bodySideLength**2 - self._bodyCenterOffset1**2)

		self._bodyCenterOffsetX_1 = self._bodyCenterOffset1
		self._bodyCenterOffsetX_2 = bodySideLength
		self._bodyCenterOffsetX_3 = self._bodyCenterOffset1
		self._bodyCenterOffsetX_4 = -self._bodyCenterOffset1
		self._bodyCenterOffsetX_5 = bodySideLength
		self._bodyCenterOffsetX_6 = -self._bodyCenterOffset1

		self._bodyCenterOffsetY_1 = self._bodyCenterOffset2
		self._bodyCenterOffsetY_2 = 0
		self._bodyCenterOffsetY_3 = -self._bodyCenterOffset2 
		self._bodyCenterOffsetY_4 = -self._bodyCenterOffset2
		self._bodyCenterOffsetY_5 = 0
		self._bodyCenterOffsetY_6 = self._bodyCenterOffset2

		self._feetPosX_1 = cos(60/180*pi)*(coxaLength + femurLength)
		self._feetPosZ_1 = tibiaLength
		self._feetPosY_1 = sin(60/180*pi) * (coxaLength + femurLength)

		self._feetPosX_2 = coxaLength + femurLength
		self._feetPosZ_2 = tibiaLength
		self._feetPosY_2 = 0

		self._feetPosX_3 = cos(60/180*pi)*(coxaLength + femurLength)
		self._feetPosZ_3 = tibiaLength
		self._feetPosY_3 = sin(-60/180*pi) * (coxaLength + femurLength)

		self._feetPosX_4 = -cos(60/180*pi)*(coxaLength + femurLength)
		self._feetPosZ_4 = tibiaLength
		self._feetPosY_4 = sin(-60/180*pi) * (coxaLength + femurLength)

		self._feetPosX_5 = -(coxaLength + femurLength)
		self._feetPosZ_5 = tibiaLength
		self._feetPosY_5 = 0

		self._feetPosX_6 = -cos(60/180*pi)*(coxaLength + femurLength)
		self._feetPosZ_6 = tibiaLength
		self._feetPosY_6 = sin(60/180*pi) * (coxaLength + femurLength)
	try:
		from ._reverse_servos import reverse_servos
		from ._shift_lean import shift_lean
		from ._cartesian_to_servo import cartesian_to_servo
	except Exception as e:
		print('This is a python package that works with hexapod robots. This is not an executable file, therefore it cannot be simply executed.')                                                       
		

if __name__ == '__main__':	
	pass