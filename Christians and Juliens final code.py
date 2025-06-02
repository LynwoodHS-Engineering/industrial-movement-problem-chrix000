#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
claw_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
# AI Vision Color Descriptions
ai_vision_5__BlueBox = Colordesc(1, 25, 77, 108, 24, 0.25)
ai_vision_5__GreenBall = Colordesc(2, 72, 190, 72, 24, 0.28)
# AI Vision Code Descriptions
ai_vision_5 = AiVision(Ports.PORT5, ai_vision_5__BlueBox, ai_vision_5__GreenBall)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

from vex import *
import urandom

brain = Brain()

left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
claw_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)

ai_vision_5__BlueBox = Colordesc(1, 25, 77, 108, 24, 0.25)
ai_vision_5__GreenBall = Colordesc(2, 72, 190, 72, 24, 0.28)
ai_vision_5 = AiVision(Ports.PORT5, ai_vision_5__BlueBox, ai_vision_5__GreenBall)

wait(30, MSEC)

def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))

initializeRandomSeed()

def play_vexcode_sound(sound_name):
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

wait(200, MSEC)
print("\033[2J")

# Set speeds
drivetrain.set_drive_velocity(30, PERCENT)
drivetrain.set_turn_velocity(30, PERCENT)
arm_motor.set_velocity(50, PERCENT)
claw_motor.set_velocity(50, PERCENT)

# Target bounding box properties with tolerance
TARGET_CENTER_X = 130
TARGET_CENTER_Y = 220
TARGET_WIDTH = 225
TARGET_HEIGHT = 40
TOLERANCE = 10  # pixels

def is_target_position(obj):
    return (
        abs(obj.centerX - TARGET_CENTER_X) <= TOLERANCE and
        abs(obj.centerY - TARGET_CENTER_Y) <= TOLERANCE and
        abs(obj.width - TARGET_WIDTH) <= TOLERANCE and
        abs(obj.height - TARGET_HEIGHT) <= TOLERANCE
    )

def perform_task():
    drivetrain.drive_for(FORWARD, 60, INCHES)
    claw_motor.spin_for(REVERSE, 200, DEGREES)
    arm_motor.spin_for(FORWARD, 100, DEGREES)

    # Vision loop to find and approach ball
    while True:
        ai_vision_5_objects = ai_vision_5.take_snapshot(ai_vision_5__GreenBall)

        if ai_vision_5_objects[0].exists:
            if ai_vision_5_objects[0].centerX > 190:
                drivetrain.turn_for(RIGHT, 3, DEGREES)
            elif ai_vision_5_objects[0].centerX < 130:
                drivetrain.turn_for(LEFT, 3, DEGREES)
            else:
                if not is_target_position(ai_vision_5_objects[0]):
                    drivetrain.drive(FORWARD)
                else:
                    drivetrain.stop()
                    claw_motor.spin_for(FORWARD, 90, DEGREES)
                    break
        else:
            drivetrain.stop()

        wait(5, MSEC)

    # Part 2: Deliver and reset
    drivetrain.drive_for(REVERSE, 10, INCHES)
    wait(1.5, SECONDS)

    arm_motor.spin_for(REVERSE, 100, DEGREES)
    wait(1, SECONDS)

    drivetrain.turn_for(LEFT, 220, DEGREES)
    wait(2, SECONDS)

    drivetrain.drive_for(FORWARD, 80, INCHES)
    wait(1, SECONDS)

    arm_motor.spin_for(FORWARD, 760, DEGREES)
    wait(1, SECONDS)

    drivetrain.drive_for(FORWARD, 35, INCHES)
    arm_motor.spin_for(REVERSE, 110, DEGREES)
    claw_motor.spin_for(FORWARD, 150, DEGREES)
    wait(0.5, SECONDS)

    claw_motor.spin_for(REVERSE, 150, DEGREES)
    wait(0.5, SECONDS)

    arm_motor.spin_for(FORWARD, 110, DEGREES)
    wait(1, SECONDS)

    drivetrain.drive_for(REVERSE, 15, INCHES)
    wait(1, SECONDS)

    arm_motor.spin_for(REVERSE, 780, DEGREES)
    wait(2, SECONDS)

    drivetrain.turn_for(RIGHT, 190, DEGREES)
    drivetrain.drive_for(FORWARD, 20, INCHES)

while True:
    perform_task()
