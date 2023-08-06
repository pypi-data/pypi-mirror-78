# Swimlane Platform

## Install

### Prerequisites

See [the Linux Swimlane Installation end user documentation](https://swimlane.com/knowledge-center/install/Swimlane_Installation/Linux_Swimlane_Installation/) for prerequisite information and installation instructions.

### Install online master package

Run `pip install swimlane-platform --upgrade`

### Install the offline master package

The offline master package must be downloaded first from TBD.

You must then unpack it to the folder of your choice with `tar -xvf /path/to/swimlane-platform.tar.bz2`

Change to the user you want to run everything under.

After above step is completed switch to that folder and run `pip install --user swimlane-platform-*.whl --no-index --find-links .`

Two more images is bundled in the file, they are used in docker-compose
override file. They are not expanded by default and if overide
file is use, you need to load them manually `docker load override-images.tgz`

## Run

You can execute master script by running `swimlane-platform`.

### Hidden Switches.

`--dev` - if you want to run from developers distributions.

`--turbine_enable` - if you want to enable turbine task engine.

## After install

### Optional Add-on services

By default, optional services such as the Syslog Receiver and Selenium Chrome are commented out in the `docker-compose.override.yml`. You will need to uncomment the service (and it's corresponding volume if applicable), and then run `docker-compose up -d` to run Swimlane with the additional services enabled.

#### Workspace volume

The workspace volume can be utilized by commenting out the `volumes` key on the tasks container in the `docker-compose.override.yml`. Specify the path to a local directory on the host that contains files you wish to share with the tasks service.

Example:

```yaml
sw_tasks:
  volumes:
    - /opt/swimlane/workspace:/app/workspace
```

#### Third party certificates volume

The third party certificates volume can be utilized by commenting out the `volumes` key on the api and tasks containers in `docker-compose.override.yml`. Specify the path to a local directory on the host that contains files you wish to share with the tasks service. On each start of the api and tasks services `update-ca-certificates` will be run to import the certificates. The api and tasks containers need to be restarted for the changes to take affect if new certs are added.

Example:

```yaml
sw_api:
  volumes:
    - /opt/swimlane/ca-certs/:/usr/local/share/ca-certificates/swimlane/
sw_tasks:
  volumes:
    - /opt/swimlane/ca-certs/:/usr/local/share/ca-certificates/swimlane/
```

## Local Build and Install

To build the package locally (from the top level directory of this repo): `python setup.py build sdist bdist_wheel clean`

To install the built package: `pip install ./dist/swimlane_platform-<version>.tar.gz --user --force-reinstall`
