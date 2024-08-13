# Copyright (c) 2024, Hadeel Milad and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cint
from erpnext.accounts.report.financial_statements import (
	get_columns,
	get_cost_centers_with_children,
	get_data,
	get_filtered_list_for_consolidated_report,
	get_period_list,
)

def execute(filters=None):
	period_list = get_period_list(
		filters.from_fiscal_year,
		filters.to_fiscal_year,
		filters.period_start_date,
		filters.period_end_date,
		filters.filter_based_on,
		filters.periodicity,
		company=filters.company,
	)
	currency = filters.presentation_currency or frappe.get_cached_value('Company',  filters.company,  "default_currency")
	asset = get_data(
		filters.company,
		"Asset",
		"Debit",
		period_list,
		filters=filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True,
		ignore_accumulated_values_for_fy=True,
	)

	for a in asset:
		a.update({'root_type': 'asset'})

	liability = get_data(
		filters.company,
		"Liability",
		"Credit",
		period_list,
		filters=filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True,
		ignore_accumulated_values_for_fy=True,
	)
	for l in liability:
		l.update({'root_type': 'liability'})

	equity = get_data(
		filters.company,
		"Equity",
		"Credit",
		period_list,
		only_current_fiscal_year=False,
		filters=filters,
		accumulated_values=filters.accumulated_values,
	)

	for l in liability:
		l.update({'root_type': 'liability'})

	print(liability)
	# equity = get_data(filters.company, "Equity", "Debit", period_list, only_current_fiscal_year=False, filters=filters, accumulated_values=filters.accumulated_values)
	if equity:
		for l in equity:
			l.update({'root_type': 'liability'})
	print("equity ooooooooooooooooo")
	print(equity)

	provisional_profit_loss, total_credit = get_provisional_profit_loss(
		asset, liability, equity, period_list, filters.company, currency
	)

	message, opening_balance = check_opening_balance(asset, liability, equity)

	data = []
	data.extend(asset or [])
	data.extend(liability or [])
	data.extend(equity or [])
	if opening_balance and round(opening_balance,2) !=0:
		unclosed ={
			"account_name": "'" + _("Unclosed Fiscal Years Profit / Loss (Credit)") + "'",
			"account": "'" + _("Unclosed Fiscal Years Profit / Loss (Credit)") + "'",
			"warn_if_negative": True,
			"currency": currency
		}
		for period in period_list:
			unclosed[period.key] = opening_balance
			if provisional_profit_loss:
				provisional_profit_loss[period.key] = provisional_profit_loss[period.key] - opening_balance

		unclosed["total"]=opening_balance
		data.append(unclosed)

	if provisional_profit_loss:
		data.append(provisional_profit_loss)
	if total_credit:
		data.append(total_credit)

	columns = get_columns(filters.periodicity, period_list, filters.accumulated_values, company=filters.company)

	return columns, data, message

def get_provisional_profit_loss(
	asset, liability, equity, period_list, company, currency=None, consolidated=False
):
	provisional_profit_loss = {}
	total_row = {}
	if asset and (liability or equity):
		total = total_row_total = 0
		currency = currency or frappe.get_cached_value("Company", company, "default_currency")
		total_row = {
			"account_name": "'" + _("Total (Credit)") + "'",
			"account": "'" + _("Total (Credit)") + "'",
			"warn_if_negative": True,
			"currency": currency,
		}
		has_value = False

		for period in period_list:
			key = period if consolidated else period.key
			effective_liability = 0.0
			if liability:
				effective_liability += flt(liability[-2].get(key))
			if equity:
				effective_liability += flt(equity[-2].get(key))

			provisional_profit_loss[key] = flt(asset[-2].get(key)) - effective_liability
			total_row[key] = effective_liability + provisional_profit_loss[key]

			if provisional_profit_loss[key]:
				has_value = True

			total += flt(provisional_profit_loss[key])
			provisional_profit_loss["total"] = total

			total_row_total += flt(total_row[key])
			total_row["total"] = total_row_total

		if has_value:
			provisional_profit_loss.update(
				{
					"account_name": "'" + _("Provisional Profit / Loss (Credit)") + "'",
					"account": "'" + _("Provisional Profit / Loss (Credit)") + "'",
					"warn_if_negative": True,
					"currency": currency,
				}
			)

	return provisional_profit_loss, total_row


def check_opening_balance(asset, liability, equity):
	# Check if previous year balance sheet closed
	opening_balance = 0
	float_precision = cint(frappe.db.get_default("float_precision")) or 2
	if asset:
		opening_balance = flt(asset[-1].get("opening_balance", 0), float_precision)
	if liability:
		opening_balance -= flt(liability[-1].get("opening_balance", 0), float_precision)
	if equity:
		opening_balance -= flt(equity[-1].get("opening_balance", 0), float_precision)

	opening_balance = flt(opening_balance, float_precision)
	if opening_balance:
		return _("Previous Financial Year is not closed"), opening_balance
	return None, None
