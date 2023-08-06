import collections
import docker
import json
from docker import errors, types
from utilities import SingletonMeta

from .exceptions import *

RepoTag = collections.namedtuple("RepoTag", 'repo tag')


class DockerWrapper(metaclass=SingletonMeta):
    """
    Wrapper class for Docker SDKs
    """

    def __init__(self) -> None:
        self.docker_client = None
        self.dcli = None
        self.containers = []
        try:
            self.docker_client = docker.from_env()
            self.dcli = self.docker_client.api
        except Exception as e:
            raise ConfigError("Unable to initialize docker_client", e)

    def create_container(self, container_config) -> {}:
        """
        Create a Docker container based on input parameters
        :param container_config: all information needed to create a new docker container
        :return: dict
        """
        cont_id = None  # Id of new created container

        # default container resource limits & other configuration
        defaults = {
            'mem_limit': None,
            'memswap_limit': None,
            'publish_all_ports': True,
            'ipc_mode': None,
            'devices': [],
            'cap_add': []
        }

        # check image for existence
        cont_image = self.get_image_repo_tag(container_config['image'])

        if not self._image_pulled(cont_image.repo, cont_image.tag):
            raise ContainerError("Cannot create container {}. Image {} not found.".format(
                container_config['container'], container_config['image']), None)

        # get entrypoint from image if not provided in config
        if not container_config['entrypoint']:
            try:
                image_info = self.dcli.inspect_image("{}:{}".format(*cont_image))

                if image_info['ContainerConfig']:
                    container_config['entrypoint'] = image_info['ContainerConfig']['Entrypoint']
                elif image_info['Config']:
                    container_config['entrypoint'] = image_info['Config']['Entrypoint']

                # check if command is also not provided in the configuration
                if not container_config['command']:
                    if image_info['Config']:
                        container_config['command'] = image_info['Config']['Cmd']
            except errors.APIError as err:
                raise ContainerError("Cannot create container {} using image {}. Entrypoint not found.".format(
                    container_config['container'], container_config['image']), err)

        # create container's host_config
        host_config = self.dcli.create_host_config(
            network_mode=container_config['network_mode'],
            privileged=container_config['privileged'],
            binds=container_config['volumes'],
            tmpfs=container_config['tmpfs'],
            publish_all_ports=defaults['publish_all_ports'],
            mem_limit=defaults['mem_limit'],
            memswap_limit=defaults['memswap_limit'],
            dns=container_config['dns'],
            ipc_mode=defaults['ipc_mode'],
            devices=defaults['devices'],
            cap_add=defaults['cap_add'],
            sysctls=container_config['sysctls'],
            port_bindings=self._get_port_bindings(container_config['ports']) if container_config['ports'] else {},
            restart_policy=self._get_restart_policy(container_config['restart']) if container_config[
                'restart'] else None,
            extra_hosts=self._get_extra_hosts(container_config['extra_hosts']) if container_config[
                'extra_hosts'] else None,
            pid_mode=container_config['pid']
        )

        main_net_config = {}
        remain_net_configs = []
        net_count = 1
        # check and get first network as main config, other networks will be connected later
        if 'networks' in container_config:
            for network in container_config['networks']:
                if net_count == 1:
                    # print("Create main_net_config")
                    # create endpoint_config
                    endpoint_config = self.dcli.create_endpoint_config(
                        aliases=network['config']['aliases'],
                        ipv4_address=network['config']['ipv4_address'],
                        ipv6_address=network['config']['ipv6_address'],
                    )
                    main_net_config = self.dcli.create_networking_config({
                        network['name']: endpoint_config,
                    })
                else:
                    # print("Create other_net_config")
                    created_net = self.get_network_by_name(network['name'])
                    if created_net:
                        remain_net_configs.append({
                            'net_id': created_net['Id'],
                            'aliases': network['config']['aliases'],
                            'ipv4_address': network['config']['ipv4_address'],
                            'ipv6_address': network['config']['ipv6_address'],
                        })

                net_count += 1

        # create new docker container
        try:
            container = self.dcli.create_container(
                name=container_config['container_name'],
                image=container_config['image'],
                command=container_config['command'],
                entrypoint=container_config['entrypoint'],
                stdin_open=True,  # keep container open
                tty=True,  # allocate pseudo tty
                environment=container_config['environment'],
                host_config=host_config,
                networking_config={} if not main_net_config else main_net_config,
                ports=self._get_ports(container_config['ports']),
                volumes=[self._extract_volume_mount_name(p) for p in container_config['volumes']
                         if self._extract_volume_mount_name(p) is not None],
                labels=container_config['labels'],
                hostname=container_config['hostname']
            )
        except errors.APIError as err:
            raise ContainerError("Failed to create container.", err)

        cont_id = container.get('Id')
        try:
            self.dcli.start(container=cont_id)
        except errors.APIError as err:
            raise ContainerError("Failed to start container {}-{}.".format(container_config['container_name'],
                                                                           cont_id), err)

        # attach container to all remaining networks
        for net_conf in remain_net_configs:
            self.dcli.connect_container_to_network(cont_id,
                                                   net_id=net_conf['net_id'],
                                                   ipv4_address=net_conf['ipv4_address'],
                                                   ipv6_address=net_conf['ipv6_address'],
                                                   aliases=net_conf['aliases'])

        return {'container_id': cont_id,
                'container_info': self.dcli.inspect_container(cont_id)}

    def get_container_by_name(self, container_name: str) -> {}:
        """
        Get a container by name
        :param container_name: Name of the container
        :return: dict
        """
        try:
            return self.dcli.containers(all=True, filters={
                'name': container_name
            })
        except errors.APIError as err:
            raise ContainerError("Cannot get container: name={}.".format(container_name), err)

    def get_container_by_id(self, container_id: str) -> {}:
        """
        Get a container by name
        :param container_id: Id of the container
        :return: dict
        """
        try:
            return self.dcli.containers(all=True, filters={
                'id': container_id
            })
        except errors.APIError as err:
            raise ContainerError("Cannot get container: id={}.".format(container_id), err)

    def get_containers(self, show_all: bool = True, trunc: bool = False, filters=None):
        """
        List containers. Similar to the docker ps command.
        :param show_all: Show all containers. Only running containers are shown by default (=True)
        :param trunc: Truncate output (default=False)
        :param filters: Filters to be processed on the image list. See more:
        https://docker-py.readthedocs.io/en/stable/api.html#docker.api.container.ContainerApiMixin.containers
        :return: List of dicts, one per container
        """
        try:
            return self.dcli.containers(all=show_all, trunc=trunc, filters=filters)
        except errors.APIError as err:
            raise ContainerError("Cannot get running containers using filters=[all={},trunc={},filters={}]"
                                 .format(show_all, trunc, filters), err)

    def stop_container(self, container_id: str, timeout: int = None):
        """
        Stops a container. Similar to the docker stop command.
        :param container_id: Id of the container we want to stop
        :param timeout:  Timeout in seconds to wait for the container to stop before sending a SIGKILL.
        :return: True if done, ContainerError otherwise
        """
        try:
            self.dcli.stop(container_id, timeout=timeout)
            return True
        except errors.APIError as err:
            raise ContainerError("Cannot stop container with id={}".format(container_id), err)

    def remove_container(self, container_id: str, remove_volume: bool = False, remove_link: bool = False,
                         force: bool = False):
        """
        Remove a container.
        :param container_id: Id of the container we want to remove
        :param remove_volume: Remove the volumes associated with the container
        :param remove_link: Remove the specified link and not the underlying container
        :param force: Force the removal of a running container (uses SIGKILL)
        :return: True if done, ContainerError otherwise
        """
        try:
            self.dcli.remove_container(container_id, v=remove_volume, link=remove_link, force=force)
            return True
        except errors.APIError as err:
            raise ContainerError("Cannot remove container with id={}".format(container_id), err)

    def remove_unused_containers(self, filters=None) -> {}:
        """
        Delete all stopped containers
        :param filters:  Filters to process on the prune list.
        :return: A dict containing a list of deleted container IDs and
                the amount of disk space reclaimed in bytes.
        """
        try:
            return self.dcli.prune_containers(filters=filters)
        except errors.APIError as err:
            raise ContainerError("Cannot prune containers with filters={}".format(filters), err)

    # VOLUME SECTION
    def create_volume(self, volume_config) -> {}:
        """
        Create a docker volume
        :param volume_config: all information needed to create a new docker volume
        :return: dict
        """
        try:
            # skip all volumes that are already marked as "external"
            if 'external' not in volume_config:
                volume = self.dcli.create_volume(name=volume_config['name'],
                                                 driver=volume_config['driver'],
                                                 driver_opts=volume_config['driver_opts'],
                                                 labels=volume_config['labels'])
                return volume
            return None
        except errors.APIError as err:
            raise VolumeError("Error creating docker volume {}".format(volume_config), err)

    def get_volume_by_name(self, volume_name: str) -> {}:
        """
        Get volume by a given name
        :param volume_name: name of volume we want to search for
        :return: Network object if network is existed, None otherwise
        """
        volumes = self.dcli.volumes()
        if len(volumes['Volumes']) > 0:
            for volume in volumes['Volumes']:
                if volume_name == volume['Name']:
                    return volume
        return None

    def get_volumes(self, filters=None):
        """
        List all volumes, can be filtered by names and/or additional information
        :param filters:
        :return:
        """
        try:
            return self.dcli.volumes(filters=filters)
        except errors.APIError as err:
            raise VolumeError('Cannot show all volumes using filter={}'.format(filters), err)

    def remove_volume_by_name(self, volume_name: str):
        """
        Try to remove volume using its name
        :param volume_name: The volume’s name will be removed
        """
        try:
            removed_volume = self.get_volume_by_name(volume_name)

            if removed_volume:
                self.dcli.remove_volume(removed_volume['Name'], force=True)
            else:
                raise VolumeError('Cannot find volume name={} to remove'.format(volume_name), None)
        except VolumeError as err:
            raise err

    def remove_unused_volumes(self, filters=None) -> {}:
        """
        Remove all unused volumes
        :param filters: Filters to process on the prune list.
        :return: dict
        """
        try:
            return self.dcli.prune_volumes(filters=filters)
        except errors.APIError as err:
            raise VolumeError('Cannot prune volumes.', err)

    # NETWORK SECTION
    def create_network(self, network_config):
        """
        Create a docker network
        :param network_config: all information needed to create a new docker network
        :return: dict
        """
        try:
            # skip all networks that are already marked as "external"
            if 'external' not in network_config and network_config['driver'] != "none":
                if not network_config['ipam']:
                    network = self.dcli.create_network(name=network_config['name'],
                                                       driver=network_config['driver'],
                                                       options=network_config['options'],
                                                       ipam=network_config['ipam'],
                                                       check_duplicate=network_config['check_duplicate'],
                                                       internal=network_config['internal'],
                                                       labels=network_config['labels'],
                                                       enable_ipv6=network_config['enable_ipv6'],
                                                       attachable=network_config['attachable'],
                                                       scope=network_config['scope'],
                                                       ingress=network_config['ingress'])

                    return network
                else:
                    pool_configs = []
                    for pcf in network_config['ipam']['pool_configs']:
                        ipam_pool = types.IPAMPool(
                            subnet=None if not pcf['subnet'] else pcf['subnet'],
                            iprange=None if not pcf['iprange'] else pcf['iprange'],
                            gateway=None if not pcf['gateway'] else pcf['gateway'],
                            aux_addresses=None if not pcf['aux_addresses'] else pcf['aux_addresses']
                        )
                        pool_configs.append(ipam_pool)

                    ipam_conf = docker.types.IPAMConfig(
                        driver=network_config['ipam']['driver'],
                        pool_configs=pool_configs,
                        options=network_config['ipam']['options']
                    )

                    network = self.dcli.create_network(name=network_config['name'],
                                                       driver=network_config['driver'],
                                                       options=network_config['options'],
                                                       ipam=ipam_conf,
                                                       check_duplicate=network_config['check_duplicate'],
                                                       internal=network_config['internal'],
                                                       labels=network_config['labels'],
                                                       enable_ipv6=network_config['enable_ipv6'],
                                                       attachable=network_config['attachable'],
                                                       scope=network_config['scope'],
                                                       ingress=network_config['ingress'])

                    return network

            return None
        except errors.APIError as err:
            raise NetworkError("Error creating docker network {}".format(network_config), err)

    def get_network_by_name(self, network_name: str) -> {}:
        """
        Get network by a given name
        :param network_name: name of network we want to search for
        :return: Network object if network is existed, None otherwise
        """
        networks = self.dcli.networks(names=[network_name])
        if len(networks) > 0:
            for network in networks:
                if network_name == network['Name']:
                    return network
        return None

    def disconnect_container_network(self, container_id: str, net_id: str, force: bool = True):
        """
        Remove connect between container and one of its attached networks
        :param container_id: container ID to be disconnected from the network
        :param net_id: network ID to be disconnected to container
        :param force: Force disconnection
        """
        self.dcli.disconnect_container_from_network(container_id, net_id, force)

    def get_networks(self, names=None, filters=None) -> []:
        """
        List all docker networks, can be filtered by names and/or additional information
        :param names: List of names to filter by
        :param filters: Filters to be processed on the network list
        :return: List of networks objects
        """
        try:
            return self.dcli.networks(names=names, filters=filters)
        except errors.APIError as err:
            raise NetworkError('Cannot show all networks using filter names={};filters={}'.format(names, filters),
                               err)

    def remove_network_by_name(self, network_name: str):
        """
        Try to remove network using its name
        :param network_name: The network’s name will be removed
        """
        try:
            removed_network = self.get_network_by_name(network_name)

            if removed_network:
                self.dcli.remove_network(removed_network['Id'])
            else:
                raise NetworkError('Cannot find network name={} to remove'.format(network_name), None)
        except NetworkError as err:
            raise err

    def remove_unused_networks(self, filters=None):
        """
        Remove all unused networks
        :param filters: Filters to process on the prune list.
        :return: dict
        """
        try:
            self.dcli.prune_networks(filters=filters)
        except errors.APIError as err:
            raise NetworkError('Cannot prune networks.', err)

    # IMAGE SECTION
    def _image_pulled(self, repo: str, tag: str) -> bool:
        """
        Check if image with repo:tag already pulled
        :param repo: repo of image
        :param tag: tag of image
        :return: True if image has already downloaded, False otherwise.
        """
        local_images = self.dcli.images()
        image = "{}:{}".format(repo, tag)
        for img in local_images:
            if img.get("RepoTags", None):
                if image in img.get("RepoTags", []):
                    return True

        return False

    def pull_image(self, repo: str, tag: str):
        """
        Try to download image from docker hub/custom repo
        :param repo: repo of image
        :param tag: tag of image
        """
        try:
            message = ""
            for line in self.dcli.pull(repo, tag, stream=True):
                message = message + json.dumps(json.loads(line), indent=4)
            # print("Image {}:{} pulled".format(repo, tag))
        except errors.APIError as err:
            raise ImageError("Cannot pull image {}:{}".format(repo, tag), err)

    # UTILITY SECTION
    def get_image_repo_tag(self, image: str) -> RepoTag:
        # construct repo & tag attribute of an image
        repo = None
        tag = None
        if image:
            # e.g., redis or tutum/influxdb
            if ':' not in image:
                repo = image
                tag = "latest"
            else:
                # custom repository with ip:port combination
                # e.g., example-registry.com:4000/postgresql:1.0.0
                if image.count(':') == 2:
                    # split image based on '/'
                    image_tup = tuple(part for part in image.split('/') if part)
                    repo = image_tup[0] + tuple(part for part in image_tup[1].split(':') if part)[0]
                    tag = tuple(part for part in image_tup[1].split(':') if part)[1]
                # default docker hub or custom repository with ip:port combination without image tag
                # e.g., tutum/influxdb:1.0.0 -> case #1
                # or 159.100.243.157:5000/hello-world -> case #2
                else:
                    if image.index(':') > image.index('/'):
                        repo, tag = tuple(part for part in image.split(':') if part)
                    else:
                        repo = image
                        tag = "latest"

        return RepoTag(repo=repo, tag=tag)

    def _get_ports(self, container_port_conf: []) -> []:
        """
        Get ports used in docker.client.create_container(...)
        :param container_port_conf: container original port config
        :return: list
        """
        ports = []
        for port_conf in container_port_conf:
            if 'proto' in port_conf:
                ports.append((port_conf['cont_port'], port_conf['proto']))
            else:
                ports.append(port_conf['cont_port'])
        return ports

    def _get_port_bindings(self, container_port_conf) -> {}:
        """
        Get port_bindings used in docker.client.create_host_config(...)
        :param container_port_conf: container original port config
        :return: dict
        """
        port_bindings = {}
        for port_conf in container_port_conf:
            k, v = None, None
            if 'proto' in port_conf:
                k = "{}.{}".format(port_conf['cont_port'], port_conf['proto'])
            else:
                k = port_conf['cont_port']
            if 'host_ip' in port_conf:
                v = (port_conf['host_ip'], port_conf['host_port'])
            else:
                v = port_conf['host_port']

            port_bindings[k] = v

        return port_bindings

    def _extract_volume_mount_name(self, volume_path: str):
        """ Helper to extract mount names from volume specification paths"""
        parts = volume_path.split(":")
        if len(parts) < 3:
            return None
        return parts[1]

    def _get_restart_policy(self, container_restart_conf) -> {}:
        """
        Get restart policy used in docker.create_host_config(...)
        :param container_restart_conf: container original restart config
        :return: dict
        """
        default_max_retries = 10
        if container_restart_conf != 'no':
            if 'on-failure' in container_restart_conf:
                if ':' in container_restart_conf:
                    retry_count = tuple(container_restart_conf.split(':'))[1]
                    return {
                        'Name': 'on-failure',
                        'MaximumRetryCount': retry_count
                    }
                else:
                    return {
                        'Name': 'on-failure',
                        'MaximumRetryCount': default_max_retries
                    }
            else:
                return {
                    'Name': 'always'
                }
        else:
            return {}

    def _get_extra_hosts(self, container_extra_conf) -> {}:
        """
        Get extra host used in docker.client.create_host_config(...)
        :param container_extra_conf: container original extra config
        :return: dict
        """
        extra_hosts = {}
        for host in container_extra_conf:
            hostname, ip = tuple(part for part in host.split(':') if part)
            extra_hosts[hostname] = ip

        return extra_hosts
