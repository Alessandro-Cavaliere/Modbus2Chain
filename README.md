# Blockchain & Back-End Application

The project consists of a back-end based on Hyperledger Fabric, an enterprise blockchain platform, and middleware written in Python. The goal of the project is to provide a secure and reliable infrastructure for managing environmental data collected from IoT devices using the Modbus RTU protocol.

The middleware in Python is used to convert Modbus data into formats readable by the Hyperledger Fabric blockchain, thus enabling secure and reliable recording and management of environmental data.

The IoT device communication framework is written in Python and is part of the back-end. The project can be used in different contexts, such as for real-time environmental data management, supply chain tracking, or smart contract management. Due to its modularity and flexibility, the project can be easily adapted to the specific needs of different organizations.

In summary, the project provides a robust and secure infrastructure for managing environmental data taken from IoT devices using the Modbus RTU protocol, based on Hyperledger Fabric and middleware in Python.

## Pre-requisite
The following is the list of requirements for the application to function properly

 -  *Unix/Linux system or shell bash (using WSL, Git Bash etc...)*
 -  *Python 3.x*
 -  *Docker >=17.06.2*
 -  *Docker Compose >=1.14.0*
 -  *Binaries of Hyperledger Fabric (provided in the repository)*


## Installation

Install all dependencies with ***pip***:

```pip
    pip install -r .\requirements.txt            
```
To create a private blockchain network using Hyperledger Fabric, use this script:
 
```bash
    bash start.sh          
```
Specifically, this command performs these operations:
- Definition of environment variables for Hyperledger Fabric binaries and blockchain network configuration;
 - Generation of cryptographic material for the organizations involved;
 - Creating blockchain network genesis block using the "***modbus2chainNetworkProfile***" configuration profile by saving it in the "***system-genesis-block***" directory;
 - Starting Docker Containers using ***docker-compose.yaml***;
 - Creating the transaction for creating the communication channel "***modbus2chainchannel***" using the configuration profile "***modbus2chainChannelProfile***" saving it in the directory "***channel-artifacts***";
 - Creation of anchor peer updates for organizations;
 - Adding the involved organizations to the communication channel;
 - Update anchors peer for the involved organizations.

To eventually delete all files and configurations associated with the Hyperledger Fabric blockchain network, run the following script:
```bash
    bash stop.sh          
```

## Usage
To launch and run this application assumes proper configuration and setting of the IoT device architecture and middleware. 
To launch the application:
```python
    cd app
    python app.py          
```


    