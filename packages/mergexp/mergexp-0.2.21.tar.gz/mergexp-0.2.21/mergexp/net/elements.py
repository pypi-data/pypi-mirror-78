from .. import ConstraintGenerator

capacity = ConstraintGenerator("capacity")
latency = ConstraintGenerator("latency")
loss = ConstraintGenerator("loss")

# Routing is a reticulator. "static" may be a type of routing.
routing = ConstraintGenerator("routing")
static = "static"

# Addressing reticulator. 
addressing = ConstraintGenerator("addressing")
ipv4 = "ipv4"
