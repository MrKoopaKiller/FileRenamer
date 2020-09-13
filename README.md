# FileRenamer

Rename file extension from `.txt` to `.cvs` recursively into the user specified directory and send an email with the list of the renamed files.

## About

**FileRenamer** will rename all file extensions from `.txt` to `.cvs` from the user specified directory. After renamed all files, an email is sent with a list of all modified files.

The destination path and smtp settings are specified by `environment variables`. See details below.

## How to use

The docker volume and environment variables must be used in `docker run` command:

```
docker run -v /myfiles/data:/data \
  --env DEST_PATH=/data \
  --env SMTP_SERVER=smtp.gmail.com \
  --env SMTP_PORT=587 \
  --env SMTP_USER=mymail@gmail.com \
  --env SMTP_PASSWORD=<BASE64_ENCODED_PASSWORD> \
  --env EMAIL_TO=mr.boss@gmail.com \
  rabeloo/file-renamer:latest
```

Also, the `env.list` file could be used, just run:

```
docker run --env-file env.list -v /myfiles/data:/data rabeloo/file-renamer:latest
```

### Building image
In order to build your custom image, just clone this repository and execute `docker build` command:

``` 
$ git clone https://github.com/MrKoopaKiller/FileRenamer.git
$ cd FileRenamer

$ docker build -t file-renamer:latest .
``` 

## Variables
| Variable | Content | Example
|---|:---:| :---: |
| `SMTP_SERVER`  | SMTP server | `smtp.gmail.com` 
| `SMTP_PORT`  | SMTP server port |`587`  |
| `SMTP_USER`  | SMTP server user | `mymail@gmail.com` |
| `SMTP_PASSWORD`  | SMTP server password **encoded in base64**. Details below. | `TXlTM2NyZXRQQHNzd29yZA==`
| `EMAIL_TO`  | Email address to send the list of the files renamed | `mr.boss@gmail.com`  |

### Base64 enconded variable

To correctly encode the password to set in `SMTP_PASSWORD` use the following command:

**Linux:**
```
echo -ne '<YOUR_PASSWORD>' | base64
```

**Windows:**
```
powershell "[convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes(\"<YOUR_PASSWORD>\"))"
```

**Online:**
https://www.base64encode.net