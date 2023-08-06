#!/usr/bin/env python

from CGPCLI.Connection import read
from CGPCLI.Errors import CommandFailedError
from CGPCLI.Parser import parse_to_python_object, parse_to_CGP_object

def _operate(sock, payload):
  
  sock.send(payload.encode())

  result = read(sock, get=True)
  
  if result['header'] == '200 OK':
    return {"header":'200', "body":'OK'}
  
  elif result['header'] == '200 data follow':
    result['body'] = parse_to_python_object(result['body'])
    return result
  
  else:
    raise CommandFailedError(str(result))

#Domain Set Administration
def list_domains(sock):
  '''Use this command to get the list of domains.
     The command produces output data - an list with the names of all server domains.'''
  
  return _operate(sock, 'LISTDOMAINS\n')

def main_domain_name(sock):
  '''Use this command to get the name of the Main Domain.
     The command produces output data - a string with the Main Domain name.'''
  
  return _operate(sock, 'MAINDOMAINNAME\n')
      
def get_domain_defaults(sock):
  '''Use this command to get the server-wide default Domain Settings.
     The command produces an output - a dictionary with the default Domain Settings.'''

  return _operate(sock, 'GETDOMAINDEFAULTS\n')

def update_domain_defaults(sock, new_settings):
  '''Use this command to change the server-wide default Domain settings.
  
     new_settings : dictionary
     This dictionary is used to update the default Domain settings dictionary.
     It does not have to contain all settings data, the omitted settings will be left unmodified.'''

  return _operate(sock, 'UPDATEDOMAINDEFAULTS ' + parse_to_CGP_object(new_settings) + '\n')

def set_domain_defaults(sock, new_settings):
  '''Use this command to change the server-wide default Domain settings.
  
     new_settings : dictionary
     This dictionary is used to replace the server-wide default Domain settings dictionary.'''

  return _operate(sock, 'SETDOMAINDEFAULTS ' + parse_to_CGP_object(new_settings) + '\n')

def get_cluster_domain_defaults(sock):
  '''These command is available in the Dynamic Cluster only.
  Use this command to get the cluster-wide default Domain Settings.
  The command produces an output - a dictionary with the default Domain Settings.'''

  return _operate(sock, 'GETCLUSTERDOMAINDEFAULTS\n')

def update_cluster_domain_defaults(sock, new_settings):
  '''These command is available in the Dynamic Cluster only.
     Use this command to change the cluster-wide default Domain settings.
  
     new_settings : dictionary
     This dictionary is used to update the default Domain settings dictionary.
     It does not have to contain all settings data, the omitted settings will be left unmodified.'''

  return _operate(sock, 'UPDATECLUSTERDOMAINDEFAULTS ' + parse_to_CGP_object(new_settings) + '\n')

def set_cluster_domain_defaults(sock, new_settings):
  '''These command is available in the Dynamic Cluster only.
     Use this command to change the cluster-wide default Domain settings.
  
     new_settings : dictionary
     This dictionary is used to replace the cluster-wide default Domain settings dictionary.'''

  return _operate(sock, 'SETCLUSTERDOMAINDEFAULTS ' + parse_to_CGP_object(new_settings) + '\n')

def get_server_account_defaults(sock):
  '''Use this command to get the server-wide Default Account settings.
     The command produces an output - a dictionary with the global default Account settings.'''
  
  return _operate(sock, 'GETSERVERACCOUNTDEFAULTS\n')

def update_server_account_defaults(sock, new_settings):
  '''Use this command to update the server-wide Default Account settings.
  
     new_settings : dictionary
     This dictionary is used to update the Default Account settings dictionary.
     It does not have to contain all settings data, the omitted settings will be left unmodified.'''

  return _operate(sock, 'UPDATESERVERACCOUNTDEFAULTS ' + parse_to_CGP_object(new_settings) + '\n')

def set_server_account_defaults(sock, new_settings):
  '''Use this command to set the server-wide Default Account settings.
  
     new_settings : dictionary
     This dictionary is used to replace the server-wide Default Account settings dictionary.'''

  return _operate(sock, 'SETSERVERACCOUNTDEFAULTS ' + parse_to_CGP_object(new_settings) + '\n')

def get_cluster_account_defaults(sock):
  '''These command is available in the Dynamic Cluster only.
     Use this command to get the cluster-wide Default Account settings.
     The command produces an output - a dictionary with the global default Account settings.'''
  
  return _operate(sock, 'GETCLUSTERACCOUNTDEFAULTS\n')

def update_cluster_account_defaults(sock, new_settings):
  '''These command is available in the Dynamic Cluster only.
     Use this command to update the cluster-wide Default Account settings.
  
     new_settings : dictionary
     This dictionary is used to update the Default Account settings dictionary.
     It does not have to contain all settings data, the omitted settings will be left unmodified.'''

  return _operate(sock, 'UPDATECLUSTERACCOUNTDEFAULTS ' + parse_to_CGP_object(new_settings) + '\n')

def set_cluster_account_defaults(sock, new_settings):
  '''These command is available in the Dynamic Cluster only.
     Use this command to set the cluster-wide Default Account settings.
  
     new_settings : dictionary
     This dictionary is used to replace the cluster-wide Default Account settings dictionary.'''

  return _operate(sock, 'SETCLUSTERACCOUNTDEFAULTS ' + parse_to_CGP_object(new_settings) + '\n')

def get_server_account_prefs(sock):
  '''Use this command to get the server-wide Default Account Preferences.
     The command produces an output - a dictionary with the default Preferences.'''
  
  return _operate(sock, 'GETSERVERACCOUNTPREFS\n')

def update_server_account_prefs(sock, new_settings):
  '''Use this command to change the server-wide Default Account Preferences.
  
     new_settings : dictionary
     This dictionary is used to update the Default Account Preferences.
     It does not have to contain all preferences data, the omitted Preferences will be left unmodified.'''

  return _operate(sock, 'UPDATESERVERACCOUNTPREFS ' + parse_to_CGP_object(new_settings) + '\n')

def set_server_account_prefs(sock, new_settings):
  '''Use this command to change the server-wide Default Account Preferences.
  
     new_settings : dictionary
     This dictionary is used to replace the server-wide Default Account Preferences.
     All old server-wide Default Account Preferences are removed.'''

  return _operate(sock, 'SETSERVERACCOUNTPREFS ' + parse_to_CGP_object(new_settings) + '\n')

def get_cluster_account_prefs(sock):
  '''These command is available in the Dynamic Cluster only.
     Use this command to get the cluster-wide Default Account Preferences.
     The command produces an output - a dictionary with the global default Account Preferences.'''
  
  return _operate(sock, 'GETCLUSTERACCOUNTPREFS\n')

def update_cluster_account_prefs(sock, new_settings):
  '''These command is available in the Dynamic Cluster only.
     Use this command to update the cluster-wide Default Account Preferences.
  
     new_settings : dictionary
     This dictionary is used to update the Default Account Preferences dictionary.
     It does not have to contain all Preferences data, the omitted Preferences will be left unmodified.'''

  return _operate(sock, 'UPDATECLUSTERACCOUNTPREFS ' + parse_to_CGP_object(new_settings) + '\n')

def set_cluster_account_prefs(sock, new_settings):
  '''These command is available in the Dynamic Cluster only.
     Use this command to set the cluster-wide Default Account Preferences.
  
     new_settings : dictionary
     This dictionary is used to replace the cluster-wide Default Account Preferences dictionary.'''

  return _operate(sock, 'SETCLUSTERACCOUNTPREFS ' + parse_to_CGP_object(new_settings) + '\n')

def create_domain(sock, domain_name, shared=False, storage=None, settings=None):
  '''Use this command to create a new secondary Domain.
    
     domain_name : string
     This parameter specifies the Domain name to create.
     
     storage : string
     This optional parameter specifies the "storage mount Point" directory for the Domain data (the name should be specified without the .mnt suffix).
     
     settings : dictionary
     This optional parameter specifies the Domain settings.
     
     
     Use the SHARED keyword to create a Cluster-wide Domain in a Dynamic Cluster.'''

  params = domain_name
  
  if shared:
      params += ' SHARED'
    
  if storage is not None:
    params += ' PATH ' + storage
    
  if settings is not None:
    params += ' ' + parse_to_CGP_object(settings)
  
  return _operate(sock, 'CREATEDOMAIN ' + params + '\n')

def rename_domain(sock, old_domain_name, new_domain_name, storage=None):
  '''Use this command to rename a Domain.
    
     old_domain_name : string
     This parameter specifies the name of an existing secondary Domain.
     
     new_domain_name : string
     This parameter specifies the new Domain name.

     storage : string
     This optional parameter specifies the new "storage mount Point" directory for the Domain data (the name should be specified without the .mnt suffix).'''

  params = old_domain_name + ' INTO ' + new_domain_name
  
  if storage is not None:
    params += ' PATH ' + storage
  
  return _operate(sock, 'RENAMEDOMAIN ' + params + '\n')

def delete_domain(sock, domain_name, force=False):
  '''Use this command to remove a Domain.
    
     domain_name : string
     This parameter specifies the name of the Domain to be removed.
     
     FORCE
     This optional parameter specifies that the Domain should be removed even if it is not empty.
     All Domain objects (Accounts, Groups, etc.) will be removed.'''

  params = domain_name

  if force:
    params += ' FORCE'    
  
  return _operate(sock, 'DELETEDOMAIN ' + params + '\n')

def create_directory_domain(sock, domain_name, settings=None):
  '''Use this command to create a new directory-based Domain.
     
     domain_name : string
     This parameter specifies the Domain name to create.
     
     settings : dictionary
     This optional parameter specifies the Domain settings.
     
     This operation is allowed only when the Directory-based Domains are enabled.'''

  params = domain_name
  
  if settings is not None:
    params += ' ' + parse_to_CGP_object(settings)
  
  return _operate(sock, 'CREATEDIRECTORYDOMAIN ' + params + '\n')

def reload_directory_domains(sock):
  '''Use this command to tell the server to scan the Domains Directory subtree so it can find all additional Directory-based Domains created directly in the Directory, bypassing the CommuniGate Pro Server.
     This operation is allowed only when the Directory-based Domains are enabled.'''
  
  return _operate(sock, 'RELOADDIRECTORYDOMAINS\n')

def list_server_telnums(sock, limit, filter=None):
  '''Use this command to read Telnum numbers created in all (non-clustered) Domains.
     The command produces an output - a dictionary where each key is a Telnum number, and its value is the Account name it is assigned to.
     An numeric element for an empty ("") key is added, it contains the total number of Telnum numbers created.
    
     filter : string
     If this optional parameter is specified, only the telnum numbers containing the specified string are returned.
    
     limit : int
     The maximum number of Telnum numbers to return.'''
  
  params = str(limit)
  
  if filter is not None:
    params += 'FILTER ' + filter + ' ' + params
  
  return _operate(sock, 'LISTSERVERTELNUMS ' + params + '\n')

def list_cluster_telnums(sock, limit, filter=None):
  '''Use this command to read Telnum numbers created in all clustered Domains.
     The command produces an output - a dictionary where each key is a Telnum number, and its value is the Account name it is assigned to.
     An numeric element for an empty ("") key is added, it contains the total number of Telnum numbers created.
    
     filter : string
     If this optional parameter is specified, only the telnum numbers containing the specified string are returned.
    
     limit : int
     The maximum number of Telnum numbers to return.'''
  
  params = str(limit)
  
  if filter is not None:
    params += 'FILTER ' + filter + ' ' + params
  
  return _operate(sock, 'LISTCLUSTERTELNUMS ' + params + '\n')

def get_server_trusted_certs(sock):
  '''Use this command to get the server-wide set of Trusted Certificates.
     The command produces an output - an list of datablocks.
     Each datablock contains one X.509 certificate data.'''
  
  return _operate(sock, 'GETSERVERTRUSTEDCERTS\n')

def set_server_trusted_certs(sock, new_certificates):
  '''Use this command to set the server-wide set of Trusted Certificates.

     new_certificates : list
     This list should contain datablocks with X.509 certificate data.
     It is used to replace the server-wide list of Trusted Certificates.'''

  return _operate(sock, 'SETSERVERTRUSTEDCERTS ' + parse_to_CGP_object(new_certificates) + '\n')

def get_cluster_trusted_certs(sock):
  '''These command is available in the Dynamic Cluster only.
     Use this command to get the cluster-wide set of Trusted Certificates.
     The command produces an output - an list of datablocks.
     Each datablock contains one X.509 certificate data.'''
    
  return _operate(sock, 'GETCLUSTERTRUSTEDCERTS\n')
 
def set_cluster_trusted_certs(sock, new_certificates):
  '''These command is available in the Dynamic Cluster only.
     Use this command to set the cluster-wide set of Trusted Certificates.

     new_certificates : list
     This list should contain datablocks with X.509 certificate data.
     It is used to replace the cluster-wide list of Trusted Certificates.'''

  return _operate(sock, 'SETCLUSTERTRUSTEDCERTS ' + parse_to_CGP_object(new_certificates) + '\n')

def get_directory_integration(sock):
  '''Use this command to get the server-wide Directory Integration settings.
     The command produces an output - a dictionary with the Directory Integration settings.'''
  
  return _operate(sock, 'GETDIRECTORYINTEGRATION\n')
 
def set_directory_integration(sock, new_settings):
  '''Use this command to set the server-wide Directory Integration settings.
     
     new_settings : dictionary
     This dictionary is used to replace the server-wide Directory Integration settings dictionary.'''

  return _operate(sock, 'SETDIRECTORYINTEGRATION ' + parse_to_CGP_object(new_settings) + '\n')

def get_cluster_directory_integration(sock):
  '''Use this command to get the cluster-wide Directory Integration settings.
     The command produces an output - a dictionary with the Directory Integration settings.'''

  return _operate(sock, 'GETCLUSTERDIRECTORYINTEGRATION\n')
 
def set_cluster_directory_integration(sock, new_settings):
  '''Use this command to set the cluster-wide Directory Integration settings.
     
     new_settings : dictionary
     This dictionary is used to replace the cluster-wide Directory Integration settings dictionary.'''

  return _operate(sock, 'SETCLUSTERDIRECTORYINTEGRATION ' + parse_to_CGP_object(new_settings) + '\n')

def create_domain_storage(sock, storage, shared=False):
  '''Use this command to create a "storage mount point" for new Domains.
  
     storage : string
     This parameter specifies the "storage mount Point" name.
     
     Use the SHARED keyword to create a "storage mount point" for Cluster Domains in a Dynamic Cluster.'''

  params = ''
  
  if shared:
    params += 'SHARED '
    
  params += 'PATH ' + storage
  
  return _operate(sock, 'CREATEDOMAINSTORAGE ' + params + '\n')

def list_domain_storage(sock, shared=False):
  '''Use this command to list "storage mount points" for Domains.
     The command produces an output - an list with "storage mount points" names.
     Use the SHARED keyword to list "storage mount point" for Cluster Domains in a Dynamic Cluster.'''
  
  params = ''
  
  if shared:
    params += ' SHARED'
  
  return _operate(sock, 'LISTDOMAINSTORAGE' + params + '\n')

#Domain Administration
def get_domain_settings(sock, domain_name=None):
  '''Use this command to get the Domain settings.
     The command produces an output - a dictionary with the domain_name settings.
     Only the explicitly set (not the default) settings are included into that dictionary.
     
     domain_name : string
     This optional parameter specifies the name of an existing Domain.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name
  
  return _operate(sock, 'GETDOMAINSETTINGS' + params + '\n')

def get_domain_effective_settings(sock, domain_name=None):
  '''Use this command to get the Domain settings.
     The command produces an output - a dictionary with the domain_name settings.
     Both the explicitly set and the default settings are included into that dictionary.
     
     domain_name : string
     This optional parameter specifies the name of an existing Domain.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name
  
  return _operate(sock, 'GETDOMAINEFFECTIVESETTINGS' + params + '\n')

def update_domain_settings(sock, new_settings, domain_name=None):
  '''Use this command to update the Domain settings.
     
     domain_name : string
     This optional parameter specifies the name of an existing Domain.
     
     new_settings : dictionary
     This dictionary is used to update the Domain settings dictionary. It does not have to contain all settings data, the omitted settings will be left unmodified. If a new setting value is specified as the string default, the Domain setting value is removed, so the default Domain settings value will be used.
     
     If this command is used by a Domain Administrator, it will update only those Domain Settings that this Domain Administrator is allowed to modify.'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' '
      
  return _operate(sock, 'UPDATEDOMAINSETTINGS ' + params + parse_to_CGP_object(new_settings) + '\n')

def get_account_defaults(sock, domain_name=None):
  '''Use this command to get the default Account settings for the specified Domain.
     The command produces an output - a dictionary with the default settings.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the Administrator Domain.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name
      
  return _operate(sock, 'GETACCOUNTDEFAULTS' + params + '\n')

def update_account_defaults(sock, new_settings, domain_name=None):
  '''Use this command to modify the Default Account settings for the specified Domain.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.
     
     new_settings : dictionary
     This dictionary is used to modify the Domain Default Account settings.
     The dictionary does not have to contain all settings data, the omitted settings will be left unmodified.
     If a new setting value is specified as the string default, the setting value is removed, so the global Server Default Account Settings will be used.
     
     If this command is used by a Domain Administrator, it will update only those Default Account settings this Administrator is allowed to modify.'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' '
      
  return _operate(sock, 'UPDATEACCOUNTDEFAULTS ' + params + parse_to_CGP_object(new_settings) + '\n')
      
def get_account_default_prefs(sock, domain_name=None):
  '''Use this command to get the Default Account Preferences for the specified Domain.
     The command produces an output - a dictionary with the default Preferences.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name
      
  return _operate(sock, 'GETACCOUNTDEFAULTPREFS' + params + '\n')

def update_account_default_prefs(sock, new_settings, domain_name=None):
  '''Use this command to change the Default Account Preferences for the specified Domain.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the authenticated user Domain.
     
     new_settings : dictionary
     This dictionary is used to modify the Domain Default Account Preferences.
     It does not have to contain all Preferences data, the omitted elements will be left unmodified.
     If a new element value is specified as the string default, the Default Preferences value is removed, so the default Server-wide (or Cluster-wide) Account Preferences value will be used.'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' '
      
  return _operate(sock, 'UPDATEACCOUNTDEFAULTPREFS ' + params + parse_to_CGP_object(new_settings) + '\n')

def set_account_default_prefs(sock, new_settings, domain_name=None):
  '''Use this command to change the Default Account Preferences for the specified Domain.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the authenticated user Domain.
     
     new_settings : dictionary
     This dictionary is used to replace the Default Account Preferences.
     All old Default Account Preferences are removed.
     
     This command can be used by Domain Administrators only if they have the WebUserSettings access right.'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' '
      
  return _operate(sock, 'SETACCOUNTDEFAULTPREFS ' + params + parse_to_CGP_object(new_settings) + '\n')

def get_account_template(sock, domain_name=None):
  '''Use this command to get the Account Template settings.
     The command produces an output - a dictionary with the Template settings.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name
      
  return _operate(sock, 'GETACCOUNTTEMPLATE' + params + '\n')

def update_account_template(sock, new_settings, domain_name=None):
  '''Use this command to modify the Account Template settings.
    
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.
    
     new_settings : dictionary
     This dictionary is used to modify the Domain Account Template.
     All new Accounts in the specified Domain will be created with the Template settings.
     The dictionary does not have to contain all settings data, the omitted settings will be left unmodified.
     If a new setting value is specified as the string default, the Template setting value is removed.
    
     If this command is used by a Domain administrator, it will update only those Template settings that the Domain administrator is allowed to modify.'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' '
      
  return _operate(sock, 'UPDATEACCOUNTDEFAULTPREFS ' + params + parse_to_CGP_object(new_settings) + '\n')

def get_domain_aliases(sock, domain_name):
  '''Use this command to get the list of Domain Aliases.
     The command produces an output - an list with the Domain alias names.
     
     domain_name : string
     This parameter specifies the name of an existing Domain.'''
  
  return _operate(sock, 'GETDOMAINALIASES ' + domain_name + '\n')
  
  result = read(sock, get=True)

def get_domain_mail_rules(sock, domain_name):
  '''Use this command to get the list of Domain Queue Rules.
     The command produces an output - an list of the Queue Rules specified for the Domain.
     
     domain_name : string
     This parameter specifies the name of an existing Domain.'''
  
  return _operate(sock, 'GETDOMAINMAILRULES ' + domain_name + '\n')
  
def set_domain_mail_rules(sock, domain_name, new_rules):
  '''Use this command to set the Domain Queue Rules.
     
     domain_name : string
     This parameter specifies the name of an existing Domain.
    
     new_rules : list
     This list should contain the Domain Queue Rules.
     All old Domain Queue Rules are removed.
     
     This command can be used by Domain Administrators only if they have the RulesAllowed access right.'''

  return _operate(sock, 'SETDOMAINMAILRULES ' + domain_name +  ' ' + parse_to_CGP_object(new_rules) + '\n')

def get_domain_signal_rules(sock, domain_name):
  '''Use this command to get the list of Domain Signal Rules.
     The command produces an output - an list of the Signal Rules specified for the Domain.
     
     domain_name : string
     This parameter specifies the name of an existing Domain.'''
  
  return _operate(sock, 'GETDOMAINSIGNALRULES ' + domain_name + '\n')
  
def set_domain_signal_rules(sock, domain_name, new_rules):
  '''Use this command to set the Domain Signal Rules.
     
     domain_name : string
     This parameter specifies the name of an existing Domain.
    
     new_rules : list
     This list should contain the Domain Signal Rules.
     All old Domain Signal Rules are removed.
     
     This command can be used by Domain Administrators only if they have the SignalRulesAllowed access right.'''

  return _operate(sock, 'SETDOMAINSIGNALRULES ' + domain_name +  ' ' + parse_to_CGP_object(new_rules) + '\n')

