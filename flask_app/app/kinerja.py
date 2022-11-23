from app.conn import cur, conn

class Kinerja:
    kpi = ['EAF', 'EFOR', 'SOF', 'CF', 'SdOF', 'PS', 'SFC']
    rsh = '(ph - ((po + mo + fo) + sh))'
    total_derating = '(epdh + eudh + esdh)'
    total_ps = '(ps_sentral + ps_trafo)'
    produksi_netto = f'(produksi - {total_ps})'
    dtp_ph = '(dtp * ph)'
    dmn_ph = '(dmn * ph)'
    dmn_ph_der = f'(dmn * (sh + {rsh} - {total_derating}))'
    dmn_fo_eudh = '(dmn * (fo + eudh))'
    dmn_fo_sh_efdhrs = '(dmn * (fo + sh + efdhrs))'
    dmn_har = '(dmn * (po + mo))'
    sdof = 'trip_internal'