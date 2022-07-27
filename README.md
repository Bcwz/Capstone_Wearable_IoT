# Capstone_Wearable_IoT

**Title**
>Detection and prevention of heat-related injuries using real-time health monitoring and thermoregulated wearable IoT. 


**Deliverables**
>A working demonstrable portal that shows the integration of at least one non-wearable and one wearable device that provide a data logging (configurable timer) to a back-end portal.

**Scope**
>Include 2 groups of devices: 
>1. Heating, ventilation, and air conditioning (HVAC) with temperature and humidity as a baseline.

**Use case and application environment**
>This project is designed to be used in a military training environment where soliders will be wearing the thermoregulated wearable IoT device to monitor their body temperature for early detection and preventation of heat-releated injuries. These readings are gathered and analyzed to provide on-site medical personnel in-sights on the physical condition of soliders and provide timely medical attention if there is a risk of heat-injury.

**Libraries used (requirements.txt)**
>1. Adafruit_DHT==1.4.0
>2. Flask==1.1.2
>3. keras==2.9.0
>4. keras_nightly==2.10.0.dev2022072107
>5. numpy==1.20.2
>6.paho_mqtt==1.6.1
>7. pandas==1.2.3
>8. pymongo==3.11.2
>9. python-dotenv==0.20.0
>10. requests==2.25.1
>11. scikit_learn==1.1.1
>12. statsmodels==0.13.2

**Protocol Stack**
>![Capstone - Communication (OSI) Protocol Layer](https://user-images.githubusercontent.com/57914467/178656726-3f486bf7-eefb-4441-b992-09d3c7331339.png)
>
>The protocol stack diagram illustrates the different layers used for Hypertext Transfer Protocol / Hypertext Transfer Protocol Secure (HTTP/HTTPS) communication between the wearable IoT controller (Raspberry Pi 3b+) and a centralised server. The HTTP / HTTPS communication protocol is choosen as it is able to long range and secure communications using TLS/SSL encryption. In addition, HTTP/HTTPS is also able to provide quality-of-service (QoS) by utilising TCP/IP for the transport layer  to ensure the successful delivery of data to server.

**High level process flowchart**
>![Capstone - High level swim lane](https://user-images.githubusercontent.com/57914467/178658961-8323f1b4-77a6-45bc-8bf2-10236a01551b.png)
>
>As the controller (Raspberry Pi 3b+) executes the program, it would gather data such as body temperature (°C) and environment humidity (%) readings from the DHT11 sensor placed on the front chest area to calculate the WBGT reading using a predefinded formula. These readings are used to determine if the wearer is at risk of having a heat related injuries by checking if the reading exceeds a certain threshold (WBGT >=32 [high risk], 31.9 > WBGT >= 31 [medium risk], 30.9 > WBGT >=29.9 [low risk]) according to the work rest cycle diagram shown below. 
>![image](https://user-images.githubusercontent.com/57914467/178665374-7eb9ce82-92c9-4ae2-aefc-bb4033d96b44.png)
>
>In the event that the wearer exceeds a certain WBGT threshold (high risk & medium risk), various heat reducing/cooling measures will be activated such as triggering the Peltier module and side exhaust fans to generate and circulate cool air for **active cooling** for the wearer. However, if the wearer is at a low risk threshold, only the side exhaust fans would be triggered to circulate air and improve perspiration to allow for natural **passive cooling**.
>
>As heatstroke is defined as having a body temperature of ~41°C or higher within 10min-15mins[1], the aim is to reduce the wearer body temperature to below 39°C within 30 minutes to prevent any serious heat injuries[2][3].

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
> The Raspberry Pi 3b+ will act as the main controller to control the various sensors and hardware and utilises HTTP/HTTPS communication protocol to communicate with a centralised server. In order to develop the Minimum viable product (MVP) to demostrate the portability and wearability, the Raspberry Pi 3b+ will rely on a portal power supply to provide power for the whole setup.
>There will be a total of one DHT11 sensor, two 5V, 1A Peltier module, four USB side exhaust fans, four thermal tapes and four heatsinks to faciliate with the heat & cold transfer from the Peltier module. The DHT11 sensor will be utilizing the Raspberry Pi’s Pin 17 for 3.3v power, Pin 20 for ground and Pin 18 (GPIO24) for data transfer. One of the peltier module will be using the Pin 4 for 5V, 1A power & Pin 6 for ground, while the other Peltier module will be using Pin 2 for 5V, 1A power & Pin 14 for ground. Finally, all of the USB side exhaust fans will be controlled using the Raspberry Pi’s onboard USB ports.



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
