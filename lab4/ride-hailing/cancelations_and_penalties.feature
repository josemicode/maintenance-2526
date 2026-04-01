Feature: Cancellations and Penalties

	Handling rider cancellations and driver no-shows

	Background:
		Given a rider has requested a trip

	@happy_path
	Scenario: Rider cancels before driver assignment
		Given no driver has been assigned yet
		When the rider cancels the trip
		Then no cancellation fee should apply

	@happy_path
	Scenario: Rider cancels within 2 minutes of assignment
		Given a driver has been assigned to the trip
		When cancellation occurs within 2 minutes of driver assignment
		Then no cancellation fee should apply

	@edge_case
	Scenario: Rider cancels after 2 minutes of assignment
		Given a driver has been assigned to the trip
		When cancellation occurs more than 2 minutes after driver assignment
		Then a cancellation fee should apply

	@edge_case
	Scenario: Driver no-show
		Given the driver has accepted the trip
		When the driver does not arrive within 8 minutes
		Then the rider can report a no-show
		And the driver should be penalized