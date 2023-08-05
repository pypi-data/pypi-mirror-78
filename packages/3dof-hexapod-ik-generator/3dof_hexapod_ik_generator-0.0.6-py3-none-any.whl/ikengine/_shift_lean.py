from math import cos, sin, tan, acos, atan, atan2, pi
sqrt = lambda x: x**0.5
def shift_lean(self, posX, posY, posZ, rotX, rotY, rotZ):
	try:
		self._totalY_1 = self._feetPosY_1 + self._bodyCenterOffsetY_1 + posY
		self._totalX_1 = self._feetPosX_1 + self._bodyCenterOffsetX_1 + posX
		self._distBodyCenterFeet_1 = sqrt(self._totalY_1**2 + self._totalX_1**2)
		self._angleBodyCenterX_1 = pi/2 - atan2(self._totalX_1, self._totalY_1)
		self._rollZ_1 = tan(rotZ * pi / 180) * self._totalX_1
		self._pitchZ_1 = tan(rotX * pi / 180) * self._totalY_1
		self._bodyIKX_1 = cos(self._angleBodyCenterX_1 + (rotY * pi/180)) * self._distBodyCenterFeet_1 - self._totalX_1
		self._bodyIKY_1 = (sin(self._angleBodyCenterX_1 + (rotY * pi/180)) * self._distBodyCenterFeet_1) - self._totalY_1
		self._bodyIKZ_1 = self._rollZ_1 + self._pitchZ_1

		self._totalY_2 = self._feetPosY_2 + self._bodyCenterOffsetY_2 + posY
		self._totalX_2 = self._feetPosX_2 + self._bodyCenterOffsetX_2 + posX
		self._distBodyCenterFeet_2 = sqrt(self._totalY_2**2 + self._totalX_2**2)
		self._angleBodyCenterX_2 = pi/2 - atan2(self._totalX_2, self._totalY_2)
		self._rollZ_2 = tan(rotZ * pi / 180) * self._totalX_2
		self._pitchZ_2 = tan(rotX * pi / 180) * self._totalY_2
		self._bodyIKX_2 = cos(self._angleBodyCenterX_2 + (rotY * pi/180)) * self._distBodyCenterFeet_2 - self._totalX_2
		self._bodyIKY_2 = (sin(self._angleBodyCenterX_2 + (rotY * pi/180)) * self._distBodyCenterFeet_2) - self._totalY_2
		self._bodyIKZ_2 = self._rollZ_2 + self._pitchZ_2

		self._totalY_3 = self._feetPosY_3 + self._bodyCenterOffsetY_3 + posY
		self._totalX_3 = self._feetPosX_3 + self._bodyCenterOffsetX_3 + posX
		self._distBodyCenterFeet_3 = sqrt(self._totalY_3**2 + self._totalX_3**2)
		self._angleBodyCenterX_3 = pi/2 - atan2(self._totalX_3, self._totalY_3)
		self._rollZ_3 = tan(rotZ * pi / 180) * self._totalX_3
		self._pitchZ_3 = tan(rotX * pi / 180) * self._totalY_3
		self._bodyIKX_3 = cos(self._angleBodyCenterX_3 + (rotY * pi/180)) * self._distBodyCenterFeet_3 - self._totalX_3
		self._bodyIKY_3 = (sin(self._angleBodyCenterX_3 + (rotY * pi/180)) * self._distBodyCenterFeet_3) - self._totalY_3
		self._bodyIKZ_3 = self._rollZ_3 + self._pitchZ_3

		self._totalY_4 = self._feetPosY_4 + self._bodyCenterOffsetY_4 + posY
		self._totalX_4 = self._feetPosX_4 + self._bodyCenterOffsetX_4 + posX
		self._distBodyCenterFeet_4 = sqrt(self._totalY_4**2 + self._totalX_4**2)
		self._angleBodyCenterX_4 = pi/2 - atan2(self._totalX_4, self._totalY_4)
		self._rollZ_4 = tan(rotZ * pi / 180) * self._totalX_4
		self._pitchZ_4 = tan(rotX * pi / 180) * self._totalY_4
		self._bodyIKX_4 = cos(self._angleBodyCenterX_4 + (rotY * pi/180)) * self._distBodyCenterFeet_4 - self._totalX_4
		self._bodyIKY_4 = (sin(self._angleBodyCenterX_4 + (rotY * pi/180)) * self._distBodyCenterFeet_4) - self._totalY_4
		self._bodyIKZ_4 = self._rollZ_4 + self._pitchZ_4

		self._totalY_5 = self._feetPosY_5 + self._bodyCenterOffsetY_5 + posY
		self._totalX_5 = self._feetPosX_5 + self._bodyCenterOffsetX_5 + posX
		self._distBodyCenterFeet_5 = sqrt(self._totalY_5**2 + self._totalX_5**2)
		self._angleBodyCenterX_5 = pi/2 - atan2(self._totalX_5, self._totalY_5)
		self._rollZ_5 = tan(rotZ * pi / 180) * self._totalX_5
		self._pitchZ_5 = tan(rotX * pi / 180) * self._totalY_5
		self._bodyIKX_5 = cos(self._angleBodyCenterX_5 + (rotY * pi/180)) * self._distBodyCenterFeet_5 - self._totalX_5
		self._bodyIKY_5 = (sin(self._angleBodyCenterX_5 + (rotY * pi/180)) * self._distBodyCenterFeet_5) - self._totalY_5
		self._bodyIKZ_5 = self._rollZ_5 + self._pitchZ_5

		self._totalY_6 = self._feetPosY_6 + self._bodyCenterOffsetY_6 + posY
		self._totalX_6 = self._feetPosX_6 + self._bodyCenterOffsetX_6 + posX
		self._distBodyCenterFeet_6 = sqrt(self._totalY_6**2 + self._totalX_6**2)
		self._angleBodyCenterX_6 = pi/2 - atan2(self._totalX_6, self._totalY_6)
		self._rollZ_6 = tan(rotZ * pi / 180) * self._totalX_6
		self._pitchZ_6 = tan(rotX * pi / 180) * self._totalY_6
		self._bodyIKX_6 = cos(self._angleBodyCenterX_6 + (rotY * pi/180)) * self._distBodyCenterFeet_6 - self._totalX_6
		self._bodyIKY_6 = (sin(self._angleBodyCenterX_6 + (rotY * pi/180)) * self._distBodyCenterFeet_6) - self._totalY_6
		self._bodyIKZ_6 = self._rollZ_6 + self._pitchZ_6

		self._newPosX_1 = self._feetPosX_1 + posX + self._bodyIKX_1
		self._newPosY_1 = self._feetPosY_1 + posY + self._bodyIKY_1
		self._newPosZ_1 = self._feetPosZ_1 + posZ + self._bodyIKZ_1
		self._coxaFeetDist_1 = sqrt(self._newPosX_1**2 + self._newPosY_1**2)
		self._IKSW_1 = sqrt((self._coxaFeetDist_1 - self._coxaLength)**2 + self._newPosZ_1**2)
		self._IKA1_1 = atan((self._coxaFeetDist_1 - self._coxaLength)/self._newPosZ_1)
		self._IKA2_1 = acos((self._tibiaLength**2 - self._femurLength**2 - self._IKSW_1**2)/(-2 * self._IKSW_1 * self._femurLength))
		self._TAngle_1 = acos((self._IKSW_1**2 - self._tibiaLength**2 - self._femurLength**2) / (-2 * self._femurLength * self._tibiaLength))
		self._IKTibiaAngle_1 = 90 - self._TAngle_1 * 180 / pi
		self._IKFemurAngle_1 = 90 - (self._IKA1_1 + self._IKA2_1) * 180/pi
		self._IKCoxaAngle_1 = 90 - atan2(self._newPosX_1, self._newPosY_1) * 180 / pi

		self._newPosX_2 = self._feetPosX_2 + posX + self._bodyIKX_2
		self._newPosY_2 = self._feetPosY_2 + posY + self._bodyIKY_2
		self._newPosZ_2 = self._feetPosZ_2 + posZ + self._bodyIKZ_2
		self._coxaFeetDist_2 = sqrt(self._newPosX_2**2 + self._newPosY_2**2)
		self._IKSW_2 = sqrt((self._coxaFeetDist_2 - self._coxaLength)**2 + self._newPosZ_2**2)
		self._IKA1_2 = atan((self._coxaFeetDist_2 - self._coxaLength)/self._newPosZ_2)
		self._IKA2_2 = acos((self._tibiaLength**2 - self._femurLength**2 - self._IKSW_2**2)/(-2 * self._IKSW_2 * self._femurLength))
		self._TAngle_2 = acos((self._IKSW_2**2 - self._tibiaLength**2 - self._femurLength**2) / (-2 * self._femurLength * self._tibiaLength))
		self._IKTibiaAngle_2 = 90 - self._TAngle_2 * 180 / pi
		self._IKFemurAngle_2 = 90 - (self._IKA1_2 + self._IKA2_2) * 180/pi
		self._IKCoxaAngle_2 = 90 - atan2(self._newPosX_2, self._newPosY_2) * 180 / pi

		self._newPosX_3 = self._feetPosX_3 + posX + self._bodyIKX_3
		self._newPosY_3 = self._feetPosY_3 + posY + self._bodyIKY_3
		self._newPosZ_3 = self._feetPosZ_3 + posZ + self._bodyIKZ_3
		self._coxaFeetDist_3 = sqrt(self._newPosX_3**2 + self._newPosY_3**2)
		self._IKSW_3 = sqrt((self._coxaFeetDist_3 - self._coxaLength)**2 + self._newPosZ_3**2)
		self._IKA1_3 = atan((self._coxaFeetDist_3 - self._coxaLength)/self._newPosZ_3)
		self._IKA2_3 = acos((self._tibiaLength**2 - self._femurLength**2 - self._IKSW_3**2)/(-2 * self._IKSW_3 * self._femurLength))
		self._TAngle_3 = acos((self._IKSW_3**2 - self._tibiaLength**2 - self._femurLength**2) / (-2 * self._femurLength * self._tibiaLength))
		self._IKTibiaAngle_3 = 90 - self._TAngle_3 * 180 / pi
		self._IKFemurAngle_3 = 90 - (self._IKA1_3 + self._IKA2_3) * 180/pi
		self._IKCoxaAngle_3 = 90 - atan2(self._newPosX_3, self._newPosY_3) * 180 / pi

		self._newPosX_4 = self._feetPosX_4 + posX + self._bodyIKX_4
		self._newPosY_4 = self._feetPosY_4 + posY + self._bodyIKY_4
		self._newPosZ_4 = self._feetPosZ_4 + posZ + self._bodyIKZ_4
		self._coxaFeetDist_4 = sqrt(self._newPosX_4**2 + self._newPosY_4**2)
		self._IKSW_4 = sqrt((self._coxaFeetDist_4 - self._coxaLength)**2 + self._newPosZ_4**2)
		self._IKA1_4 = atan((self._coxaFeetDist_4 - self._coxaLength)/self._newPosZ_4)
		self._IKA2_4 = acos((self._tibiaLength**2 - self._femurLength**2 - self._IKSW_4**2)/(-2 * self._IKSW_4 * self._femurLength))
		self._TAngle_4 = acos((self._IKSW_4**2 - self._tibiaLength**2 - self._femurLength**2) / (-2 * self._femurLength * self._tibiaLength))
		self._IKTibiaAngle_4 = 90 - self._TAngle_4 * 180 / pi
		self._IKFemurAngle_4 = 90 - (self._IKA1_4 + self._IKA2_4) * 180/pi
		self._IKCoxaAngle_4 = 90 - atan2(self._newPosX_4, self._newPosY_4) * 180 / pi

		self._newPosX_5 = self._feetPosX_5 + posX + self._bodyIKX_5
		self._newPosY_5 = self._feetPosY_5 + posY + self._bodyIKY_5
		self._newPosZ_5 = self._feetPosZ_5 + posZ + self._bodyIKZ_5
		self._coxaFeetDist_5 = sqrt(self._newPosX_5**2 + self._newPosY_5**2)
		self._IKSW_5 = sqrt((self._coxaFeetDist_5 - self._coxaLength)**2 + self._newPosZ_5**2)
		self._IKA1_5 = atan((self._coxaFeetDist_5 - self._coxaLength)/self._newPosZ_5)
		self._IKA2_5 = acos((self._tibiaLength**2 - self._femurLength**2 - self._IKSW_5**2)/(-2 * self._IKSW_5 * self._femurLength))
		self._TAngle_5 = acos((self._IKSW_5**2 - self._tibiaLength**2 - self._femurLength**2) / (-2 * self._femurLength * self._tibiaLength))
		self._IKTibiaAngle_5 = 90 - self._TAngle_5 * 180 / pi
		self._IKFemurAngle_5 = 90 - (self._IKA1_5 + self._IKA2_5) * 180/pi
		self._IKCoxaAngle_5 = 90 - atan2(self._newPosX_5, self._newPosY_5) * 180 / pi

		self._newPosX_6 = self._feetPosX_6 + posX + self._bodyIKX_6
		self._newPosY_6 = self._feetPosY_6 + posY + self._bodyIKY_6
		self._newPosZ_6 = self._feetPosZ_6 + posZ + self._bodyIKZ_6
		self._coxaFeetDist_6 = sqrt(self._newPosX_6**2 + self._newPosY_6**2)
		self._IKSW_6 = sqrt((self._coxaFeetDist_6 - self._coxaLength)**2 + self._newPosZ_6**2)
		self._IKA1_6 = atan((self._coxaFeetDist_6 - self._coxaLength)/self._newPosZ_6)
		self._IKA2_6 = acos((self._tibiaLength**2 - self._femurLength**2 - self._IKSW_6**2)/(-2 * self._IKSW_6 * self._femurLength))
		self._TAngle_6 = acos((self._IKSW_6**2 - self._tibiaLength**2 - self._femurLength**2) / (-2 * self._femurLength * self._tibiaLength))
		self._IKTibiaAngle_6 = 90 - self._TAngle_6 * 180 / pi
		self._IKFemurAngle_6 = 90 - (self._IKA1_6 + self._IKA2_6) * 180/pi
		self._IKCoxaAngle_6 = 90 - atan2(self._newPosX_6, self._newPosY_6) * 180 / pi

		self._coxaAngle_1 = self._IKCoxaAngle_1 - 60
		self._femurAngle_1 = self._IKFemurAngle_1
		self._tibiaAngle_1 = self._IKTibiaAngle_1

		self._coxaAngle_2 = self._IKCoxaAngle_2
		self._femurAngle_2 = self._IKFemurAngle_2
		self._tibiaAngle_2 = self._IKTibiaAngle_2

		self._coxaAngle_3 = self._IKCoxaAngle_3 + 60
		self._femurAngle_3 = self._IKFemurAngle_3
		self._tibiaAngle_3 = self._IKTibiaAngle_3

		self._coxaAngle_4 = self._IKCoxaAngle_4 - 240
		self._femurAngle_4 = self._IKFemurAngle_4
		self._tibiaAngle_4 = self._IKTibiaAngle_4

		self._coxaAngle_5 = self._IKCoxaAngle_5 - 180
		self._femurAngle_5 = self._IKFemurAngle_5
		self._tibiaAngle_5 = self._IKTibiaAngle_5

		self._coxaAngle_6 = self._IKCoxaAngle_6 - 120
		self._femurAngle_6 = self._IKFemurAngle_6
		self._tibiaAngle_6 = self._IKTibiaAngle_6
	except Exception as e:
		return None
	angles = [
		self._tibiaAngle_6, 
		self._femurAngle_6, 
		self._coxaAngle_6, 
		self._tibiaAngle_1, 
		self._femurAngle_1, 
		self._coxaAngle_1,
		self._tibiaAngle_5, 
		self._femurAngle_5, 
		self._coxaAngle_5,
		self._tibiaAngle_2, 
		self._femurAngle_2, 
		self._coxaAngle_2,
		self._tibiaAngle_4, 
		self._femurAngle_4, 
		self._coxaAngle_4,
		self._tibiaAngle_3, 
		self._femurAngle_3, 
		self._coxaAngle_3,
	]
	for index, angle in enumerate(angles):
		if self._reversed_servos[index]==True:
			angle = 180-angle
	angles = [int(i+90) for i in angles]
	return angles