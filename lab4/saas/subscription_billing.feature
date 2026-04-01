Feature: Subscription Billing

	Managing subscriptions

	Scenario Outline: User upgrades from trial
		Given I am a user on the 14 day free trial for the <cheaper_plan>
		When I upgrade to <plan>
		Then the trial period for <cheaper_plan> should end immediately
		And I should be charged for the <plan> immediately

		Examples:
			| cheaper_plan 	| plan		|
			| Basic 	| Pro 		|
			| Basic		| Enterprise 	|
			| Pro 		| Enterprise 	|

	Scenario: Automatic suspension after failed payment retries
		Given a subscription has entered the "Past Due" state
		When the system has attempted to process the payment daily for 3 days to no success
		Then the subscription status should change to "Suspended"
		And the customer's access to the product should be blocked
	
	
