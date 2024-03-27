



class Position_Size():
    base_deal = 33
    base_risk = 3
    # max deal risk 1%
    balace = 100
    def __init__(self, symbol, lp, body_size_ticks, body_prc, today_atr) -> None:
        self.symbol = symbol
        self.cp = lp
        self.body = body_size_ticks
        self.body_prc = body_prc
        self.atr = today_atr
        self.atr_prc = (today_atr/lp)*100

    def pos_size(self):
        # vars
        arred = lambda x,n : x*(10**n)//1/(10**n)
        risk = self.atr_prc/4
        # logic
        if risk < Position_Size.base_risk:
            current_risk_prc = (risk) / Position_Size.base_risk
            amount_of_position = (
                Position_Size.base_deal-(Position_Size.base_deal * current_risk_prc)) + Position_Size.base_deal
        elif risk > Position_Size.base_risk:
            amount_of_position = (Position_Size.base_risk/(risk))*Position_Size.base_deal
        else:
            amount_of_position = (Position_Size.base_deal*Position_Size.base_risk)/100
        # result
        futures_pos = arred((amount_of_position / self.cp), 2)
        max_prc_stop = arred(risk, 1)

        max_stop_long = self.cp - self.atr/4
        max_stop_short = self.cp + self.atr/4
        margin2 = amount_of_position / 2
        margin3 = amount_of_position / 3
        margin5 = amount_of_position / 5
        return (futures_pos, max_prc_stop, int(amount_of_position))
    