"""
Extends `openpyxl` classes for easier operation on Excel tables.
"""

__all__ = ["attach", "get_tables"]

from typing import Dict, Union

from pyxltab import classes


def attach(openpyxl_book: classes.openpyxl_Workbook) -> classes.Book:
    """
    Attach to an `openpyxl` workbook, allowing other operations to be performed.
    """

    book = classes.Book(openpyxl_book)
    return book


def get_tables(
    book: Union[classes.Book, classes.openpyxl_Workbook]
) -> Dict[str, classes.Table]:
    """
    Get all tables in the workbook.
    """

    if isinstance(book, classes.openpyxl_Workbook):
        book = attach(book)

    tables: Dict[str, classes.Table] = {}

    for sheet in book:
        tables.update(sheet.tables)

    return tables
