import dockerwrapper


def show_all_volumes(docker_manager: 'dockerwrapper.DockerWrapper'):
    try:
        volumes = docker_manager.get_volumes()
        for vol in volumes['Volumes']:
            print(vol)
    except dockerwrapper.VolumeError as err:
        print(err)


def prune_volumes(docker_manager: 'dockerwrapper.DockerWrapper'):
    try:
        removed_volumes = docker_manager.remove_unused_volumes()

        print("Remove unused volumes successfully. Info: ")
        print(removed_volumes)
    except dockerwrapper.VolumeError as err:
        print(err)


def remove_volume_by_name(docker_manager: 'dockerwrapper.DockerWrapper', name: str):
    try:
        remove_volume = docker_manager.remove_volume_by_name(name)
    except dockerwrapper.VolumeError as err:
        print(err)


def main():
    print("Do some test here")
    docker = dockerwrapper.DockerWrapper()

    # try to get all volumes
    #show_all_volumes(docker)
    #prune_volumes(docker)
    #remove_volume_by_name(docker, 'data_1')
    #remove_volume_by_name(docker, 'data_4')

    # try to get all networks
    #print(docker.get_networks('net_1'))
    #print(docker.get_networks())
    #try:
    #    docker.remove_network_by_name('net_1')
    #except dockerwrapper.NetworkError as err:
    #    print(err)

    #try:
    #    docker.remove_network_by_name('unknown')
    #except dockerwrapper.NetworkError as err:
    #    print(err)

    # try get all containers
    print(docker.get_containers(show_all=True, filters={
        'id': 'd9fc23af6b46f3f3bcd834f1ebddfefc2110cb6d9cce04529097e87e47317f45'
    }))

    print(docker.get_container_by_name('ubuntu'))

    try:
        docker.remove_container('ubuntu')
        print('Remove container {} successfully.'.format('ubuntu'))
    except dockerwrapper.ContainerError as err:
        print(err)

    try:
        result = docker.remove_unused_containers()
        print(result)
    except dockerwrapper.ContainerError as err:
        print(err)


if __name__ == '__main__':
    main()
