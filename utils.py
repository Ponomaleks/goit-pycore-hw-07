from models import Record


def display_contacts(contacts: list[Record]) -> str:
    cell_length = 20
    header_name = "Name"
    header_phones = "Phones"
    header_birthday = "Birthday"
    header = f"{header_name:<{cell_length}}|{header_phones:<{cell_length}}|{header_birthday:<{cell_length}}"
    header_separator = (
        "-" * cell_length + "|" + "-" * cell_length + "|" + "-" * cell_length
    )
    table_rows = []

    for record in contacts:
        name = record.name.value
        phones_list = [phone.value for phone in record.phones]
        birthday = record.birthday if record.birthday else "N/A"

        first_row = f"{name:<{cell_length}}|{phones_list[0]:<{cell_length}}|{birthday}"
        next_rows = "\n".join(
            f"{'':<{cell_length}}|{phones:<{cell_length}}|{'':<{cell_length}}"
            for phones in phones_list[1:]
        )
        table_rows.append(first_row + ("\n" + next_rows if next_rows else ""))

    return header + "\n" + header_separator + "\n" + "\n".join(table_rows)
