from math import cos, sin, tan, acos, atan, atan2, pi, tau
sqrt = lambda x: x**0.5
class IKGenerator:
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
	from _reverse_servos import reverse_servos
	from _shift_lean import shift_lean
	def cartesian_to_servo(self, leg_number, posX, posY, posZ): # Leg numbers go from left to right, front to back (leg 0 is front left and leg 6 is back right). Positions are given in relation to the coxa servo of each leg
		self._coxaFeetDist = sqrt(posX**2 + posY**2)
		self._IKSW = sqrt((self._coxaFeetDist - self._coxaLength)**2 + posZ**2)
		self._IKA1 = atan((self._coxaFeetDist - self._coxaLength)/posZ)
		self._IKA2 = acos((self._tibiaLength**2 - self._femurLength**2 - self._IKSW**2)/(-2 * self._IKSW * self._femurLength))
		self._TAngle = acos((self._IKSW**2 - self._tibiaLength**2 - self._femurLength**2) / (-2 * self._femurLength * self._tibiaLength))
		self._tibiaAngle = 90 - self._TAngle * 180 / pi
		self._femurAngle = 90 - (self._IKA1 + self._IKA2) * 180/pi
		self._coxaAngle = 90 - atan2(posX, posY) * 180 / pi
		if leg_number == 0:
			self._coxaAngle -= 120
		elif leg_number == 1:
			self._coxaAngle -= 60
		elif leg_number == 2:
			self._coxaAngle -= 180
		elif leg_number == 4:
			self._coxaAngle -= 240
		elif leg_number == 5:
			self._coxaAngle += 60
		angles = [
			self._tibiaAngle,
			self._femurAngle,
			self._coxaAngle
		]
		for index, angle in enumerate(angles):
			if self._reversed_servos[index]==True:
				angle = 180-angle
		angles = [int(i+90) for i in angles]
		return angles
		

if __name__ == '__main__':	
	print('This is a python package that works with hexapod robots. This is not an executable file, therefore it cannot be simply executed.')                                                       