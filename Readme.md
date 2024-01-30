# PPE_Detection_YoloV8 / Project

A PPE detection and calssification model.

## What it is


This app will help you automatically Detect and classify PPE compliance.

Ther model runs via flask and is hosted on a local server, running in th ebackground once initiated.

Data is processed in batches daily at midnight.

Results are shown both on the consol and saved to file with the processed images both being moved and saved in 
a separate, labelled format.

This app will greatly improve PPE compliance thereby ensuring optimal safety in the workplace.


## Installation

```shell
pip install -r requirements.txt
```

## Usage

Start the app by running shell command

```shell
flask_apschedulerv6.py
```
