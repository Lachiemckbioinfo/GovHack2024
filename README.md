# GovHack 2024 - HikeAware

## The Product
Our project had a two-pronged approach: to both aid in citizen science and local animal awareness from an app, and to help provide greater data awareness and analysis capabilities to the local council.To do so, we have created two outputs: the app [HikeAware](https://hikeaware.vercel.app/), and an associated backend data dashboard, accessible directly through the app, or via its own address. 



## Technical Specifications

### Dashboard
The HikeAware dashboard was created using the Python Plotly Dash library. It is hosted on an ARDC Nectar cloud virtual machine. It can be accessed [here](http://203.101.226.242:8050/).

## The Challenge
We have entered into the challenge [Smart infrastructure for data-driven decision making](https://hackerspace.govhack.org/challenges/smart_infrastructure_for_data_driven_decision_making).

We are utilising the following datasets:
+ Mary Cairncross Scenic Reserve Farmo PIR Counter
+ Mary Cairncross Scenic Reserve NCount WiFi Counter
+ Mary Cairncross Scenic Reserve Atmos Weather Station
+ Mary Cairncross Scenic Reserve Milesight Occupancy Counter
+ Sugar Bag Road Recreation Reserve Atmos Weather Station
+ Sugar Bag Road Recreation Reserve Farmo PIR Counter

We have also created some mock data for the app to utilise. This data is in the form of animal sighting counts per hour.
Data was aggregated into two CSV files: ALLDATA.csv, and ALLDATA_sbr.csv. These are located in the code folder.

## The Team
We are a team of four people: Lachlan McKinnie (PhD student, bioinformatics), Milan (3rd year engineering student), Jack Thorpe (3rd year engineering student), and Zeke xxx (3rd year IT student).


