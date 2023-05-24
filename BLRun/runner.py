import BLRun.scodeRunner as SCODE
import BLRun.pidcRunner as PIDC
import BLRun.genie3Runner as GENIE3
import BLRun.grnboost2Runner as GRNBOOST2
import BLRun.grnvaeRunner as GRNVAE

from pathlib import Path

InputMapper = {'SCODE':SCODE.generateInputs,
               'PIDC':PIDC.generateInputs,
               'GENIE3':GENIE3.generateInputs,
               'GRNBOOST2':GRNBOOST2.generateInputs,
               'GRNVAE':GRNVAE.generateInputs,}


AlgorithmMapper = {'SCODE':SCODE.run,
            'PIDC':PIDC.run,
            'GENIE3':GENIE3.run,
            'GRNBOOST2':GRNBOOST2.run,
            'GRNVAE':GRNVAE.run,}



OutputParser = {'SCODE':SCODE.parseOutput, 
            'PIDC':PIDC.parseOutput,
            'GENIE3':GENIE3.parseOutput,
            'GRNBOOST2':GRNBOOST2.parseOutput,
            'GRNVAE':GRNVAE.parseOutput,}


class Runner(object):
    '''
    A runnable analysis to be incorporated into the pipeline
    '''
    def __init__(self,
                params):
        self.name = params['name']
        self.inputDir = params['inputDir']
        self.params = params['params']
        self.exprData = params['exprData']
        self.cellData = params['cellData']
        self.trueEdges = params['trueEdges'] #used for evaluation
        
    def generateInputs(self):
        InputMapper[self.name](self)
        
        
    def run(self):
        AlgorithmMapper[self.name](self)

    def parseOutput(self):
        OutputParser[self.name](self)
