def reverse_servos(self, *servonums): 
    # Pass the servo numbers to be reversed as seperate arguments (not as a tuple). The servo numbering system goes: tibia to coxa, left to right, front to back, so servo 0 is the front left tibia and servo 17 is the back right coxa. 
    for i in servonums:
        self._reversed_servos[i] = True