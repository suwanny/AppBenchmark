#! /bin/bash

ROOT=${PWD}

function install_gnuplot {
  sudo apt-get install gnuplot
}

function install_xlwt {
  cd ${ROOT}/ext/xlwt-0.7.2
  sudo python setup.py install
  cd ${ROOT}
}

function install_PyGnuplot {
  sudo apt-get install python-numpy
  cd ${ROOT}/ext/gnuplot-py-1.8
  sudo python setup.py install
  cd ${ROOT}
}

install_gnuplot
install_xlwt
install_PyGnuplot

