# Modbus2Chain
<picture>
  <source srcset="./app/assets/LogoProgetto.png" media="(min-width: 680px)">
  <img src="./app/assets/LogoProgetto.png" alt="Logo Progetto">
</picture>

Table of contens
=============

* [Description](#description)
* [Installation](#installation)
  * [Back_End_And_Blockchain_Application](#back_end_and_blockchain_application)
  * [React_Application](#react_application)

Description
--------

**Modbus2Chain** is an IoT project that uses the Modbus protocol to acquire environmental data from sensors and send it securely to the blockchain via a `TCP` connection. This choice was made because `Modbus TCP` is very popular for implementing IoT communications in industrial environments, due to its wide adoption, compatibility with Ethernet networks, adequate security and real-time communication capabilities

To achieve the goal of creating an efficient system for collecting and sharing critical environmental data, the project uses a number of technologies:
 
 - The Modbus protocol back-end and device management is implemented in `Python`, using the `micropython-modbus` library for communication with sensors.
 - The blockchain that is used is `Hyperledger Fabric`, a framework for creating highly scalable and modular enterprise blockchains. Hyperledger Fabric provides a secure and reliable platform for logging and sharing critical data, enabling easy permission management and enhanced data privacy.
 - The user interface is developed in `React`, a JavaScript framework for creating responsive and dynamic user interfaces. 

The system workflow begins with the collection of environmental data from sensors using the Modbus TCP protocol. The acquired data is then sent to the Python back-end, which processes it and sends it to the `Hyperledger Fabric` blockchain using the APIs made available by the framework. The blockchain guarantees the integrity and immutability of data, which can be easily shared with other authorized users.

⬇️Below, a graphic diagram of the workflow in order to make it easier to understand and interact between the different components of the system⬇️.

<picture>
  <source srcset="./app/assets/ArchitectureDiagram.jpg" media="(min-width: 680px)">
  <img src="./app/assets/ArchitectureDiagram.png" alt="ArchitectureDiagram">
</picture>


Thanks to **Modbus2Chain**, it is possible to create an efficient system for collecting and sharing critical environmental data, guaranteeing their security and integrity through the `Hyperledger Fabric` blockchain. Furthermore, thanks to the use of modern technologies such as `React` and `Python`, the project is highly flexible and easily scalable to meet the needs of any IoT application.

Installation
--------
For the correct functioning of the application, READMEs are linked below to the respective sections. Read all the READMEs carefully to avoid making configuration errors.

### Back_End_And_Blockchain_Application
For detailed instructions on setting up and using the Back-End and the Blockchain network of this application, please refer to the [Back-End & Blockchain README](./README_BE_BC.md).
### React_Application
For detailed instructions on setting up and using the Front-End of this application, please refer to the [Front-End README](https://github.com/Alessandro-Cavaliere/Modbus2Chain/blob/MC_FE/README.md).