def list_admin_domains(sock, domain_name=None):
  '''Use this command to get the list of Domains that can be administered by Domain Administrator Accounts in the specified domain_name Domain.
     The command produces an output - an list with the Domain names.

     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the authenticated user Domain.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name
  
  return _operate(sock, 'LISTADMINDOMAINS' + params + '\n')

def list_domain_objects(sock, domain_name, limit,
                        account=False, aliases=False, forwarders=False,
                        filter=None, cookie=None):
  '''Use this command to get a list of Domain objects.
     
     domain_name : string
     This parameter specifies the Domain name.
     
     filter : string
     This optional parameter specifies a filter string: only objects with names including this string as a substring are listed.
    
     limit : int
     This parameter specifies the maximum number of objects to list.
     
     ACCOUNTS, ALIASES, FORWARDERS
     These keywords specify which Domain objects should be listed.
     
     cookie : string
     This optional parameter specifies a "cookie" string.
     
     The command produces output data - an list with the following elements:
     
     - a numeric string with the total number of Domain Accounts
     - a dictionary with Domain Objects. Each dictionary key is a Domain Object name.
     The dictionary value depends on the Domain Object type:
     
     Account
     the dictionary object is a string (the Account file extension)
     
     Account Alias
     the dictionary object is an list. Its only element is a string with the Alias owner (Account) name.
     
     Forwarder
     the dictionary object is an list. Its only element is an list. Its only element is a string with the Forwarder address.
     
     - a numeric string with the total number of Aliases in the Domain.
     - a numeric string with the total number of Forwarders in the Domain.
     - a new "cookie" string (optional, exists only if there was the COOKIE cookie part in the command.)
   
     To list Objects in large Domains, specify some reasonable limit value (below 10,000) and specify and empty cookie string.
     If not all Objects are returned, issue the command again, using the new cookie value specified in the response list.
     When all Objects are returned, the new cookie value in the response is an empty string.'''
  
  params = domain_name
  
  if filter is not None:
    params += ' FILTER ' + filter
  
  params += ' ' + str(limit)
  
  if account:
    params += ' ACCOUNTS'
  if aliases:
    params += ' ALIASES'
  if forwarders:
    params += ' FORWARDERS'

  if cookie is not None:
    params += ' COOKIE ' + cookie
  
  return _operate(sock, 'LISTDOMAINOBJECTS ' + params + '\n')

def list_accounts(sock, domain_name=None):
  '''Use this command to get the list of all Accounts in the Domain.
     The command produces output data - a dictionary with the keys listing all Accounts in the specified (or default) Domain.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name
  
  return _operate(sock, 'LISTACCOUNTS' + params + '\n')

def list_domain_telnums(sock, domain_name, limit, filter=None):
  '''Use this command to read Telnum numbers created in the specified Domain.
     The command produces an output - a dictionary where each key is a Telnum number, and its value is the Account name it is assigned to.
     An numeric element for an empty ("") key is added, it contains the total number of Telnum numbers created.
     
     domain_name : string
     This parameter specifies the Domain name.
     
     filter : string
     If this optional parameter is specified, only the telnum numbers containing the specified string are returned.
     
     limit : int
     The maximum number of Telnum numbers to return.'''
  
  params = domain_name
  
  if filter is not None:
    params += ' FILTER ' + filter
  
  params += ' ' + str(limit)
  
  return _operate(sock, 'LISTDOMAINTELNUMS' + params + '\n')

def insert_directory_records(sock, domain_name):
  '''Use this command to insert records for Domain objects (Accounts, Groups, Mailing Lists, Forwarders) into the Directory.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the authenticated user Domain.
     
     This command can be used by Domain Administrators only if they have the CentralDirectory access right.'''

  return _operate(sock, 'INSERTDIRECTORYRECORDS ' + domain_name + '\n')

def delete_directory_records(sock, domain_name):
  '''Use this command to delete Domain object records from the Directory.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the authenticated user Domain.
     
     This command can be used by Domain Administrators only if they have the CentralDirectory access right.'''

  return _operate(sock, 'DELETEDIRECTORYRECORDS ' + domain_name + '\n')

def create_account_storage(sock, domain_name, storage):
  '''Use this command to create a "storage mount point" for new Accounts in the Domain.
     
     domain_name : string
     This parameter specifies the Domain name.

     storage : string
     This parameter specifies the "storage mount Point" name.'''

  return _operate(sock, 'CREATEACCOUNTSTORAGE ' + domain_name + ' PATH ' + storage + '\n')

def list_account_storage(sock, domain_name):
  '''Use this command to list Account "storage mount points" in the specified Domain.
     The command produces an output - an list with "storage mount points" names.
     
     domain_name : string
     This parameter specifies the Domain name.'''

  return _operate(sock, 'LISTACCOUNTSTORAGE ' + domain_name + '\n')

def set_domain_aliases(sock, domain_name, new_aliases):
  '''The following command is available for the System Administrators only
     Use this command to set the Domain aliases.
    
     domain_name : string
     This parameter specifies the name of an existing Domain.
    
     new_aliases : list
     This list should contain the Domain alias name strings.
     All old Domain aliases are removed.'''

  return _operate(sock, 'SETDOMAINALIASES ' + domain_name + ' ' + parse_to_CGP_object(new_aliases) + '\n')

def set_domain_settings(sock, domain_name, new_settings):
  '''The following command is available for the System Administrators only
     Use this command to change the Domain settings.
    
     domain_name : string
     This parameter specifies the name of an existing Domain.
    
     new_settings : dictionary
     This dictionary is used to replace the Domain settings dictionary.
     All old Domain aliases are removed.'''

  return _operate(sock, 'SETDOMAINSETTINGS ' + domain_name + ' ' + parse_to_CGP_object(new_settings) + '\n')
       
def set_account_defaults(sock, new_settings, domain_name=None):
  '''The following command is available for the System Administrators only
     Use this command to change the Default Account settings for the specified Domain.

     domain_name : string
     This parameter specifies the Domain name.
     
     new_settings : dictionary
     This dictionary is used to replace the Domain Default Account settings.
     All old Account Default settings are removed.'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' '
      
  return _operate(sock, 'SETACCOUNTDEFAULTS ' + params + parse_to_CGP_object(new_settings) + '\n')

def set_account_template(sock, new_settings, domain_name=None):
  '''The following command is available for the System Administrators only
     Use this command to change the Account Template settings.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.
     
     new_settings : dictionary
     This dictionary is used to update the Domain Account Template.
     All new Accounts in the specified Domain will be created with the Template settings.
     All old Account Template settings are removed.'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' '
      
  return _operate(sock, 'SETACCOUNTTEMPLATE ' + params + parse_to_CGP_object(new_settings) + '\n')

def get_domain_location(sock, domain_name=None):
  '''The following command is available for the System Administrators only
     Use this command to get the Domain file directory path (relative to the Server base directory).
     The command produces an output - a string with the Domain file path.

     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.'''

  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name
      
  return _operate(sock, 'GETDOMAINLOCATION' + params + '\n')

def suspend_domain(sock, domain_name):
  '''The following command is available for the System Administrators only
     Use this command to suspend a Domain, so all currently active Accounts are closed and no Account can be opened in this Domain.
     
     domain_name : string
     This parameter specifies the name of the Domain to be suspended.'''

  return _operate(sock, 'SUSPENDDOMAIN ' + domain_name + '\n')

def resume_domain(sock, domain_name):
  '''The following command is available for the System Administrators only
     Use this command to resume a Domain, so Accounts can be opened in this Domain.
     
     domain_name : string
     This parameter specifies the name of the Domain to be resumed.'''

  return _operate(sock, 'RESUMEDOMAIN ' + domain_name + '\n')

#Account Administration
def create_account(sock, account_name, account_type='MultiMailbox', legacy=False,
                   storage=None, settings=None):
  '''Use this command to create new accounts.
     
     account_name : string
     This parameter specifies the name for the new Account.
     The name can contain the @ symbol followed by the Domain name, in this case the Account is created in the specified Domain.
     If the Domain name is not specified, the command applies to the administrator Domain.
     
     account_type : MultiMailbox | TextMailbox | MailDirMailbox | SlicedMailbox | AGrade | BGrade | CGrade
     This optional parameter specifies the type of the Account to create. If no Account type is specified a MultiMailbox-type Account is created.
     
     storage : string
     This optional parameter specifies the "storage mount Point" directory for the Account data (the name should be specified without the .mnt suffix).
     
     LEGACY
     This optional flag tells the system to create an Account with a Legacy (visible for legacy mailers) INBOX.
     
     settings : dictionary
     This optional parameter specifies the initial Account settings.
     Account is created using the settings specified in the Account Template for the target Domain.
     If the settings parameter is specified, it is used to modify the Template settings.
     
     This command can be used by Domain Administrators only if they have the CanCreateAccounts access right.
     Additionally, if a single-mailbox Account format is requested or the LEGACY flag is used, the Domain Administrators must have the CanCreateSpecialAccounts access right.
     If this command is used by a Domain Administrator, it will use only those Account settings this Administrator is allowed to modify.'''

  params = ''

  if account_type not in ['MultiMailbox', 'TextMailbox', 'MailDirMailbox',
                          'SlicedMailbox', 'AGrade', 'BGrade', 'CGrade']:
    raise ValueError("Value is out of list")
        
  if legacy:        
    params += ' LEGACY'

  if storage is not None:
    params += ' PATH ' + storage        
    
  if settings is not None:
    params += ' ' + parse_to_CGP_object(settings)
  
  return _operate(sock, 'CREATEACCOUNT ' + params + '\n')

def rename_account(sock, old_account_name, new_account_name, storage=None):
  '''Use this command to rename Accounts.
     
     old_account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
     
     new_account_name : string
     This parameter specifies the new Account name. The name can include the Domain name (see above).
     
     storage : string
     This optional parameter specifies the "storage mount Point" directory for the moved Account data (the name should be specified without the .mnt suffix).
     
     This command can be used by Domain Administrators only if they have the CanCreateAccounts access right.'''

  params = ''

  if storage is not None:
    params  = ' PATH ' + storage        
  
  return _operate(sock, 'RENAMEACCOUNT ' + old_account_name + ' into ' + new_account_name + params + '\n')

def delete_account(sock, old_account_name):
  '''Use this command to remove Accounts.
     
     old_account_name : string
     This parameter specifies the name of an existing Account. The name can include the Domain name (see above).
     
     This command can be used by Domain Administrators only if they have the CanCreateAccounts access right.'''

  return _operate(sock, 'DELETEACCOUNT ' + old_account_name + '\n')

def set_account_type(sock, account_name, account_type):
  '''Use this command to change the Account type.
     
     account_name : string
     This parameter specifies the name of an existing Account. The name can include the Domain name (see above).
     
     account_type : MultiMailbox | AGrade | BGrade | CGrade
     This parameter specifies the new Account type. The current Account type must also belong to this type set.'''

  return _operate(sock, 'SETACCOUNTTYPE ' + account_name + ' ' + account_type + '\n')

def get_account_settings(sock, account_name):
  '''Use this command to get the Account settings. The command produces an output - a dictionary with the Account settings. Only the explicitly set (not the default) Account settings are included into the dictionary.
     
     account_name : string
     This parameter specifies the name of an existing Account. The name can include the Domain name (see above).
     You can also specify the single asterisk (*) symbol instead of an Account name.
     This will indicate the current authenticated Account.'''
  
  return _operate(sock, 'GETACCOUNTSETTINGS ' + account_name + '\n')

def update_account_settings(sock, account_name, new_settings):
  '''Use this command to update the Account settings.

     account_name : string
     This parameter specifies the name of an existing Account. The name can include the Domain name (see above).
     
     new_settings : dictionary
     This dictionary is used to update the Account settings dictionary.
     It does not have to contain all settings data, the omitted settings will be left unmodified.
     If a new setting value is specified as the string default, the Account setting value is removed, so the default Account setting value will be used.
     
     If this command is used by a Domain Administrator, it will update only those Account settings this Administrator is allowed to modify.'''

  return _operate(sock, 'UPDATEACCOUNTSETTINGS ' + account_name + ' ' + parse_to_CGP_object(new_settings) + '\n')

def get_account_effective_settings(sock, account_name):
  '''Use this command to get the effective Account settings.
     The command produces an output - a dictionary with the Account settings.
     Both the explicitly set and the default Account settings are included into the dictionary.
     
     account_name : string
     This parameter specifies the name of an existing Account. The name can include the Domain name (see above).
     You can also specify the single asterisk (*) symbol instead of an Account name.
     This will indicate the current authenticated Account.'''
  
  return _operate(sock, 'GETACCOUNTEFFECTIVESETTINGS ' + account_name + '\n')

def get_account_setting(sock, account_name, key_name):
  '''Use this command to get a single setting from the effective Account settings list.
  The command produces an output - an object which can be a string, an list or a dictionary with the Account setting, or null-object.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
     You can also specify the single asterisk (*) symbol instead of an Account name.
     This will indicate the current authenticated Account.
     
     key_name : string
     This parameter specifies the name of the setting to read.'''
  
  return _operate(sock, 'GETACCOUNTONESETTING ' + account_name + ' ' + key_name + '\n')

def set_account_password(sock, account_name, new_password, check=False, method=None, tag=None):
  '''Use this command to update the Account password.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
     
     new_password : string
     This string specifies the new Account password.
     The new password will be stored using the effective Password Encryption setting of the target Account.
     
     tag : string
     This optional parameter specifies the tag for an application-specific password.
     If the new_password string is empty, the corresponding application-specific password is removed.
     
     method : string
     This optional parameter specifies the Account Access Mode.
     If this mode is "SIP", the the Alternative SIP Password Setting is modified, if this mode is RADIUS, then the Alternative RADIUS Password Setting is modified.
     In all other cases, the CommuniGate Password setting is modified.
     The new password will be stored using the effective Password Encryption setting of the target Account.
     
     To use this command, the user should have the "Basic Settings" Domain Administration right for the target Account Domain.
     Any user can modify her own Account password.
     In this case, or when the CHECK keyword is explicitly specified, the operation succeeds only if the the supplied password matches the size and complexity restrictions and the Account CanModifyPassword effective Setting is enabled.'''

  params = ''
  
  if method is not None and tag is not None:
    raise AttributeError('You can not use "method" and "tag" parameters at the same time')
      
  if method is not None:
    params += ' ' + method
    
  if tag is not None:
    params += ' ' + tag  

  if check:
    params += ' CHECK'

  return _operate(sock, 'SETACCOUNTPASSWORD ' + account_name + ' PASSWORD ' + new_password + params + '\n')

def verify_account_password(sock, account_name, password):
  '''Use this command to verify the Account password.
     
     account_name : string
     This parameter specifies the name of an existing Account. The name can include the Domain name (see above).
     
     password : string
     This string is used to specify the password to check (in the clear text format).
     
     To use this command, the user should have any Domain Administration right for the target Account Domain.'''

  return _operate(sock, 'VERIFYACCOUNTPASSWORD ' + account_name + ' PASSWORD ' + password + '\n')

def verify_account_identity(sock, account_name, identity):
  '''Use this command to check if the value of 'From:' header is allowed to be used by the Account.
     
     account_name : string
     This parameter specifies the name of an existing Account. The name can include the Domain name (see above).
    
     identity : string
     This string is to be the value of 'From:' header, e.g. "Real Name <user@domain.dom>".
     
     To use this command, the user should have any Domain Administration right for the target Account Domain.'''

  return _operate(sock, 'VERIFYACCOUNTIDENTITY ' + account_name + ' FOR ' + identity + '\n')

def get_account_aliases(sock, account_name):
  '''Use this command to get the list of Account aliases.
     The command produces an output - an list with the Account alias names.

     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETACCOUNTALIASES ' + account_name + '\n')

def set_account_aliases(sock, account_name, new_aliases):
  '''Use this command to set the Account aliases.
     
     account_name : string
     This parameter specifies the name of an existing Account. The name can include the Domain name (see above).
     
     new_aliases : list
     This list should contain the Account alias name strings. All old Account aliases are removed.
     
     This command can be used by Domain Administrators only if they have the CanCreateAliases access right.'''

  return _operate(sock, 'SETACCOUNTALIASES ' + account_name + ' ' + parse_to_CGP_object(new_aliases) + '\n')

def get_account_telnums(sock, account_name):
  '''Use this command to get the list of telephone numbers assigned to the Account.
     The command produces an output - an list with the assigned numbers.

     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETACCOUNTTELNUMS ' + account_name + '\n')

def set_account_telnums(sock, account_name, new_telnums):
  '''Use this command to assign telephone numbers to the Account.
  
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
    
     new_telnums : list
     This list should contain the telephone number strings.
     All old numbers assigned to the Account are removed.
     
     This command can be used by Domain Administrators only if they have the CanCreateTelnums access right.'''

  return _operate(sock, 'SETACCOUNTTELNUMS ' + account_name + ' ' + parse_to_CGP_object(new_telnums) + '\n')

def modify_account_telnums(sock, account_name, parameters):
  '''Use this command to change telephone numbers assigned to the Account.
  
    account_name : string
    This parameter specifies the name of an existing Account.
    The name can include the Domain name (see above).
    
    parameters : dictionary
    This dictionary should contain the op string element specifying the requested operation:

       add
         the parameters dictionary must contain the telnum string element with a telnum number to be added (atomically) to the set of Telnums assigned to the specified Account.
         If this set already contains this Telnum, an error code is returned.
      
       del
         the parameters dictionary must contain the telnum string element with a telnum number to be removed (atomically) from the set of Telnums assigned to the specified Account.
         If this set does not contain this Telnum, an error code is returned.
      
       pop
         The parameters dictionary must not contain any other elements.
         The first Telnum assigned to the specified Account is atomically removed from the Account Telnum set, and copied into the command result dictionary.
         If the Account Telnum set was empty, no error code is returned, and no element is copied into the command result dictionary.
    
    The command produces an output - a dictionary.
    For the pop operation, this dictionary can contain the telnum string element - the Telnum removed from the Account Telnum set.
    This command can be used by Domain Administrators only if they have the CanCreateTelnums access right.'''

  return _operate(sock, 'MODIFYACCOUNTTELNUMS ' + account_name + ' ' + parse_to_CGP_object(parameters) + '\n')

def get_account_mail_rules(sock, account_name):
  '''Use this command to get the list of Account Queue Rules.
     The command produces an output - an list of the Queue Rules specified for the Account.

     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETACCOUNTMAILRULES ' + account_name + '\n')

def set_account_mail_rules(sock, account_name, new_rules):
  '''Use this command to set the Account Queue Rules.

     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
     
     new_rules : list
     This list should contain the Account Queue Rules.
     All old Account Queue Rules are removed.
     
     This command can be used by Domain Administrators only if they have the RulesAllowed access right.
     This command can be used by any Account user to modify own Rules (subject to "allowed actions" restrictions).'''

  return _operate(sock, 'SETACCOUNTMAILRULES ' + account_name + ' ' + parse_to_CGP_object(new_rules) + '\n')

def get_account_signal_rules(sock, account_name):
  '''Use this command to get the list of Account Signal Rules.
     The command produces an output - an list of the Signal Rules specified for the Account.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETACCOUNTSIGNALRULES ' + account_name + '\n')

def set_account_signal_rules(sock, account_name, new_rules):
  '''Use this command to set the Account Signal Rules.
    
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
     
     new_rules : list
     This list should contain the Account Signal Rules.
     All old Account Signal Rules are removed.
    
     This command can be used by Domain Administrators only if they have the SignalRulesAllowed access right.'''

  return _operate(sock, 'SETACCOUNTSIGNALRULES ' + account_name + ' ' + parse_to_CGP_object(new_rules) + '\n')
def update_account_mail_rule(sock, account_name, rule):
  '''Use these commands to update an Account Queue.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
    
     rule : list
     This parameter should be an list, its first element specifies the Rule priority, its second element specifies the Rule name.
     The optional third, forth, and fifth elements specify the Rule conditions, Rule actions, and Rule comment.
     If the parameter list contains less than 4 elements, the list first element is used to update the priority of the already existing Rule with the name specified as the second list element.
     If such a Rule does not exist, the command returns an error.
     If the parameter list contains 4 or more elements, the entire parameter list is stored as a new Rule.
     If there is an existing Rule with the same name, it is removed.
     
     rule : string
     This string parameter specifies a name of the Rule to be removed.
     If such a Rule does not exist, the command does nothing and it does not return an error.
     
     The command can be used by Domain Administrators only if they have the RulesAllowed access right.
     This command can be used by any Account user to modify own Rules (subject to "allowed actions" restrictions).'''

  if isinstance(rule,list):
    rule = parse_to_CGP_object(rule)
  
  elif isinstance(rule,str):
    rule = 'DELETE ' + rule
  
  else:
    raise TypeError('Only string or list is allowed')
  
  return _operate(sock, 'UPDATEACCOUNTMAILRULE ' + account_name + ' ' + rule + '\n')

def update_account_signal_rule(sock, account_name, rule):
  '''Use these commands to update a Signal Rule.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
    
     rule : list
     This parameter should be a list, its first element specifies the Rule priority, its second element specifies the Rule name.
     The optional third, forth, and fifth elements specify the Rule conditions, Rule actions, and Rule comment.
     If the parameter list contains less than 4 elements, the list first element is used to update the priority of the already existing Rule with the name specified as the second list element.
     If such a Rule does not exist, the command returns an error.
     If the parameter list contains 4 or more elements, the entire parameter list is stored as a new Rule.
     If there is an existing Rule with the same name, it is removed.
     
     rule : string
     This string parameter specifies a name of the Rule to be REMOVED.
     If such a Rule does not exist, the command does nothing and it does not return an error.
     
     The command can be used by Domain Administrators only if they have the SignalRulesAllowed access right.
     This command can be used by any Account user to modify own Rules (subject to "allowed actions" restrictions).'''

  if isinstance(rule,list):
    rule = parse_to_CGP_object(rule)
  
  elif isinstance(rule,str):
    rule = 'DELETE ' + rule
  
  else:
    raise TypeError('Only string or list is allowed')
  
  return _operate(sock, 'UPDATEACCOUNTSIGNALRULE ' + account_name + ' ' + rule + '\n')
      
