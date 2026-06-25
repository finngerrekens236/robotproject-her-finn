// ===============================
// Conveyor Controller Arduino (STATE MACHINE)
// ===============================

// Motor pins
const int motorForward  = 7;
const int motorBackward = 6;
const int motorEnable   = 9;

// snelheid
const int motorSpeed = 255;

// sensors
const int trigStart = 4;
const int echoStart = 5;
const int trigEnd   = 2;
const int echoEnd   = 3;

// state machine
enum State {IDLE, RUNNING, READY};
State state = IDLE;

// command flag
bool startCommand = false;

// ===============================
// SETUP
// ===============================
void setup()
{
    pinMode(motorForward,  OUTPUT);
    pinMode(motorBackward, OUTPUT);
    pinMode(motorEnable,   OUTPUT);
    pinMode(trigStart,     OUTPUT);
    pinMode(echoStart,     INPUT);
    pinMode(trigEnd,       OUTPUT);
    pinMode(echoEnd,       INPUT);

    Serial.begin(9600);
    stopMotor();

    state = IDLE;
    Serial.println("Conveyor: Idle");
}

// ===============================
// LOOP
// ===============================
void loop()
{
    handleSerialCommands();

    float startDistance = readDistance(trigStart, echoStart);
    float endDistance   = readDistance(trigEnd,   echoEnd);

    bool startDetected = startDistance < 8.0;
    bool endDetected   = endDistance   < 8.0;

    // ==========================
    // READY → IDLE
    // Robot has picked the item and sent "start" again.
    // Reset to IDLE so the start-sensor can trigger a new run.
    // ==========================
    if (state == READY && startCommand)
    {
        state = IDLE;
        Serial.println("Conveyor: Idle");
    }

    // ==========================
    // IDLE → RUNNING
    // ==========================
    if (state == IDLE && startCommand && startDetected)
    {
        state = RUNNING;
        moveForward();
        Serial.println("Conveyor: Running");
    }

    // ==========================
    // RUNNING → READY
    // ==========================
    if (state == RUNNING && endDetected)
    {
        stopMotor();
        state        = READY;
        startCommand = false;
        Serial.println("Conveyor: Ready");
    }
}

// ===============================
// SERIAL COMMANDS
// ===============================
void handleSerialCommands()
{
    if (!Serial.available()) return;

    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "start")
    {
        startCommand = true;
    }
    else if (command == "stop")
    {
        startCommand = false;
        stopMotor();
        state = IDLE;
        Serial.println("Conveyor: Idle");
    }
}

// ===============================
// MOTOR FUNCTIONS
// ===============================
void moveForward()
{
    analogWrite(motorEnable, motorSpeed);
    digitalWrite(motorForward,  HIGH);
    digitalWrite(motorBackward, LOW);
}

void stopMotor()
{
    analogWrite(motorEnable, 0);
    digitalWrite(motorForward,  LOW);
    digitalWrite(motorBackward, LOW);
}

// ===============================
// ULTRASONIC SENSOR
// ===============================
float readDistance(int trigPin, int echoPin)
{
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH, 30000);

    if (duration == 0)
    {
        return 999.0;
    }

    return duration * 0.034 / 2.0;
}
