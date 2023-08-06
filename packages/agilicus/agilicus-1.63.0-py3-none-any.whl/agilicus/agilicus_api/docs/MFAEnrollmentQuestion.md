# MFAEnrollmentQuestion

A question to the Open Policy Agent to determine if a multi-factor authentication challenge should occur.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enrollment_expiry** | **datetime** | The expiry time for multi-factor authentication enrollment. Requests to enroll outside this time bound will be denied. | 
**user_mfa_methods** | **list[str]** | The list of multi-factor challenge methods the user has set up. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


