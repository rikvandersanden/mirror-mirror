#define ROT_LEDG A4     // green LED
#define ROT_B 13        // rotary B
#define ROT_A 12         // rotary A
#define ROT_SW 10         // rotary puhbutton
#define ROT_LEDB A3      // blue LED
#define ROT_LEDR 1      // red LED

#define POT_BRIGHTNESS A1
#define POT_SPEED 9
#define POT_DRIFT A2

#define HUE 1 << 0
#define BRIGHTNESS 1 << 1
#define SPEED 1 << 2
#define DRIFT 1 << 3

#define BUTTON_PRESSED 1 << 6
#define BUTTON_RELEASED 1 << 7

// Global variables that can be changed in interrupt routines
volatile int rotary_counter = 0; // current "position" of rotary encoder (increments CW)
volatile boolean rotary_change = false; // will turn true if rotary_counter has changed

byte hue; // doesn't need to be a state
byte brightness;
byte speed;
byte drift;
bool buttonState = false;

void setup()
{
  // Set up all the I/O pins. Unused pins are commented out.
  pinMode(ROT_B, INPUT);
  digitalWrite(ROT_B, HIGH); // turn on weak pullup
  pinMode(ROT_A, INPUT);
  digitalWrite(ROT_A, HIGH); // turn on weak pullup
  pinMode(ROT_SW, INPUT);
  digitalWrite(ROT_SW, LOW ); // turn on weak pulldown
  
  // The rotary switch is common anode with external pulldown, do not turn on pullup
  pinMode(ROT_LEDB, OUTPUT);
  pinMode(ROT_LEDG, OUTPUT);
  pinMode(ROT_LEDR, OUTPUT);

  pinMode(POT_SPEED, INPUT);
  pinMode(POT_BRIGHTNESS, INPUT);
  pinMode(POT_DRIFT, INPUT);

  Serial.begin(9600); // Use serial for debugging
  Serial.println("Begin RGB Rotary Encoder Testing");

  attachInterrupt(digitalPinToInterrupt(ROT_A), rotaryIRQ, CHANGE);
}

void rotaryIRQ()
{
  static unsigned char rotary_state = 0; // current and previous encoder states

  rotary_state <<= 2;  // remember previous state
  rotary_state |= (digitalRead(ROT_A) | (digitalRead(ROT_B) << 1));  // mask in current state
  rotary_state &= 0x0F; // zero upper nybble

  //Serial.println(rotary_state,HEX);

  if (rotary_state == 0x09) // from 10 to 01, increment counter. Also try 0x06 if unreliable
  {
    rotary_counter++;
    rotary_change = true;
  }
  else if (rotary_state == 0x03) // from 00 to 11, decrement counter. Also try 0x0C if unreliable
  {
    rotary_counter--;
    rotary_change = true;
  }
}

void loop()
{
  if (Serial.available() > 0)
    receive();
  
  send();
  setLEDHSV(hue, 255, brightness);

  delay(10);
}

void receive()
{
  int newHue = hue;
  while(Serial.available() > 0)
  {
    newHue = Serial.read();
  }
  hue = newHue;
}

// split into update and send?
void send()
{
  bool newButtonState = digitalRead(ROT_SW) == HIGH;
  byte newBrightness = analogRead(POT_BRIGHTNESS) / 4;
  byte newSpeed = analogRead(POT_SPEED) / 4;
  byte newDrift = analogRead(POT_DRIFT) / 4;

  if (newButtonState != buttonState)
  {
    if (newButtonState)
      Serial.write(BUTTON_PRESSED);
    else
      Serial.write(BUTTON_RELEASED);
      
    buttonState = newButtonState;
  }
  if (newBrightness != brightness)
  {
    Serial.write(BRIGHTNESS);
    Serial.write(newBrightness);
    brightness = newBrightness;
  }

  if (newSpeed != speed)
  {
    Serial.write(SPEED);
    Serial.write(newSpeed);
    speed = newSpeed;
  }

  if (newDrift != drift)
  {
    Serial.write(DRIFT);
    Serial.write(newDrift);
    drift = newDrift;
  }

  if (rotary_change)
  {
    byte delta = 128 + rotary_counter;
    Serial.write(HUE);
    Serial.write(delta);
    rotary_change = false;
    rotary_counter = 0;
  }
}

