#include <DRV8835MotorShield.h>
#include <Servo.h>
DRV8835MotorShield motors;
Servo head;
const int debugLED = 13; 

//serial info

String state;
const String GROSS_STATE = "gross";
const String CONTENT_STATE = "content";
const String ROAM_STATE = "roam";
const String WAIT_STATE = "wait";
const String EXCITED_STATE = "excited";
const String DRUNK_STATE = "drunk";
const String CALIBRATE = "calibrate";
const String TURNAROUND = "turnaround";

//packet


// ir sensor pins
const int centerSONAR = A0;
const int leftIR = A1; 
const int rightIR = A2;

// adc value storage
int duration;
int centerSONARvalue;

int leftIRvalue;
int rightIRvalue;
//int frontLeftPWRvalue;
int backLeftPWRvalue;     
//int frontRightPWRvalue;    
int backRightPWRvalue; 

// ir threshold
int trapThreshIR;
int turnThreshIR;
const int TRAP = 400;
const int ROAM = 295;
const int WAIT = 400;

// motor driver constants
const int FORWARD = 1;
const int REVERSE = 0;

// io direction pins
//const int frontLeftDIR = 47;       // CH1
const int backLeftDIR = 7;        // CH2
//const int frontRightDIR = 51;      // CH3
const int backRightDIR = 8;       // CH4

// pwm pins
//const int frontLeftWHEEL = 3;      // CH1
const int backLeftWHEEL =  9;      // CH2
//const int frontRightWHEEL = 6;     // CH3
const int backRightWHEEL = 10;     // CH4
const int headSERVO = 11; 

// current pins
//const int frontLeftPWR = A8;       // CH1
//const int backLeftPWR = A9;        // CH2
//const int frontRightPWR = A10;     // CH3
//const int backRightPWR = A11;      // CH4

long randNum;

int count;
const int avgTotal = 50;
int leftIRval[avgTotal];
int leftIRavg;
int rightIRval[avgTotal];
int rightIRavg;

const int calibrationTotal = 100;
const int calibrationDuration = 5000; //seconds
int calibrationValues[calibrationTotal];

long microsecondsToInches(long microseconds) {
  // According to Parallax's datasheet for the PING))), there are
  // 73.746 microseconds per inch (i.e. sound travels at 1130 feet per
  // second).  This gives the distance travelled by the ping, outbound
  // and return, so we divide by 2 to get the distance of the obstacle.
  // See: http://www.parallax.com/dl/docs/prod/acc/28015-PING-v1.3.pdf
  return microseconds / 74 / 2;
}

void getSonarMeasurement() {
  pinMode(centerSONAR, OUTPUT);
  digitalWrite(centerSONAR, LOW);
  delayMicroseconds(2);
  digitalWrite(centerSONAR, HIGH);
  delayMicroseconds(5);
  digitalWrite(centerSONAR, LOW);
  pinMode(centerSONAR, INPUT);
  duration = pulseIn(centerSONAR, HIGH);
  centerSONARvalue = microsecondsToInches(duration);
}

void calcMovAvg() {
    for (int n = 0; n < avgTotal; n++)
  {
    leftIRvalue = analogRead(leftIR);
    rightIRvalue = analogRead(rightIR);
    leftIRval[n] = leftIRvalue;
    rightIRval[n] = rightIRvalue;
  }

  leftIRavg = 0;
  rightIRavg = 0;
  
  for (int n = 0; n < avgTotal; n++)
  {
    leftIRavg = leftIRavg + leftIRval[n];
    rightIRavg = rightIRavg + rightIRval[n];
  }

  leftIRvalue = leftIRavg/avgTotal;
  rightIRvalue = rightIRavg/avgTotal;
}


void turnHead(int deg) {
  head.write(deg);
}

void neutral() {

  motors.flipM1(!false);
  motors.setM1Speed(0);
  motors.flipM2(!false);
  motors.setM2Speed(0);
}

void forward(int s) {

 
  motors.flipM1(!true);
  motors.setM1Speed(s);
  motors.flipM2(!false);
  motors.setM2Speed(s);

}

void reverse(int s) {

  
  motors.flipM1(!false);
  motors.setM1Speed(s);
  motors.flipM2(!true);
  motors.setM2Speed(s);

}

void turnLeft(int s) {
  motors.flipM1(!false);
  motors.setM1Speed(s);
  motors.flipM2(!false);
  motors.setM2Speed(s);
}


void turnRight(int s) {
  motors.flipM1(!true);
  motors.setM1Speed(s);
  motors.flipM2(!true);
  motors.setM2Speed(s);

}

int offsetFL(int s){
  return s;
}

int offsetFR(int s){
  return s - 2;
}

int offsetBL(int s){
  return s + 15;
}

int offsetBR(int s){
  return s + 3;
}

void content() {
  forward(150);
  delay(500);
  reverse(150);
  delay(500);
    forward(150);
  delay(500);
  reverse(150);
  delay(500);
  
}

