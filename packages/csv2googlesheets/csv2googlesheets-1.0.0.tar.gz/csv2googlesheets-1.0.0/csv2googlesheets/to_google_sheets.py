"""This module provides a console interface to convert CSV to Google Sheets."""

from csv2googlesheets.gapi_authorization import auth_with_google
from csv2googlesheets.gapi_create_sheet import create_sheet
from csv2googlesheets.gapi_write_to_sheet import write_to_sheet

from csv2googlesheets.parse_file import build_spreadsheet_title
from csv2googlesheets.parse_file import parse_file
from csv2googlesheets.parse_cli_args import parse_cli_args


def main():
    """Control the flow of operations to write data from csv to G Sheets."""
    cli_args = parse_cli_args()
    values = parse_file(path=cli_args.csv)
    spreadsheet_title = build_spreadsheet_title(cli_args.csv)

    google_service = auth_with_google(path_creds=cli_args.credentials_json)
    spreadsheet_id = create_sheet(google_service, spreadsheet_title)

    write_to_sheet(
        google_service,
        sheet_id=spreadsheet_id,
        values=values,
        )


if __name__ == '__main__':
    main()
