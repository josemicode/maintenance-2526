Feature: Subscription Billing

	Managing subscriptions

	Scenario Outline: User upgrades from trial
		Given I am a user on the 14 day free trial for the <cheaper_plan> plan
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
	
	Scenario: Prorated billing
		Given I am a user on the <first_plan> plan
		When I <operation> to "<second_plan>" mid-cycle
		Then the <operation> should take effect immediately
		And I should be charged for the corresponding "<first_plan>" usage (relative to the days passed since this month started) immediately
		And I should be charged for the rest of the usage at the end of the month attending to the <second_plan> plan prices

		Examples:
			| operation 	| first_plan 	| second_plan	|
			| upgrade 	| Basic 	| Pro 		|
			| upgrade	| Pro		| Enterprise 	|
			| downgrade	| Enterprise	| Pro		|
			| downgrade	| Pro 		| Basic		|
 
