import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Keypad layout for 4x3
KEYS = [
    ['1','2','3'],
    ['4','5','6'],
    ['7','8','9'],
    ['*','0','#']
]

ROW_PINS = [4, 17, 27, 22] # Yellow, Blue, Gray, White
COL_PINS = [5, 6, 13] # Green, Purple, Black

GREEN_LED = 25
RED_LED = 21
BUZZER = 20
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)





# Setup keypad pins
for row in ROW_PINS:
    GPIO.setup(row, GPIO.OUT)
    GPIO.output(row, GPIO.LOW)

for col in COL_PINS:
    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Servo setup (update if your signal pin is different)
SERVO_PIN = 18 # Default PWM pin
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50) # 50Hz
pwm.start(0)

def unlock_servo():
    pwm.ChangeDutyCycle(7.5) # ~90°
    time.sleep(1)
    pwm.ChangeDutyCycle(2.5) # ~0°
    time.sleep(0.5)

def light_led(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(pin, GPIO.LOW)

def buzzer_beep(buzz):
    GPIO.output(buzz, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(buzz, GPIO.LOW)

def get_key():
    for i, row in enumerate(ROW_PINS):
        GPIO.output(row, GPIO.HIGH)
        for j, col in enumerate(COL_PINS):
            if GPIO.input(col) == GPIO.HIGH:
                GPIO.output(row, GPIO.LOW)
                return KEYS[i][j]
        GPIO.output(row, GPIO.LOW)
    return None


def clean_and_exit():
    pwm.stop()
    GPIO.cleanup()
    print("Servo exited flawlessly.")
    exit()


CORRECT_CODE = "1234"
code = ""
EXIT_CODE = "0000"


try:
    print("Enter code (press '#' to submit):")
    while True:
        key = get_key()
        if key:
            print("Pressed:", key)
            if key == '#':
                if code == EXIT_CODE:
                    print("Exit code entered. Stopping...")
                    break
                elif code == CORRECT_CODE:
                    print("✅ Correct! Unlocking...")
                    light_led(GREEN_LED)
                    unlock_servo()
                    clean_and_exit()
                else:
                    print("❌ Wrong code.")
                    light_led(RED_LED)
                    buzzer_beep(BUZZER)
                code = ""
            elif key == '*':
                print("Code cleared")
                code = ""
            else:
                code += key
            time.sleep(0.3) # debounce delay
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    pwm.stop()
    GPIO.cleanup()
    print("Servo and GPIO stopped cleangly.")
