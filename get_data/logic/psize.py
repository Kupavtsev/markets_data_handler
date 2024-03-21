



class Position_Size():
    # max deal risk 1%
    balace = 100
    lots = 4
    max_position = balace / lots
    # LOGIC
    max_position_amount = balace / lots
    def __init__(self, data) -> None:
        self.cp = data['current price']
        self.atr = data['atr']
        self.atr_prc = data['atr%']
        self.body = data['body']
        self.body_prc = data['body%']
        self.tail = data['tail']
        self.tail_prc = data['tail%']

    def pos_size(self):
        half_body_risk = Position_Size.max_position_amount * (self.body_prc/100) / 2
        amount_of_position = Position_Size.max_position_amount / half_body_risk
        futures_pos = amount_of_position / self.cp
        max_prc_stop = self.body_prc/2
        max_stop_long = self.cp - self.body/2
        max_stop_short = self.cp + self.body/2

        margin3 = amount_of_position / 3
        margin5 = amount_of_position / 5
        margin10 = amount_of_position / 10
        return (futures_pos, max_prc_stop)
    



'''
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
'''