from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
import pox.lib.packet.arp as arp


# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()


#use this table to add the needed entries
table = {"10.0.0.1":"00.00.00.00.00.01", "10.0.0.2":"00.00.00.00.00.02", 
"10.0.0.3":"00.00.00.00.00.03", "10.0.0.4":"00.00.00.00.00.04", "10.0.0.5":"00.00.00.00.00.015",
"10.0.0.6":"00.00.00.00.00.06"}
all_ports = of.OFPP_FLOOD

# Handle messages the switch has sent us because it has no
# matching rule.

def _handle_PacketIn (event):
    packet = event.parsed
    if packet.type == packet.ARP_TYPE:
        if packet.payload.opcode == arp.REQUEST:

            arp_reply = arp()
            arp_reply.hwsrc = table[packet.payload.protodst]#<requested mac address>
            arp_reply.hwdst = packet.src
            arp_reply.opcode = arp.REPLY
            arp_reply.protosrc = packet.payload.protodst#<IP of requested mac-associated machine>
            arp_reply.protodst = packet.payload.protosrc
            ether = ethernet()
            ether.type = ethernet.ARP_TYPE
            ether.dst = packet.src
            ether.src = table[packet.payload.protodst]#<requested mac address>
            ether.payload = arp_reply
            #send this packet to the switch
            msg = of.ofp_packet_out(data = ether.pack())
            msg.actions.append(of.ofp_action_output(port = event.ofp.in_port))
            event.connection.send(msg)

            #see section below on this topic
        elif packet.payload.opcode == arp.REPLY:
            print "It's a reply; do something cool"
        else:
            print "Some other ARP opcode, probably do something smart here"

# check if the entry is in the table or not
# if it's not in the table, add an entry to the table
# We don't know where the destination is yet.  So, we'll just
# send the packet out all ports (except the one it came in on!)
# and hope the destination is out there somewhere. :)
# To send out all ports, we can use either of the special ports
# OFPP_FLOOD or OFPP_ALL.
# if the appropriate entry is in the table, just forward the packet to that port

def launch ():
	core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
	log.info("Simple Routing Switch Running.")