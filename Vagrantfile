# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

git_branch = `git rev-parse --abbrev-ref HEAD`.strip
if(git_branch == "master") then
  git_branch = "default"
end
GIT_BRANCH = git_branch

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define GIT_BRANCH, primary: true do |branch|

    branch.vm.provision :shell, :inline => "ln -sf /vagrant/vagrant-env.sh /etc/profile.d/vagrant.sh; echo source /etc/profile.d/vagrant.sh >> ~/.bashrc"
    branch.vm.provision :shell, :inline => "echo source /etc/profile.d/vagrant.sh >> ~/.bashrc", :privileged => "false"
    branch.vm.provision :shell, :path => "vagrant-setup.sh"
    branch.vm.provision :shell, :path => "vagrant-start.sh"

    branch.vm.box = 'ubuntu/xenial64'
    branch.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
    branch.vm.network "forwarded_port", guest: 8081, host: 8081, host_ip: "127.0.0.1"
    branch.vm.synced_folder ".", "/vagrant"

    if File.directory?("../priy-report") then
      branch.vm.synced_folder "../priy-report", "/report"
    end

    branch.vm.network "private_network", ip: "192.168.50.100"

  end

  config.vm.define GIT_BRANCH + "-achecker" do |achecker|

    achecker.vm.provision :shell, :inline => "ln -sf /vagrant/vagrant-env.sh /etc/profile.d/vagrant.sh; echo source /etc/profile.d/vagrant.sh >> ~/.bashrc"
    achecker.vm.provision :shell, :inline => "echo source /etc/profile.d/vagrant.sh >> ~/.bashrc", :privileged => "false"
    achecker.vm.provision :shell, :path => "vagrant-setup-achecker.sh"

    achecker.vm.box = 'ubuntu/trusty64'
    achecker.vm.network "forwarded_port", guest: 9080, host: 9080, host_ip: "127.0.0.1"
    achecker.vm.synced_folder ".", "/vagrant"

    achecker.vm.network "private_network", ip: "192.168.50.101"

  end

  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", "2000"]
    v.customize ["modifyvm", :id, "--cpuexecutioncap", "80"]
  end

end
