# Copyright 2012-2013 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A shortest-path forwarding application.

This is a standalone L2 switch that learns ethernet addresses
across the entire network and picks short paths between them.

You shouldn't really write an application this way -- you should
keep more state in the controller (that is, your flow tables),
and/or you should make your topology more static.  However, this
does (mostly) work. :)

Depends on openflow.discovery
Works with openflow.spanning_tree
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.recoco import Timer
from collections import defaultdict
from pox.lib.addresses import IPAddr, EthAddr
from pox.openflow.discovery import Discovery
from pox.lib.util import dpid_to_str
import time

log = core.getLogger()
e1 = EthAddr('00:00:00:00:00:01')
e2 = EthAddr('00:00:00:00:00:02')
e3 = EthAddr('00:00:00:00:00:03')
e4 = EthAddr('00:00:00:00:00:04')
e5 = EthAddr('00:00:00:00:00:05')
e6 = EthAddr('00:00:00:00:00:06')
num_mac = {1 : e1, 2 : e2, 3 : e3, 4 : e4, 5 : e5, 6 : e6}

mac_to_number = {e1 : 1, e2 : 2, 
e3 : 3, e4 : 4, e5 : 5, e6 : 6}
print EthAddr('00:00:00:00:00:01')
switch1_all_right = {
#host 1 send
(3, num_mac[2]) : 4,
(3, num_mac[3]) : 1,
(3, num_mac[4]) : 1,
(3, num_mac[5]) : 1,
(3, num_mac[6]) : 1,
#host 2 send
(4, num_mac[1]) : 3,
(4, num_mac[3]) : 2,
(4, num_mac[4]) : 2,
(4, num_mac[5]) : 2,
(4, num_mac[6]) : 2,
# host 1, 2 recv
(1, num_mac[1]) : 3,
(1, num_mac[2]) : 4,
(2, num_mac[1]) : 3,
(2, num_mac[2]) : 4,
}
switch2_all_right = {
# host 3
(3, num_mac[4]) : 4,
(3, num_mac[5]) : 1,
(3, num_mac[6]) : 1,
(3, num_mac[1]) : 1,
(3, num_mac[2]) : 1,
#host 4
(4, num_mac[3]) : 3,
(4, num_mac[5]) : 2,
(4, num_mac[6]) : 2,
(4, num_mac[1]) : 2,
(4, num_mac[2]) : 2,
# host 3, 4 recv
(1, num_mac[3]) : 3,
(1, num_mac[4]) : 4,
(2, num_mac[3]) : 3,
(2, num_mac[4]) : 4,
}
switch3_all_right = {
#host 5
(3, num_mac[6]) : 4,
(3, num_mac[1]) : 1,
(3, num_mac[2]) : 1,
(3, num_mac[3]) : 1,
(3, num_mac[4]) : 1,
#host 6
(4, num_mac[5]) : 3,
(4, num_mac[1]) : 2,
(4, num_mac[2]) : 2,
(4, num_mac[3]) : 2,
(4, num_mac[4]) : 2,
# host 5, 6 recv
(1, num_mac[5]) : 3,
(1, num_mac[6]) : 4,
(2, num_mac[5]) : 3,
(2, num_mac[6]) : 4,
}
switch4_all_right = {
(1, num_mac[3]) : 2,
(1, num_mac[4]) : 2,
(1, num_mac[5]) : 3,
(1, num_mac[6]) : 3,

(2, num_mac[1]) : 1,
(2, num_mac[2]) : 1,
(2, num_mac[5]) : 3,
(2, num_mac[6]) : 3,

(3, num_mac[1]) : 1,
(3, num_mac[2]) : 1,
(3, num_mac[3]) : 2,
(3, num_mac[4]) : 2,
}

switch5_all_right = {
(1, num_mac[3]) : 2,
(1, num_mac[4]) : 2,
(1, num_mac[5]) : 3,
(1, num_mac[6]) : 3,

(2, num_mac[1]) : 1,
(2, num_mac[2]) : 1,
(2, num_mac[5]) : 3,
(2, num_mac[6]) : 3,

(3, num_mac[1]) : 1,
(3, num_mac[2]) : 1,
(3, num_mac[3]) : 2,
(3, num_mac[4]) : 2,
}

routing_rules_all_right = [0, switch1_all_right, switch2_all_right, switch3_all_right, switch4_all_right, switch5_all_right]


class main_controller (EventMixin):
  def __init__ (self):
    # Listen to dependencies
    def startup ():
      core.openflow.addListeners(self, priority=0)
      core.openflow_discovery.addListeners(self)
    core.call_when_ready(startup, ('openflow','openflow_discovery'))

  def _handle_LinkEvent (self, event):
    print "LinkEvent"
   

  def install_rules(self, event, table):
    pass

  def _handle_ConnectionUp (self, event):
    # print event.connection.dpid
    # print "connectionUP"
    seq = event.dpid
    table_for_this = routing_rules_all_right[event.dpid]
    keys = table_for_this.keys()
    for key in keys:
      msg = of.ofp_flow_mod()
      msg.match.in_port = key[0]
      msg.match.dl_dst = key[1]
      msg.actions.append(of.ofp_action_output(port = table_for_this[key]))
      event.connection.send(msg)




def launch ():
  core.registerNew(main_controller)
