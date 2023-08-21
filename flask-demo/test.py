import os
from cedarpy import is_authorized, AuthzResult, Decision

def read_file_to_string(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Load up Demo App Entities and Schema from file

cedar_app_entities = read_file_to_string('entities.json')
cedar_app_schema = read_file_to_string('schema.json')
policy = read_file_to_string('flask.cedar.policy')

#this request should work/allow
request = {
    "principal": "PhotoApp::User::\"JohnDoe\"",
    "action": "PhotoApp::Action::\"viewPhoto\"",
    "resource": "PhotoApp::Album::\"DoePhotos\"",
    "context": {}
}
#this request should be allowed
request2 = {
    "principal": "PhotoApp::User::\"ric\"",
    "action": "PhotoApp::Action::\"viewPhoto\"",
    "resource": "PhotoApp::Album::\"DoePhotos\"",
    "context": { }
}

authz_result: AuthzResult = is_authorized(request2, policy, cedar_app_entities, cedar_app_schema, True)


if str(authz_result.decision) == 'Decision.Deny':
    print("Forbidden")  # Forbidden
if str(authz_result.decision) == 'Decision.Allow':
    print("Welcome to the admin dashboard!")

print (authz_result.decision)

print (authz_result.metrics)
