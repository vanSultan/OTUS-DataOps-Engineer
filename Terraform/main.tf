terraform {
    required_providers {
        yandex = {
            source = "yandex-cloud/yandex"
        }
    }
    required_version = ">= 0.74.0"
}

provider "yandex" {
    token     = file("${path.module}/token.txt")
    cloud_id  = "b1grt10391028oivisor"
    folder_id = "b1gco3soqqhophq3s5md"
    zone      = "ru-central1-a"
}

resource "yandex_vpc_network" "otus-network" {
    name = "otus-network"
}

resource "yandex_vpc_subnet" "otus-subnet" {
    name           = "otus-subnet"
    zone           = "ru-central1-a"
    network_id     = yandex_vpc_network.otus-network.id
    v4_cidr_blocks = ["192.168.10.0/24"]
}

resource "yandex_compute_instance" "otus-vm" {
    name = "otus-vm"

    resources {
        cores  = 2
        memory = 2
    }

    boot_disk {
        initialize_params {
            image_id = "fd809bfjomj9a1dngteo"  # Ubuntu 16.04 GPU
        }
    }

    network_interface {
        subnet_id = yandex_vpc_subnet.otus-subnet.id
        nat       = true
    }

    metadata = {
        user-data = "${file("${path.module}/meta.txt")}"
    }
}

output "internal_ip_address_vm" {
    value = yandex_compute_instance.otus-vm.network_interface.0.ip_address
}

output "external_ip_address_vm" {
    value = yandex_compute_instance.otus-vm.network_interface.0.nat_ip_address
}
