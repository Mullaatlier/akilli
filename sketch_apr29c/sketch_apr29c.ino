#include <DHT.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

// DHT Sensör Pin ve Tip
#define DHTPIN 6
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Diğer kontrol pinleri
#define FanPin 4
#define SuMotoruPin 2
#define LambaPin 3
#define FanButonPin 7 // Fan butonu pini
#define LambaButonPin 8 // Lamba butonu pini
#define SuMotoruButonPin 9 // Su motoru butonu pini

// Su seviye sensörü pinleri
#define sensorPower 10
#define sensorPin A2

// LCD ekran kurulumu
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Zamanlayıcılar için değişkenler
unsigned long previousMillis = 0;
const long interval = 2000;  // 2 saniye aralıklarla güncelle

// LCD ekranda gösterilecek sensör verilerini tutan dizin
enum SensorType { SICAKLIK, NEM, TOPRAKNEM, ISIKSEVIYESI, SUSEVIYESI };
SensorType currentSensor = SICAKLIK;

// Kalp animasyonu için desenler
const byte heart[8] = {
  B00000,
  B01010,
  B11111,
  B11111,
  B01110,
  B00100,
  B00000,
  B00000
};

// Loading (yükleniyor) animasyonu için desenler
const byte loading[8] = {
  B00000,
  B00000,
  B00000,
  B00000,
  B11111,
  B11111,
  B00000,
  B00000
};

// Cihaz durumları
bool fanState = false;
bool fanButtonState = false; // Fan buton durumu takip edicisi
bool lambaState = false;
bool lambaButtonState = false; // Lamba buton durumu takip edicisi
bool suMotoruState = false;
bool suMotoruButtonState = false; // Su motoru buton durumu takip edicisi

void setup() {
  Serial.begin(9600);
  dht.begin();
  lcd.begin(16, 2);  // LCD ekranı başlatırken sütun ve satır sayısını belirtin
  lcd.createChar(0, heart); // Kalp desenini oluştur
  lcd.createChar(1, loading); // Loading desenini oluştur
  lcd.backlight();
  pinMode(FanPin, OUTPUT);
  pinMode(SuMotoruPin, OUTPUT);
  pinMode(LambaPin, OUTPUT);
  pinMode(FanButonPin, INPUT_PULLUP); // Fan buton giriş modunu INPUT_PULLUP olarak ayarla
  pinMode(LambaButonPin, INPUT_PULLUP); // Lamba buton giriş modunu INPUT_PULLUP olarak ayarla
  pinMode(SuMotoruButonPin, INPUT_PULLUP); // Su motoru buton giriş modunu INPUT_PULLUP olarak ayarla
  pinMode(sensorPower, OUTPUT);  // Su seviye sensörü güç pini

  // Başlangıçta fan, su motoru ve lamba kapalı olsun
  digitalWrite(FanPin, HIGH);
  digitalWrite(SuMotoruPin, HIGH);
  digitalWrite(LambaPin, HIGH);

  // Su seviye sensörünü kapalı başlat
  digitalWrite(sensorPower, LOW);

  // Fan, lamba ve su motorunu başlangıçta aç
  digitalWrite(FanPin, LOW);
  fanState = true;
  digitalWrite(LambaPin, LOW);
  lambaState = true;
  digitalWrite(SuMotoruPin, LOW);
  suMotoruState = true;

  // LCD'yi başlat ve ilk mesajı göster
  lcd.setCursor(0, 0);
  lcd.print("Baslatiliyor...");
}

