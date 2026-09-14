// Copyright (c) 2026, Samtech Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on("Expense Entry", {
	setup(frm) {
		frm.set_query("cash_or_bank_account", () => ({
			filters: {
				account_type: ["in", ["Bank", "Cash"]],
				is_group: 0,
			},
		}));
		frm.set_query("account", "accounts", () => ({
			filters: {
				account_type: ["not in", ["Receivable", "Stock"]],
				is_group: 0,
			},
		}));
	},
});
