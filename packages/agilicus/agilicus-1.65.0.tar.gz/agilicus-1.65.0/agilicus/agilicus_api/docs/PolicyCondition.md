# PolicyCondition

A condition to be evaluated by the policy engine
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**condition_type** | **str** | The type of this condition. The type determines how the value will be evaluated. This parameter is case sensitive. | 
**inverted** | **bool** | Whether to invert the condition (ie the not operator). If the condition is &#x60;a &#x3D;&#x3D; b&#x60; inverting the condition results in &#x60;not (a &#x3D;&#x3D; b)&#x60; | [optional] [default to False]
**value** | **str** | A JSON string representing the value to compare against. The structure of the comparision and type of the value depends on the condition type. A comparision is done to determine the result of the condition (either &#x60;true&#x60; or &#x60;false&#x60;) | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


