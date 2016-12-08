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
from pox.openflow.discovery import Discovery
from pox.lib.util import dpid_to_str
import time

log = core.getLogger()

class main_controller (EventMixin):
  def __init__ (self):
    # Listen to dependencies
    def startup ():
      core.openflow.addListeners(self, priority=0)
      core.openflow_discovery.addListeners(self)
    core.call_when_ready(startup, ('openflow','openflow_discovery'))

  def _handle_LinkEvent (self, event):
    print "LinkEvent"
    #def flip (link):
    #  return Discovery.Link(link[2],link[3], link[0],link[1])

    #l = event.link
   

    # Invalidate all flows and path info.
    # For link adds, this makes sure that if a new link leads to an
    # improved path, we use it.
    # For link removals, this makes sure that we don't use a
    # path that may have been broken.
    #NOTE: This could be radically improved! (e.g., not *ALL* paths break)
    #clear = of.ofp_flow_mod(command=of.OFPFC_DELETE)
    #for sw in switches.itervalues():
    #  if sw.connection is None: continue
    #  sw.connection.send(clear)
    #path_map.clear()

    #if event.removed:
      # This link no longer okay
      # But maybe there's another way to connect these...
    #else:
    #  print 123
      # If we already consider these nodes connected, we can

  def _handle_ConnectionUp (self, event):
    #sw = switches.get(event.dpid)
    print "connectionUP"
    #if sw is None:
    #  pass
    #else:
    #  print 123



def launch ():
  core.registerNew(main_controller)
