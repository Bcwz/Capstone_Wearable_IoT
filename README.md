# Capstone_Wearable_IoT

**Title**: Prevention of heat-related work injuries using real-time health monitoring and thermoregulated wearable IoT. 


**Deliverables**: A working demonstrable portal that shows the integration of at least one non-wearable and one wearable device that provide a data logging (configurable timer) to a back-end portal.

**Scope**: Include 2 groups of devices: 
1. Heating, ventilation, and air conditioning (HVAC) with temperature and humidity as a baseline.
2. Personal Healthcare with any two of body temperature, heartbeat and BPM (Pulse) as a baseline.
These data collected should be presented as part of the data visualisation module in the back-end portal.

**Software**:
1. Python - Version 3.10.1

**Libraries used**
1. TBD

**Software Architecture Design**
- TBD

**High level process flowchart**
![HighLevelSwimLane](https://user-images.githubusercontent.com/57914467/146107998-1ab472d3-36fa-4026-bfd5-eba3c4b3079e.jpeg)



**Hardware required**
1. Raspberry Pi 3b+
2. Jumper cables (Male to Female, Female to Female)
3. DHT11
4. Peltier Module (5V 1A as Raspberry Pi maximum power output is 5V)
5. Side Exhaust Fans
6. Heatsink
7. Thermal Tape
8. Jacket

**Hardware Architecture Design**
![Hardware Architecture](https://user-images.githubusercontent.com/57914467/146115213-5405eb65-aaaa-42a7-87e5-37cfe4cd8d74.jpeg)


**Hardware Technical Information**
1. Raspberry Pi 3b+ - https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/
- Purpose: To control sensors, communicate with backend/frontend/server and perform edge computation.
- Datasheet: https://static.raspberrypi.org/files/product-briefs/Raspberry-Pi-Model-Bplus-Product-Brief.pdf
2. Jumper cables (Male to Female, Female to Female)
- Purpose: To connect controller (Raspberry Pi 3b+) to sensors.
3. DHT11 - https://www.adafruit.com/product/386
- Purpose: To real-time data such as the wearer body temperature (°C) and environment humidity (%).
- Datasheet: https://www.mouser.com/datasheet/2/737/dht-932870.pdf
4. Peltier Module (5V 1A) - https://www.mouser.sg/ProductDetail/426-FIT0826
- Purpose: To create a cool air supply.
- Datasheet:https://www.mouser.sg/new/dfrobot/dfrobot-electric-cooler-module-5v-1a/
5. Side Exhaust Fans - https://www.amazon.sg/gp/product/B07V2KVQB7/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1
- Purpose: To circulate cool air supply and dissipate heat from heatsink.
- Datasheet: https://www.amazon.sg/gp/product/B07V2KVQB7/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1
6. Heatsink - https://www.mouser.sg/ProductDetail/532-371824B34G
- Purpose: To dissipate heat from Peltier Module.
- Datasheet: https://www.mouser.sg/pdfDocs/Boyd-Board-Level-Heatsinks-Catalog.pdf
7. Thermal Tape - https://www.mouser.sg/ProductDetail/485-1467
- Purpose: To transfer heat from Peltier Module to heatsink.
- Datasheet: https://www.mouser.sg/datasheet/2/737/3m8810-1020955.pdf
8. Jacket
- Purpose: To house all components.