def get_account_RPOPs(sock, account_name):
  '''Use this command to get the list of Account RPOP records.
     The command produces an output - a dictionary with RPOP records specified for the Account.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETACCOUNTRPOPS ' + account_name + '\n')

def set_account_RPOPs(sock, account_name, new_records):
  '''Use this command to set the Account RPOP records.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
     
     new_records : dictionary
     This dictionary should contain the Account RPOP records.
     All old Account RPOP records are removed.
     
     This command can be used by Domain Administrators only if they have the CanModifyRPOP access right.'''

  return _operate(sock, 'SETACCOUNTRPOPS ' + account_name + ' ' + parse_to_CGP_object(new_records) + '\n')

def get_account_RSIPs(sock, account_name):
  '''Use this command to get the list of Account RSIP records.
     The command produces an output - a dictionary with RSIP records specified for the Account.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETACCOUNTRSIPS ' + account_name + '\n')

def set_account_RSIPs(sock, account_name, new_records):
  '''Use this command to set the Account RSIP records.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
     
     new_records : dictionary
     This dictionary should contain the Account RSIP records.
     All old Account RSIP records are removed.
     
     This command can be used by Domain Administrators only if they have the CanModifyRSIP access right.'''

  return _operate(sock, 'SETACCOUNTRSIPS ' + account_name + ' ' + parse_to_CGP_object(new_records) + '\n')
 
def update_scheduled_task(sock, account_name, task_data):
  '''Use this command to set the Account Scheduled Task records.

     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
     
     task_data : dictionary
     This dictionary should contain the Scheduled Task data:
     
       id
         the Scheduled Task name string.
         If there is no existing task with this name, a new Scheduled Task record is created.
       
       program
         the Scheduled Task program name string.
         It should be a name of the Real-Time Application available for the Account Domain environment.
         If this element is not specfied, an existing Scheduled Task record (if any) is deleted.
    
       parameter
         an optional simple Object.
         When the Scheduled Task program is launched, this Object is passed to it as its startParameter element.
     
       when
         a timestamp (GMT time) specifying when the Scheduled Task should be launched, or now string.
     
       period
         an optional parameter - a day, week, month, or year string, or a number.
         When specified, the Scheduled Task is automatically re-scheduled after the specified period of time (if this parameter is a number, then it specified the number of seconds).
         If this parameter is not specified, the Scheduled Task record is removed as soon as the Task is launched.
     
     When a Scheduled Task is launched, its main entry point is launched.
     The Task startParameter array contains the following elements:
     
     - startParameter[0] is the Scheduled Task name string
     - startParameter[1] is the timestamp specifying the moment the Task was started
     - startParameter[2] (optional) is the Scheduled Task parameter data
     
     This command can be used by Domain Administrators with the CanModifyRSIP access right for the target Account.'''

  return _operate(sock, 'UPDATESCHEDULEDTASK ' + account_name + ' ' + parse_to_CGP_object(task_data) + '\n')

def get_account_rights(sock, account_name):
  '''Use this command to get the array of the Server or Domain access rights granted to the specified user.
     The command produces output data - an array listing all Account Server Access rights.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name.'''
  
  return _operate(sock, 'GETACCOUNTRIGHTS ' + account_name + '\n')

def get_account_info(sock, account_name, key_name=None, key_list=None):
  '''Use this command to get an element of the Account "info" dictionary.
     The command produces an output - see below.

     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
     You can also specify the single asterisk (*) symbol instead of an Account name.
     This will indicate the current authenticated Account.
     
     key_list : list
     This optional parameter specifies the names of the info keys to retrieve.
     Note that when Account "info" data are stored in .info dictionary files, the "info" elements have dictionary names starting with the hash (#) symbol.
     You should NOT include the hash symbol into the keys parameter of the command.
    
     Note: the "info" element names are case-sensitive.
     The output is a dictionary with all those "info" elements that exist and are specified in the keys list.
     
     key_name : string
     This optional parameter specifies the name of the requested "info" element.
     Note that when Account "info" data are stored in .info dictionary files, the "info" elements have dictionary names starting with the hash symbol.
     You should NOT include the hash symbol into the keys parameter of the command.
    

     Note: the "info" element names are case-sensitive.
     The output is the specified "info" element.
     If the element is not found, the output is an empty string - two quotation marks ("").'''
  
  if key_name is not None and key_list is not None:
    raise AttributeError('You can not use "key_name" and "key_list" parameters at the same time')
  
  if key_list is not None:
    keys = parse_to_CGP_object(key_list)
  
  if key_name is not None:
    keys = 'Key ' + key_name
  
  return _operate(sock, 'GETACCOUNTINFO ' + account_name + ' ' + keys + '\n')

def get_account_prefs(sock, account_name):
  '''Use this command to get the Account Preferences.
     The command produces an output - a dictionary with the Account Preferences.

     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETACCOUNTPREFS ' + account_name + '\n')

def update_account_prefs(sock, account_name, new_settings):
  '''Use this command to modify the Account Preferences.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).

     new_settings : dictionary
     This dictionary is used to update the Account Preferences dictionary.
     It does not have to contain all Preferences data, the omitted elements will be left unmodified.
     If a new Preferences value is specified as the string default, the Preferences value is removed, so the default Preferences value will be used.
     
     This command can be used by Domain Administrators only if they have the WebUserSettings access right.'''

  return _operate(sock, 'UPDATEACCOUNTPREFS ' + account_name + ' ' + parse_to_CGP_object(new_settings) + '\n')

def set_account_prefs(sock, account_name, new_settings):
  '''Use this command to set the Account Preferences.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).

     new_settings : dictionary
     This dictionary should contain the new Account Preferences.
     All old Account Preferences are removed.

     This command can be used by Domain Administrators only if they have the WebUserSettings access right.'''

  return _operate(sock, 'SETACCOUNTPREFS ' + account_name + ' ' + parse_to_CGP_object(new_settings) + '\n')

def get_account_effective_prefs(sock, account_name):
  '''Use this command to get the effective Account Preferences.
     The command produces an output - a dictionary with Account Preferences.
     Both the explicitly set and the default settings are included into that dictionary.
    
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETACCOUNTEFFECTIVEPREFS ' + account_name + '\n')

def kill_account_sessions(sock, account_name):
  '''Use this command to interrupt all Account sessions (POP, IMAP, FTP, WebUser, etc.).
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).
     
     Note: All Domain Administrators can use this command.'''

  return _operate(sock, 'KILLACCOUNTSESSIONS ' + account_name + '\n')

def get_account_ACL(sock, account_name):
  '''The following command manage the Account Access Rights.
     These command can be used by the Account owner and by Domain Administrators who have the CanImpersonate access right.
     Use this command to get the Account Rights ACLs (Access Control Lists).
     The command produces an output - a dictionary with the ACL elements.
     
     account_name : string
     This parameter specifies the name of an existing Account (target Account).
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.
     If this name is specified, the ACL info is returned only if the specified Account has the Admin access right for the target Account.'''
  
  params = ''
  
  if auth_account_name is not None:
    params += ' ' + auth_account_name

  return _operate(sock, 'GETACCOUNTACL ' + account_name + params + '\n')

def set_account_ACL(sock, account_name, new_ACL):
  '''The following command manage the Account Access Rights.
     These command can be used by the Account owner and by Domain Administrators who have the CanImpersonate access right.
     Use this command to modify the access control list for the Account Access Rights.
     
     account_name : string
     This parameter specifies the name of an existing Account (target Account).
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.
     If this name is specified, the ACL info is updated only if the specified Account has the Admin access right for target Account.
    
     new_ACL : dictionary
     This parameter specifies the access right elements to be modified.
     Each dictionary key specifies an identifier, and the key value should be a string with access right symbols.
     If the key value string starts with the minus ("-") symbol, access rights specified in the string are removed from the access right element.
     If the key value string starts with the plus ("+") symbol, access rights specified in the string are added to the access right element.
     In other cases, access rights specified in the string replace the set of rights in the access right element.
     If the access right element for the specified key did not exist, it is created.
     If the new access right element has empty set of access rights, the element is removed.'''

  params = parse_to_CGP_object(new_ACL)
  
  if auth_account_name is not None:
    params = 'AUTH ' + auth_account_name + ' ' + params

  return _operate(sock, 'SETACCOUNTACL ' + account_name + ' ' + params + '\n')

def account_ACL_rights(sock, account_name, auth_account_name):
  '''The following command manage the Account Access Rights.
     These command can be used by the Account owner and by Domain Administrators who have the CanImpersonate access right.
     This command produces an output - a string with the effective access rights for the given auth_account_name.
     
     account_name : string
     This parameter specifies the name of an existing Account (target Account). The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     auth_account_name : string
     This parameter specifies the name of an Account whose effective access rights for the target Account should be retrieved.'''
  
  return _operate(sock, 'GETACCOUNTACLRIGHTS ' + account_name + ' AUTH ' + auth_account_name + '\n')

def set_account_settings(sock, account_name, new_settings):
  '''The following command are available for the System Administrators only:
     Use this command to change the Account settings.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     
     new_settings : dictionary
     This dictionary is used to replace the Account settings dictionary.
     All old Account settings are removed.'''

  return _operate(sock, 'SETACCOUNTSETTINGS ' + account_name + ' ' + parse_to_CGP_object(new_settings) + '\n')

def get_account_location(sock, account_name):
  '''The following command are available for the System Administrators only:
     Use this command to get the Account file directory path (for multi-mailbox Accounts) or the Account INBOX Mailbox path (for single-mailbox Accounts).
     The command produces an output - a string with the Account file path.
     The path is relative to the file directory of the Account Domain.
    
     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETACCOUNTLOCATION ' + account_name + '\n')

def get_account_presence(sock, account_name):
  '''The following command are available for the System Administrators only:
     Use this command to get the Account "presence" status.
     The command produces an output:
     
     - array of two strings - the Account "presence" status and its custom status message, or
     - string - the Account "presence" status (if no custom status message is set), or
     - null-object - if the Account "presence" status is not set at all.
     
     account_name : string
     This parameter specifies the name of an existing Account. The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETACCOUNTPRESENCE ' + account_name + '\n')

#Group Administration
def list_groups(sock, domain_name=None):
  '''Use this command to get the list of all Groups in the Domain.
     The command produces output data - an array with the names of all Groups in the specified (or default) Domain.
    
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name

  return _operate(sock, 'LISTGROUPS' + params + '\n')

def create_group(sock, group_name, settings=None):
  '''Use this command to create new Groups.
   
     group_name : string
     This parameter specifies the name for the new Group.
     The name can contain the @ symbol followed by the Domain name, in this case the Group is created in the specified Domain.
     If the Domain name is not specified, the command applies to the administrator Domain.
    
     settings : dictionary
     This optional parameter specifies the initial Group settings and the members list.
     This command can be used by Domain Administrators only if they have the CanCreateGroups access right.'''

  params = ''
  
  if settings is not None:
    params = parse_to_CGP_object(settings)

  return _operate(sock, 'CREATEGROUP ' + group_name + params + '\n')

def rename_group(sock, old_group_name, new_group_name):
  '''Use this command to rename Groups.
    
     old_group_name : string
     This parameter specifies the name of an existing Group. The name can include the Domain name (see above).
     
     new_group_name : string
     This parameter specifies the new Group name. The name can include the Domain name (see above).
     
     This command can be used by Domain Administrators only if they have the CanCreateGroups access right.'''

  return _operate(sock, 'RENAMEGROUP ' + old_group_name + ' into ' + new_group_name + '\n')

def delete_group(sock, group_name):
  '''Use this command to remove Groups.
     
     group_name : string
     This parameter specifies the name of an existing Group.
     The name can include the Domain name (see above).'''

  return _operate(sock, 'DELETEGROUP ' + group_name + '\n')

def get_group(sock, group_name):
  '''Use this command to get the Group settings.
     The command produces an output - a dictionary with the Group settings and members.
     
     group_name : string
     This parameter specifies the name of an existing Group.
     The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETGROUP ' + group_name + '\n')

def set_group(sock, group_name, new_settings):
  '''Use this command to set the Group settings.
     
     group_name : string
     This parameter specifies the name of an existing Group.
     The name can include the Domain name (see above).
     
     new_settings : dictionary
     This dictionary is used to replace the Group settings dictionary.
     
     This command can be used by Domain Administrators only if they have the CanCreateGroups access right.'''

  return _operate(sock, 'SETGROUP ' + group_name + ' ' + parse_to_CGP_object(new_settings) + '\n')

#Forwarder Administration
def list_forwarders(sock, domain_name=None):
  '''Use this command to get the list of all Forwarders in the Domain.
     The command produces output data - an array with the names of all Forwarders in the specified (or default) Domain.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name

  return _operate(sock, 'LISTFORWARDERS' + params + '\n')

def create_forwarder(sock, forwarder_name, address):
  '''Use this command to create new Forwarders.
     
     forwarder_name : string
     This parameter specifies the name for the new Forwarder.
     The name can contain the @ symbol followed by the Domain name, in this case the Forwarder is created in the specified Domain.
     If the Domain name is not specified, the command applies to the administrator Domain.

     address : string
     This parameter specifies the E-mail address the Forwarder should reroute E-mail messages and Signals to.

     This command can be used by Domain Administrators only if they have the CanCreateForwarders access right.'''

  return _operate(sock, 'CREATEFORWARDER ' + forwarder_name + ' TO ' + address + '\n')

def rename_forwarder(sock, old_forwarder_name, new_forwarder_name):
  '''Use this command to rename Forwarders.
     
     old_forwarder_name : string
     This parameter specifies the name of an existing Forwarder.
     The name can include the Domain name (see above).

     new_forwarder_name : string
     This parameter specifies the new Forwarder name.
     The name can include the Domain name (see above).

     This command can be used by Domain Administrators only if they have the CanCreateForwarders access right.'''

  return _operate(sock, 'RENAMEFORWARDER ' + old_forwarder_name + ' INTO ' + new_forwarder_name + '\n')

def delete_forwarder(sock, forwarder_name):
  '''Use this command to remove Forwarders.
     
     forwarder_name : string
     This parameter specifies the name of an existing Forwarder.
     The name can include the Domain name (see above).
     This command can be used by Domain Administrators only if they have the CanCreateForwarders access right.'''

  return _operate(sock, 'DELETEFORWARDER ' + forwarder_name + '\n')

def get_forwarder(sock, forwarder_name):
  '''Use this command to get the Forwarder address.
     The command produces an output - a string with the E-mail address this Forwarder reroutes all E-mail messages and Signals to.

     forwarder_name : string
     This parameter specifies the name of an existing Forwarder.
     The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETFORWARDER' + forwarder_name + '\n')

def find_forwarders(sock, domain_name, forwarder_address):
  '''Use this command to find all Forwarders pointing to the specified address.
     The command produces an output - an array with the found Forwarder names.
  
     domain_name : string
     This parameter specifies the Domain name.

     forwarder_address : string
     This parameter specifies an E-mail address to look for.'''
  
  return _operate(sock, 'FINDFORWARDERS' + domain_name + ' ' + forwarder_address + '\n')
      
#Named Task Administration
def list_domain_named_tasks(sock, domain_name=None):
  '''Use this command to get the list of all Named Tasks in the Domain.
     The command produces output data - a dictionary where the keys are the Named Task names, and the values are dictionaries, containing the Task owner name, the task Real Name, and the name of the Real-Time Application program this Named Task runs.

     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name
      
  return _operate(sock, 'LISTDOMAINNAMEDTASKS' + params + '\n')

def list_account_named_tasks(sock, account_name):
  '''Use this command to get the list of all Named Tasks owned by the specified Account.
     The command produces output data - a dictionary containing the same data as the domain_namedTasks command result.
     
     account_name : string
     This parameter specifies the owner Account name.'''
  
  return _operate(sock, 'LISTACCOUNTNAMEDTASKS ' + account_name + '\n')

def create_named_task(sock, task_name, account_name):
  '''Use this command to create new Named Tasks.
   
     task_name : string
     This parameter specifies the name for the new Named Task.
     The name can contain the @ symbol followed by the Domain name, in this case the Named Task is created in the specified Domain.
     If the Domain name is not specified, the command applies to the administrator Domain.
    
     account_name : string
     This parameter specifies the owner Account name.
     It must not contain the @ symbol and a Domain name, as this owner Account must be in the same Domain as the Named Task itself.
    
     This command can be used by Domain Administrators only if they have the CanCreateNamedTasks access right.'''

  return _operate(sock, 'CREATENAMEDTASK ' + task_name + ' FOR ' + account_name + '\n')

def rename_named_task(sock, old_task_name, new_task_name):
  '''Use this command to rename Named Tasks.
  
     old_task_name : string
     This parameter specifies the name of an existing Named Task.
     The name can include the Domain name (see above).

     new_task_name : string
     This parameter specifies the new Named Task name.

     This command can be used by Domain Administrators only if they have the CanCreateNamedTasks access right.'''

  return _operate(sock, 'RENAMENAMEDTASK ' + old_task_name + ' into ' + new_task_name + '\n')

def delete_named_task(sock, task_name):
  '''Use this command to remove Named Tasks.
     
     task_name : string
     This parameter specifies the name of an existing Named Task.
     The name can include the Domain name (see above).
     
     This command can be used by Domain Administrators only if they have the CanCreateNamedTasks access right.'''

  return _operate(sock, 'DELETENAMEDTASK ' + task_name + '\n')

def get_named_task(sock, task_name):
  '''Use this command to get the Named Task settings.
     The command produces an output - a dictionary with the Named Task settings.
     
     task_name : string
     This parameter specifies the name of an existing Named Task.
     The name can include the Domain name (see above).'''
  
  return _operate(sock, 'GETNAMEDTASK ' + task_name + '\n')

def update_named_task(sock, task_name, new_settings):
  '''Use this command to set the Named Task settings.
     
     task_name : string
     This parameter specifies the name of an existing Named Task. The name can include the Domain name (see above).
    
     new_settings : dictionary
     This dictionary is used to update the Named Task settings dictionary.
     
     This command can be used by Domain Administrators only if they have the CanCreateNamedTasks access right.'''

  return _operate(sock, 'UPDATENAMEDTASK ' + task_name + ' ' + parse_to_CGP_object(new_settings) + '\n')
      
#Access Rights Administration
def set_account_rights(sock, account_name, new_rights):
  '''A user should have the Master Server access right to use this command.
     Use this command to set the Account Server Access rights.

     account_name : string
     This parameter specifies the name of an existing Account.
     The name can include the Domain name.

     new_rights : array
     This array should contain the Access Right codes.
     All old Account access rights are removed.
     To set access rights for an Account in a secondary Domain (i.e. Domain Administration Rights), the user may have only the All Domains Server access right.'''

  return _operate(sock, 'SETACCOUNTRIGHTS ' + account_name + ' ' + parse_to_CGP_object(new_rights) + '\n')
      
#Mailbox Administration
def list_mailboxes(sock, account_name, filter=None, auth_account_name=None):
  '''Use this command to get the list of Account Mailboxes.
     The command produces an output - a dictionary.
     each dictionary key specifies a Mailbox name;
     if the auth_account_name user is not specified or if the specified user has the Select access right for this Mailbox, the key value contains a dictionary with Mailbox information;
     if the specified auth_account_name does not have the Select access right, the key value contains an empty array;
     if there is a 'mailbox folder' with the dictionary key, but there is no 'regular' Mailbox with that name, the key value is an empty array;
     if there is a 'mailbox folder' with the dictionary key, and there is also a 'regular' Mailbox with that name, the key value is an array with one element - the information for the 'regular' Mailbox (either a dictionary or an empty array).
    
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     filter : string
     This optional parameter specifies the filter string to apply to Account Mailbox names.
     The filter can use the same wildcard symbols "*" and "%" as the IMAP LIST command.
     If the filter is not specified, the filter string "*" is assumed, and all Account Mailboxes are returned.
    
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the LIST operation should be executed.
     If this name is specified, the output includes only those Mailboxes for which the specified Account has the Lookup Mailbox access right.'''
  
  params = ''
  
  if filter is not None:
    params += ' FILTER '  + filter
    
  if auth_account_name is not None:
    params += ' AUTH '  + auth_account_name
      
  return _operate(sock, 'LISTMAILBOXES ' + account_name + params + '\n')
      
def create_mailbox(sock, account_name, mailbox_name, auth_account_name=None, mailbox_class=None):
  '''Use this command to create a Mailbox in the specified Account.
  
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     mailbox_name : string
     This parameter specifies the name for the new Mailbox.
    
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf this operation should be executed.
   
     mailbox_class : string
     This optional parameter specifies the Mailbox class for the new Mailbox'''

  params = ''
  
  if auth_account_name is not None:
    params += ' AUTH ' + auth_account_name  

  if mailbox_class is not None:
    params += ' CLASS ' + mailbox_class

  return _operate(sock, 'CREATEMAILBOX ' + account_name + ' MAILBOX ' + mailbox_name + params + '\n')

def delete_mailbox(sock, account_name, mailbox_name, mailboxes=False, auth_account_name=None):
  '''Use this command to remove a Mailbox from the specified Account.
     If the keyword MAILBOXES is used, all nested Mailboxes (submailboxes) are deleted, too.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     mailbox_name : string
     This parameter specifies the name of the Mailbox to be deleted.
     
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.
     If this name is specified, the Mailbox is deleted only if the specified Account has the Create access right for the 'outer' Mailbox (this means that an Account should have the Create access right for the Archive Mailbox in order to delete the Archive/March Mailbox), and the specified Account should have the DELETE right for the specified Mailbox.'''

  if mailboxes:
      params = 'ES ' + mailbox_name
  else:
    params += ' ' + mailbox_name
    
  if auth_account_name is not None:
    params += ' AUTH ' + auth_account_name 

  return _operate(sock, 'DELETEMAILBOX ' + account_name + ' MAILBOX' + params + '\n')

def rename_mailbox(sock, account_name, mailbox_name, new_mailbox_name, mailboxes=False, auth_account_name=None):
  '''Use this command to rename a Mailbox in the specified Account.
     If the keyword MAILBOXES is used, all nested Mailboxes (submailboxes) are renamed, too.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
    
     mailbox_name : string
     This parameter specifies the name of the Mailbox to be renamed.
    
     new_mailbox_name : string
     This parameter specifies the new name for the Mailbox.
    
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.
     If this name is specified, the Mailbox is renamed only if the specified Account has a right to perform the DELETEMAILBOX operation with the original Mailbox name and the CREATEMAILBOX operation with the new Mailbox name (see above).'''

  if mailboxes:
      mailbox_name = 'ES ' + mailbox_name
  else:
    mailbox_name = ' ' + mailbox_name
  
  params = ''
  
  if auth_account_name is not None:
    params += ' AUTH ' + auth_account_name 

  return _operate(sock, 'RENAMEMAILBOX ' + account_name + ' MAILBOX' + mailbox_name + ' INTO ' + new_mailbox_name + params + '\n')

def get_mailbox_info(sock, account_name, mailbox_name, auth_account_name=None):
  '''Use this command to get the internal information about the Account Mailbox.
     The command produces an output - a dictionary with the Mailbox internal information.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
    
     mailbox_name : string
     This parameter specifies the name of an existing Mailbox in the specified Account.
    
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.
     If this name is specified, the Mailbox info is returned only if the specified Account has the Select Mailbox access right.'''
  
  params = ''
    
  if auth_account_name is not None:
    params += ' AUTH '  + auth_account_name
      
  return _operate(sock, 'GETMAILBOXINFO ' + account_name + ' MAILBOX ' + mailbox_name + params + '\n')

def get_mailbox_ACL(sock, account_name, mailbox_name, filter=None, auth_account_name=None):
  '''Use this command to get the access control list for the Account Mailbox.
     The command produces an output - a dictionary with the Mailbox access elements.
  
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
    
     mailbox_name : string
     This parameter specifies the name of an existing Mailbox in the specified Account.
     
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.
     If this name is specified, the ACL info is returned only if the specified Account has the Admin access right for the specified Mailbox.'''
  
  params = ''
  
  if filter is not None:
    params += ' FILTER '  + filter
    
  if auth_account_name is not None:
    params += ' AUTH '  + auth_account_name
      
  return _operate(sock, 'GETMAILBOXACL ' + account_name + ' MAILBOX ' + mailbox_name + params + '\n')
      
def set_mailbox_ACL(sock, account_name, mailbox_name, new_ACL, auth_account_name=None):
  '''Use this command to modify the access control list for the Account Mailbox.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
    
     mailbox_name : string
     This parameter specifies the name of an existing Mailbox in the specified Account.
     
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.
     If this name is specified, the ACL info is updated only if the specified Account has the Admin access right for the specified Mailbox.
    
     new_ACL : dictionary
     This parameter specifies the access right elements to be modified.
     Each dictionary key specifies an identifier, and the key value should be a string with access right symbols.
     If the key value string starts with the minus ("-") symbol, access rights specified in the string are removed from the access right element.
     If the key value string starts with the plus ("+") symbol, access rights specified in the string are added to the access right element.
     In other cases, access rights specified in the string replace the set of rights in the access right element.
     If the access right element for the specified key did not exist, it is created.
     If the new access right element has empty set of access rights, the element is removed.'''

  params = ''
    
  if auth_account_name is not None:
    params += ' AUTH '  + auth_account_name

  return _operate(sock, 'SETMAILBOXACL ' + account_name + ' MAILBOX ' + mailbox_name + params + ' ' + parse_to_CGP_object(new_ACL) + '\n')

def get_mailbox_rights(sock, account_name, mailbox_name, auth_account_name):
  '''This command produces an output - a string with the effective Mailbox access rights for the given auth_account_name.
  
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
    
     mailbox_name : string
     This parameter specifies the name of an existing Mailbox in the specified Account.
   
     auth_account_name : string
     This parameter specifies the name of an Account whose effective access rights should be retrieved.'''
  
  return _operate(sock, 'GETMAILBOXRIGHTS ' + account_name + ' MAILBOX ' + mailbox_name + ' AUTH ' + auth_account_name + '\n')

def set_mailbox_class(sock, account_name, mailbox_name, new_class, auth_account_name=None):
  '''Use this command to set the "class" of an Account Mailbox.
     
     account_name : string
     This parameter specifies the name of an existing Account. The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     mailbox_name : string
     This parameter specifies the name of an existing Mailbox in the specified Account.
     
     auth_account_name : string
     This optional parameter specifies the name of an Account whose Mailbox access rights should be used.
    
     new_class : string
     The Mailbox class.'''

  params = ''
    
  if auth_account_name is not None:
    params += ' AUTH '  + auth_account_name

  return _operate(sock, 'SETMAILBOXCLASS ' + account_name + ' MAILBOX ' + mailbox_name + params + ' CLASS ' + new_class + '\n')

def get_mailbox_subscription(sock, account_name):
  '''This command produces an output - an array with the list of Account "subscribed Mailboxes".
   
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.'''
  
  return _operate(sock, 'GETMAILBOXSUBSCRIPTION ' + account_name + '\n')

def set_mailbox_subscription(sock, account_name, new_subscription):
  '''Use this command to set the Account "subscribed Mailboxes" list.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     new_subscription : array
     The list of subscribed Mailboxes. Each array element should be a string with a Mailbox name.'''

  return _operate(sock, 'SETMAILBOXSUBSCRIPTION ' + account_name + ' ' + parse_to_CGP_object(new_subscription) + '\n')

def get_mailbox_aliases(sock, account_name):
  '''This command produces an output - a dictionary.
     Each dictionary key is the name of an existing Mailbox alias, and the key value is a string with the name of Mailbox this alias points to.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.'''
  
  return _operate(sock, 'GETMAILBOXALIASES ' + account_name + '\n')

def set_mailbox_aliases(sock, account_name, new_aliases):
  '''Use this command to set the Account Mailbox aliases.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     new_aliases : dictionary
     The set of new Mailbox aliases.'''

  return _operate(sock, 'SETMAILBOXALIASES ' + account_name + ' ' + parse_to_CGP_object(new_aliases) + '\n')

#Alert Administration
def get_domain_alerts(sock, domain_name=None):
  '''Use this command to get the Domain Alerts.
     The command produces an output - a dictionary with the Domain alert strings and time stamps.
    
     domain_name : string
     This optional parameter specifies the name of an existing Domain.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name
      
  return _operate(sock, 'GETDOMAINALERTS' + params + '\n')

