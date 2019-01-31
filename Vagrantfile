# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = '2'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "centos/7"
  config.vm.synced_folder 'artifacts', '/tmp/artifacts'

  config.vm.provider :virtualbox do |vbx|
    vbx.customize ['modifyvm', :id, '--cpus', 2]
    vbx.customize ['modifyvm', :id, '--memory', 2048]
  end

  config.vm.provider :vmware_desktop do |vmw, override|
    if Vagrant::Util::Platform.windows? then
      override.vm.synced_folder 'artifacts', '/tmp/artifacts', type: "smb"
    else
      override.vm.synced_folder 'artifacts', '/tmp/artifacts', type: "nfs"
    end
    vmw.vmx["memsize"] = "2048"
    vmw.vmx["numvcpus"] = "2"
  end

  config.vm.provision 'file', source: './SOURCES', destination: '/tmp/build/'
  config.vm.provision 'file', source: './SPECS', destination: '/tmp/build/'
  config.vm.provision "shell", inline: "touch /.doing_the_vagrant"
  config.vm.provision 'shell', path: 'build.sh', privileged: false
end
