#!/usr/bin/env python

import yaml
import crypt

class DBConfig: 
  def __init__(self):
    self.HOST="bulls.cs.ucsb.edu"
    self.DATABASE="appbench"
    self.USER="uid"
    self.PASS="password"

    self.SCHEMA=""" (
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  agent varchar(20) NOT NULL,
  sample int(4) UNSIGNED NOT NULL,
  thread int(4) UNSIGNED NOT NULL,
  run int(4)  UNSIGNED NOT NULL,
  test int(4)  UNSIGNED NOT NULL,
  start BIGINT UNSIGNED NOT NULL,
  latency INT UNSIGNED NOT NULL,
  errors INT UNSIGNED NOT NULL,
  res_code INT UNSIGNED NOT NULL,
  res_len INT UNSIGNED NOT NULL,
  res_err INT UNSIGNED NOT NULL,
  resolve INT UNSIGNED NOT NULL,
  establish INT UNSIGNED NOT NULL,
  firstbyte INT UNSIGNED NOT NULL,
  PRIMARY KEY  (id)
);"""

"""
config = DBConfig()
yaml.dump(config, file('dbconfig.yaml', 'w'))
dbconf = yaml.load(file('dbconfig.yaml', 'r'))
print dbconf.HOST
print dbconf.USER
print dbconf.PASS
print dbconf.DATABASE
print dbconf.SCHEMA
"""
