## Lassi - Basic Configuration Management Tool

### Setup

Lassi is built as a python module. It requires some build time dependencies to be installed.

#### Ubuntu

1. Run bootstrap.sh
  >```
  > $ bash bootstrap.sh
  >```

2. Install the python module
  >```
  > $ sudo python setup.py install
  >```

3. Copy the example configuration file (lassi.config.example) to `/etc/lassi.config`. This contains the host list along with the changes that needs to be pushed for each host.

4. You can run the tool now
  >```
  > $ lassi
  >```

  It will read the /etc/lassi.config file and configure each of the server one by one.

#### OSX

Didn't test on OSX but once the dependencies specified in bootstrap.sh are installed via homebrew, things should work fine.


### Configuration Syntax

The configuration file is a JSON file which specifies the packages, services and files needs to be available on the host.

#### Package resource

```
"package": [
  {
    "name": "apache2",
    "ensure": "absent"
  },
  {
    "name": "php-fpm",
    "ensure": "present"
    "notify": ["apache2"]
  }
]
```

Default value of `ensure` is `present`

`notify` will reload those services whenever that package is installed
#### Service resource

```
"service": ["apache2"]
```

This ensures that services are started

#### File resource

```
"file": [
  {
    "source": "/tmp/testphp.php",
    "destination": "/var/www/html/testphp.php",
    "owner": "www-data",
    "group": "www-data",
    "permissions": "0755",
    "notify": ["apache2"]
  }
]
```

`source` is the path in the local filesystem
`destination` is the path in the remote filesystem
`owner` is the file owner
`group` is the file group owner
`permissions` is the file permissions
`notify` will reload the services whenever the file content changes
