import os
import threading
from openpyxl import Workbook, load_workbook

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.xlsx")
LOCK = threading.Lock()

SHEETS = {
    "Users": ["id", "name", "email", "password"],
    "Events": ["id", "title", "category", "date", "time", "venue",
               "organizer", "capacity", "description", "created_by"],
}


def _open():
    """Open data.xlsx, creating it with headers on first run."""
    if not os.path.exists(FILE):
        wb = Workbook()
        wb.remove(wb.active)
        for name, head in SHEETS.items():
            wb.create_sheet(name).append(head)
        wb.save(FILE)
    return load_workbook(FILE)


def all_rows(sheet):
    with LOCK:
        ws = _open()[sheet]
        rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:] if r[0] is not None]


def add_row(sheet, data):
    with LOCK:
        wb = _open()
        ws = wb[sheet]
        ids = [r[0] for r in ws.iter_rows(min_row=2, values_only=True) if r[0] is not None]
        data["id"] = max(ids, default=0) + 1
        ws.append([data.get(h, "") for h in SHEETS[sheet]])
        wb.save(FILE)
    return data["id"]