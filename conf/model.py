from collections import namedtuple


class Model:
    def __init__(self):
        super().__init__()

        self.port = None

        Devices = namedtuple('Devices', 'ai di')
        self.device = Devices(ai=None,
                              di=None,
                              )

        ControlButtons = namedtuple('ControlButtons', 'back up down yes no')
        self.ctrl_btn = ControlButtons(back=None,
                                       up=None,
                                       down=None,
                                       yes=None,
                                       no=None,
                                       )

        Buttons = namedtuple('Buttons', 'examination auto')
        self.btn = Buttons(examination=None,
                           auto=None,
                           )

        Switches = namedtuple('Switches', 'ku breaking speed rd upr_rd keb red leak_1 leak_05 ok')
        self.switch = Switches(ku=None,
                               breaking=None,
                               speed=None,
                               rd=None,
                               upr_rd=None,
                               keb=None,
                               red=None,
                               leak_1=None,
                               leak_05=None,
                               ok=None,
                               )
        SwitchesNeutral = namedtuple('SwitchesNeutral', 'enter rd_keb tank')
        self.switch_n = SwitchesNeutral(enter=None,
                                        rd_keb=None,
                                        tank=None,
                                        )

        Manometers = namedtuple('Manometers', 'ppm pim ptc1 ptc2 pupr')
        self.manometers = Manometers(ppm=None,
                                     pim=None,
                                     ptc1=None,
                                     ptc2=None,
                                     pupr=None,
                                     )
