import sys


def create_sheet(service, spreadsheet_title: str) -> str:
    """Create a Google spreadsheet."""
    spreadsheet_body = {
        'properties': {
            'title': spreadsheet_title
            }
        }
    # Call the Sheets API to create a spreadsheet
    spreadsheet = service.spreadsheets().create(
        body=spreadsheet_body,
        fields='spreadsheetId'
        ).execute()

    spreadsheet_id = spreadsheet.get('spreadsheetId')

    if not spreadsheet_id:
        sys.exit('SpreadsheetID not returned. Failed to create a spreadsheet.')
    else:
        print(f'Created spreadsheet ID: {spreadsheet_id}')

    return spreadsheet_id