def set_domain_alerts(sock, new_alerts, domain_name=None):
  '''Use this command to change the Domain alerts.
     
     domain_name : string
     This optional parameter specifies the name of an existing Domain.
   
     new_alerts : dictionary
     This dictionary is used to replace the Domain alert dictionary.
     All old Domain alerts are removed.'''

  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name
      
  return _operate(sock, 'SETDOMAINALERTS' + params + ' ' + parse_to_CGP_object(new_alerts) + '\n')

def post_domain_alert(sock, domain_name , new_alert):
  '''Use this command to post a Domain-wide alert message.
     
     domain_name : string
     This parameter specifies the name of an existing Domain.

     new_alert : string
     This string specifies the Alert text.'''

  return _operate(sock, 'POSTDOMAINALERT ' + domain_name + ' ALERT ' + new_alert + '\n')
      
def remove_domain_alert(sock, domain_name , time_stamp):
  '''Use this command to remove a Domain-wide alert message.

     domain_name : string
     This parameter specifies the name of an existing Domain.

     time_stamp : string
     This string specifies the time stamp of the Alert message to be removed.'''

  return _operate(sock, 'REMOVEDOMAINALERT ' + domain_name + ' ALERT ' + time_stamp + '\n')

def get_account_alerts(sock, account_name):
  '''Use this command to get the Domain Alerts.
     The command produces an output - a dictionary with the Domain alert strings and time stamps.
     
     accountName : string
     This parameter specifies the name of an existing Account. The asterisk (*) symbol can be used to specify the current authenticated Account.'''
  
  return _operate(sock, 'GETACCOUNTALERTS ' + account_name + '\n')
      
def set_account_alerts(sock, account_name, new_alerts):
  '''Use this command to change the Account alerts.

     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.

     new_alerts : dictionary
     This dictionary is used to replace the Account alert dictionary.
     All old Account alerts are removed.'''

  return _operate(sock, 'SETACCOUNTALERTS ' + account_name + ' ' + new_alerts + '\n')

def post_account_alert(sock, account_name, new_alert):
  '''Use this command to post an Account alert message.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     new_alert : string
     This string specifies the Alert text.'''

  return _operate(sock, 'POSTACCOUNTALERT ' + account_name + ' ALERT ' + new_alert + '\n')

def remove_account_alert(sock, account_name , time_stamp):
  '''Use this command to remove an Account alert message.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     time_stamp : string
     This string specifies the time stamp of the Alert message to be removed.'''

  return _operate(sock, 'REMOVEACCOUNTALERT ' + account_name + ' ALERT ' + time_stamp + '\n')

def get_server_alerts(sock):
  '''The following command is available for the System Administrators only.
     Use this command to get the list of the server-wide Alerts.
     The command produces an output - a dictionary with the server alert strings and time stamps.'''
  
  return _operate(sock, 'GETSERVERALERTS\n')
      
def set_server_alerts(sock, new_alerts):
  '''The following command is available for the System Administrators only.
     Use this command to change the server-wide Alerts.
    
    new_alerts : dictionary
    This dictionary is used to replace the server-wide Alert dictionary.
    All old server-wide alerts are removed.'''

  return _operate(sock, 'SETSERVERALERTS ' + parse_to_CGP_object(new_alerts) + '\n')

def post_server_alert(sock, new_alert):
  '''The following command is available for the System Administrators only.
     Use this command to post a server-wide Alert message.

     new_alert : string
     This string specifies the Alert text.'''

  return _operate(sock, 'POSTSERVERALERT ' + new_alert + '\n')
      
def remove_server_alert(sock, time_stamp):
  '''The following command is available for the System Administrators only.
     Use this command to remove a server-wide Alert message.
   
     time_stamp : string
     This string specifies the time stamp of the Alert message to be removed.'''

  return _operate(sock, 'REMOVESERVERALERT ' + time_stamp + '\n')

def get_cluster_alerts(sock, account_name):
  '''The following command is available for the System Administrators only.
     These command is available in the Dynamic Cluster only.
     Use this command to get the list of the cluster-wide Alerts.
     The command produces an output - a dictionary with the cluster alert strings and time stamps.'''
  
  return _operate(sock, 'GETCLUSTERALERTS ' + account_name + '\n')

def set_cluster_alerts(sock, account_name, new_alerts):
  '''The following command is available for the System Administrators only.
     These command is available in the Dynamic Cluster only.
     Use this command to change the cluster-wide Alerts.

     new_alerts : dictionary
     This dictionary is used to replace the cluster-wide Alert dictionary.
     All old cluster-wide alerts are removed.'''

  return _operate(sock, 'SETCLUSTERALERTS ' + account_name + ' ' + new_alerts + '\n')

def post_cluster_alert(sock, account_name, new_alert):
  '''The following command is available for the System Administrators only.
     These command is available in the Dynamic Cluster only.
     Use this command to post a cluster-wide Alert message.
     
     new_alert : string
     This string specifies the Alert text.'''

  return _operate(sock, 'POSTCLUSTERALERT ' + account_name + ' ALERT ' + new_alert + '\n')
      
def remove_cluster_alert(sock, account_name , time_stamp):
  '''The following command is available for the System Administrators only.
     These command is available in the Dynamic Cluster only.
     Use this command to remove a cluster-wide Alert message.
     
     time_stamp : string
     This string specifies the time stamp of the Alert message to be removed.'''

  return _operate(sock, 'REMOVECLUSTERALERT ' + account_name + ' ALERT ' + time_stamp + '\n')

#File Storage Administration
def read_storage_file(sock, account_name, file_name,
                      position=None, slice_size=None, auth_account_name=None):
  '''Use this command to retrieve a file from the Account File Storage.
     This command produces an output - a array of 3 elements.
     The first element is a datablock with the content of the specified file, the second element is a timestamp with the file modification date, and the third element is a number equal to the current file size.
  
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
    
     file_name : string
     This parameter specifies the name of the File Storage file to be retrieved.
   
     position : int
     If this parameter is specified the File Storage file is read starting from the specified file position.
    
     slice_size : int
     If this parameter is specified, no more than the specified number of file data bytes is returned.
    
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.'''
  
  params = ''
  
  if position is not None:
    params += ' OFFSET ' + str(position)
    
  if slice_size is not None:
    params += ' SIZE ' + str(slice_size)
    
  if auth_account_name is not None:
    params += ' AUTH ' + slice_size

  return _operate(sock, 'READSTORAGEFILE ' + account_name + ' FILE ' + file_name + params + '\n')
      
def write_storage_file(sock, account_name, file_name, file_data,
                       position=None, auth_account_name=None):
  '''Use this command to store a file in the Account File Storage.
     If a File Storage file with the specified name already exists, the old file is removed.
     If the file_name specifies a directory (it ends with the slash (/) symbol) the command creates a directory.
     In this case, the OFFSET position part must be absent, and the file_data parameter must be an empty datablock.
    
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
    
     file_name : string
     This parameter specifies the name for the File Storage file.
   
     position : offset
     If this parameter is absent, or it exists and it is the zero number, the existing file (if any) is removed first, and a new file is created.
     If this parameter is a non-zero number, its value must be positive; the File Storage file is rewritten/extended starting from the specified file position.
     The file should already exist, and the specified position should not be larger than the current file size.
     If this option is BEG, then the file should already exist, the file is rewritten from the beginning, but its old data beyond the end of the file_data (if any) is not removed.
     If this option is END, then the file_data is appended to the end of the file.
     If the file does not exist, it is created.
     If this option is NEW, then the file must not exist, a new file is created and file_data is stored in it.
    
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.
    
     file_data : bytes
     This parameter contains the file data.'''

  params = ''
  
  if position is not None:
    params += ' OFFSET ' + str(position)
    
  if auth_account_name is not None:
    params += ' AUTH ' + slice_size    
      
  return _operate(sock, 'WRITESTORAGEFILE ' + account_name + ' FILE ' + file_name + params + ' DATA ' + file_data + '\n')

def rename_storage_file(sock, account_name, old_file_name, new_file_name, auth_account_name=None):
  '''Use this command to rename a file or a file directory in the Account File Storage.
  
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     old_file_name : string
     This parameter specifies the name of an existing File Storage file or file directory.
    
     new_file_name : string
     This parameter specifies the new name for the File Storage file or file directory.
    
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.'''

  params = ''
    
  if auth_account_name is not None:
    params += ' AUTH ' + slice_size    
      
  return _operate(sock, 'RENAMESTORAGEFILE ' + account_name + ' FILE ' + old_file_name + ' INTO ' + new_file_name + params + '\n')
      
def delete_storage_file(sock, account_name, file_name, auth_account_name=None):
  '''Use this command to remove a file or a file directory from the Account File Storage.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.

     file_name : string
     This parameter specifies the name of an existing File Storage file or file directory.

     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.'''

  params = ''
    
  if auth_account_name is not None:
    params += ' AUTH ' + slice_size       
      
  return _operate(sock, 'DELETESTORAGEFILE ' + account_name + ' FILE ' + file_name + params + '\n')

def list_storage_files(sock, account_name, file_path=None, auth_account_name=None):
  '''Use this command to list all files in the File Storage top directory or in one of its subdirectories.
     This command produces an output - a dictionary, where each key is a name of the File Storage file, and the key value is a dictionary for a regular file and an empty array for subdirectories.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
  
     file_path : string
     This optional parameter specifies the name of the File Storage subdirectory.
     You can omit this parameter along with the PATH keyword, in this case the command returns the list of files in the top File Storage directory.
    
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.'''
  
  params = ''
  
  if file_path is not None:
    params += ' PATH ' + file_path
    
  if auth_account_name is not None:
    params += ' AUTH ' + slice_size

  return _operate(sock, 'LISTSTORAGEFILES ' + account_name + params + '\n') 
      
def get_storage_file_info(sock, account_name, file_path=None, auth_account_name=None):
  '''Use this command to get the statistical information about all files in the Account File Storage.
     This command produces an output - an array with 2 number elements.
     The first element contains the total size of all File Storage files, the second element contains the number of files in the File Storage.
  
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     file_path : string
     This optional parameter specifies the name of the File Storage subdirectory.
     You can omit this parameter along with the PATH keyword, in this case the command returns the list of files in the top File Storage directory.
     
     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.'''
  
  params = ''
  
  if file_path is not None:
    params += ' PATH ' + file_path
    
  if auth_account_name is not None:
    params += ' AUTH ' + slice_size

  return _operate(sock, 'GETSTORAGEFILEINFO ' + account_name + params + '\n')

def read_storage_file_attr(sock, account_name, file_name, attributes=None, auth_account_name=None):
  '''Use this command to read attributes of an Account File Storage file or file directory.
     This command produces an output - an array of XML elements containing file or file directory attributes.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.

     file_name : string
     This parameter specifies the name of an existing File Storage file or file directory.

     attributes : array
     This optional parameter specifies an array of strings.
     If specified, only file attributes with names included into this array are retrieved.

     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.'''
  
  params = ''
  
  if attributes is not None:
    params += ' PATH ' + parse_to_CGP_object(attributes)
    
  if auth_account_name is not None:
    params += ' AUTH ' + slice_size

  return _operate(sock, 'READSTORAGEFILEATTR ' + account_name + ' FILE ' + file_name + params + '\n')
      
def update_storage_file_attr(sock, account_name, file_name, attributes, auth_account_name=None):
  '''Use this command to update attributes of an Account File Storage file or file directory.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.

     file_name : string
     This parameter specifies the name of an existing File Storage file or file directory.

     attributes : array
     This parameter specifies an array of XML elements - the new file attribute values.

     auth_account_name : string
     This optional parameter specifies the name of an Account on whose behalf the operation should be executed.'''

  params = ''
    
  if auth_account_name is not None:
    params += ' AUTH ' + slice_size       
      
  return _operate(sock, 'UPDATESTORAGEFILEATTR ' + account_name + ' FILE ' + file_name + ' ' + parse_to_CGP_object(attributes) + params + '\n')

def get_file_subscription(sock, account_name):
  '''This command produces an output - an array with the list of Account "subscribed files".

     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.'''
  
  return _operate(sock, 'GETFILESUBSCRIPTION ' + account_name + '\n')
      
def set_file_subscription(sock, account_name, new_subscription):
  '''Use this command to set the Account "subscribed files" list.

     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.

     new_subscription : array
     The list of subscribed files. Each array element should be a string with a file name.'''

  return _operate(sock, 'SETFILESUBSCRIPTION ' + account_name + ' ' + parse_to_CGP_object(new_subscription) + '\n')

#Mailing Lists Administration
def list_lists(sock, domain_name=None):
  '''Use this command to get the list of all mailing lists in the Domain.
     The command produces output data - an array of strings.
     Each string is the name of a mailing list in the specified (or default) Domain.
     
     domain_name : string
     This optional parameter specifies the Domain name.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' OFFSET ' + domain_name
      
  return _operate(sock, 'LISTLISTS' + params + '\n')
      
def get_domain_lists(sock, domain_name=None):
  '''Use this command to get the list of all mailing lists in the Domain.
     The command produces output data - a dictionary.
     Each dictionary key is the name of a mailing list in the specified (or default) Domain.
     The key value is a numeric string with the actual number of the list subscribers ("-1" if the current number of subscribers is not known).
    
     domain_name : string
     This optional parameter specifies the Domain name.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' OFFSET ' + domain_name
      
  return _operate(sock, 'GETDOMAINLISTS' + params + '\n')

def get_account_lists(sock, account_name):
  '''Use this command to get the list of all mailing lists belonging to the specified Account.
     The command produces output data - a dictionary.
     Each dictionary key is the name of a mailing list belonging to the specified (or default) Account.
     The key value is a numeric string with the actual number of the list subscribers ("-1" if the current number of subscribers is not known).

     account_name : string
     This parameter specifies the list's owner Account name.'''
  
  return _operate(sock, 'GETACCOUNTLISTS ' + account_name + '\n')
      
def create_list(sock, list_name, account_name):
  '''Use this command to create a mailing list.
     
     list_name : string
     This parameter specifies the name of a mailing list to create.
     It can include the Domain name.
     If the Domain name is not specified, the user Domain is used by default.
     
     account_name : string
     This parameter specifies the name of the mailing list owner (without the Domain name).
     It should be the name of an already existing Account in the mailing list Domain.
     Domain Administrators can use this command if they have the CanCreateLists Domain access right.'''

  return _operate(sock, 'CREATELIST ' + list_name + ' for ' + account_name + '\n')

def rename_list(sock, list_name, new_name):
  '''Use this command to rename a mailing list.

     list_name : string
     This parameter specifies the name of an existing mailing list.
     It can include the Domain name.
     If the Domain name is not specified, the user Domain is used by default.

     new_name : string
     This parameter specifies the new name for the mailing list (without the Domain part).
     Domain Administrators can use this command if they have the CanCreateLists Domain access right.'''

  return _operate(sock, 'RENAMELIST ' + list_name + ' into ' + new_name + '\n')
      
def delete_list(sock, list_name):
  '''Use this command to remove a mailing list.

     list_name : string
     This parameter specifies the name of an existing mailing list.
     It can include the Domain name.
     If the Domain name is not specified, the user Domain is used by default.

     Domain Administrators can use this command if they have the CanCreateLists Domain access right.'''

  return _operate(sock, 'DELETELIST ' + list_name + '\n')
      
def get_list(sock, list_name):
  '''The following command can be used by the mailing list owner, by a Domain Administrator with the CanAccessLists access right, or by a Server Administrator with the All Domains Server access right.
    
     Use this command to retrieve list settings.
     The command produces an output - a dictionary with the list_name mailing list settings.
     
     list_name : string
     This parameter specifies the name of an existing mailing list. It can include the Domain name.
     If the Domain name is not specified, the user Domain is used by default.'''
  
  return _operate(sock, 'GETLIST ' + list_name + '\n')
      
