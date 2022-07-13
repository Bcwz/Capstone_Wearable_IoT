# Capstone_Wearable_IoT

**Title**
>Detection and prevention of heat-related injuries using real-time health monitoring and thermoregulated wearable IoT. 


**Deliverables**
>A working demonstrable portal that shows the integration of at least one non-wearable and one wearable device that provide a data logging (configurable timer) to a back-end portal.

**Scope**
>Include 2 groups of devices: 
>1. Heating, ventilation, and air conditioning (HVAC) with temperature and humidity as a baseline.
>2. Personal Healthcare with any two of body temperature, heartbeat and BPM (Pulse) as a baseline.
>These data collected should be presented as part of the data visualisation module in the back-end portal.

**Use case and application environment**
>This project is designed to be used in a military training environment where soliders will be wearing the thermoregulated wearable IoT device to monitor their body temperature for early detection and preventation of heat-releated injuries. These readings are gathered and analyzed to provide on-site medical personnel in-sights on the physical condition of soliders and provide timely medical attention if there is a risk of heat-injury.

**Software**:
>1. Python - Version 3.10.1

**Libraries used**
>1. TBD

**Software Architecture Design**
>- TBD

**Protocol Stack**
>![Capstone - Communication (OSI) Protocol Layer](https://user-images.githubusercontent.com/57914467/178656726-3f486bf7-eefb-4441-b992-09d3c7331339.png)
>
>The protocol stack diagram illustrates the different layers used for Message Queue Telemetry Transport (MQTT) communication between Thingsboard and the wearable IoT controller (Raspberry Pi 3b+). MQTT protocol is built on top of the TCP/IP stack which enables efficient scalability with millions of IoT devices and support for communication over unreliable networks and allows for optional TLS/SSL message encryption. While MQTT is designed as a lightweight, flexible and efficient protocol, it is able to utilize minimal resources to transmit messages using the Publish/Subscribe model and also able to provide reliable message delivery via the different Quality of Service (QoS) levels (0 = At most once, 1 = At least once, 2 = Exactly once). 

**High level process flowchart**
>![Capstone - High level swim lane](https://user-images.githubusercontent.com/57914467/178658961-8323f1b4-77a6-45bc-8bf2-10236a01551b.png)
>
>As the controller (Raspberry Pi 3b+) executes the program, it would gather real-time (polling inverval of 5 seconds) body temperature (°C) and environment humidity (%) readings from the DHT11 sensor placed on the front chest area. These readings are used to determine if the wearer is at risk of having a heatstroke by checking if the reading exceeds a certain threshold (>=40°C [high risk], >=39°C [medium risk], >=38°C [low risk]). 
>
>In the event that the wearer exceeds a certain body temperature (°C) threshold (high risk & medium risk), various heat reducing/cooling measures will be activated such as triggering the Peltier module and side exhaust fans to generate and circulate cool air for **active cooling** for the wearer. Simultaneously, these readings would be constantly monitored and transmitted to Thingsboard to generate an alarm to notify medical personnel of the medical emergency. However, if the wearer is at a low risk threshold, only the side exhaust fans would be triggered to circulate air and improve perspiration to allow for natural **passive cooling**.
>
>As heatstroke is defined as having a body temperature of ~41°C or higher within 10min-15mins[1], the aim is to reduce the wearer body temperature to below 39°C within 30 minutes to prevent any serious heat injuries[2][3]. By having an alarm generated on Thingsboard, medical personnel should attend to the person at risk and examine if they require additional medical attention within the 30min timeframe.

**Hardware required**
>1. Raspberry Pi 3b+
>2. Jumper cables (Male to Female, Female to Female)
>3. DHT11
>4. Peltier Module (5V 1A as Raspberry Pi maximum power output is 5V)
>5. Side Exhaust Fans
>6. Heatsink
>7. Thermal Tape
>8. Jacket
>9. Portable power supply

**Hardware Architecture Design**
>![Capstone - Hardware Design](https://user-images.githubusercontent.com/57914467/178659183-6f7424cd-cab0-455c-ba0b-83b2c5422c8e.png)
>
> The Raspberry Pi 3b+ will act as the main controller to control the various sensors and hardware and as a MQTT publisher to publish the real-time body temperature (°C) and environment humidity (%) readings to Thingsboard for data visualization and analysis. In order to develop the Minimum viable product (MVP) to demostrate the portability and wearability, the Raspberry Pi 3b+ will rely on a portal power supply to provide power for the whole setup.
> 
> There will be a total of one DHT11 sensor, two 5V, 1A Peltier module and four USB side exhaust fans which requires active management (coding), while there will be a total of four heatsinks and four thermal tapes to faciliate with the heat & cold transfer from the Peltier module. The DHT11 sensor will be utilizing the Pin 17 for 3.3v power,  Pin 20 for ground and Pin 18 (GPIO24) for data transfer. One of the peltier module will be using the Pin 4 for 5V, 1A power & Pin 6 for ground, while the other Peltier module will be using Pin 2 for 5V, 1A power & Pin 14 for ground. Finally, all of the USB side exhaust fans will be controlled using the USB ports.

**Hardware Technical Information**
>1. Raspberry Pi 3b+ - https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/
>- Purpose: To control sensors, communicate with backend/frontend/server and perform edge computation.
>- Datasheet: https://static.raspberrypi.org/files/product-briefs/Raspberry-Pi-Model-Bplus-Product-Brief.pdf
>2. Jumper cables (Male to Female, Female to Female)
>- Purpose: To connect controller (Raspberry Pi 3b+) to sensors.
>3. DHT11 - https://www.adafruit.com/product/386
>- Purpose: To gather real-time data such as the wearer body temperature (°C) and environment humidity (%).
>- Datasheet: https://www.mouser.com/datasheet/2/737/dht-932870.pdf
>4. Peltier Module (5V 1A) - https://www.mouser.sg/ProductDetail/426-FIT0826
>- Purpose: To create a cool air supply.
>- Datasheet:https://www.mouser.sg/new/dfrobot/dfrobot-electric-cooler-module-5v-1a/
>5. Side Exhaust Fans - https://www.amazon.sg/gp/product/B07V2KVQB7/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1
>- Purpose: To circulate cool air supply and dissipate heat from heatsink.
>- Datasheet: https://www.amazon.sg/gp/product/B07V2KVQB7/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1
>6. Heatsink - https://www.mouser.sg/ProductDetail/532-371824B34G
>- Purpose: To dissipate heat from Peltier Module.
>- Datasheet: https://www.mouser.sg/pdfDocs/Boyd-Board-Level-Heatsinks-Catalog.pdf
>7. Thermal Tape - https://www.mouser.sg/ProductDetail/485-1467
>- Purpose: To transfer heat from Peltier Module to heatsink.
>- Datasheet: https://www.mouser.sg/datasheet/2/737/3m8810-1020955.pdf
>8. Jacket
>- Purpose: To house all components.

**Dataset**
>1.Wet Bulb Temperature, Hourly - https://data.gov.sg/dataset/wet-bulb-temperature-hourly?view_id=7ed27d62-730e-4986-8dee-72f1d243583e&resource_id=0195dc7a-2f49-4107-ac7c-3112ca4a09a8


**References**
>[1] “Heat Stress Related Illness,” Centers for Disease Control and Prevention, 06-Jun-2018. [Online]. Available: https://www.cdc.gov/niosh/topics/heatstress/heatrelillness.html#:~:text=When heat stroke occurs, the,emergency treatment is not given.&text=Symptoms of heat stroke include,altered mental status, slurred speech. [Accessed: 26-Nov-2021].
>
>[2] NHS Choices. [Online]. Available: https://www.nhs.uk/conditions/heat-exhaustion-heatstroke/. [Accessed: 26-Nov-2021].
>
>[3] L. Xing, S.-Y. Liu, H.-D. Mao, K.-G. Zhou, Q. Song, and Q.-M. Cao, “The prognostic value of routine coagulation tests for patients with heat stroke,” The American Journal of Emergency Medicine, 22-Apr-2020. [Online]. Available: https://www.sciencedirect.com/science/article/abs/pii/S0735675720302916. [Accessed: 26-Nov-2021].