void setLEDHSV(byte hue, byte saturation, byte brightness)
{
  uint32_t rgb = ColorHSV(hue << 8, saturation, brightness);
  setLEDRGB(
    (uint8_t)(rgb >> 16),
    (uint8_t)(rgb >> 8),
    (uint8_t)(rgb));
}

void setLEDRGB(byte r, byte g, byte b)
{
  // Common anode LED, so 0 is ON, 1 is OFF
  analogWrite(ROT_LEDR, 255 - r);
  analogWrite(ROT_LEDG, 255 - g);
  analogWrite(ROT_LEDB, 255 - b);
}

// stolen from Adafruit NeoPixel library
uint32_t ColorHSV(uint16_t hue, uint8_t sat, uint8_t val) {

  uint8_t r, g, b;

  // Remap 0-65535 to 0-1529. Pure red is CENTERED on the 64K rollover;
  // 0 is not the start of pure red, but the midpoint...a few values above
  // zero and a few below 65536 all yield pure red (similarly, 32768 is the
  // midpoint, not start, of pure cyan). The 8-bit RGB hexcone (256 values
  // each for red, green, blue) really only allows for 1530 distinct hues
  // (not 1536, more on that below), but the full unsigned 16-bit type was
  // chosen for hue so that one's code can easily handle a contiguous color
  // wheel by allowing hue to roll over in either direction.
  hue = (hue * 1530L + 32768) / 65536;
  // Because red is centered on the rollover point (the +32768 above,
  // essentially a fixed-point +0.5), the above actually yields 0 to 1530,
  // where 0 and 1530 would yield the same thing. Rather than apply a
  // costly modulo operator, 1530 is handled as a special case below.

  // So you'd think that the color "hexcone" (the thing that ramps from
  // pure red, to pure yellow, to pure green and so forth back to red,
  // yielding six slices), and with each color component having 256
  // possible values (0-255), might have 1536 possible items (6*256),
  // but in reality there's 1530. This is because the last element in
  // each 256-element slice is equal to the first element of the next
  // slice, and keeping those in there this would create small
  // discontinuities in the color wheel. So the last element of each
  // slice is dropped...we regard only elements 0-254, with item 255
  // being picked up as element 0 of the next slice. Like this:
  // Red to not-quite-pure-yellow is:        255,   0, 0 to 255, 254,   0
  // Pure yellow to not-quite-pure-green is: 255, 255, 0 to   1, 255,   0
  // Pure green to not-quite-pure-cyan is:     0, 255, 0 to   0, 255, 254
  // and so forth. Hence, 1530 distinct hues (0 to 1529), and hence why
  // the constants below are not the multiples of 256 you might expect.

  // Convert hue to R,G,B (nested ifs faster than divide+mod+switch):
  if(hue < 510) {         // Red to Green-1
    b = 0;
    if(hue < 255) {       //   Red to Yellow-1
      r = 255;
      g = hue;            //     g = 0 to 254
    } else {              //   Yellow to Green-1
      r = 510 - hue;      //     r = 255 to 1
      g = 255;
    }
  } else if(hue < 1020) { // Green to Blue-1
    r = 0;
    if(hue <  765) {      //   Green to Cyan-1
      g = 255;
      b = hue - 510;      //     b = 0 to 254
    } else {              //   Cyan to Blue-1
      g = 1020 - hue;     //     g = 255 to 1
      b = 255;
    }
  } else if(hue < 1530) { // Blue to Red-1
    g = 0;
    if(hue < 1275) {      //   Blue to Magenta-1
      r = hue - 1020;     //     r = 0 to 254
      b = 255;
    } else {              //   Magenta to Red-1
      r = 255;
      b = 1530 - hue;     //     b = 255 to 1
    }
  } else {                // Last 0.5 Red (quicker than % operator)
    r = 255;
    g = b = 0;
  }

  // Apply saturation and value to R,G,B, pack into 32-bit result:
  uint32_t v1 =   1 + val; // 1 to 256; allows >>8 instead of /255
  uint16_t s1 =   1 + sat; // 1 to 256; same reason
  uint8_t  s2 = 255 - sat; // 255 to 0
  return ((((((r * s1) >> 8) + s2) * v1) & 0xff00) << 8) |
          (((((g * s1) >> 8) + s2) * v1) & 0xff00)       |
         ( ((((b * s1) >> 8) + s2) * v1)           >> 8);
}