def update_list(sock, list_name, new_settings):
  '''The following command can be used by the mailing list owner, by a Domain Administrator with the CanAccessLists access right, or by a Server Administrator with the All Domains Server access right.
     Use this command to modify list settings.

     list_name : string
     This parameter specifies the name of an existing mailing list.
     It can include the Domain name.
     If the Domain name is not specified, the user Domain is used by default.

     new_settings : dictionary
     This dictionary is used to update the mailing list settings dictionary. 
     It does not have to contain all settings data, the omitted settings will be left unmodified.'''

  return _operate(sock, 'UPDATELIST ' + list_name + ' ' + parse_to_CGP_object(new_settings) + '\n')

def list(sock, list_name, operation, subscriber, silently=False, confirm=False):
  '''The following command can be used by the mailing list owner, by a Domain Administrator with the CanAccessLists access right, or by a Server Administrator with the All Domains Server access right.
     Use this command to update the subscribers list.
  
     list_name : string
     This parameter specifies the name of an existing mailing list.
     It can include the Domain name.
     If the Domain name is not specified, the user Domain is used by default.
  
     operation : subscribe | feed | digest | index | null | banned | unsubscribe
     This parameter specifies the operation (see the LIST module section for the details).
  
     silently
     This optional parameter tells the server not to send the Welcome/Bye message to the subscriber.
  
     confirm
     This optional parameter tells the server to send a confirmation request to the subscriber.
  
     subscriber : E-mail address
     The subscriber address. It can include the comment part used as the subscriber's real name.'''

  params = ''
  
  if operation not in ['subscribe', 'feed', 'digest', 'index', 'null', 'banned', 'unsubscribe']:
    raise ValueError("Value is out of list")
  
  if silently:
    params += ' silently'
  
  if confirm:
    params += ' confirm'  

  return _operate(sock, 'LIST ' + list_name + ' ' + operation + params + ' ' + subscriber + '\n')

def list_subscribers(sock, list_name, filter=None, limit=None):
  '''The following command can be used by the mailing list owner, by a Domain Administrator with the CanAccessLists access right, or by a Server Administrator with the All Domains Server access right.
    
     Use this command to retrieve list subscribers.
     The command produces an output - an array with subscribers' E-mail addresses.
   
     list_name : string
     This parameter specifies the name of an existing mailing list.
     It can include the Domain name.
     If the Domain name is not specified, the user Domain is used by default.
   
     filter : string
     If this optional parameter is specified, only the addresses containing the specified string are returned.
     It won't work if list_name is not set.
   
     limit : int
     This optional parameter limits the number of subscriber addresses returned. ("filter" required)'''
  
  params = ''
      
  if filter is not None:
    params += ' FILTER ' + filter
    
    if limit is not None:
      params += ' ' + str(limit)
    
  return _operate(sock, 'LISTSUBSCRIBERS ' + list_name + params + '\n')

def read_subscribers(sock, list_name, filter=None, limit=None):
  '''The following command can be used by the mailing list owner, by a Domain Administrator with the CanAccessLists access right, or by a Server Administrator with the All Domains Server access right.
    
     Use this command to retrieve list subscribers.
     The command produces an output - an array, where the first element is a number - the total number of list subscribers, and the second element is an array of subscriber descriptor dictionaries.
   
     list_name : string
     This parameter specifies the name of an existing mailing list.
     It can include the Domain name.
     If the Domain name is not specified, the user Domain is used by default.
    
     filter : string
     If this optional parameter is specified, only subscribers with addresses containing the specified string are returned.
    
     limit : int
     This optional parameter limits the number of subscriber dictionaries returned.
     It won't work if list_name is not set.
    
     A dictionary describing a subscriber has the following elements:
     
     Sub
       E-mail address string
    
     RealName
       an optional string with Real name
    
     mode
       a string with subscription mode (index, digest, null, etc.)
    
     subscribeTime
       timestamp data specifying the moment when this user subscribed.
    
     posts
       number of postings on this list
    
     lastBounceTime
       optional timestamp data specifying the last time when messages sent to this user failed.
    
     bounces
       optional numeric data specifying the number of failed delivery reports received for this user.'''
  
  params = ''
      
  if filter is not None:
    params += ' FILTER ' + filter
    
    if limit is not None:
      params += ' ' + str(limit)
    
  return _operate(sock, 'READSUBSCRIBERS ' + list_name + params + '\n')

def get_subscriber_info(sock, list_name, subscriber_address):
  '''The following command can be used by the mailing list owner, by a Domain Administrator with the CanAccessLists access right, or by a Server Administrator with the All Domains Server access right.
     Use this command to retrieve information about a list subscriber.
     The command produces an output - a dictionary with subscriber information.
   
     list_name : string
     This parameter specifies the name of an existing mailing list.
     It can include the Domain name.
     If the Domain name is not specified, the user Domain is used by default.
  
     subscriber_address : string
     This parameter specifies the E-mail address of the list subscriber.
 
     If the subscriber does not exist, an empty dictionary is returned. Otherwise, the dictionary contains the following elements:
   
     mode
       This string element specified the subscription mode (digest, index, etc.)
     This element is equal to unsubscribe if the address has been unsubscribed, but has not been removed from the list. This element is equal to subscribe if a user has started subscription, but the subscription has not been confirmed.
 
     confirmationID
       This element contains the subscriber's Confirmation ID string.
 
     timeSubscribed
       This string element specifies when the address was subscribed (in the ACAP date/time format).
  
     posts
       This string element may contain the strings special, moderateAll, prohibited, or the string with the number of messages posted from this address. If the next postings from this address are to be moderated, the element contains an array with one string element that contains the number of postings to be moderated.
    
     bounces
       This optional string element contains the number of bounces received from this address.
   
     lastBounced
       This optional string element specifies the last time when messages to this address bounced were bounced.
     The data and time are specified in the ACAP format.
     
     RealName
       This optional string element contains the real name of the subscriber.'''
  
  return _operate(sock, 'GETSUBSCRIBERINFO ' + list_name + ' NAME ' + subscriber_address + '\n')

def set_posting_mode(sock, list_name, subscriber_address, posting_mode=None):
  '''The following command can be used by the mailing list owner, by a Domain Administrator with the CanAccessLists access right, or by a Server Administrator with the All Domains Server access right.
     Use this command to set the posting mode for the specified subscriber.
     
     list_name : string
     This parameter specifies the name of an existing mailing list. It can include the Domain name.
     If the Domain name is not specified, the user Domain is used by default.
    
     subscriber_address : string
     This parameter specifies the E-mail address of the list subscriber.
     
     posting_mode : UNMODERATED | MODERATEALL | PROHIBITED | SPECIAL | number
     This optional parameter limits the number of subscriber addresses returned.
     
     The command sets the posting mode the specified subscriber.
     If numberOfModerated (a number) is specified, the posting mode set requires moderation of the first numberOfModerated messages from this subscriber.'''
  
  params = ''
  
  if posting_mode is not None:
    if posting_mode in ['UNMODERATED', 'MODERATEALL', 'PROHIBITED', 'SPECIAL', 'number']:
      params += ' ' + posting_mode
    else:
      raise ValueError("Value is out of list")

  return _operate(sock, 'SETPOSTINGMODE ' + list_name + ' FOR ' + subscriber_address + params + '\n')

def process_bounce(sock, list_name, subscriber_address, fatal=False):
  '''The following command can be used by the mailing list owner, by a Domain Administrator with the CanAccessLists access right, or by a Server Administrator with the All Domains Server access right.
     Use this command to perform the same action the List Manager performs when it receives a bounce message for the subscriber address.
     
     list_name : string
     This parameter specifies the name of an existing mailing list. It can include the Domain name.
     If the Domain name is not specified, the user Domain is used by default.

     subscriber_address : string
     This parameter specifies the E-mail address of the list subscriber.

     Use the FATAL keyword to emulate a "fatal" bounce.
     Otherwise the command emulates a non-fatal bounce.'''

  params = ''
  
  if fatal:
      params += ' FATAL'

  return _operate(sock, 'PROCESSBOUNCE ' + list_name + params + ' FOR ' + subscriber_address + '\n')

#Web Skins Administration
def list_domain_skins(sock, domain_name=None):
  '''The following commands can be used to manage CommuniGate Pro Skins used for the CommuniGate Pro WebUser Interface.
     A user should have the All Domains Server access right or the CanModifySkins Domain Administration access right to modify the Domain Skins.

     Use this command to list custom Domain Skins.
     The command produces an output - an array with Skin names.
   
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.'''
  
  params = ''
  
  if domain_name is not None:
    params += ' ' + domain_name
      
  return _operate(sock, 'LISTDOMAINSKINS' + params + '\n')
      
def create_domain_skin(sock, skin_name, domain_name=None):
  '''The following commands can be used to manage CommuniGate Pro Skins used for the CommuniGate Pro WebUser Interface.
     A user should have the All Domains Server access right or the CanModifySkins Domain Administration access right to modify the Domain Skins.
     
     Use this command to create a custom Domain Skin.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.

     skin_name : string
     This parameter specifies the name of the new Skin.
  
     To create the unnamed Domain Skin, specify an empty string as the skin_name parameter value.
     A named Domain Skin can be created only when the unnamed Domain Skin exists.'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' SKIN  '

  return _operate(sock, 'CREATEDOMAINSKIN ' + params + skin_name + '\n')

def rename_domain_skin(sock, skin_name, new_skin_name, domain_name=None):
  '''The following commands can be used to manage CommuniGate Pro Skins used for the CommuniGate Pro WebUser Interface.
     A user should have the All Domains Server access right or the CanModifySkins Domain Administration access right to modify the Domain Skins.
     
     Use this command to rename a custom named Domain Skin.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.

     skin_name : string
     This parameter specifies the name of an existing named Skin.

     new_skin_name : string
     This parameter specifies the new name for the Skin.'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' SKIN  '

  return _operate(sock, 'RENAMEDOMAINSKIN ' + params + skin_name + ' INTO ' + new_skin_name + '\n')

def delete_domain_skin(sock, skin_name, domain_name=None): 
  '''The following commands can be used to manage CommuniGate Pro Skins used for the CommuniGate Pro WebUser Interface.
     A user should have the All Domains Server access right or the CanModifySkins Domain Administration access right to modify the Domain Skins.
     
     Use this command to delete a custom Domain Skin.
     
     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.

     
     skin_name : string
     This parameter specifies the name of the Skin to be deleted.
     
     To delete the unnamed Domain Skin, specify an empty string as the skin_name parameter value.
     The unnamed Domain Skin can be deleted only when no named Domain Skin exists.'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' SKIN  '

  return _operate(sock, 'DELETEDOMAINSKIN ' + params + skin_name + '\n')

def list_domain_skin_files(sock, skin_name, domain_name=None):
  '''The following commands can be used to manage CommuniGate Pro Skins used for the CommuniGate Pro WebUser Interface.
     A user should have the All Domains Server access right or the CanModifySkins Domain Administration access right to modify the Domain Skins.

     Use this command to list files in a custom Domain Skin.
     The command produces an output - a dictionary with Skin file names as keys.
     The dictionary element values are dictionaries with file attributes.

     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.

     skin_name : string
     This parameter specifies the name of an existing Domain Skin.'''
  
  params = ''
  
  if domain_name is not None:
    params = domain_name + ' SKIN '
      
  return _operate(sock, 'LISTDOMAINSKINFILES ' + params + skin_name + '\n')
      
def read_domain_skin_file(sock, skin_name, file_name, domain_name=None):
  '''The following commands can be used to manage CommuniGate Pro Skins used for the CommuniGate Pro WebUser Interface.
     Use this command to read a file from a custom Domain Skin.
     The command produces an output - an array.
     The first array element is a datablock with the Skin file content, the second array element is a timestamp with the file modification date.

     domain_name : string
     This optional parameter specifies the Domain name.
     If the Domain name is not specified, the command applies to the administrator Domain.

     skin_name : string
     This parameter specifies the name of an existing Domain Skin.

     file_name : string
     This parameter specifies the name of an existing file in the specified Domain Skin.'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' SKIN  '

  return _operate(sock, 'READDOMAINSKINFILE ' + params + skin_name + ' FILE ' + file_name + '\n')

