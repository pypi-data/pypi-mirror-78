# PolicySpec

The definition of the policy.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the policy so that it can be identifiable when applied to organizations or clients | [optional] 
**issuer_id** | **str** | The issuer that this policy applies to | 
**org_id** | **str** | The org id corresponding to the issuer whose policy you are updating | [optional] 
**supported_mfa_methods** | **list[str]** | A list of supported MFA methods. An empty list implies that no MFA methods are acceptable | 
**default_action** | **str** | The action to take if none of the conditions evaluate to true. Actions are case sensitive. | 
**rules** | [**list[PolicyRule]**](PolicyRule.md) | The list of rules defining the policy. A rule consists of conditions, actions, and a priority | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


