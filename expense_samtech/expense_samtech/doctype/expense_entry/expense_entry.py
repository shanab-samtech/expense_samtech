# Copyright (c) 2026, Samtech Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class ExpenseEntry(Document):
	def on_submit(self):
		if not self.accounts:
			frappe.throw("At least one expense account is required")

		total_amount = 0
		journal_entry = frappe.new_doc("Journal Entry")
		journal_entry.voucher_type = "Journal Entry"
		journal_entry.company = self.company
		journal_entry.posting_date = self.posting_date

		for row in self.accounts:
			if not row.account:
				frappe.throw(f"Account is required in row {row.idx}")
			if flt(row.amount) <= 0:
				frappe.throw(f"Amount must be greater than zero in row {row.idx}")

			total_amount += flt(row.amount)
			journal_entry.append(
				"accounts",
				{
					"account": row.account,
					"debit_in_account_currency": row.amount,
					"cost_center": row.cost_center,
					"project": row.project,
					"user_remark": row.remark,
				},
			)

		journal_entry.append(
			"accounts",
			{
				"account": self.cash_or_bank_account,
				"credit_in_account_currency": total_amount,
			},
		)
		journal_entry.submit()
		self.db_set("journal_entry", journal_entry.name)

	def on_cancel(self):
		if self.journal_entry:
			journal_entry = frappe.get_doc("Journal Entry", self.journal_entry)
			if journal_entry.docstatus == 1:
				journal_entry.cancel()
