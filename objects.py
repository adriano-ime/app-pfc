class SeverObject():
    def __init__(self, id, name, status, networks, image, flavor):
        self.id = id
        self.name = name
        self.status = status
        self.networks = networks
        self.image = image
        self.flavor = flavor

class FlavorObject():
    def __init__(self, name, ram, disk, ephemeral, vcpus, is_public):
        self.name = name
        self.ram = ram
        self.disk = disk
        self.ephemeral = ephemeral
        self.vcpus = vcpus
        self.is_public = is_public

class ImageObject():
    def __init__(self, id, name, status):
        self.id = id
        self.name = name
        self.status = status


class NetworkObject():
    def __init__(self, id, name, subnets):
        self.id = id
        self.name = name
        # TODO: Update the parser to consider mutliple subnets split by comma (,)
        self.subnets = subnets
    
class SecurityGroupObject():
    def __init__(self, id, name, description, project, tags):
        self.id = id
        self.name = name
        self.description = description
        self.project = project
        # TODO: Update parser to consider arrays ([])
        self.tags = tags