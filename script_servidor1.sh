#!/bin/bash

echo "Instalando paquetes"
sudo apt-get install net-tools -y
sudo apt-get install vim -y

#consul
echo "Instalando CONSUL"
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install consul -y
consul -v

echo "Instalando NodeJS"
sudo apt-get install nodejs -y
node -v

echo "Instalando npm"
sudo apt install npm -y
npm -v

echo "Instalando git"
sudo apt-get install git -y
npm -v

#echo "Configurando consul"
#consul agent -ui -server -bootstrap-expect=1 -bind=192.168.100.3 -client=0.0.0.0 -data-dir=.
#sudo consul members
#sudo consul join ip 192.168.100.20 (IP - haproxy )
#sudo consul members


#echo "Configurando consul"
#git clone https://github.com/omondragon/consulService
#cd consulService/app
#npm install consul
#npm install express

