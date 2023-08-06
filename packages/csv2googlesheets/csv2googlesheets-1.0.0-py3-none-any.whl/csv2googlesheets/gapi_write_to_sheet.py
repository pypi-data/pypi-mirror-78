def write_to_sheet(service, sheet_id: str, values: list) -> None:
    """Write data to Google spreadsheet."""
    result = service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Sheet1!A1',
        valueInputOption='USER_ENTERED',
        body={'values': values}
        ).execute()

    print(f'{result.get("updatedCells")} cells updated.')
