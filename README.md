# Expense Tracker CLI

A command-line expense tracker that helps you track your expenses.

## Features

- Create and manage multiple expense reports
- Add expenses with dates, amounts and descriptions
- View summarised expense reports grouped by date
- Export reports to Excel spreadsheets
- Set maximum daily claimable amounts (Useful for corporate expenses)
- Support for multiple currency symbols
- Data storage using JSON

## Installation

1. Clone the repository:

``git clone https://github.com/TNorth1/expense-tracker-cli.git``

2. Navigate to the project directory:

``cd expense-tracker-cli``

3. Install the package:

``pip install .``

## Usage

### Basic Commands

#### Display help page

``exptrack --help``

#### Create a new expense report

``exptrack create <report-name>``

#### Add expenses to a report

``exptrack update <report-name>``

#### Display a report

``exptrack display <report-name>``

#### Display summarised report grouped by date

``exptrack display <report-name> --summary``

#### List all reports

``exptrack ls``

#### Delete a report

``exptrack rm <report-name>``

#### Delete specific expense entry inside a report

``exptrack rm <report-name> --id <entry-id>``

#### Export report to Excel

``exptrack export <report-name>``

### Configuration

#### Set maximum daily claimable amount

``exptrack set-max <amount>``

Example:

``exptrack set-max 50.00``

Use 'unlimited' for no limit:

``exptrack set-max unlimited``

#### Set currency symbol

``exptrack set-currency <symbol>``

Example:

``exptrack set-currency £``

## File Storage

* Expense reports are stored as JSON files in the `reports` directory located at `~/.local/share/expense-tracker-cli/reports`
* Configuration settings are stored in `config.json` located at `~/.config/expense-tracker-cli/config.json`

## Dependencies

- pandas: Data manipulation and Excel export
- PyQt5: File dialog windows for export functionality
- rich: Terminal formatting and tables
- platformdirs: Saving config/report files in platform specific directories

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
