'''
Parse the output for lots and return the array of lots for a symbol
'''

class LotParser:
    def __init__(self, logger):
        super().__init__()

        self.logger = logger
    
    def get_lots(self, symbol):
        from .ledger_exec import LedgerExecutor
        from .ledger_output_parser import LedgerOutputParser

        params = f"b ^Assets and :{symbol}$ --lots"
    
        ledger = LedgerExecutor(self.logger)
        output = ledger.run(params)
        output = ledger.split_lines(output)

        # parser = LedgerOutputParser()
        # total_lines = parser.get_total_lines(output)

        #
        num_lines = len(output)
        last_line = output[num_lines - 1]
        if "Assets" in last_line:
            #position = last_line.find("Assets")
            #last_line = last_line.substring(0, position)
            parts = last_line.split("Assets")
            last_line = parts[0].strip()
            output[num_lines - 1] = last_line

        return output
