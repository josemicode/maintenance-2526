Feature: Shipping Logic

	How the system handles stock distribution upon ordering from multiple warehouses

	Background:
		Given the customer is logged in the site

	Scenario: Stock distribution
		Given the customer has multiple products in the cart
		And the stock of those items cannot be found in a single warehouse
		When the customer attempts to place the order
		And there are one or more warehouses that have availability for the rest of the stock
		Then the order should be placed successfully
		And a partial shipment should be issued