def store_domain_skin_file(sock, skin_name, file_name, file_content, domain_name=None): 
  '''The following commands can be used to manage CommuniGate Pro Skins used for the CommuniGate Pro WebUser Interface.
     Use this command to store a file into a custom Domain Skin.
    
    domain_name : string
    This optional parameter specifies the Domain name.
    If the Domain name is not specified, the command applies to the administrator Domain.
  
    skin_name : string
    This parameter specifies the name of an existing Domain Skin.

    file_name : string
    This parameter specifies the Skin file name.
 
    file_content : datablock
    This datablock contains file content.

    If the DATA keyword is specified and the Skin contains a file with the same name, the old file is deleted.
    The file with the specified name is removed from the Skin Cache (in the Dynamic Cluster the file is removed from Skin caches on all cluster members).'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' SKIN  '

  return _operate(sock, 'STOREDOMAINSKINFILE ' + params + skin_name + ' FILE ' + file_name + ' DATA ' + str(file_content) + '\n')

def remove_domain_skin_file(sock, skin_name, file_name, domain_name=None): 
  '''The following commands can be used to manage CommuniGate Pro Skins used for the CommuniGate Pro WebUser Interface.
     Use this command to delete a file from a custom Domain Skin.'''

  params = ''
  
  if domain_name is not None:
    params = domain_name + ' SKIN  '

  return _operate(sock, 'STOREDOMAINSKINFILE ' + params + skin_name + ' FILE ' + file_name + ' DELETE\n')

def list_server_skins(sock):
  '''The following command is available for the System Administrators only.    
     Use this command to list custom Server Skins.
     The command produces an output - an array with Skin names.'''
  
  return _operate(sock, 'LISTSERVERSKINS\n')
      
def create_server_skin(sock, skin_name):
  '''The following command is available for the System Administrators only.
     Use this command to create a custom Server Skin.
  
     skin_name : string
     This parameter specifies the name of the new Skin.'''

  return _operate(sock, 'CREATESERVERSKIN ' + skin_name + '\n')

def rename_server_skin(sock, skin_name, new_skin_name):
  '''The following command is available for the System Administrators only.
     Use this command to rename a custom Server Skin.
    
     skin_name : string
     This parameter specifies the name of an existing Skin.
   
     new_skin_name : string
     This parameter specifies the new name for the Skin.'''

  return _operate(sock, 'RENAMESERVERSKIN ' + skin_name + ' INTO ' + new_skin_name + '\n')
      
def delete_server_skin(sock, skin_name): 
  '''The following command is available for the System Administrators only.
     Use this command to delete a custom Server Skin.

     skin_name : string
     This parameter specifies the name of the Skin to be deleted.'''

  return _operate(sock, 'DELETESERVERSKIN ' + skin_name + '\n')

def list_server_skin_files(sock, skin_name):
  '''The following command is available for the System Administrators only.
     Use this command to list files in a custom Server Skin.
     The command produces an output - a dictionary with Skin file names as keys.
     The dictionary element values are dictionaries with file attributes.

     skin_name : string
     This parameter specifies the name of an existing Server Skin.'''
  
  return _operate(sock, 'LISTSERVERSKINFILES ' + skin_name + '\n')

def read_server_skin_file(sock, skin_name, file_name):
  '''The following command is available for the System Administrators only.
     Use this command to read a file from a custom Server Skin.
     The command produces an output - an array.
     The first array element is a datablock with the Skin file content, the second array element is a timestamp with the file modification date.
    
     skin_name : string
     This parameter specifies the name of an existing Server Skin.
    
     file_name : string
     This parameter specifies the name of an existing file in the specified Server Skin.'''

  return _operate(sock, 'READSERVERSKINFILE ' + skin_name + ' FILE ' + file_name + '\n')

def store_server_skin_file(sock, skin_name, file_name, file_content): 
  '''The following command is available for the System Administrators only.
     Use this command to store a file into a custom Server Skin.
   
     skin_name : string
     This parameter specifies the name of an existing Server Skin.
    
     file_name : string
     This parameter specifies the Skin file name.
    
     file_content : datablock
     This datablock contains the file content.
     This parameter is specified only if the DATA keyword is used.
     
     If the DATA keyword is specified and the Skin contains a file with the same name, the old file is deleted.
     The file with the specified name is removed from the Skin Cache (in the Dynamic Cluster the file is removed from Skin caches on all cluster members).'''

  return _operate(sock, 'STORESERVERSKINFILE ' + skin_name + ' FILE ' + file_name + ' DATA ' + str(file_content) + '\n')

def remove_server_skin_file(sock, skin_name, file_name): 
  '''The following command is available for the System Administrators only.
     Use this command to delete a file from a custom Server Skin.'''

  return _operate(sock, 'STORESERVERSKINFILE ' + skin_name + ' FILE ' + file_name + ' DELETE\n')
    
def list_cluster_skins(sock):
  '''The following command is available for the System Administrators only.    
     These command is available in the Dynamic Cluster only.
     Use these commands to list the cluster-wide Skins.'''
  
  return _operate(sock, 'LISTCLUSTERSKINS\n')
      
def create_cluster_skin(sock, skin_name):
  '''The following command is available for the System Administrators only.
     These command is available in the Dynamic Cluster only.
     Use these commands to create the cluster-wide Skins.
  
     skin_name : string
     This parameter specifies the name of the new Skin.'''

  return _operate(sock, 'CREATECLUSTERSKIN ' + skin_name + '\n')

def rename_cluster_skin(sock, skin_name, new_skin_name):
  '''The following command is available for the System Administrators only.
     These command is available in the Dynamic Cluster only.
     Use these commands to rename the cluster-wide Skins.
    
     skin_name : string
     This parameter specifies the name of an existing Skin.
   
     new_skin_name : string
     This parameter specifies the new name for the Skin.'''

  return _operate(sock, 'RENAMECLUSTERSKIN ' + skin_name + ' INTO ' + new_skin_name + '\n')
      
def delete_cluster_skin(sock, skin_name): 
  '''The following command is available for the System Administrators only.
     These command is available in the Dynamic Cluster only.
     Use these commands to delete the cluster-wide Skins.

     skin_name : string
     This parameter specifies the name of the Skin to be deleted.'''

  return _operate(sock, 'DELETECLUSTERSKIN ' + skin_name + '\n')

def list_cluster_skin_files(sock, skin_name):
  '''The following command is available for the System Administrators only.
     These command is available in the Dynamic Cluster only.
     Use these command to list files in the cluster-wide Skins.
     The command produces an output - a dictionary with Skin file names as keys.
     The dictionary element values are dictionaries with file attributes.

     skin_name : string
     This parameter specifies the name of an existing Server Skin.'''
  
  return _operate(sock, 'LISTCLUSTERSKINFILES ' + skin_name + '\n')
      
def read_cluster_skin_file(sock, skin_name, file_name):
  '''The following command is available for the System Administrators only.
     These command is available in the Dynamic Cluster only.
     Use these command to read files in the cluster-wide Skins.
     The command produces an output - an array.
     The first array element is a datablock with the Skin file content, the second array element is a timestamp with the file modification date.
    
     skin_name : string
     This parameter specifies the name of an existing Server Skin.
    
     file_name : string
     This parameter specifies the name of an existing file in the specified Server Skin.'''

  return _operate(sock, 'READCLUSTERSKINFILE ' + skin_name + ' FILE ' + file_name + '\n')

def store_cluster_skin_file(sock, skin_name, file_name, file_content): 
  '''The following command is available for the System Administrators only.
     These command is available in the Dynamic Cluster only.
     Use these command to store files in the cluster-wide Skins.
   
     skin_name : string
     This parameter specifies the name of an existing Server Skin.
    
     file_name : string
     This parameter specifies the Skin file name.
    
     file_content : datablock
     This datablock contains the file content.
     This parameter is specified only if the DATA keyword is used.
     
     If the DATA keyword is specified and the Skin contains a file with the same name, the old file is deleted.
     The file with the specified name is removed from the Skin Cache (in the Dynamic Cluster the file is removed from Skin caches on all cluster members).'''

  return _operate(sock, 'STORECLUSTERSKINFILE ' + skin_name + ' FILE ' + file_name + ' DATA ' + str(file_content) + '\n')

def remove_cluster_skin_file(sock, skin_name, file_name): 
  '''The following command is available for the System Administrators only.
     These command is available in the Dynamic Cluster only.
     Use these command to delete files in the cluster-wide Skins.'''

  return _operate(sock, 'STORECLUSTERSKINFILE ' + skin_name + ' FILE ' + file_name + ' DELETE\n')

def list_stock_skin_files(sock, skin_name):
  '''The following command is available for the System Administrators only.
     Use these command list files in the built-in Skins
     The command produces an output - a dictionary with Skin file names as keys.
     The dictionary element values are dictionaries with file attributes.

     skin_name : string
     This parameter specifies the name of an existing Server Skin.'''
  
  return _operate(sock, 'LISTSTOCKSKINFILES ' + skin_name + '\n')
      
def read_stock_skin_file(sock, skin_name, file_name):
  '''The following command is available for the System Administrators only.
     Use these command read files in the built-in Skins.
     The command produces an output - an array.
     The first array element is a datablock with the Skin file content, the second array element is a timestamp with the file modification date.
    
     skin_name : string
     This parameter specifies the name of an existing Server Skin.
    
     file_name : string
     This parameter specifies the name of an existing file in the specified Server Skin.'''

  return _operate(sock, 'READSTOCKSKINFILE ' + skin_name + ' FILE ' + file_name + '\n')

# Web Interface Integration
def create_web_user_session(sock, account_name, ip_address, 
                            orig_address=None, skin_name=None, mode=None):
  '''The following command can be used to integrate the CommuniGate Pro WebUser Interface with third-party applications.
    
     Use this command to create a WebUser session for the specified Account.
     The command produces an output - a string that contains the WebUser Session ID.
     This string can be used to compose a URL that will allow the client browser to "enter" the WebUser Session.
     That URL can have the following format:
     http://cgateproserver:port/Session/rrrrrrrrrrrr/Mailboxes.wssp
     where rrrrrrrrrrrr is the Session ID string returned.
  
     account_name : string
     This parameter specifies the Account name.
    
     ip_address : string
     This parameter specifies the IP address and port of the client browser.
     If the Account has the "Fixed IP" Preference setting enabled, connections to the session will be allowed from this IP address only.
   
     orig_address : string
     This parameter specifies the original IP address of the client browser, if the client connects via a proxy.
     The ip-address parameter specifies the proxy IP address.
     If the Account has the "Fixed IP" Preference setting enabled, connections to the session will be allowed from the proxy IP address only and only from this original IP address (passed by the proxy in the X-FORWARDED-FOR HTTP header field).
  
     skin_name : string
     This optional parameter specifies the Skin to use for the newly created session.
   
     The optional WML or IMode keywords can be used to emulate login via a WML or I-Mode browser.
     The authenticated user should have the All Domains Server access right or the CanCreateWebUserSessions Domain Administration access right to create WebUser Sessions.'''

  params = ''
  
  if orig_address is not None:
    params += ' FOR ' + orig_address
    
  if mode is not None:
    if mode in ['WML', 'IMode']:
      params += ' ' + mode
    else:
      raise ValueError("Value is out of list")

  if skin_name is not None:
    params += ' SKIN ' + skin_name
    
  return _operate(sock, 'CREATEWEBUSERSESSION ' + account_name + ' ADDRESS ' + ip_address + params + '\n')

def create_XIMSS_session(sock, account_name, ip_address, orig_address=None):
  '''The following command can be used to integrate the CommuniGate Pro WebUser Interface with third-party applications.
    
     Use this command to create a XIMSS session for the specified Account.
     The command produces an output - a string that contains the XIMSS Session ID.
     This string can be used to compose a URL that will allow the client browser to work with the XIMSS Session using HTTP Binding.
    
     account_name : string
     This parameter specifies the Account name.
     
     ip_address : string
     orig_address : string
     These parameters have the same meaning as for the createWebUserSession command.
     
     The authenticated user should have the All Domains Server access right or the CanCreateWebUserSessions Domain Administration access right to create XIMSS Sessions.'''

  params = ''
  
  if orig_address is not None:
    params += ' FOR ' + orig_address
    
  return _operate(sock, 'CREATEXIMSSSESSION ' + account_name + ' ADDRESS ' + ip_address + prarms + '\n')

def find_account_session(sock, account_name,
                          ip_address=None, proxiedAddress=None,
                          protocol=None, transport=None, client=None):
  '''The following command can be used to integrate the CommuniGate Pro WebUser Interface with third-party applications.
     Use this command to find an existing session for the specified Account. The command produces an output - a string that contains the Session ID.
    
     account_name : string
     This parameter specifies the Account name.
  
     ip_address : string or IP address
     This optional parameter specifies the IP address of the client browser.
     If it is specified, the command will find only those sessions that have the "Fixed IP" Preference disabled or have the same login IP address as the specified one.
   
     proxiedAddress : string
     This optional parameter specifies the IP address of the client browser, if this browser is located behind an HTTP proxy.
     The ip-address then specifies the IP address of that proxy.
   
     protocol : string
     This optional parameter specifies the Session protocol (WebUser, XIMSS, XMPP, etc.)
     If specified, only the sessions created with the specified protocol are searched.
  
     transport : string
     This optional parameter specifies the Session transport (HTTP, XIMSS, XMPP, etc.)
     If specified, only the sessions created with the specified transport are searched.
   
     client : string
     This optional parameter specifies the Session client.
     If specified, only the sessions created with the specified client (if the client has informed the session about its name) are searched.
   
     The authenticated user should have the All Domains Server access right or the CanCreateWebUserSessions Domain Administration access right to use this command.'''

  params = ''

  if ip_address is not None:
    params += ' ADDRESS ' + ip_address
    
    if proxiedAddress is not None:
      params += ' FOR ' + proxiedAddress
  
  if protocol is not None:
    params += ' PROTOCOL ' + protocol  

  if transport is not None:
    params += ' TRANSPORT ' + transport  
    
  if client is not None:
    params += ' CLIENT ' + client  
    
  return _operate(sock, 'FINDACCOUNTSESSION ' + account_name + params + '\n')

def list_account_sessions(sock, account_name,
                          ip_address=None, proxiedAddress=None,
                          protocol=None, transport=None, client=None):
  '''The following command can be used to integrate the CommuniGate Pro WebUser Interface with third-party applications.
     
     Use this command to retrieve all existing sessions for the specified Account.
     The command produces an output - an array of strings, where each string is the Session ID.
     Command parameters are the same as the findAccountSession command parameters.
     The authenticated user should have the All Domains Server access right or the CanCreateWebUserSessions Domain Administration access right to use this command.'''

  params = ''

  if ip_address is not None:
    params += ' ADDRESS ' + ip_address
    
    if proxiedAddress is not None:
      params += ' FOR ' + proxiedAddress
  
  if protocol is not None:
    params += ' PROTOCOL ' + protocol

  if transport is not None:
    params += ' TRANSPORT ' + transport
    
  if client is not None:
    params += ' CLIENT ' + client
    
  return _operate(sock, 'LISTACCOUNTSESSIONS ' + account_name + params + '\n')

def get_account_session(sock, sessionID, domain_name=None):
  '''The following command can be used to integrate the CommuniGate Pro WebUser Interface with third-party applications.
     Use this command to retrieve Session data.
     The command produces an output - a dictionary with the session dataset (specified in the WSSP section of this manual).
     
     sessionID : string
     This parameter specifies the Session ID.
    
     domain_name : string
     This optional parameter specifies the name of Domain the session Account belongs to.
     The authenticated user should have the All Domains Server access right to retrieve Session data if the domain_name parameter is not specified.
     If the domain_name is specified, the authenticated user should have the CanCreateWebUserSessions Domain Administration access right for the specified Domain.
     This operation resets the session inactivity timer.'''

  params = ''

  if domain_name is not None:
    params += ' DOMAIN ' + domain_name
    
  return _operate(sock, 'GETSESSION ' + sessionID + params + '\n')

def kill_account_session(sock, sessionID, domain_name=None):
  '''The following command can be used to integrate the CommuniGate Pro WebUser Interface with third-party applications.
    
     Use this command to terminate a Session.
     
     sessionID : string
     This parameter specifies the Session ID.
    
     domain_name : string
     This optional parameter specifies the name of Domain the session Account belongs to.
     The authenticated user should have the All Domains Server access right to terminate a Session if the domain_name parameter is not specified.
     If the domain_name is specified, the authenticated user should have the CanCreateWebUserSessions Domain Administration access right for the specified Domain.'''

  params = ''

  if domain_name is not None:
    params += ' DOMAIN ' + domain_name
    
  return _operate(sock, 'KILLSESSION ' + sessionID  + prarms + '\n')

def bless_account_session(sock, sessionID, secret=None, domain_name=None):
  '''The following command can be used to integrate the CommuniGate Pro WebUser Interface with third-party applications.
     Use this command to complete the second stage of a Two-factor authentication process for the given session.
     
     sessionID : string
     This parameter specifies the Session ID.
    
     secret : string
     This optional parameter specifies the one-time secret used with Two-factor Authentication.
    
     domain_name : string
     This optional parameter specifies the name of Domain the session Account belongs to.
    
     The authenticated user should have the All Domains Server access right to complete the Two-factor Authentication process for a Session if the domain_name parameter is not specified.
     If the domain_name is specified, the authenticated user should have the CanCreateWebUserSessions Domain Administration access right for the specified Domain.
     If the secret parameter is not specified then the Session should be waiting the Two-factor Authentication process completion in background and authenticated user should have the Master Server Administration access right.'''

  params = ''
  
  if secret is not None:
    params += ' PASSWORD ' + secret
    
  if domain_name is not None:
    params += ' DOMAIN ' + domain_name
    
  return _operate(sock, 'BLESSSESSION ' + sessionID  + prarms + '\n')

#Real-Time Application Administration
def create_domain_PBX(sock, domain_name, language=None):
  '''The following commands can be used to manage CommuniGate Pro Real-Time Application Environments.
     A user should have the All Domains Server access right or the CanModifyPBXApps Domain Administration access right to modify the Domain Real-Time Application Environment.
    
     Use this command to create the Domain Real-Time Application Environment or to create its national subset.
     domain_name : string
     This parameter specifies the Domain name.
     
     language : string
     This optional parameter specifies a national subset name.'''

  params = ''
  
  if language is not None:
    params += ' FILE ' + language

  return _operate(sock, 'CREATEDOMAINPBX ' + domain_name + params + '\n')

def delete_domain_PBX(sock, domain_name, language):
  '''The following commands can be used to manage CommuniGate Pro Real-Time Application Environments.
     A user should have the All Domains Server access right or the CanModifyPBXApps Domain Administration access right to modify the Domain Real-Time Application Environment.
     
     Use this command to remove a national subset from the Domain Real-Time Application Environment.
   
     domain_name : string
     This parameter specifies the Domain name.
   
     language : string
     This parameter specifies a national subset name.'''

  return _operate(sock, 'DELETEDOMAINPBX ' + domain_name + ' FILE ' + language + '\n')

def list_domain_PBX_files(sock, domain_name, language=None):
  '''The following commands can be used to manage CommuniGate Pro Real-Time Application Environments.
     A user should have the All Domains Server access right or the CanModifyPBXApps Domain Administration access right to modify the Domain Real-Time Application Environment.
     
     Use this command to list files in the Domain Real-Time Application Environment.
     The command produces an output - a dictionary with file names used as keys. The dictionary element values are dictionaries with file attributes.
  
     domain_name : string
     This optional parameter specifies the Domain name. If the Domain name is not specified, the command applies to the administrator Domain.
   
     language : string
     This optional parameter specifies a national subset name.'''

  params = ''

  if language is not None:
    params += ' FILE ' + language
       
  return _operate(sock, 'LISTDOMAINPBXFILES ' + domain_name + params + '\n')

def read_domain_PBX_file(sock, domain_name, file_name):
  '''The following commands can be used to manage CommuniGate Pro Real-Time Application Environments.
     A user should have the All Domains Server access right or the CanModifyPBXApps Domain Administration access right to modify the Domain Real-Time Application Environment.
     
     Use this command to read a file from the Domain Real-Time Application Environment.
     The command produces an output - a datablock with the file contents.
     
     domain_name : string
     This parameter specifies the Domain name.
     
     file_name : string
     This parameter specifies the file name.
     To retrieve a file from a national subset, specify the name as language/file_name.'''

  return _operate(sock, 'READDOMAINPBXFILE ' + domain_name + ' FILE ' + file_name + '\n')

def store_domain_PBX_file(sock, domain_name, file_name, file_content): 
  '''The following commands can be used to manage CommuniGate Pro Real-Time Application Environments.
     A user should have the All Domains Server access right or the CanModifyPBXApps Domain Administration access right to modify the Domain Real-Time Application Environment.
     
     Use this command to store a file into the Domain Real-Time Application Environment.
    
     domain_name : string
     This parameter specifies the Domain name.
    
     file_name : string
     This parameter specifies the file name. To store a file into a national subset, specify the name as language/file_name.
    
     file_content : datablock
     This parameter is specified only if the DATA keyword is used. It should contain the file contents.
    
     If the DATA keyword is specified and the environment contains a file with the specified name, the old file is deleted.
     The file with the specified name is removed from the Environment cache (in the Dynamic Cluster the file is removed from all cluster members caches).
     
     Use delete_domain_PBX_file command to DELETE file.'''

  return _operate(sock, 'STOREDOMAINPBXFILE ' + domain_name + ' FILE ' + file_name + ' DATA ' + str(file_content) + '\n')

def delete_domain_PBX_file(sock, domain_name, file_name): 
  '''The following commands can be used to manage CommuniGate Pro Real-Time Application Environments.
     A user should have the All Domains Server access right or the CanModifyPBXApps Domain Administration access right to modify the Domain Real-Time Application Environment.
     
     Use this command to delete a file from the Domain Real-Time Application Environment.
    
     domain_name : string
     This parameter specifies the Domain name.
    
     file_name : string
     This parameter specifies the file name. To store a file into a national subset, specify the name as language/file_name.
    
     file_content : datablock
     This parameter is specified only if the DATA keyword is used. It should contain the file contents.
    
     If the DATA keyword is specified and the environment contains a file with the specified name, the old file is deleted.
     The file with the specified name is removed from the Environment cache (in the Dynamic Cluster the file is removed from all cluster members caches).'''

  return _operate(sock, 'STOREDOMAINPBXFILE ' + domain_name + ' FILE ' + file_name + ' DELETE\n')

def create_server_PBX(sock, language):
  '''The following command is available for the System Administrators only.
  
     Use this command to create the Server-wide Real-Time Application Environment or to create its national subset.
     
     language : string
     This parameter specifies a national subset name.'''

  return _operate(sock, 'CREATESERVERPBX ' + language + '\n')

def delete_server_PBX(sock, language):
  '''The following command is available for the System Administrators only.
  
     Use this command to remove a national subset of the Server-wide Real-Time Application Environment.
     
     language : string
     This parameter specifies a national subset name.'''

  return _operate(sock, 'DELETESERVERPBX ' + ' FILE ' + language + '\n')

def list_server_PBX_files(sock, language=None):
  '''The following command is available for the System Administrators only.
  
     Use this command to list files in the Server-wide Real-Time Application Environment.
     The command produces an output - a dictionary with file names used as keys.
     The dictionary element values are dictionaries with file attributes.
    
     language : string
     This optional parameter specifies a national subset name.'''

  params = ''

  if language is not None:
    params += ' ' + language
       
  return _operate(sock, 'LISTSERVERPBXFILES' + params + '\n')

def read_server_PBX_file(sock, file_name):
  '''The following command is available for the System Administrators only.
     Use this command to read a file from the Server-wide Real-Time Application Environment.
     The command produces an output - a datablock with the file contents.
    
     file_name : string
     This parameter specifies the file name.
     To retrieve a file from a national subset, specify the name as language/file_name.'''

  return _operate(sock, 'READSERVERPBXFILE ' + file_name + '\n')

def store_server_PBX_file(sock, file_name, file_content): 
  '''The following command is available for the System Administrators only.
     
     Use this command to store a file into the Server-wide Real-Time Application Environment.
     
     file_name : string
     This parameter specifies the file name.
     To store a file into a national subset, specify the name as language/file_name.
    
     file_content : datablock
     It should contain the file contents.
     
     If the DATA keyword is specified and the environment contains a file with the specified name, the old file is deleted.
     The file with the specified name is removed from the Environment cache (in the Dynamic Cluster the file is removed from all cluster members caches).
     
     Use delete_server_PBX_file command to DELETE file.'''

  return _operate(sock, 'STORESERVERPBXFILE ' + file_name + ' DATA ' + str(file_content) + '\n')

def delete_server_PBX_file(sock, file_name): 
  '''The following command is available for the System Administrators only.
     
     Use this command to delete a file from the Server-wide Real-Time Application Environment.
     
     file_name : string
     This parameter specifies the file name.
     To store a file into a national subset, specify the name as language/file_name.'''

  return _operate(sock, 'STORESERVERPBXFILE ' + file_name + ' DELETE\n')

def create_cluster_PBX(sock, language):
  '''The following command is available for the System Administrators only.
     
     These command is available in the Dynamic Cluster only.
     Use this command to create the cluster-wide Real-Time Application Environment or to create its national subset.'''

  return _operate(sock, 'CREATECLUSTERPBX ' + language + '\n')

def delete_cluster_PBX(sock, language):
  '''The following command is available for the System Administrators only.
     
     These command is available in the Dynamic Cluster only.
     Use this command to delete the cluster-wide Real-Time Application Environment or to create its national subset.'''

  return _operate(sock, 'DELETECLUSTERPBX ' + language + '\n')
    
def list_cluster_PBX_files(sock, language=None):
  '''The following command is available for the System Administrators only.
     
     These command is available in the Dynamic Cluster only.
     Use these command to list files in the cluster-wide Real-Time Application Environment.'''

  params = ''

  if language is not None:
    params += ' ' + language
       
  return _operate(sock, 'LISTCLUSTERPBXFILES' + params + '\n')

def read_cluster_PBX_file(sock, file_name):
  '''The following command is available for the System Administrators only.
     
     These command is available in the Dynamic Cluster only.
     Use these command to read files in the cluster-wide Real-Time Application Environment.'''

  return _operate(sock, 'READCLUSTERPBXFILE ' + file_name + '\n')

def store_cluster_PBX_file(sock, file_name, file_content): 
  '''The following command is available for the System Administrators only.
     
     These command is available in the Dynamic Cluster only.
     Use these command to store files in the cluster-wide Real-Time Application Environment.
     
     
     Use delete_cluster_PBX_file command to DELETE file.'''

  return _operate(sock, 'STORECLUSTERPBXFILE ' + file_name + ' DATA ' + str(file_content) + '\n')

def delete_cluster_PBX_file(sock, file_name): 
  '''The following command is available for the System Administrators only.
     
     These command is available in the Dynamic Cluster only.
     Use these command to delete files in the cluster-wide Real-Time Application Environment.'''

  return _operate(sock, 'STORECLUSTERPBXFILE ' + file_name + ' DELETE\n')

def list_stock_PBX_files(sock, language=None):
  '''The following command is available for the System Administrators only.
     
     Use these command to list files in the stock (built-in) Real-Time Application Environment.'''

  params = ''

  if language is not None:
    params += ' ' + language
       
  return _operate(sock, 'LISTSTOCKPBXFILES' + params + '\n')

def read_stock_PBX_file(sock, file_name):
  '''The following command is available for the System Administrators only.
     
     Use these command to read files in the stock (built-in) Real-Time Application Environment.'''

  return _operate(sock, 'READSTOCKPBXFILE ' + file_name + '\n')
  
#Real-Time Application Control
def start_PBX_task(sock, account_name, program_name, entry_name=None, parameter=None):
  '''The following command can be used to manage CommuniGate Pro Real-Time Application Tasks.
     
     Use this command to start a new PBX Task. The command produces an output - a string with the Task ID.
    
     account_name : string
     This parameter specifies the name of an Account.
     The Task is started on this Account behalf.
     The name can include the Domain name.
     If the Domain name is not specified, the current user Domain is used by default.
    
     program_name : string
     The name of the program (the .sppr file) to start.
    
     entry_name : string
     This optional parameter specifies the program entry point.
     If this parameter is not specified, the main entry point is used.
   
     parameter : string
     This optional parameter specifies the program parameter.The program code can retrieve it using the following code:
     Vars().startParameter'''

  params = ''
  
  if entry_name is not None:
    params += ' ENTRY ' + entry_name
  
  if parameter is not None:
    params += ' PARAM ' + parameter
       
  return _operate(sock, 'STARTPBXTASK ' + account_name + ' PROGRAM ' + program_name + params + '\n')  

def send_task_event(sock, task_ID, event_name, parameter=None): 
  '''The following command can be used to manage CommuniGate Pro Real-Time Application Tasks.
     
     Use this command to send an Event to an existing PBX Task.
   
     task_ID : string
     This parameter specifies the Task ID.
   
     event_name : string
     The name of the Event to send.
    
     parameter : object
     This optional parameter specifies the Event parameter.'''

  params = ''
  
  if parameter is not None:
    params += ' PARAM ' + parameter

  return _operate(sock, 'SENDTASKEVENT ' + task_ID + ' EVENT ' + event_name + params + '\n')


def kill_node(sock, task_ID): 
  '''The following command can be used to manage CommuniGate Pro Real-Time Application Tasks.
     
     Use this command to kill an existing PBX Task.
     
     task_ID : string
     This parameter specifies the Task ID.'''

  return _operate(sock, 'KILLNODE ' + task_ID + '\n')
    
def read_node_status(sock, task_ID): 
  '''The following command can be used to manage CommuniGate Pro Real-Time Application Tasks.
     
     Use this command to read the current application status of an existing PBX Task.
     The command produces an output - the application status object.
     
     task_ID : string
     This parameter specifies the Task ID.'''

  return _operate(sock, 'READNODESTATUS ' + task_ID + '\n')
      
#Account Services
def remove_account_subset(sock, account_name, subset_name): 
  '''Use this command to remove an Account "dataset" (such as the RepliedAddresses dataset).
     A user should be the Account owner or should have the BasicSettings Domain Administration access right to use this command.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     subset_name : string
     This parameter specifies the name of an existing data subset in the specified Account.'''

  return _operate(sock, 'REMOVEACCOUNTSUBSET ' + account_name + ' SUBSET ' + subset_name + '\n')

def dataset(sock, account_name, parameters): 
  '''Use this command to manage Account "datasets".
     The command produces an output - a dictionary with the operation results.
     A user should be the Account owner or should have the BasicSettings Domain Administration access right to use this command.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
 
     parameters : dictionary
     This dictionary should contain:
   
       subset_name
          a string element specifying the target dataset or the dataset subset
       what
          a string element specifying the operation to apply.
       Other dictionary elements are operation-specific.
 
     The following is the list of supported operations (the what values) and the additional parameters dictionary elements used for each operation:
       
       listSubsets
         this operation lists all subsets of the specified dataset.
         To list all top-level datasets in the Account, specify the an empty string as the subset_name value.
         The resulting dictionary contains the found subset names as keys and empty strings as values.
  
       createSet
         this operation creates the specified dataset.

       removeSet
         this operation removes the specified dataset.
   
       listEntries
         this operation lists subset entries.
         The resulting dictionary contains the found entry names as keys and the entry attribute name-value dictionaries as values.
       
           attribute, data
             optional string elements; they specify the name and the value of an entry attribute.
             If specified, the result includes only the entries that have the specified attribute with the specified value.
             Use the entry attribute name to filter by entry names.
       
          mode
             an optional string element; if it is absent or its value is eq, then the specified attribute should have the specified value;
             if its value is beg, then the beginning of the specified attribute value should match the specified value.
             if its value is end, then the tail of the specified attribute value should match the specified value.
             if its value is incl, then the specified attribute value should include the specified value.
       
       setEntry
         this operation creates a new entry or updates an existing entry.
       
           data
             a dictionary with the attribute name-value pairs; they are used to update an existing entry or to create a new one.
       
           entry_name
             the entry name string; if the entry with the specified name does not exist, it is created.
             If this element is absent, a unique entry name is generated.
             
           ifExists
             if this element exists, then the new entry cannot be created, and only an existing entry can be updated; if this element is absent and the specified dataset is not found, the dataset is created.
       
       deleteEntry
         this operation removes the specified entry from the specified dataset.
       
           entry_name
             the entry name string
       
       addRandomEntry
         this operation adds a new entry to the specified dataset or the dataset subset.
         A unique name is generated and assigned to this entry.
         If the operation succeeds, the resulting dictionary has the string entry_name element with the entry name generated.
   
           data
             a dictionary with the attribute name-value pairs.
             It must contain the addressbook.Email attribute.
     
           entryLimit
             an optional numeric value; if specified and positive, then the operation checks the the current number of subset entries does not exceed this limit.
      
         If the dataset already contains an entry with the same addressbook.Email attribute value, the dataset is not modified.
       
       findAddress
         this operation finds an entry with the specified addressbook.Email attribute value.
         The operation result is a dictionary.
         If an entry is found, its name is returned as the dictionary element with an empty-string name.
       
           address
             a string with an E-mail address to look for'''

  return _operate(sock, 'DATASET ' + account_name + ' ' + parameters + '\n')

def roster(sock, account_name, parameters): 
  '''Use this command to manage Account Roster.
     The command produces an output - a dictionary with the operation results.
     A user should be the Account owner or should have the BasicSettings Domain Administration access right to use this command.
     
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
     
     parameters : dictionary
     This dictionary should contain the what string element, specifying the operation to apply: List, Update, remove, Presence, probe. Other dictionary elements are operation-specific.'''

  return _operate(sock, 'ROSTER ' + account_name + ' ' + parameters + '\n')

def balance(sock, account_name, parameters): 
  '''Use this command to manage Account Billing Balances.
     The command produces an output - a dictionary with the operation results (as specified in the Billing section).
     A user should be the Account owner or should have the CanCreditAccounts Domain Administration access right to use this command.
  
     account_name : string
     This parameter specifies the name of an existing Account. The asterisk (*) symbol can be used to specify the current authenticated Account.
    
     parameters : dictionary
     This dictionary should contain the op string element, specifying the operation to apply: list, reserve, release, charge, credit, read, readAll, history, remove.
     Other dictionary elements are operation-specific, they are specified in the Billing section.'''

  return _operate(sock, 'BALANCE ' + account_name + ' ' + parameters + '\n')

#Server Settings
def list_modules(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to list all Server modules.
     The command produces an output - an array with all module names.'''

  return _operate(sock, 'LISTMODULES\n')

