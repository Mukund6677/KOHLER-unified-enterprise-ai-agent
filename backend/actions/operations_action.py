import re

from backend.database.db import SessionLocal
from backend.database.enterprise_models import InventoryItem


def execute_operations_modification(
    employee,
    details,
    approved_by
):
    """
    Execute an approved operations modification
    against the live enterprise database.

    Supported examples:

    1. Change inventory of Hydraulic Pumps to 500 units.
       -> Sets quantity to 500

    2. Increase Hydraulic Pumps by 80 units.
       -> Adds 80 to current quantity

    3. Decrease Hydraulic Pumps by 20 units.
       -> Subtracts 20 from current quantity
    """

    query = details.lower().strip()

    db = SessionLocal()

    try:
        # -------------------------------------------------
        # FIND INVENTORY ITEM
        # -------------------------------------------------

        inventory_items = db.query(InventoryItem).all()

        item = None

        for inventory_item in inventory_items:
            if inventory_item.item_name.lower() in query:
                item = inventory_item
                break

        if not item:
            return {
                "status": "FAILED",
                "message": (
                    "Inventory item could not be identified."
                ),
                "details": details
            }

        old_quantity = item.quantity

        # -------------------------------------------------
        # DETECT NUMBER
        # -------------------------------------------------

        numbers = re.findall(r"\d+", query)

        if not numbers:
            return {
                "status": "FAILED",
                "message": (
                    "No quantity was specified."
                ),
                "details": details
            }

        requested_quantity = int(numbers[-1])

        # -------------------------------------------------
        # DETECT OPERATION
        # -------------------------------------------------

        if any(
            phrase in query
            for phrase in [
                "increase",
                "add",
                "add by",
                "increase by"
            ]
        ):
            new_quantity = old_quantity + requested_quantity
            operation = "INCREASE"

        elif any(
            phrase in query
            for phrase in [
                "decrease",
                "reduce",
                "remove",
                "decrease by"
            ]
        ):
            new_quantity = old_quantity - requested_quantity
            operation = "DECREASE"

        elif any(
            phrase in query
            for phrase in [
                "change",
                "set",
                "update",
                "to"
            ]
        ):
            new_quantity = requested_quantity
            operation = "SET"

        else:
            return {
                "status": "FAILED",
                "message": (
                    "Could not determine the inventory operation."
                ),
                "details": details
            }

        # -------------------------------------------------
        # VALIDATE RESULT
        # -------------------------------------------------

        if new_quantity < 0:
            return {
                "status": "FAILED",
                "message": (
                    "Inventory quantity cannot be negative."
                ),
                "details": details
            }

        # -------------------------------------------------
        # UPDATE DATABASE
        # -------------------------------------------------

        item.quantity = new_quantity

        db.commit()

        return {
            "status": "EXECUTED",
            "message": (
                "Operations modification executed "
                "successfully."
            ),
            "employee": employee,
            "approved_by": approved_by,
            "item": item.item_name,
            "operation": operation,
            "old_quantity": old_quantity,
            "new_quantity": new_quantity,
            "details": details
        }

    except Exception as error:

        db.rollback()

        return {
            "status": "FAILED",
            "message": (
                "Database update failed: "
                + str(error)
            ),
            "details": details
        }

    finally:
        db.close()