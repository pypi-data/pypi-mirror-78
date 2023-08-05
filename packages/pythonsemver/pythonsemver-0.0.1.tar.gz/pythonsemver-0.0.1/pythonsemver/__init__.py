import urllib.parse
import re
import logging
from distutils.version import LooseVersion

def symentric_version_redirection(versions_list,uri_requested):
  version_list_sort = sorted(versions_list, key=LooseVersion)
  uri_requested = urllib.parse.unquote(uri_requested)
  regex_match_1 = '^(~\d.*)'
  regex_match_2 = '^([ ^].*)'
  regex_match_3 = '^[*].*'
  matcher_flag = False
  patch_version = []
  minor_version = []
  major_version = []
  for i in version_list_sort:
    split_data = i.split('.')
    patch_version.append(int(split_data[2]))
    minor_version.append(int(split_data[1]))
    major_version.append(int(split_data[0]))

  logging.info('MajorVersion: '.join(map(str, major_version)))
  logging.info('MinorVersion: '.join(map(str, minor_version)))
  logging.info('PatchVersion: '.join(map(str, patch_version)))

  dot_count = len(re.findall('[.]', uri_requested))
  # print(uri_requested[len(uri_requested)-1])
  if dot_count == len(uri_requested):
    return "404-Found"
  if dot_count == 0 and not re.match(regex_match_3, uri_requested) and not uri_requested.isnumeric():
    return "404-Found"
  if not re.match(regex_match_3, uri_requested):
    if re.match(regex_match_1, uri_requested) or re.match(regex_match_2, uri_requested):
      if dot_count == 1 and uri_requested[len(uri_requested)-1] !='.':
        uri_requested = uri_requested+'.0'
      elif dot_count == 0:
        uri_requested = uri_requested+'.0.0'
      else:
        uri_requested = uri_requested+'0.0'
    elif dot_count == 1:
      uri_requested = '~'+uri_requested+'.0'
    elif dot_count == 0:
      uri_requested = '^'+uri_requested+'.0.0'

  split_uri_requested = uri_requested[1:len(uri_requested):1].split('.')
  ##--------------------------------------------------
  # Exit function when there is uri requested without any special characters
  if split_uri_requested[0] == '' and not re.match(regex_match_3, uri_requested):
    logging.info("Exact Version Requested")
    return uri_requested
  ##--------------------------------------------------
  # Exit function when there is uri requested without any special characters
  if re.match(regex_match_3, uri_requested):
    matcher_flag = True
    return_result = version_list_sort[len(version_list_sort)-1]
    logging.info("Asterisk Condition")
    return return_result

  try:
    major_uri_version = int(split_uri_requested[0])
    minor_uri_version = int(split_uri_requested[1])
    patch_uri_version = int(split_uri_requested[2])
  except:
    return "404-Found"
    logging.info("Exception")
  # print(major_version)

  if re.match(regex_match_1, uri_requested):
    matcher_flag = True
    major_count=0
    minor_count=0
    for i in range(len(major_version)):
      if major_version[i] == major_uri_version:
        major_count=i+1
    # print(major_count)
    for i in range(major_count):
      # print(i)
      if minor_version[i]==minor_uri_version:
        minor_count=i
    # print(minor_count)
    if major_count>1 and minor_count==0:
      return_result = 'No Patch version found'
    else:
      logging.info("Tilde Condition")
      return_result = str(major_version[minor_count])+"."+str(minor_version[minor_count])+"."+str(patch_version[minor_count])


  if re.match(regex_match_2, uri_requested):
    matcher_flag = True
    major_count=0
    for i in range(len(major_version)):
      if major_version[i]==major_uri_version:
        major_count=i
    logging.info("Caret Condition")
    return_result = str(major_version[major_count])+"."+str(minor_version[major_count])+"."+str(patch_version[major_count])
    # print(major_count)

  return return_result
