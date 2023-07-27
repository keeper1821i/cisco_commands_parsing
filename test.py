import textfsm


with open ("Current configuration  978 bytes.template") as f:
    fsm = textfsm.TextFSM(f)
    resust = fsm.ParseText()