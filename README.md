# QuickEurope
This application allows you to select up to 4 cities in Europe and it will tell you the lowest price it takes to go to all of them in sequence by airplane.

## Dependencies

This project uses the python3 modules: `flask` and `requests`, so before installation make sure that both `python3` the dependencies and those modules are installed on the system.

## Installation

To install, simply clone the GitHub repository and compile the backend:

```bash
git clone https://github.com/OneStone2/HackUPC
cd HackUPC/backend
make bin #c++ compile backend
cd -
```

### Running

To run the problem change to the directory `flask` inside the main folder of the project and start the flask server by issuing the command:

```bash
python3 routes.py
```
 This will start the flask web server that you can access through `http://localhost:5000`

To make a query, you should click the "Let's give it a try" link and it will bring up a page where you can give all the information required.

Please note the following constraints:

- The difference between arrival and departure days cannot be larger than 31, otherwise it would result in an error
- You must choose between 1 and 4 destinations, and specify what is the minimum number of days you want to spend on each one in the corresponding box. Failure to do this will result in an error.
- Please take note that for longer inputs (4 destinations and 10+ days) the program might take about a minute to fetch all the information from the API.
