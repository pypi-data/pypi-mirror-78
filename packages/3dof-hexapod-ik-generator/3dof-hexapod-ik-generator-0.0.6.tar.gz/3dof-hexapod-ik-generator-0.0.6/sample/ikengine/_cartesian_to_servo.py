from math import cos, sin, tan, acos, atan, atan2, pi
sqrt = lambda x: x**0.5
"""
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
"""
