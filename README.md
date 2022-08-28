# AWS CLI Credentials Switcher

### How it works
This switcher changes your [default] profile to the profile of your choice in
both the _config_ and _credentials_ files that AWS CLI uses. So if you use
this script to switch profiles, you no longer have to specify the 

--profile

switch when using aws cli or when using other apps that may be using the default
profile (for example if running python unit tests, boto3 might automatically be
trying to use the [default] credentials.)

### How To Use

**FIRST** make sure that ALL your profiles in BOTH the _config_ and _credentials_
files are NAMED. Because this script will always OVERWRITE the current [default] with your choice.
So, for example, if at the moment your _config_ file looks like 

    [default]
    region = us-west-1
    [profile dis-sandbox-servicaccount1]
    region = us-west-1
    
you need to copy paste [default] and give it a name. So, for example, it should become

    [default]
    region = us-west-1
    [profile dis-sandbox-servicaccount1]
    region = us-west-1
    [profile svcacc-sam-stack]
    region = us-east-1


To use the script, clone this repo or copy the directory  for this specific app to your computer.

cd into the directory where the _switcher.py_ file is and type

    python switcher.py

This script does not have any dependencies (other than the files in its local folder),
and most linux distributions should have
at least python3.8 installed by default, so if the line above does not work, try substituting
'python' for 'python3.8' in the line above.

(Note, if your aws _credentials_ and _config_ files are not in the default location,
you'll need to modify the initialization of the class in the switcher.py file,
and pass the Path as a parameter to AWSCredentialsManager() )

### NOTES!!!
- You MUST have all NAMED credentials in your credentials file.
Otherwise this code would need an additional structure (saved to disk somewhere) 
to 'remember' the original name of the profile that is currently set as the 
default. Another way to express this is that if you have a credential named
_profile1_ and then you switch to _profile2_, in a sense _profile1_ will
be forgotten. 

    So each profile you want to use needs to be NAMED with a name other 
than _default_ in the file, because each time you switch credential,
the _default_ profile will be overwritten by the profile of choice.


- The [default] section of the config file and the credentials file
cannot have any comments or blank lines in it. (Blank lines and comments *before*
the [default] section, or in sections
_other than_ [default] are okay.) So, for example, you should _**NOT**_ have a
comment right after the parameters for [default] that says something like

      # This comment is fine
      [default]
      region = us-west-2
      # The profile below is for bla bla bla  <-- this comment is not ok 
      [service-account-for-sweet-stuff]

    Instead, have that comment _underneath_ the declaration of the next named profile, like

      [service-account-for-sweet-stuff]
      # This profile is for bla bla bla
