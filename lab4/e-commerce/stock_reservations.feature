Feature: Stock Reservations

	How the system handles inventory

	Background:
		Given the customer is logged in the site
		And the customer's cart contains a product

	@happy_path
	Scenario: Correct order
		When the order is placed
		Then an unit of said product is reserved for the customer for a total of 30 minutes
		When the payment is processed within the time window
		Then the order should be confirmed

	@edge_case
	Scenario: Order timeout
		When the order is placed
		Then an unit of said product is reserved for the customer for a total of 30 minutes
		When the payment is not processed within the time window
		Then the order should be cancelled
		And the stock should be released
