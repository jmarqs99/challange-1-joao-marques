# TodoMVC UI Testing with Playwright

This repository contains automated UI tests for the [TodoMVC](http://todomvc.com/examples/react/#/) application using Playwright. The tests are implemented in Python and cover functionalities such as adding, completing, and deleting TODO items, with additional features like screenshot and video recording.

## Features

- Navigate to TodoMVC.
- Add TODO items with current and future dates.
- Mark TODO items as completed.
- Delete TODO items.
- Capture multiple screenshots at different stages of the test.
- Record video of the test execution.

## Requirements

- Python 3.10 used 
- [Node.js](https://nodejs.org/) (for Playwright)
- Playwright library for Python
- Allure command-line tool (for reporting)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/jmarqs99/challange-1-joao-marques.git

2. **Install dependencies:**
   ```bash
    pip install playwright allure-pytest
    playwright install

3. **Install Allure:**
Follow the Allure (https://allurereport.org/docs/install/) installation guide.

### Usage

1. **Run the tests:**
   ```bash
    pytest challange1.py --alluredir=allure-results
   
2. Generate and view Allure reports:
   ```bash
    allure generate allure-results --clean
    allure open
   
### Screenshots and Videos
Screenshots will be saved in the screenshots folder, and the test video will be recorded at videos folder.
