# PolicyRuleSpec

A rule to be evaluated by the policy engine.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | The action to take if the conditions are evaluated to true. Actions are case sensitive. | 
**org_id** | **str** | The org id corresponding to the issuer whose policy you are updating | [optional] 
**priority** | **int** | The priority of this rule relative to other rules. Rules of a higher priority will be evaluated first and if the condition evaluates to true the action will be taken. 1 is the highest priority. | 
**conditions** | [**list[PolicyCondition]**](PolicyCondition.md) | An array mapping a condition type to a condition. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


