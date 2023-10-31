import geni.portal as portal
import geni.rspec.pg as rspec

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()

prefixForIP = "192.168.1."
link = request.LAN("lan")

# Create a control node
control_node = request.XenVM("control")
control_node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD"
control_iface = control_node.addInterface("if0")
control_iface.component_id = "eth1"
control_iface.addAddress(rspec.IPv4Address(prefixForIP + "1", "255.255.255.0"))
link.addInterface(control_iface)
control_node.addService(rspec.Execute(shell="sh", command="sudo bash /local/repository/setup_control.sh"))

# Create two host nodes
for i in range(2):
    host_node = request.XenVM("host" + str(i))
    host_node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD"
    iface = host_node.addInterface("if" + str(i + 1))
    iface.component_id = "eth1"
    iface.addAddress(rspec.IPv4Address(prefixForIP + str(i + 2), "255.255.255.0"))
    link.addInterface(iface)
    host_node.addService(rspec.Execute(shell="sh", command="sudo bash /local/repository/setup_host.sh"))

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()
