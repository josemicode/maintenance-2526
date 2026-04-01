Feature: Driver Matching

	Matching riders to nearby drivers

	Background:
		Given a rider has requested a trip

	@happy_path
	Scenario: Successful driver match
		Given there is at least one driver within 3 km who is 'Available'
		When the system searches for drivers
		Then the closest available driver should be offered the trip
		And the driver should have 15 seconds to accept

	@edge_case
	Scenario: Driver declines trip
		Given the closest available driver has been offered the trip
		When the driver declines the trip
		Then the system should offer the trip to the next closest available driver

	@edge_case
	Scenario: Driver times out
		Given the closest available driver has been offered the trip
		When the driver does not accept within 15 seconds
		Then the system should offer the trip to the next closest available driver

	@edge_case
	Scenario: No driver accepts within 2 minutes
		Given multiple drivers have been offered the trip sequentially
		When no driver accepts within 2 minutes
		Then the request should be cancelled automatically

	@edge_case
	Scenario: Surge pricing confirmation required
		Given demand exceeds supply
		When surge pricing applies
		Then the rider must confirm the surge multiplier before matching proceeds

	@happy_path
	Scenario: Rider confirms surge multiplier
		Given surge pricing has been applied
		When the rider confirms the surge multiplier
		Then matching should proceed with the confirmed multiplier

	@edge_case
	Scenario: Rider rejects surge multiplier
		Given surge pricing has been applied
		When the rider rejects the surge multiplier
		Then the request should be cancelled

	@edge_case
	Scenario: No available drivers within 3 km
		Given there are no drivers within 3 km who are 'Available'
		When the system searches for drivers
		Then the request should be cancelled after 2 minutes

	@edge_case
	Scenario: Multiple drivers equally close
		Given there are multiple available drivers at the same distance from the rider
		When the system searches for drivers
		Then one of the equally close drivers should be selected arbitrarily