void loop() {
  // Buton durumlarını oku
  int fanButonDurumu = digitalRead(FanButonPin);
  int lambaButonDurumu = digitalRead(LambaButonPin);
  int suMotoruButonDurumu = digitalRead(SuMotoruButonPin);

  // Seri monitörden komut oku
  if (Serial.available() > 0) {
    char komut = Serial.read();

    // Seri monitörden gelen komutlara göre fanı, lambayı veya su motorunu kontrol et
    if (komut == '1') {
      fanState = true;
      digitalWrite(FanPin, LOW);
      Serial.println("Fan acildi.");
    } else if (komut == '2') {
      fanState = false;
      digitalWrite(FanPin, HIGH);
      Serial.println("Fan kapatildi.");
    } else if (komut == '5') {
      lambaState = true;
      digitalWrite(LambaPin, LOW);
      Serial.println("Lamba acildi.");
    } else if (komut == '6') {
      lambaState = false;
      digitalWrite(LambaPin, HIGH);
      Serial.println("Lamba kapatildi.");
    } else if (komut == '3') {
      suMotoruState = true;
      digitalWrite(SuMotoruPin, LOW);
      Serial.println("Su motoru acildi.");
    } else if (komut == '4') {
      suMotoruState = false;
      digitalWrite(SuMotoruPin, HIGH);
      Serial.println("Su motoru kapatildi.");
    } else if (komut == 'T' || komut == 't') { // Toprak nemini sorgulama komutu
      float toprakNemi = analogRead(A1);
      Serial.print("Toprak Nem: ");
      Serial.println(toprakNemi);
  } else if (komut == 'S' || komut == 's') { // Sıcaklık ve nemi sorgulama komutu
      float sicaklik = dht.readTemperature();
      
      Serial.print("Sicaklik: ");
      Serial.print(sicaklik);
      
     } else if (komut == 'H' || komut == 'h'){
        float nem = dht.readHumidity();
        Serial.print("Nem: ");
      Serial.print(nem);
      Serial.println(" %");

    } else if (komut == 'I' || komut == 'i') { // Işık seviyesini sorgulama komutu
      int isikSeviyesi = analogRead(A0);
      Serial.print("Isik Seviyesi: ");
      Serial.println(isikSeviyesi);
    } else if (komut == 'W' || komut == 'w') { // Su seviyesini sorgulama komutu
      digitalWrite(sensorPower, HIGH);  // Su seviye sensörünü aç
      delay(10);  // Sensörün stabil hale gelmesi için bekle
      int suSeviyesi = analogRead(sensorPin);
      Serial.print("Su Seviyesi: ");
      Serial.println(suSeviyesi);
      digitalWrite(sensorPower, LOW);  // Su seviye sensörünü kapat
    }
  }

  // Fan buton durumuna göre fanı kontrol et
  if (fanButonDurumu == LOW && !fanButtonState) {
    // Buton basılı ve daha önce basılmamış ise fan durumunu tersine çevir
    fanState = !fanState;
    digitalWrite(FanPin, fanState ? LOW : HIGH); // Fan durumuna göre fanı aç veya kapat
    fanButtonState = true; // Fan buton durumu takipçisini güncelle
    lcd.setCursor(0, 1);
    lcd.print("Fan: ");
    lcd.print(fanState ? "Acildi  " : "Kapali  ");
    Serial.println(fanState ? "Fan acildi." : "Fan kapatildi.");
  } else if (fanButonDurumu == HIGH && fanButtonState) {
    // Buton bırakıldı ve daha önce basılmış ise fan buton durumu takipçisini sıfırla
    fanButtonState = false;
  }

  // Lamba buton durumuna göre lambayı kontrol et
  if (lambaButonDurumu == LOW && !lambaButtonState) {
    // Buton basılı ve daha önce basılmamış ise lamba durumunu tersine çevir
    lambaState = !lambaState;
    digitalWrite(LambaPin, lambaState ? LOW : HIGH); // Lamba durumuna göre lambayı aç veya kapat
    lambaButtonState = true; // Lamba buton durumu takipçisini güncelle
    lcd.setCursor(9, 1);
    lcd.print("Lamba: ");
    lcd.print(lambaState ? "Acildi  " : "Kapali  ");
    Serial.println(lambaState ? "Lamba acildi." : "Lamba kapatildi.");
  } else if (lambaButonDurumu == HIGH && lambaButtonState) {
    // Buton bırakıldı ve daha önce basılmış ise lamba buton durumu takipçisini sıfırla
    lambaButtonState = false;
  }

  // Su motoru buton durumuna göre su motorunu kontrol et
  if (suMotoruButonDurumu == LOW && !suMotoruButtonState) {
    // Buton basılı ve daha önce basılmamış ise su motoru durumunu tersine çevir
    suMotoruState = !suMotoruState;
    digitalWrite(SuMotoruPin, suMotoruState ? LOW : HIGH); // Su motoru durumuna göre su motorunu aç veya kapat
    suMotoruButtonState = true; // Su motoru buton durumu takipçisini güncelle
    lcd.setCursor(0, 1);
    lcd.print("Su Motoru: ");
    lcd.print(suMotoruState ? "Acildi  " : "Kapali  ");
    Serial.println(suMotoruState ? "Su motoru acildi." : "Su motoru kapatildi.");
  } else if (suMotoruButonDurumu == HIGH && suMotoruButtonState) {
    // Buton bırakıldı ve daha önce basılmış ise su motoru buton durumu takipçisini sıfırla
    suMotoruButtonState = false;
  }

  // Zamanlayıcı ile sensör verilerini sırayla göster
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    switch (currentSensor) {
      case SICAKLIK:
        showSensorValue("Sicaklik: ", dht.readTemperature());
        currentSensor = NEM;
        break;
      case NEM:
        showSensorValue("Nem: ", dht.readHumidity());
        currentSensor = TOPRAKNEM;
        break;
      case TOPRAKNEM:
        showSensorValue("Toprak Nem: ", analogRead(A1));
        currentSensor = ISIKSEVIYESI;
        break;
      case ISIKSEVIYESI:
        showSensorValue("Isik Seviyesi: ", analogRead(A0));
        currentSensor = SUSEVIYESI;
        break;
      case SUSEVIYESI:
        digitalWrite(sensorPower, HIGH);  // Su seviye sensörünü aç
        delay(10);  // Sensörün stabil hale gelmesi için bekle
        showSensorValue("Su Seviyesi: ", analogRead(sensorPin));
        digitalWrite(sensorPower, LOW);  // Su seviye sensörünü kapat
        currentSensor = SICAKLIK;
        break;
    }
  }
  showAnimations();
}

void showSensorValue(const char *message, float value) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(message);
  lcd.print(value);
}

void showAnimations() {
  static byte heartIndex = 0;
  static byte loadingIndex = 0;

  // Kalp animasyonu
  lcd.setCursor(15, 1);
  lcd.write(byte(heartIndex));
  heartIndex = (heartIndex + 1) % 8;

  // Loading animasyonu
  lcd.setCursor(14, 1);
  lcd.write(byte(loadingIndex));
  loadingIndex = (loadingIndex + 1) % 8;

  delay(250); // Animasyonlar arası geçiş için bekleme süresi
}