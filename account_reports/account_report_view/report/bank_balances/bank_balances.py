# Copyright (c) 2024, Hadeel Milad and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext.accounts.utils import get_balance_on
from erpnext import get_default_currency

def execute(filters=None):

	return get_columns(), get_data(filters)

def get_columns():
	currency = get_default_currency()
	columns = [
		{
			"label": _("Account"),
			"fieldname": "account",
			"fieldtype": "Link",
			"options": "Account",
			"width": 200
		},
		{
			"label": _("Account Name"),
			"fieldname": "account_name",
			"fieldtype": "Data",
			"options": "Account",
			"width": 200
		},
		{
			"label": _("Account No"),
			"fieldname": "account_number",
			"fieldtype": "Data",
			"options": "Account",
			"width": 100
		},
		{
			"label": _("Attach No"),
			"fieldname": "attach_no",
			"fieldtype": "Int"
		},
		{
			"label": _("Balance ({})".format(currency)),
			"fieldname": "balance",
			"fieldtype": "Currency",
			"options": "Currency",
			"width": 200
		}
	]
	return columns

def get_data(filters):
	account = filters.get('account')
	cond = ""
	if account:
		cond = " AND name='{}' ".format(account)
	accounts = frappe.db.sql(""" 
				SELECT name as account, account_name, account_number, is_group
				FROM tabAccount 
				WHERE account_type='Bank' {}""".format(cond)
				, as_dict=True)
	data = []
	total = 0
	for no, acc in enumerate(accounts, 1):
		res = {
			'account': acc.account,
			'account': acc.account,
			'account_name': acc.account_name,
			'account_number': acc.account_number,
			'attach_no': no,
			'balance': 0
		}
		balance = get_balance_on(acc.account) or 0
		res.update({
			'balance': balance
		})
		if acc.is_group == 0:
			total += balance
		data.append(res)
	
	data.append({'balance': total, 'account': _('Total')})
	return data