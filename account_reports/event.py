import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import _
import json
from frappe.utils import (
    flt,
    getdate,
    nowdate,
)



@frappe.whitelist()
def get_items_from_purchase_receipts(self):
    print("get_items_from_purchase_ KKKKKKKKKKKKKKKKKKKKkk")
    self.set("items", [])
    for pr in self.get("purchase_receipts"):
        if pr.receipt_document_type and pr.receipt_document:
            pr_items = get_pr_items(pr)

            for d in pr_items:
                item = self.append("items")
                item.item_code = d.item_code
                item.description = d.description
                item.qty = d.qty
                item.rate = d.base_rate
                item.cost_center = d.cost_center or erpnext.get_default_cost_center(self.company)
                item.amount = d.base_amount
                item.receipt_document_type = pr.receipt_document_type
                item.receipt_document = pr.receipt_document
                item.purchase_receipt_item = d.name
                item.is_fixed_asset = d.is_fixed_asset