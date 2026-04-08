# Containerized Data Center Environment Monitoring System

## Project Description
The project involves creating a simulation of an environment monitoring system in a data center, allowing for the detection of hardware failures and overheating. 

Using scripts, virtual sensors will be implemented, operating as separate Docker containers. These sensors will cyclically generate measurements of parameters such as temperature, humidity, and power consumption. 

The architecture, based on isolated container networks, allows for flexible extension of the project with an IT infrastructure monitoring layer, examining metrics such as network latency and resource usage. 

The final result of the work will be the implementation of a dashboard that will aggregate and visualize the collected metrics in real-time through a dedicated backend communicating with sensors via the MQTT protocol and a relational database.

## Team Members
* **Mateusz Rybak** - Team Leader / Backend Developer
* **Wojciech Staruch** - System Architect / Network Engineer
* **Łukasz Cyganiuk** - Data & Documentation Engineer