def get_module(sock, module_name): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to get the module settings.
     The command produces an output - a dictionary with the module settings.
     
     module_name : string
     This parameter specifies the name of a CommuniGate Pro Server module.'''

  return _operate(sock, 'GETMODULE ' + module_name + '\n')

def set_module(sock, module_name, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the module settings.
    
     module_name : string
     This parameter specifies the name of a CommuniGate Pro Server module.
    
     new_settings : dictionary
     This dictionary is used to set the module settings dictionary.'''

  return _operate(sock, 'SETMODULE ' + module_name + ' ' + parse_to_CGP_object(new_settings) + '\n')
 
def update_module(sock, module_name, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to update the module settings.
     
     module_name : string
     This parameter specifies the name of a CommuniGate Pro Server module.
    
     new_settings : dictionary
     This dictionary is used to update the module settings dictionary.
     It does not have to contain all settings data, the omitted settings will be left unmodified.'''

  return _operate(sock, 'UPDATEMODULE ' + module_name + ' ' + parse_to_CGP_object(new_settings) + '\n')

def get_queue_settings(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to get the Queue settings.
     The command produces an output - a dictionary with the Queue settings.'''

  return _operate(sock, 'GETQUEUESETTINGS\n')

def set_queue_settings(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the Queue settings.
    
     new_settings : dictionary
     This dictionary is used to set the Queue settings dictionary.'''

  return _operate(sock, 'SETQUEUESETTINGS ' + parse_to_CGP_object(new_settings) + '\n')

def get_signal_settings(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to get the Signal component settings.
     The command produces an output - a dictionary with the component settings.'''

  return _operate(sock, 'GETSIGNALSETTINGS\n')

def set_signal_settings(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the Signal component settings.
 
     new_settings : dictionary
     This dictionary is used to set the component settings dictionary.'''

  return _operate(sock, 'SETSIGNALSETTINGS ' + parse_to_CGP_object(new_settings) + '\n')
   
def get_media_server_settings(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to read the Media Server component settings.
     The command produces an output - a dictionary with the component settings.'''

  return _operate(sock, 'GETMEDIASERVERSETTINGS\n')

def set_media_server_settings(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the Media Server component settings.
   
     new_settings : dictionary
     This dictionary is used to set the component settings dictionary.'''

  return _operate(sock, 'SETMEDIASERVERSETTINGS ' + parse_to_CGP_object(new_settings) + '\n')

def get_session_settings(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to get the user Sessions settings.
     The command produces an output - a dictionary with the Sessions settings.'''

  return _operate(sock, 'GETSESSIONSETTINGS\n')

def set_session_settings(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the user Sessions settings.
  
     new_settings : dictionary
     This dictionary is used to set the Sessions settings dictionary.'''

  return _operate(sock, 'SETSESSIONSETTINGS ' + parse_to_CGP_object(new_settings) + '\n')

def get_cluster_settings(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to get the Cluster settings.
     The command produces an output - a dictionary with the Cluster settings.'''

  return _operate(sock, 'GETCLUSTERSETTINGS\n')

def set_cluster_settings(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the Cluster settings.
   
     new_settings : dictionary
     This dictionary is used to set the Cluster settings dictionary.'''

  return _operate(sock, 'SETCLUSTERSETTINGS ' + parse_to_CGP_object(new_settings) + '\n')
      
def get_log_settings(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to get the Main Log settings.
     The command produces an output - a dictionary with the Main Log settings.'''

  return _operate(sock, 'GETLOGSETTINGS\n')

def update_log_settings(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the Main Log settings.
   
     new_settings : dictionary
     This dictionary is used to update the Main Log settings dictionary.'''

  return _operate(sock, 'UPDATELOGSETTINGS ' + parse_to_CGP_object(new_settings) + '\n')

def get_network(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the Network settings.
     The command produces an output - a dictionary with the server Network settings.'''

  return _operate(sock, 'GETNETWORK\n')

def set_network(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the server Network Settings.
     
     new_settings : dictionary
     New server Network settings.'''

  return _operate(sock, 'SETNETWORK ' + parse_to_CGP_object(new_settings) + '\n')

def get_DNR_settings(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the DNR (Domain Name Resolver) settings.
     The command produces an output - a dictionary with the DNR settings.'''

  return _operate(sock, 'GETDNRSETTINGS\n')

def set_DNR_settings(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the DNR (Domain Name Resolver) settings.
     
     new_settings : dictionary
     New DNR settings.'''

  return _operate(sock, 'SETDNRSETTINGS ' + parse_to_CGP_object(new_settings) + '\n')
   
def get_banned(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the Banned Message Lines settings.
     The command produces an output - a dictionary with the server Banned Message Lines settings.'''

  return _operate(sock, 'GETBANNED\n')

def set_banned(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the server Banned Message Line Settings.
   
     new_settings : dictionary
     New server Banned settings.'''

  return _operate(sock, 'SETBANNED ' + parse_to_CGP_object(new_settings) + '\n')

def get_cluster_network(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use these commands to retrieve the Cluster-wide Network settings.'''

  return _operate(sock, 'GETCLUSTERNETWORK\n')

def set_cluster_network(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use these commands to update the Cluster-wide Network settings.'''

  return _operate(sock, 'SETCLUSTERNETWORK ' + parse_to_CGP_object(new_settings) + '\n')
 
def get_cluster_banned(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use these commands to retrieve the Cluster-wide Banned Message Lines settings.'''

  return _operate(sock, 'GETCLUSTERBANNED\n')

def set_cluster_banned(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use these commands to update the Cluster-wide Banned Message Lines settings.'''

  return _operate(sock, 'SETCLUSTERBANNED ' + parse_to_CGP_object(new_settings) + '\n')
 
def get_server_mail_rules(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to read the Server-Wide Automated Mail Processing Rules.
     The command produces an output - an array of the Server Queue Rules.'''

  return _operate(sock, 'GETSERVERMAILRULES\n')

def set_server_mail_rules(sock, new_rules): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the Server-Wide Automated Mail Processing Rules.
  
     new_rules : array
     An array of new Server Queue Rules.'''

  return _operate(sock, 'SETSERVERMAILRULES ' + parse_to_CGP_object(new_settings) + '\n')

def get_cluster_mail_rules(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use these commands to retrieve the Cluster-wide Automated Mail Processing Rules.'''

  return _operate(sock, 'GETCLUSTERMAILRULES\n')

def set_cluster_mail_rules(sock, new_rules): 
  '''A user should have the Settings Server access right to use this command.
     
     Use these commands to retrieve and update the Cluster-wide Automated Mail Processing Rules.
     
     new_rules : array
     An array of new Cluster Mail Rules.'''

  return _operate(sock, 'SETCLUSTERMAILRULES ' + parse_to_CGP_object(new_settings) + '\n')

def get_server_signal_rules(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to read the Server-Wide Automated Signal Processing Rules.
     The command produces an output - an array of the Server Signal Rules.'''

  return _operate(sock, 'GETSERVERSIGNALRULES\n')

def set_server_signal_rules(sock, new_rules): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the Server-Wide Automated Signal Processing Rules.
     
     new_rules : array
     An array of new Server Signal Rules.'''

  return _operate(sock, 'SETSERVERSIGNALRULES ' + parse_to_CGP_object(new_settings) + '\n')
    
def get_cluster_signal_rules(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to get the Cluster-Wide Automated Signal Processing Rules.
     The command produces an output - a dictionary with the Main Log settings.'''

  return _operate(sock, 'GETCLUSTERSIGNALRULES\n')

def set_cluster_signal_rules(sock, new_rules): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the Cluster-Wide Automated Signal Processing Rules.
     
     new_rules : array
     An array of new Cluster Signal Rules.'''

  return _operate(sock, 'SETCLUSTERSIGNALRULES ' + parse_to_CGP_object(new_settings) + '\n')

def get_router_table(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to read the Router Table.
     The command produces an output - a (multi-line) string with the Router Table text.'''

  return _operate(sock, 'GETROUTERTABLE\n')

def set_router_table(sock, new_table): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the Router Table.
     
     new_table : string
     A (multi-line) string containing the text of the new Router Table
     Note: multiple lines should be separated with the \e symbols.'''

  return _operate(sock, 'SETROUTERTABLE ' + new_table + '\n')

def get_cluster_router_table(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to read the Cluster Router Table.
     The command produces an output - a (multi-line) string with the Router Table text.'''

  return _operate(sock, 'GETCLUSTERROUTERTABLE\n')

def set_cluster_router_table(sock, new_table): 
  '''A user should have the Settings Server access right to use this command.
     
     new_table : string
     A (multi-line) string containing the text of the new Cluster Router Table
     Note: multiple lines should be separated with the \e symbols.'''

  return _operate(sock, 'SETCLUSTERROUTERTABLE ' + new_table + '\n')

def get_router_settings(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to read the Router settings.
     The command produces an output - a dictionary with the Router settings.'''

  return _operate(sock, 'GETROUTERSETTINGS\n')

def set_router_settings(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the Router settings.
    
     new_settings : dictionary
     A dictionary containing new Router settings.'''

  return _operate(sock, 'SETROUTERSETTINGS ' + parse_to_CGP_object(new_settings) + '\n')

def get_cluster_router_settings(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to read the Cluster Router settings.
     The command produces an output - a dictionary with the Cluster Router settings.'''

  return _operate(sock, 'GETCLUSTERROUTERSETTINGS\n')

def set_cluster_router_settings(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to set the Cluster Router settings.
    
     new_settings : dictionary
     A dictionary containing new Cluster Router settings.'''

  return _operate(sock, 'SETCLUSTERROUTERSETTINGS ' + parse_to_CGP_object(new_settings) + '\n')

def get_server_settings(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to read the Server "other" settings.
     The command produces an output - a dictionary with the Server settings.'''

  return _operate(sock, 'GETSERVERSETTINGS\n')

def update_server_settings(sock, new_settings): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to update the "other" Server settings.

     new_settings : dictionary
     A dictionary containing new Server settings.'''

  return _operate(sock, 'UPDATESERVERSETTINGS ' + parse_to_CGP_object(new_settings) + '\n')

def refresh_OS_data(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to make the Server re-read the IP data from the server OS: the set of the local IP addresses, and the set of the DNS addresses.'''

  return _operate(sock, 'REFRESHOSDATA\n')

def get_LAN_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of LAN IP Addresses.
     The command produces an output - a (multi-line) string with LAN IP addresses and address ranges.'''

  return _operate(sock, 'GETLANIPS\n')

def set_LAN_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to update the set of LAN IP Addresses.
     
     new_addresses : string
     This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of LAN IP Addresses.'''

  return _operate(sock, 'SETLANIPS ' + parse_to_CGP_object(new_addresses) + '\n')
 
def get_cluster_LAN_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of Cluster-wide LAN IP Addresses.
     The command produces an output - a (multi-line) string with Cluster-wide LAN IP addresses and address ranges'''

  return _operate(sock, 'GETCLUSTERLANIPS\n')

def set_cluster_LAN_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
  Use this command to update the set of Cluster-wide LAN IP Addresses.
  
  new_addresses : string
  This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of Cluster-wide LAN IP Addresses.'''

  return _operate(sock, 'SETCLUSTERLANIPS ' + parse_to_CGP_object(new_addresses) + '\n')

def get_client_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of Client IP Addresses.
     The command produces an output - a (multi-line) string with Client IP addresses and address ranges.'''

  return _operate(sock, 'GETCLIENTIPS\n')

def set_client_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to update the set of Client IP Addresses.
     
     new_addresses : string
     This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of Client IP Addresses.'''

  return _operate(sock, 'SETCLIENTIPS ' + parse_to_CGP_object(new_addresses) + '\n')

def get_cluster_client_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of Cluster-wide Client IP Addresses.
     The command produces an output - a (multi-line) string with Cluster-wide Client IP addresses and address ranges'''

  return _operate(sock, 'GETCLUSTERCLIENTIPS\n')

def set_cluster_client_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
  Use this command to update the set of Cluster-wide Client IP Addresses.
  
  new_addresses : string
  This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of Cluster-wide Client IP Addresses.'''

  return _operate(sock, 'SETCLUSTERCLIENTIPS ' + parse_to_CGP_object(new_addresses) + '\n')

def get_black_listed_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of Blacklisted IP Addresses.
     The command produces an output - a (multi-line) string with Blacklisted IP addresses and address ranges.'''

  return _operate(sock, 'GETBLACKLISTEDIPS\n')

def set_black_listed_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to update the set of Blacklisted IP Addresses.
     
     new_addresses : string
     This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of Blacklisted IP Addresses.'''

  return _operate(sock, 'SETBLACKLISTEDIPS ' + parse_to_CGP_object(new_addresses) + '\n')

def get_cluster_black_listed_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of Cluster-wide Blacklisted IP Addresses.
     The command produces an output - a (multi-line) string with Cluster-wide Blacklisted IP addresses and address ranges'''

  return _operate(sock, 'GETCLUSTERBLACKLISTEDIPS\n')

def set_cluster_black_listed_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
  Use this command to update the set of Cluster-wide Blacklisted IP Addresses.
  
  new_addresses : string
  This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of Cluster-wide Blacklisted IP Addresses.'''

  return _operate(sock, 'SETCLUSTERBLACKLISTEDIPS ' + parse_to_CGP_object(new_addresses) + '\n')
   
def get_white_hole_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of WhiteHole IP Addresses.
     The command produces an output - a (multi-line) string with WhiteHole IP addresses and address ranges.'''

  return _operate(sock, 'GETWHITEHOLEIPS\n')
  
def set_white_hole_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to update the set of WhiteHole IP Addresses.
     
     new_addresses : string
     This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of WhiteHole IP Addresses.'''

  return _operate(sock, 'SETWHITEHOLEIPS ' + parse_to_CGP_object(new_addresses) + '\n')
    
def get_cluster_white_hole_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of Cluster-wide WhiteHole IP Addresses.
     The command produces an output - a (multi-line) string with Cluster-wide WhiteHole IP addresses and address ranges'''

  return _operate(sock, 'GETCLUSTERWHITEHOLEIPS\n')

def set_cluster_white_hole_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
  Use this command to update the set of Cluster-wide WhiteHole IP Addresses.
  
  new_addresses : string
  This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of Cluster-wide WhiteHole IP Addresses.'''

  return _operate(sock, 'SETCLUSTERWHITEHOLEIPS ' + parse_to_CGP_object(new_addresses) + '\n')
   
def get_NATed_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of NATed IP Addresses.
     The command produces an output - a (multi-line) string with NATed IP addresses and address ranges.'''

  return _operate(sock, 'GETNATEDIPS\n')

def set_NATed_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to update the set of NATed IP Addresses.
     
     new_addresses : string
     This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of NATed IP Addresses.'''

  return _operate(sock, 'SETNATEDIPS ' + parse_to_CGP_object(new_addresses) + '\n')

def get_cluster_NATed_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of Cluster-wide NATed IP Addresses.
     The command produces an output - a (multi-line) string with Cluster-wide NATed IP addresses and address ranges'''

  return _operate(sock, 'GETCLUSTERNATEDIPS\n')

def set_cluster_NATed_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
  Use this command to update the set of Cluster-wide NATed IP Addresses.
  
  new_addresses : string
  This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of Cluster-wide NATed IP Addresses.'''

  return _operate(sock, 'SETCLUSTERNATEDIPS ' + parse_to_CGP_object(new_addresses) + '\n')
      
def get_NAT_site_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of NAT Site IP Addresses.
     The command produces an output - a (multi-line) string with NAT Site IP addresses and address ranges.'''

  return _operate(sock, 'GETNATSITEIPS\n')

def set_NAT_site_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to update the set of NAT Site IP Addresses.
     
     new_addresses : string
     This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of NAT Site IP Addresses.'''

  return _operate(sock, 'SETNATSITEIPS ' + parse_to_CGP_object(new_addresses) + '\n')
 
def get_cluster_NAT_site_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of Cluster-wide NAT Site IP Addresses.
     The command produces an output - a (multi-line) string with Cluster-wide NAT Site IP addresses and address ranges'''

  return _operate(sock, 'GETCLUSTERNATSITEIPS\n')

def set_cluster_NAT_site_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
  Use this command to update the set of Cluster-wide NAT Site IP Addresses.
  
  new_addresses : string
  This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of Cluster-wide NAT Site IP Addresses.'''

  return _operate(sock, 'SETCLUSTERNATSITEIPS ' + parse_to_CGP_object(new_addresses) + '\n')
    
def get_debug_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of Debug IP Addresses.
     The command produces an output - a (multi-line) string with Debug IP addresses and address ranges.'''

  return _operate(sock, 'GETDEBUGIPS\n')

def set_debug_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to update the set of Debug IP Addresses.
     
     new_addresses : string
     This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of Debug IP Addresses.'''

  return _operate(sock, 'SETDEBUGIPS ' + parse_to_CGP_object(new_addresses) + '\n')
 
def get_cluster_debug_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of Cluster-wide Debug IP Addresses.
     The command produces an output - a (multi-line) string with Cluster-wide Debug IP addresses and address ranges'''

  return _operate(sock, 'GETCLUSTERDEBUGIPS\n')

def set_cluster_debug_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
  Use this command to update the set of Cluster-wide Debug IP Addresses.
  
  new_addresses : string
  This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of Cluster-wide Debug IP Addresses.'''

  return _operate(sock, 'SETCLUSTERDEBUGIPS ' + parse_to_CGP_object(new_addresses) + '\n')
 
def get_denied_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of Denied IP Addresses.
     The command produces an output - a (multi-line) string with Denied IP addresses and address ranges.'''

  return _operate(sock, 'GETDENIEDIPS\n')

def set_denied_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
     Use this command to update the set of Denied IP Addresses.
     
     new_addresses : string
     This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of Denied IP Addresses.'''

  return _operate(sock, 'SETDENIEDIPS ' + parse_to_CGP_object(new_addresses) + '\n')
     
def get_cluster_denied_IPs(sock): 
  '''A user should have the Settings Server access right to use this command.
  
     Use this command to retrieve the set of Cluster-wide Denied IP Addresses.
     The command produces an output - a (multi-line) string with Cluster-wide Denied IP addresses and address ranges'''

  return _operate(sock, 'GETCLUSTERDENIEDIPS\n')

def set_cluster_denied_IPs(sock, new_addresses): 
  '''A user should have the Settings Server access right to use this command.
     
  Use this command to update the set of Cluster-wide Denied IP Addresses.
  
  new_addresses : string
  This (multi-line) string parameter contains the set of addresses and address ranges forming the new set of Cluster-wide Denied IP Addresses.'''

  return _operate(sock, 'SETCLUSTERDENIEDIPS ' + parse_to_CGP_object(new_addresses) + '\n')
 
def route(sock, address, type=None): 
  '''A user should have the Settings or User Server access right or the to use the following CLI command.
  
     Use this command to get the routing for the specified address.
  
     address : string
     This parameter specifies the E-mail address to be processed with the CommuniGate Pro Router.
    
     mail or access or signal
     This optional flag specifies the Routing type (see the Router section for more details).
     The default mode is access.
     
     This command produces an output - an array of three strings:
     
     module
       the name of the CommuniGate Pro module the address is routed to, or SYSTEM if the address is routed to a built-in destination (like NULL).
  
     host
       the object/queue handled by the specified module: an Internet domain name for the SMTP module, a local Account name for the Local Delivery module, etc.
   
     address
       the address inside the queue (E-mail address for SMTP, Real-To: address for Local Delivery, etc.)'''

  params = ''
  
  if type is not None:
    if type in ['mail', 'access', 'signal']:
      params += ' ' + type
    else:
      raise ValueError("Value is out of list")

  return _operate(sock, 'ROUTE ' + address + params + '\n')

def get_IP_state(sock, ip_address, temp=False): 
  '''A user should have the Settings or User Server access right or the to use the following CLI command.
  
     Use this command to get the type assigned to the specified address.
     The command produces an output - a string with the IP address type.
     If the TEMP keyword is specified, the temporary Client IP Addresses set is checked.

     ip_address : string
     This parameter specifies the IP Address to check.'''

  params = ''
  
  if temp:
      params += ' TEMP'

  return _operate(sock, 'GETIPSTATE ' + address + params + '\n')

def get_server_intercept(sock): 
  '''A user should have the Master Server access right to use the following CLI command.
  
     Use this command to read the Lawful Intercept settings.
     The command produces an output - a dictionary with the Intercept settings.'''

  return _operate(sock, 'GETSERVERINTERCEPT\n')

def set_server_intercept(sock, new_settings): 
  '''A user should have the Master Server access right to use the following CLI command.
     
     Use this command to set the Lawful Intercept settings.
   
     new_settings : dictionary
     A dictionary containing new Intercept settings.'''

  return _operate(sock, 'SETSERVERINTERCEPT ' + parse_to_CGP_object(new_addresses) + '\n')
 
def get_cluster_intercept(sock): 
  '''A user should have the Master Server access right to use the following CLI command.
  
     Use this command to read the Cluster-Wide Lawful Intercept settings.
     The command produces an output - a dictionary with the Cluster-Wide Intercept settings.'''

  return _operate(sock, 'GETCLUSTERINTERCEPT\n')

def set_cluster_intercept(sock, new_settings): 
  '''A user should have the Master Server access right to use the following CLI command.
     
     Use this command to set the Cluster-Wide Lawful Intercept settings.
   
     new_settings : dictionary
     A dictionary containing new Cluster-Wide Intercept settings.'''

  return _operate(sock, 'SETCLUSTERINTERCEPT ' + parse_to_CGP_object(new_addresses) + '\n')

#Monitoring    
def get_stat_element(sock, object_ID): 
  '''A user should have the Monitoring Server access right to use the Server Monitoring CLI command.
  
     Use this command to retrieve the current value of a Server statistics (SNMP) element.
     
     object_ID : string
     The object ID of the Server statistics element (see the Statistics section for more details).
     
     This command produces an output - a number, string, or other object with the Server statistics element value.'''

  return _operate(sock, 'GETSTATELEMENT ' + object_ID + '\n')

def set_stat_element(sock, object_ID, set_value, type=None):
  '''A user should have the Monitoring Server access right to use the Server Monitoring CLI command.
     
     Use this command to update the current value of a Server statistics (SNMP) element.
     Only the "Custom" elements can be updated.
     
     object_ID : string
     The object ID of the Server statistics element (see the Statistics section for more details).
   
     type : [ INC | SET ]
     
     set_value : string
     if the INC keyword is used, this value is added to the Element value, if the SET keyword is used, this value is assigned to the Element.'''

  params = ''
  
  if type is not None:
    if type in ['INC', 'SET']:
      params += type
    else:
      raise ValueError("Value is out of list")
  
  return _operate(sock, 'SETSTATELEMENT ' + object_ID + params + ' ' + set_value + '\n')
   
def get_next_stat_name(sock, object_ID): 
  '''A user should have the Monitoring Server access right to use the Server Monitoring CLI command.
  
     Use this command to enumerate available Server statistics (SNMP) elements.
   
     object_ID : string
     An empty string or the object ID of the already found Server statistics element (see the Statistics section for more details).
    
     This command produces an output - a string with the object_ID of the next statistics element.
     If the object_ID parameter is an empty string, the object_ID of the first available Server statistics element is returned.
     If a statistics element for the specified object_ID is not found, or if the found element is the last available one, the command returns an error.'''

  return _operate(sock, 'GETNEXTSTATNAME ' + object_ID + '\n')
  
def get_dialog_info(sock, dialog_ID): 
  '''A user should have the Monitoring Server access right to use the Server Monitoring CLI command.
  
     Use this command to retrieve the information about a Signal Dialog object.
    
     dialog_ID : string
     The Dialog ID.
     
     This command produces an output - a dictionary with the Dialog status data.'''

  return _operate(sock, 'GETDIALOGINFO ' + dialog_ID + '\n')

def shutdown(sock): 
  '''A user should have the Monitoring Server access right to use the Server Monitoring CLI command.
     
     Use this command to stop the CommuniGate Pro Server.'''

  return _operate(sock, 'SHUTDOWN\n')

#Statistics      
def get_account_stat(sock, account_name, key_name=None): 
  '''Use this command to retrieve statistics data about the specified Account.
   
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.
    
     key_name : string
     This optional parameter specifies the name of the statistical entry to retrieve.
    
     This command produces an output - a number or a time_stamp with the specified statistical information, or (if the KEY keyword and the key_name parameter are not specified) a dictionary with all available statistical data.
     If the statistical data for the specified key does not exist, an empty string is returned.
     To use this command, the user should have the Domain Administration right for the target Account Domain.
     All users can retrieve the Account statistics data for their own accounts.'''

  params = ''
  
  if key_name is not None:
    params += ' KEY ' + key_name

  return _operate(sock, 'GETACCOUNTSTAT ' + account_name + params + '\n')

def reset_account_stat(sock, account_name, key_name=None): 
  '''Use this command to reset statistics data about the specified Account.
  
     account_name : string
     This parameter specifies the name of an existing Account.
     The asterisk (*) symbol can be used to specify the current authenticated Account.

     key_name : string
     This optional parameter specifies the name of the statistical entry to reset.
    
     If the KEY keyword and the key_name parameter are not specified, all Account statistical entries are reset.
     To use this command, the user should have the "Basic Settings" Domain Administration right for the target Account Domain.
    
     The following Account statistics data keys are implemented:
     
     Key Name	  	Value
     StatReset	 	The date & time when the last parameterless RESETACCOUNTSTAT command was sent to this Account
     MessagesReceived	The total number of messages delivered to the Account
     BytesReceived	The total size of all messages delivered to the Account
     MessagesSent	The total number of messages sent on the Account behalf
     BytesSent	 	The total size of all messages sent on the Account behalf
     CallsReceived	The total number of calls received for the Account
     CallsSent	 	The total number of calls placed on the Account behalf
     Logins	 	The total number of successful Account authentications'''
  
  params = ''
    
  if key_name is not None:
    params += ' KEY ' + key_name  

  return _operate(sock, 'RESETACCOUNTSTAT '+ account_name + params + '\n')

def get_domain_stat(sock, domain_name, key_name=None): 
  '''Use this command to retrieve statistics data about the specified Domain.
     
     domain_name : string
     This parameter specifies the name of an existing Domain.
     The asterisk (*) symbol can be used to specify the Domain of the current authenticated Account.
     
     key_name : string
     This optional parameter specifies the name of the statistical entry to retrieve.
     
     This command produces an output - a string with the specified statistical information, or (if the KEY keyword and the key_name parameter are not specified) a dictionary with all available statistical data.
     To use this command, the user should have the Domain Administration right for the target Domain.'''

  params = ''
  
  if key_name is not None:
    params += ' KEY ' + key_name

  return _operate(sock, 'GETDOMAINSTAT ' + domain_name + params + '\n')

def reset_domain_stat(sock, domain_name, key_name=None): 
  '''Use this command to reset statistics data about the specified Domain.
     
     domain_name : string
     This parameter specifies the name of an existing Domain.
     The asterisk (*) symbol can be used to specify the Domain of the current authenticated Account.
     
     key_name : string
     This optional parameter specifies the name of the statistical entry to reset.
   
     If the KEY keyword and the key_name parameter are not specified, all Domain statistical entries are reset.
     To use this command, the user should have the "Basic Settings" Domain Administration right for the target Domain.
   
     The following Domain statistics data keys are implemented:
     
     Key Name	  	Value
     StatReset	 	The date & time when the last parameterless RESETDOMAINSTAT command was sent to this Domains
     MessagesReceived	The total number of messages delivered to the Domain Accounts
     BytesReceived	The total size of all messages delivered to the Domain Accounts
     MessagesSent	The total number of messages sent on the Domain Accounts behalf
     BytesSent	 	The total size of all messages sent on the Domain Accounts behalf
     CallsReceived	The total number of calls received by the Domain Accounts
     CallsSent	 	The total number of calls placed on the Domain Accounts behalf'''

  params = ''

  if key_name is not None:
    params += ' KEY ' + key_name
  
  return _operate(sock, 'RESETDOMAINSTAT ' + domain_name + params + '\n')

#Directory Administration
def list_directory_units(sock, shared=False): 
  '''A user should have the Directory Server access right to use the Directory Administration CLI command.
     
     Use this command to retrieve the list of all Directory units created.
     If the SHARED keyword is used, the cluster-wide Units are listed.
     
     This command produces an output - a dictionary, where the keys are Directory Unit mount points, and the values are Directory Unit names.'''

  params = ''

  if shared:
    params += ' SHARED'

  return _operate(sock, 'LISTDIRECTORYUNITS' + params + '\n')

def create_directory_unit(sock, unit_name, mount_point, shared=False, remote=False): 
  '''A user should have the Directory Server access right to use the Directory Administration CLI command.
     
     Use this command to create a new Directory Unit.
     
     unit_name : string
     This parameter specifies the new Unit name.
     
     mount_point : string
     This parameter specifies the new Unit mount point (mount DN).
     
     If the SHARED keyword is used, a cluster-wide Directory Unit is created.
     If the REMOTE keyword is used, a Remote (LDAP-based) Directory Unit is created, otherwise a Local (File-based) Directory Unit is created.'''

  params =''

  if shared:
    params += ' SHARED'
    
  if remote:
    params += ' REMOTE'

  return _operate(sock, 'CREATEDIRECTORYUNIT ' + unit_name + params + ' ' + mount_point + '\n')

def relocate_directory_unit(sock, unit_name, mount_point, shared=False): 
  '''A user should have the Directory Server access right to use the Directory Administration CLI command.
     
     Use this command to re-mount an existing Directory Unit on a different mount point.
   
     unit_name : string
     This parameter specifies the Directory Unit name.
     If the SHARED keyword is used, this is a cluster-wide Directory Unit name.
   
     mount_point : string
     This parameter specifies the new mount point (mount DN).'''

  params = ''

  if shared:
    params += ' SHARED'

  return _operate(sock, 'RELOCATEDIRECTORYUNIT ' + unit_name + params + ' ' + mount_point + '\n')

def delete_directory_unit(sock, unit_name, shared=False): 
  '''A user should have the Directory Server access right to use the Directory Administration CLI command.
     
     Use this command to remove an existing Directory Unit.
    
     unit_name : string
     This parameter specifies the Directory Unit name.
     If the SHARED keyword is used, this is a cluster-wide Directory Unit name.'''

  params = ''

  if shared:
    params += ' SHARED'

  return _operate(sock, 'DELETEDIRECTORYUNIT ' + unit_name + params + '\n')

def get_directory_unit(sock, unit_name, shared=False): 
  '''A user should have the Directory Server access right to use the Directory Administration CLI command.
     
     Use this command to retrieve the Directory Unit settings.
   
     unit_name : string
     This parameter specifies the Directory Unit name.
     If the SHARED keyword is used, this is a cluster-wide Directory Unit name.'''

  params = ''

  if shared:
    params += ' SHARED'

  return _operate(sock, 'GETDIRECTORYUNIT ' + unit_name + params + '\n')

def set_directory_unit(sock, unit_name, new_settings, shared=False): 
  '''A user should have the Directory Server access right to use the Directory Administration CLI command.
     
     Use this command to change the Directory Unit settings.
     
     unit_name : string
     This parameter specifies the Directory Unit name. If the SHARED keyword is used, this is a cluster-wide Directory Unit name.
   
     new_settings : dictionary
     This parameter specifies the new Directory Unit settings.'''

  params = ''

  if shared:
    params += ' SHARED'

  return _operate(sock, 'SETDIRECTORYUNIT ' + unit_name + params + ' ' + parse_to_CGP_object(new_settings) + '\n')

def get_directory_access_rights(sock, shared=False): 
  '''A user should have the Directory Server access right to use the Directory Administration CLI command.
     
     Use this command to retrieve the Directory Access Rights.
     If the SHARED keyword is used, the cluster-wide Access Rights are retrieved.
     This command produces an output - an array of Access Rights elements.'''

  params = ''

  if shared:
    params += ' SHARED'

  return _operate(sock, 'GETDIRECTORYACCESSRIGHTS' + params + '\n')

def set_directory_access_rights(sock, newAccessRights, shared=False): 
  '''A user should have the Directory Server access right to use the Directory Administration CLI command.
     
     Use this command to set the Directory Access Rights.
     If the SHARED keyword is used, the cluster-wide Access Rights are set.
     
     newAccessRights : array
     This parameter specifies the new Directory Access Rights.'''

  params = ''

  if shared:
    params = 'SHARED '

  return _operate(sock, 'SETDIRECTORYACCESSRIGHTS ' + params + parse_to_CGP_object(newAccessRights) + '\n')

#Miscellaneous Commands
def list_CLI_commands(sock): 
  '''Use this command to retrieve the list of all CLI commands supported by this version of CommuniGate Pro Server.
     This command produces an output - an array of strings, where each string is a supported command name.'''

  return _operate(sock, 'LISTCLICOMMANDS\n')

def noop(sock): 
  '''This command always completes successfully.'''

  return _operate(sock, 'NOOP\n')
  
def echo(sock, CGPobject): 
  '''This command produces an output - an object, which is the command parameter copy.'''

  return _operate(sock, 'ECHO ' + parse_to_CGP_object(CGPobject) + '\n')

def get_version(sock): 
  '''This command produces an output - a string with this CommuniGate Pro Server version.'''

  return _operate(sock, 'GETVERSION\n')

def get_system_info(sock, what): 
  '''This command produces an output - an object returned by the CG/PL SystemInfo function called with the what parameter.
     If that function returns a null-object, this command returns an error.
     
     what : string'''

  return _operate(sock, 'GETSYSTEMINFO ' + what + '\n')

def get_current_time(sock, what): 
  '''This command produces an output - a timestamp with this CommuniGate Pro Server internal timer value.'''

  return _operate(sock, 'GETCURRENTTIME\n')

def set_log_all(sock, mode): 
  '''Use this command to switch on and off the "Log Everything" mode (this mode can also be enabled by using the --LogAll command line option.
     To use this command, the user should have the "Can Monitor" Server Administration right.
     
     mode : [ ON | OFF ]'''

  return _operate(sock, 'SETLOGALL ' + mode + '\n')

def dump_all_objects(sock): 
  '''Use this command to write the list of all application data objects into the OS syslog.
     Note: this list may contain millions of objects, and this command can easily overload the OS syslog facilities.
     It also blocks object creation and releasing functionality, effectively suspending CommuniGate Pro Server activities till all objects are listed.
     To use this command, the user should have the "Can Monitor" Server Administration right.'''

  return _operate(sock, 'DUMPALLOBJECTS\n')

def test_loop(sock, seconds): 
  '''Use this command to test the server CPU load.
     The command executes some calculation loop for the specified number of seconds.
     This command produces an output - a number that indicates the average CLI thread CPU performance (the number of times the test loop was executed divided by the test time).
     To use this command, the user should have the "Can Monitor" Server Administration right.
     
     seconds : int'''

  return _operate(sock, 'TESTLOOP' + str(seconds) + '\n')

def set_trace(sock, facility, mode): 
  '''To use this command, the user should have the "Can Monitor" Server Administration right
     
     Use this command to switch on and off internal logging facitilies that write to OS syslog.
     The facility parameter should be a string with one of the folloing supported values:
     
     FileIO
     record all file read/write/truncate operations
    
     FileOp
     record all file create/rename/remove operations
     
     mode : [ ON | OFF ]'''

  return _operate(sock, 'SETTRACE ' + facility + ' ' + mode + '\n')

def write_log(sock, log_level, log_record): 
  '''Use this command to store a record into the Server Log.
     
     log_level : int
     This parameter specifies the record log level.
     
     log_record : string
     This parameter specifies the string to be placed into the Server Log.
     
     Log records generated with this command have the SYSTEM prefix.
     To use this command, the user should have the "Can Monitor" Server Administration right.'''

  return _operate(sock, 'WRITELOG ' + log_level + ' ' + log_record + '\n')

def release_SMTP_queue(sock, queue_name): 
  '''Use this command to release an SMTP queue.
     
     queue_name : string
     This parameter specifies the queue (domain) name to release.
     
     In a Dynamic Cluster environment this command releases the specified SMTP queue on all servers.
     To use this command, the user should have the "Can Monitor" Server Administration right.'''

  return _operate(sock, 'RELEASESMTPQUEUE ' + queue_name + '\n')

def reject_queue_message(sock, message_ID, errorText=None): 
  '''Use this command to reject a message from the Server Queue.
     
     message_ID : int
     This parameter specifies the message ID.

     errorText : string
     This optional parameter specifies the text to be included into the error report (bounce) sent to the message sender.
     If this parameter is NONDN, no DSN report message is generated.'''

  params = ''

  if errorText is not None:
    params += ' REPORT ' + errorText

  return _operate(sock, 'REJECTQUEUEMESSAGE ' + message_ID + params + '\n')

def reject_queue_messages(sock, authed_sender, errorText=None): 
  '''Use this command to reject all messages sent by the specified sender from the Server Queue.
     
     authed_sender : string
     This parameter specifies the authenticated sender's name.

     errorText : string
     This optional parameter specifies the text to be included into the error report (bounce) sent to the message sender.
     If this parameter is NONDN, no DSN report message is generated.
     
     In a Dynamic Cluster environment this command rejects messages from all server queues.
     To use this command, the user should have the "Can Reject Queues" Server Administration right.'''

  params = ''

  if errorText is not None:
    params += ' REPORT ' + errorText

  return _operate(sock, 'REJECTQUEUEMESSAGES SENDER ' + authed_sender + params + '\n')

def get_message_queue_info(sock, module_name, queue_name): 
  '''Use this command to read information about a module message Queue.
     
     module_name : string
     This parameter specifies the module name.
   
     queue_name : string
     This parameter specifies the module queue name.
  
     This command produces an output - a dictionary with the specified queue information.
     If the module does not have the specified queue, the dictionary is empty.
     Otherwise it contains the following elements:
     
     nTotal
       a number - the total number of messages in the queue
  
     size
       a number - the total size of all messages in the queue
  
     delayedTill
       (optional) a timestamp - the effective release time for this queue
   
     lastError
       (optional) a string with the last problem report'''

  return _operate(sock, 'GETMESSAGEQUEUEINFO ' + module_name + ' QUEUE ' + queue_name + '\n')

def get_current_controller(sock, module_name, queue_name): 
  '''Use this command to get the IP address of the current Dynamic Cluster Controller.
     This command produces an output - a string with the Cluster Controller IP Address.
     To use this command, the user should have the "Can Monitor" Server Administration right.'''

  return _operate(sock, 'GETCURRENTCONTROLLER\n')

def reconnect_cluster_admin(sock): 
  '''Use this command to force a Dynamic Cluster member to re-open all its inter-cluster Administrative connections, and (for a non-controller member) to re-open its Administrative connection to the Controller.'''

  return _operate(sock, 'RECONNECTCLUSTERADMIN\n')

def get_temp_client_IPs(sock): 
  '''Use this command to retrieve the set of temporary Client IP Addresses.
     The command produces an output - a string with Temporary Client IP addresses separated with the comma (,) symbols.
     To use this command, the user should have the "Can Monitor" Server Administration right.'''

  return _operate(sock, 'GETTEMPCLIENTIPS\n')

def report_failed_login_adress(sock, address, errorText=None): 
  '''Use this command to increment the counter of failed Login attempts from the specified IP address used in the Temporarily Blocked Addresses functionality.
     
     address : string
     The Network IP Address to report.
     
     To use this command, the user should have the "Server Settings" Server Administration right.'''

  params = ''

  if errorText is not None:
    params += ' REPORT ' + errorText

  return _operate(sock, 'REPORTFAILEDLOGINADDRESS ' + address + '\n')
    
def temp_blacklist_IP(sock, address, seconds): 
  '''Use this command to add an address to the Temporary Blacklisted IP Addresses set.
     
     address : string
     The Network IP Address to add.

     seconds : int
     The time period the address should be blacklisted for.

     Specify zero time period to remove the address from the Temporary Blacklisted IP Addresses set.'''

  if seconds == 0:
    seconds = ' DELETE'
  
  else:
    seconds = ' TIMEOUT ' + str(seconds)

  return _operate(sock, 'TEMPBLACKLISTIP ' + address + seconds + '\n')
     
def get_temp_blacklisted_IPs(sock): 
  '''Use this command to retrieve the set of Temporary Blacklisted IP Addresses.
     The command produces an output - a string with Temporary Blacklisted IP addresses separated with the comma (,) symbols.
     Each IP address may have a -nnnn suffix, where nnnn is either the number of seconds this address will remain blacklisted for, or the * symbol indicating permanent address blacklisting.
     To use this command, the user should have the "Can Monitor" Server Administration right.'''

  return _operate(sock, 'GETTEMPBLACKLISTEDIPS\n')

def set_temp_blacklisted_IPs(sock, addresses): 
  '''Use this command to add addresses to the Temporary Blacklisted IP Addresses list.
    
     addresses : string
     A string with a list of IP addresses, using the output format of the GetTempBlacklistedIPs command.
    
     To use this command, the user should have the "Server Settings" Server Administration right.'''

  return _operate(sock, 'SETTEMPBLACKLISTEDIPS ' + addresses + '\n')