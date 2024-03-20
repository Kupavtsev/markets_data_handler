balace = 100
margin = None
minimum_pos = 5
deal_risk_prc_of_balance = 1
deal_risk_ticks_of_asset = None
price_move_by_atr_in_percent = None     # for prev session or atr in percent within close
risk_in_pos = None      # some part of MP
lots = 4

# do I need av Body for few days ?
# atr% = atr/cp*100
ach = {
    'current price': 0.0334412,
    'atr': 0.006215, 'atr%': 18.5,  # half_atr=9.25
    'body': 0.0028994, 'body%': 8.6,
    'tail': 0.0014001, 'tail%': 3}
fet = {
    'current price': 2.6685563,
    'atr': 0.431, 'atr%': 16,       # half_atr=6.8
    'body': 0.3203724, 'body%': 13.6,
    'tail': 0.055236, 'tail%': 2.4}
lpt = {
    'current price': 22.5852643,
    'atr': 3.368429, 'atr%': 15,    # half_atr=7.5
    'body': 3.2842183, 'body%': 14.5,
    'tail': 1.4315823, 'tail%': 5.5}

# Prepair the opposite data, when market not so volatil

assets = [ach, fet, lpt]

# LOGIC
max_position_amount = balace / lots