void drunk () {
  
    randNum = random(0,10);
    randNum = randNum % 2;
    
    if (randNum == 0) {
      /*
      while (leftIRvalue>trapThreshIR || rightIRvalue>trapThreshIR) {
        turnLeft(200);
        calcMovAvg();
      }
      */
      turnHead(0);
      turnLeft(200);
      delay(300);
            forward(350);
      delay(30);
            turnLeft(200);
      delay(300);
      turnHead(180);
           forward(350);
      delay(300);
      turnHead(118);
      delay(3000);
       turnHead(45);
            turnLeft(200);
      delay(3000);

    }
    else {
      /*
      while (leftIRvalue>trapThreshIR || rightIRvalue>trapThreshIR) {
        turnRight(200);
        calcMovAvg();
      }
      */
      turnRight(200);
      delay(3000);
    }  
}

void excited() {
  
    turnLeft(300);
    delay(6000);
  
}

void roam() {
  
  int trapThreshIR = TRAP;
  int turnThreshIR = ROAM;

  randNum = random(0,10);
  randNum = randNum % 2;
  
  if (leftIRvalue>trapThreshIR || rightIRvalue>trapThreshIR || centerSONARvalue < 2) {
    digitalWrite(debugLED, LOW);
    reverse(200);
    //turnHead(80);
    delay(250);
    //turnHead(100);
    delay(250);
    turnHead(90);
    
    if (randNum == 0) {
      turnLeft(200);
      delay(1000);
    }
    else {
      turnRight(200);
      delay(1000);
    }
//materials 3d printing lab
  } 
  else if (leftIRvalue>turnThreshIR) {
    turnRight(250);
    turnHead(105);
    delay(300);
    forward(300);
    delay(100);
  }
  else if (rightIRvalue>turnThreshIR) {
    turnLeft(250);
    turnHead(75);
    delay(300);
    forward(300);
    delay(100);
  }
  else if (centerSONARvalue<5) {
    if (randNum == 0) {
      turnLeft(200);
      delay(500);
      //turnHead(110);
      forward(300);
      delay(100);
    }
    else {
      turnRight(200);
      delay(500);
      //turnHead(70);
      forward(300);
      delay(100);
    }
  }
  else {
   forward(200);
   turnHead(90);
  } 
  
}

void wait() {

  int turnThreshIR = WAIT;

  if (leftIRvalue>turnThreshIR) {
    turnRight(150);
    turnHead(110);
    delay(50);
  }
  else if (rightIRvalue>turnThreshIR) {
    turnLeft(150);
    turnHead(60);
    delay(50);
  }
  else if (centerSONARvalue<2) {
    reverse(180);
    delay(300);
    forward(100);
    delay(100);
  }
  else {
   neutral();
   //randNum = random(0,180);
   turnHead(90);
  } 
  
}

void gross() {
  reverse(100);
  turnHead(70);
  delay(500);
  turnHead(110);
  delay(500);
  turnHead(70);
  delay(500);
  turnHead(90);
  delay(1000);
}

void turnaround() {
  reverse(100);
  turnHead(70);
  delay(500);
  reverse(300);
  delay(500);
  turnLeft(200);
  delay(3000);
  turnHead(90);
}

void serialEvent(){
  state = Serial.readString();
  state.trim();
}

void setup() {
  
  pinMode(debugLED, OUTPUT);  

  // set all motor pins
  //pinMode(frontRightDIR, OUTPUT);
  //pinMode(frontLeftDIR, OUTPUT);
  pinMode(backRightDIR, OUTPUT);
  pinMode(backLeftDIR, OUTPUT);
  pinMode(centerSONAR, OUTPUT);
  head.attach(headSERVO);

  Serial.begin(115200);
  randomSeed(analogRead(A2));

  state = "roam";
  count = 0;
}

void loop() {

  delay(25);
  
  getSonarMeasurement();
  calcMovAvg();       

  if (state.equals(ROAM_STATE)) {
    roam();
  }
  else if (state.equals(WAIT_STATE)) {
    wait();
  }
  else if (state.equals(EXCITED_STATE)) {
    excited();
    state = "wait";
  }
  else if (state.equals(DRUNK_STATE)) {
    drunk();
    state = "wait";
  }
  else if (state.equals(GROSS_STATE)) {
    gross();
    state = "wait";
  }
  else if (state.equals(CONTENT_STATE)) {
    content();
    state = "wait";
  }
  else if (state.equals(TURNAROUND)) {
    turnaround();
    state = "wait";
  }
  else {
    state = "wait";
  }

  //debugging
  if (count > 20) {
    /*
    Serial.print("Current state: ");
    Serial.println(state);
    Serial.print("Left IR: ");
    Serial.println(leftIRvalue);
    Serial.print("Right IR: ");
    Serial.println(rightIRvalue);
    Serial.print("Center SONAR: ");
    Serial.println(centerSONARvalue);
    */
    count = 0;
  }
  count++;
  
}
