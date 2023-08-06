# MFAChallengeQuestionLoginInfo

The login information required when asking the Open Policy Agent to determine if a multi-factor authentication challenge should occur.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_preference** | **str** | The user&#39;s preference regarding multi-factor authentication | [default to 'organisation_policy']
**client_id** | **str** | the client initiating the request on behalf of the user | 
**issuer_org_id** | **str** | The id of the organisation for the issuer the user is logging in through | 
**org_id** | **str** | The id of the organisation the user is a member of | 
**user_id** | **str** | The id of the user requesting access | 
**upstream_idp** | **str** | The upstream IDP that the user is authenticating against | 
**ip_address** | **str** | The source ip address of the user&#39;s request. Both IPv4 and IPv6 address are supported | 
**amr_claim_present** | **bool** | Whether the amr claim is present in the response from the upstream | [default to False]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


