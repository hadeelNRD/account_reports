import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.meta import get_field_precision
from frappe.query_builder.custom import ConstantColumn
from frappe.utils import flt

import erpnext
from erpnext.controllers.taxes_and_totals import init_landed_taxes_and_totals
from erpnext.stock.doctype.serial_no.serial_no import get_serial_nos
from erpnext.stock.doctype.landed_cost_voucher.landed_cost_voucher import LandedCostVoucher

class custom_LandedCostVoucher(LandedCostVoucher):

	@frappe.whitelist()
	def get_items_from_purchase_receipts(self):
		self.set("items", [])
		for pr in self.get("purchase_receipts"):
			if pr.receipt_document_type and pr.receipt_document:
				pr_items = get_pr_items(pr)

				for d in pr_items:
					item = self.append("items")
					item.item_code = d.item_code
					item.description = d.description
					item.custom_total_weight = d.total_weight
					item.qty = d.qty
					item.rate = d.base_rate
					item.cost_center = d.cost_center or erpnext.get_default_cost_center(self.company)
					item.amount = d.base_amount
					item.receipt_document_type = pr.receipt_document_type
					item.receipt_document = pr.receipt_document
					item.purchase_receipt_item = d.name
					item.is_fixed_asset = d.is_fixed_asset

def get_pr_items(purchase_receipt):
	item = frappe.qb.DocType("Item")
	pr_item = frappe.qb.DocType(purchase_receipt.receipt_document_type + " Item")
	return (
		frappe.qb.from_(pr_item)
		.inner_join(item)
		.on(item.name == pr_item.item_code)
		.select(
			pr_item.item_code,
			pr_item.description,
			pr_item.qty,
			pr_item.total_weight,
			pr_item.base_rate,
			pr_item.base_amount,
			pr_item.name,
			pr_item.cost_center,
			pr_item.is_fixed_asset,
			ConstantColumn(purchase_receipt.receipt_document_type).as_("receipt_document_type"),
			ConstantColumn(purchase_receipt.receipt_document).as_("receipt_document"),
		)
		.where(
			(pr_item.parent == purchase_receipt.receipt_document)
			& ((item.is_stock_item == 1) | (item.is_fixed_asset == 1))
		)
		.run(as_dict=True)
	)
