Feature: Refund Logic

	Returning and refunding products within a time window

	Background:
		Given a customer has placed an order for an item
	
	@happy_path
	Scenario: Succesful refund
		Given the item's status is set as "Delivered"
		And no more than 30 days have passed since the item was delivered
		When the customer requests a refund
		And the return is approved
		Then the customer should receive a refund for the returned item
	
	@edge_case
	Scenario: Cancelled refund
		Given the customer requested a refund
		And the item has been returned
		When the returned item is damaged
		Then the refund should be denied for such item

