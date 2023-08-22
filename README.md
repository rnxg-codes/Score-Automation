
![Logo](https://github.com/iam7t9/SocAuto/blob/Final/ScreenShots/logo.png?raw=true)


# Score Automation
#### A solution for automateing the process score and progress tracking.

The project aimed to address these by implementing an automated system that could seamlessly monitor the status of participants', checkpoints and provide real-time updates to participants

## Installation

#### Server setup
*Clone the repositry*
```bash
git clone https://github.com/iam7t9/SocAuto.git
cd .\SocAuto\Server\
```

*Create virtual environment*
```bash
python -m venv env .
.\env\Scripts\activate
```
*Install requirements*
```bash
pip install -r requirements.txt
```

### ESP

- Upload the code present in the `ESP` directory on the respective ESP32 and ESP8266  

## Tests the connection

- To tests the connection, run the following command.
- Select the port and check if data is received correctly.

```bash
python .\SerialMoniter.py
```


## Deployment

To deploy ESP data receiver run,

```bash
python .\ESP-Excel.py
```

To deploy UI server run,

```bash
python .\Server-Excel.py
```
## Screenshots

![Interface 1](https://github.com/iam7t9/SocAuto/blob/Final/ScreenShots/interface1.png?raw=true)


![Interface 2](https://github.com/iam7t9/SocAuto/blob/Final/ScreenShots/interface2.png?raw=true)

## Authors

- [Pallavi Phunde (SY EXTC)](https://github.com/pallaviphunde2003)
- [Saurav Kharat (SY EXTC)](https://github.com/alpharosto)
- [Shantanu Pande (FY EXTC)](https://github.com/iam7t9)
- [Shivam Kurhekar (FY EXTC)](https://www.github.com/rnxg-codes)
- [Rushikesh Pole (FY CSE)](https://www.github.com/rnxg-codes)   
- [Varad Wayal (FY EXTC)](https://www.github.com/rnxg-codes)   


## Contributing

Contributions are always welcome!



## License

[MIT](https://choosealicense.com/licenses/mit/)

