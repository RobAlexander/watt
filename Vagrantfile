# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

GIT_BRANCH = `git rev-parse --abbrev-ref HEAD`.strip
if(GIT_BRANCH == "master") then
  GIT_BRANCH = "default"
end

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define GIT_BRANCH do |branch|

    branch.vm.provision :shell, :path => "vagrant-setup.sh"

    branch.vm.box = 'ubuntu/xenial64'
    # branch.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
    branch.vm.synced_folder ".", "/vagrant"

  end

  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", "2000"]
    v.customize ["modifyvm", :id, "--cpuexecutioncap", "80"]
  end

end
