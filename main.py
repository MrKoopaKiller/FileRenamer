import smtplib, ssl, sys
from pathlib import Path
from os import getenv as env
from datetime import datetime
from base64 import b64decode
from socket import gaierror

# Function get_data:
#   Return a string of the current data and time.
#   Format: dd/mm/aaaa hh:mm:ss
#
def get_data():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

# Function rename_files:
#   Rename the file extesion recursively from the path given in 'DATA_PATH'.
#   Return a list with all modified files
#
def rename_files():
  try:
    dest_dir = Path(env('DEST_PATH'))
  except TypeError:
    sys.exit(get_data() + " ERROR: DATA_PATH variable is empty")

  new_ext = env('NEW_EXT')
  old_ext = env('OLD_EXT')

  if not old_ext:
    sys.exit(get_data() + " ERROR: OLD_EXT variable is empty")
  if not new_ext:
    sys.exit(get_data() + " ERROR: NEW_EXT variable is empty")

  files = dest_dir.glob("**/*." + old_ext)
  renamed_files=[]
  for f in files:
      p = Path(f)
      newf = p.rename(p.with_suffix("." + new_ext))
      renamed_files.append(newf)
  if not renamed_files:
      sys.exit(get_data() + " INFO: No files to rename")
  else:
    return renamed_files

# Function gen_message:
#   Generate a formatted message with the list of renamed files
#   Return a string with data and all renamed files
#
def gen_message(renamed_files):
  DATA=get_data()
  log_message = """\
{DATA} INFO: Files renamed:
{0}
"""
  arr=[]
  for file in renamed_files:
      arr.append('{0}'.format(file))
  log_message = log_message.format('\n'.join(arr),DATA=DATA)

  sys.stdout.write(log_message)
  return(log_message)

# Function send_email:
#   Send an email with all renamed files.
#   Uses SMTP credentials given in environment variables.
#   Receive a list of all renamed files.
#
def send_email(log_message):
  msg = log_message
  smtp_port    = env('SMTP_PORT')
  smtp_server  = env('SMTP_SERVER')
  smtp_user    = env('SMTP_USER')
  email_dest   = env('EMAIL_TO')
  try:
    smtp_passwd  = b64decode(env('SMTP_PASSWORD')).decode('ascii')
  except TypeError:
    sys.exit(get_data() + " ERROR: Failed to send email. Invalid value for SMTP_PASSWORD")

  message = """\
To: me <{TO}>
Subject: [FileRenamer] Files renamed

"""
  message = message + msg.format(TO=email_dest)
  try:
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as mail:
        mail.starttls(context=context)
        mail.login(smtp_user, smtp_passwd)
        mail.sendmail(smtp_user, email_dest, message)
  except smtplib.SMTPAuthenticationError:
    sys.exit(get_data() + " ERROR: Failed to send email. Authentication failed")
  except gaierror:
    sys.exit(get_data() + " ERROR: Failed to send email. Invalid SMTP settings")
  except TimeoutError:
    sys.exit(get_data() + " ERROR: Failed to send email. Timeout - connection failed")

  sys.stdout.write(get_data() + " INFO: Mail sent")
# Function __main__:
# Call other functions
def __main__():
    res = rename_files()
    msg = gen_message(res)
    send_email(msg)

# Call function __main__
__main__()