/*
 * Setting up i/o pins for
 *  - Switch 1 (normally closed/on)
 *  - Switch 2 (normally open/off)
 *  
 *  There is only a limited set of i/o pins for each type of
 *  Arduino that can be attached to an external interrupt.
 *  Most (if not all) ATMega-based Arduino boards support
 *  external interrupts on i/o pins 2 and 3.
 */
#define PIN_SWITCH1 2
#define PIN_SWITCH2 3

/*
 * Optimal debouncing times may vary between different dials.
 * The below values work best with _MY_ dial.
 * 
 * -> Change SWITCH1 debouncing time if the number detected is
 *    not correct
 * -> Change SWITCH2 debouncing time if turning/reaching
 *    initial resting position is not detected properly
 */
#define SWITCH1_DEBOUNCING_MILLIS 65
#define SWITCH2_DEBOUNCING_MILLIS 100

/*
 * Global variables for exchanging values between interrupt
 * calls, namely
 * - debouncing buffers, storing when an interrupt routine
 *   was last called
 * - pulse count, incremented while the dial is turned
 */
volatile unsigned long switch1_debouncing_millis_last = 0;
volatile unsigned long switch2_debouncing_millis_last = 0;
volatile byte switch1_num_pulses = 0;

/*
 * Setup routine - putting everything into order
 */
void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {/*just wait*/}
  Serial.println("Serial ready.");
  Serial.print("Setting up pins... ");
  pinMode(PIN_SWITCH1, INPUT);
  pinMode(PIN_SWITCH2, INPUT);
  Serial.println("done");
  Serial.print("Attaching interrupt... ");
  //wait for closing of Switch 2 before doing anything else
  attachInterrupt(digitalPinToInterrupt(PIN_SWITCH2), isr_switch2_rising, RISING);
  Serial.println("done");
}

/*
 * Here goes the main program code... just in case you
 * want to do anything besides just detecting numbers
 */
void loop() {
    
}

/*
 * Interrupt routine, called when Switch 2 is closed.
 * It marks the beginning of dialling and
 * - replaces itself with the interrupt routine waiting
 *   for Switch 2 to open again and
 * - attaches the interrupt to Switch 1 in order to
 *   count the pulses
 */
void isr_switch2_rising() {
  long diff = millis() - switch2_debouncing_millis_last;
  diff = abs(diff);
  if (diff >= SWITCH2_DEBOUNCING_MILLIS) {
    Serial.print("turn of dial detected - counting pulses: [");
    switch1_num_pulses = 0;
    attachInterrupt(digitalPinToInterrupt(PIN_SWITCH1), isr_switch1_falling, FALLING);
    attachInterrupt(digitalPinToInterrupt(PIN_SWITCH2), isr_switch2_falling, FALLING);
    switch2_debouncing_millis_last = millis();
    switch1_debouncing_millis_last = millis();
  }
}

/*
 * Interrupt routine, called when Switch 1 is opened
 * (marking a pulse). It is only active while
 * Switch 2 is closed and increments the global
 * variable "switch1_num_pulses"
 */
void isr_switch1_falling() {
  long diff = millis() - switch1_debouncing_millis_last;
  diff = abs(diff);
  if (diff >= SWITCH1_DEBOUNCING_MILLIS) {
    Serial.print(".");
    switch1_num_pulses++;
    switch1_debouncing_millis_last = millis();
  }
}

/*
 * Interrupt routine, called when Switch 1 is opened.
 * It marks the end of dialling and
 * - prints the detected number of pulses to the serial
 *   console
 * - detaches the interrupt routine from Switch 1
 * - replaces itself with the interrupt routine waiting
 *   for Switch 2 to close again and
 * - could be your starting point if you intend to do
 *   anything beyond simple numeral detection and output
 *   to the serial console.
 */
void isr_switch2_falling() {
  long diff = millis() - switch2_debouncing_millis_last;
  diff = abs(diff);
  if (diff >= SWITCH2_DEBOUNCING_MILLIS) {
    //do something with the detected number...
    Serial.print("]");
    for (byte b=0; b<(11-switch1_num_pulses); b++) Serial.print(" ");
    Serial.print(" detected ");
    Serial.print(switch1_num_pulses);
    Serial.print(" pulse");
    Serial.println((switch1_num_pulses!=1 ? "s" : ""));
    switch2_debouncing_millis_last = millis();
    detachInterrupt(digitalPinToInterrupt(PIN_SWITCH1));
    attachInterrupt(digitalPinToInterrupt(PIN_SWITCH2), isr_switch2_rising, RISING);
    switch2_debouncing_millis_last = millis();
  }
}


