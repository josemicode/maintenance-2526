Feature: Stock Reservations

	How the system handles inventory

	Background:
		Given the customer is logged in the site

	@happy_path
	Scenario: 
		Given the customer's cart contains a product
		When the order is placed
		Then an unit of said product is reserved for the customer for a total of 30 minutes
		When the payment is processed within the time window
		Then the order is confirmed
