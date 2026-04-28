# import socket
# import json
# from wpilib import TimedRobot, PWMVictorSPX

# class Robot(TimedRobot):

#     def robotInit(self):
#         self.left_motor = PWMVictorSPX(0)
#         self.right_motor = PWMVictorSPX(1)

#         self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server.bind(("0.0.0.0", 12345))
#         self.server.listen(1)

#         print("Waiting for Jetson...")
#         self.conn, _ = self.server.accept()
#         print("Connected!")

#     def teleopPeriodic(self):
#         try:
#             data = self.conn.recv(1024).decode()
#             if data:
#                 for line in data.strip().split("\n"):
#                     cmd = json.loads(line)

#                     left = float(cmd["left"])
#                     right = float(cmd["right"])

#                     self.left_motor.set(left)
#                     self.right_motor.set(right)

#         except:
#             pass