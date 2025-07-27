//Define chan motor
#define PWM_right D1
#define PWM_left D2

#define motorL1 D5   
#define motorL2 D6   

#define motorR1 D3
#define motorR2 D4 

int motor_speed = 150;


void setup() {
  Serial.begin(9600);
  pinMode(PWM_right, OUTPUT);
  pinMode(PWM_left, OUTPUT);
  pinMode(motorL1, OUTPUT);
  pinMode(motorL2, OUTPUT);
  pinMode(motorR1, OUTPUT);
  pinMode(motorR2, OUTPUT);

}


void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    Serial.println("Đã nhận: " + data);
    
    if(data == "forward"){
      forward();
    }
    else if(data == "backward"){
      backward();
    }
    else if(data == "right"){
      right();
    }
    else if(data == "left"){
      left();
    }
    else{
      stop();
      }
    }
}


//=========================================================================================

void right(){
  rightmotor(motor_speed);
  leftmotor(-motor_speed);
}

void left(){
  rightmotor(-motor_speed);
  leftmotor(motor_speed);
}

void forward(){
  rightmotor(motor_speed);
  leftmotor(motor_speed);
}

void backward(){
  rightmotor(-motor_speed);
  leftmotor(-motor_speed);
}
//=========================================================================================================================================
//==================================Điều khiển motor bên phải==================================
void leftmotor(int speed){
  if(speed < 0){
    //Đi tiến
    analogWrite(PWM_left, -speed);
    digitalWrite(motorL1, LOW);
    digitalWrite(motorL2, HIGH);
  }
  else{
    //Đi lùi
    analogWrite(PWM_left, speed);
    digitalWrite(motorL1, HIGH);
    digitalWrite(motorL2, LOW);
  }
}

//==================================Điều khiển motor bên trái===================================
void rightmotor(int speed){
  if(speed >= 0){
    //Đi tiến
    analogWrite(PWM_right, speed);
    digitalWrite(motorR1, LOW);
    digitalWrite(motorR2, HIGH);
  }
  else{
    //Đi lùi
    analogWrite(PWM_right, -speed);
    digitalWrite(motorR1, HIGH);
    digitalWrite(motorR2, LOW);
  }
}

//=============================================Dừng xe========================================
void stop(){
  stop_left_motor();
  stop_right_motor();
}

void stop_left_motor(){
    digitalWrite(motorL1, LOW);
    digitalWrite(motorL2, LOW);
}

void stop_right_motor(){
    digitalWrite(motorR1, LOW);
    digitalWrite(motorR2, LOW);
}

