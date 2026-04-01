Feature: Data Validation

	Validating input data for ride-hailing operations

	Scenario: Invalid rider location
		Given a rider provides an invalid pickup location
		When the rider attempts to request a trip
		Then the system should reject the request with an error message

	Scenario: Invalid driver status
		Given a driver's status is not 'Available'
		When the system attempts to offer a trip to that driver
		Then the system should skip that driver and look for another available driver

	Scenario: Invalid surge multiplier
		Given surge pricing is applied
		When the surge multiplier is zero or negative
		Then the system should not proceed with matching until a valid multiplier is confirmed