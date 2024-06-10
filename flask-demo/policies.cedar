// Policy0 - ALLOW for the Joe Public

permit (
  principal in PhotoApp::User::"JoePublic", 
  action == PhotoApp::Action::"viewPhoto", 
  resource in PhotoApp::Album::"DoePublicPhotos"
);

// Policy1 - ALLOW Public access for only authenticated users

permit (
  principal, 
  action == PhotoApp::Action::"viewPhoto", 
  resource in PhotoApp::Album::"DoePublicPhotos"
)
when { context has authenticated && context.authenticated == true };


// Policy2 - ALLOW for the Doe's to view Private Photos
// //   action in [PhotoApp::Action::"viewPhoto", PhotoApp::Action::"managePhoto"],
permit (
  principal in PhotoApp::UserGroup::"DoeFamily", 
  action == PhotoApp::Action::"viewPhoto",
  resource in PhotoApp::Album::"DoePhotos"
);

// Policy3 - ALLOW only access to pics where you are the owner
// in this case, only JaneDoe is the owner. JohnDoe will not get access
permit (
  principal in PhotoApp::UserGroup::"DoeFamily", 
  action == PhotoApp::Action::"viewPhoto",
  resource in PhotoApp::Album::"DoePhotos"
)
when { resource.owner == principal };

// policy4 - ALLOW for the Doe's to manage Photos
permit (
  principal in PhotoApp::UserGroup::"DoeFamily", 
  action == PhotoApp::Action::"managePhoto", 
  resource in PhotoApp::Album::"DoePhotos"
);

// policy5 - ALLOW for the Doe's to manage Photos who own the album
permit (
  principal in PhotoApp::UserGroup::"DoeFamily", 
  action == PhotoApp::Action::"managePhoto", 
  resource in PhotoApp::Album::"DoePhotos"
)
when { resource.owner == principal };

// policy6 - FORBID access for the Doe's to manage Photos unless you are the owner the album
// forbid (
//   principal, 
//   action == PhotoApp::Action::"managePhoto", 
//   resource in PhotoApp::Album::"DoePhotos"
// )
// unless { resource.owner == principal };

// policy7 - ALLOW for the Doe's to manage Photos when MFA is true
// permit (
//   principal in PhotoApp::UserGroup::"DoeFamily", 
//   action == PhotoApp::Action::"managePhoto", 
//   resource in PhotoApp::Album::"DoePhotos"
// )
// when { context has MFAEnable && context.MFAEnable == true };

//policy8 - ALLOW for Admin User principals
permit (
  principal == PhotoApp::User::"admin", 
  action, 
  resource
);

// policy9 - ALLOW for ric User to view photos
// permit (
//   principal == PhotoApp::User::"ric", 
//   action == PhotoApp::Action::"viewPhoto", 
//   resource
// );


// policy10 - ALLOW for ric User to be siteadmin
// permit (
//   principal == PhotoApp::User::"ric", 
//   action == PhotoApp::Action::"siteAdmin", 
//   resource
// );

// policy11 - ALLOW for ric User to be siteadmin only from specific IP
// permit (
//   principal == PhotoApp::User::"ric", 
//   action == PhotoApp::Action::"siteAdmin", 
//   resource
// )
// when { context has ip && context.ip.isInRange(ip("10.44.1.0/24")) };

// policy12 - ALLOW for ric User to be siteadmin only from specific IP
// permit (
//   principal == PhotoApp::User::"ric", 
//   action == PhotoApp::Action::"siteAdmin", 
//   resource
// )
// when { context has ip && context.ip.isInRange(ip("11.44.1.0/24")) };