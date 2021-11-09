# -*- coding: utf-8 -*-

# 라즈베리파이 GPIO 패키지 
import RPi.GPIO as GPIO
from time import sleep

# 모터 상태
STOP  = 0
FORWARD  = 1
BACKWARD = 2

# 모터 채널
CH1 = 0

# PIN 입출력 설정
OUTPUT = 1
INPUT = 0

# PIN 설정
HIGH = 1
LOW = 0

# 실제 핀 정의
#PWM PIN
ENA = 5    # BCM5 29 pin
ENB = 27   # BCM27 13 pin

#GPIO PIN
IN1 = 21   # BCM11 23 pin
IN2 = 20    # BCM9 21 pin

#모터 클래스
class motor:
    def __init__(self, inPin1, inPin2, enAPin, enBPin):        
        # GPIO 모드 설정 
        GPIO.setmode(GPIO.BCM)
        # pin을 채널당 그룹으로 저장
        self.motorPin = [[enAPin, inPin1, inPin2]]
        # pwm 변수
        self.pwm = []
        # ch1 핀 설정
        self.pwm.append(self.setPinConfig(CH1))
        # ch2 핀 설정

    # 핀 설정 함수
    def setPinConfig(self, ch):
        EN = self.motorPin[ch][0]
        INA = self.motorPin[ch][1]
        INB = self.motorPin[ch][2]

        GPIO.setup(EN, GPIO.OUT)
        GPIO.setup(INA, GPIO.OUT)
        GPIO.setup(INB, GPIO.OUT)
        # 100khz 로 PWM 동작 시킴 
        pwm = GPIO.PWM(EN, 100) 
        # 우선 PWM 멈춤.   
        pwm.start(0) 
        return pwm

    # 모터 제어 함수
    def setMotorControl(self, ch, speed, stat):        
        EN = self.motorPin[ch][0]
        INA = self.motorPin[ch][2]
        INB = self.motorPin[ch][1] #motor backward 2

        #모터 속도 제어 PWM
        self.pwm[ch].ChangeDutyCycle(speed)  
        
        if stat == FORWARD:
            GPIO.output(INA, HIGH)
            GPIO.output(INB, LOW)
            
        #뒤로
        elif stat == BACKWARD:
            GPIO.output(INA, LOW)
            GPIO.output(INB, HIGH)
            
        #정지
        elif stat == STOP:
            GPIO.output(INA, LOW)
            GPIO.output(INB, LOW)
            
   

            
    # 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
    def setMotor(self, ch, speed, stat):
        self.setMotorContorl(self.pwm[ch], self.motorPin[ch][1], speed, stat)

    def __del__(self):
        # 종료
        GPIO.cleanup()
        
class surbo:
    def __init__ (self, pin, hz):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        
        self.p = GPIO.PWM(pin, hz) # 50 Hz
        self.p.start(0)
        
    def doAngle(self, angle):
        self.p.ChangeDutyCycle(angle)  

