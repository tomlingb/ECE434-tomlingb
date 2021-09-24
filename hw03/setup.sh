# Here's how to cinfgure the pins for using the eQEP's for reading a
# rotory encoder

# eQEP 0 - This wasn't working on the Green Wireless
config-pin P9_27 eqep
config-pin P9_92 eqep    # This is really P9_41b

# eQEP 1
config-pin P8_33 eqep
config-pin P8_35 eqep

# eQEP 2
config-pin P8_11 eqep    # These have a conflict on the Green Wireless
config-pin P8_12 eqep

config-pin P8_41 default
config-pin P8_42 default
