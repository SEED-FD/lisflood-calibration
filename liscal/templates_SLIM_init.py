import os
import copy

class LisfloodSettingsTemplate():

    def __init__(self, cfg, subcatch):

        self.obsid = subcatch.obsid
        settings_dir = os.path.join(subcatch.path, 'settings')
        os.makedirs(settings_dir, exist_ok=True)

        self.outfix = os.path.join(settings_dir, os.path.basename(cfg.lisflood_template[:-4]))
        self.lisflood_template = cfg.lisflood_template
        with open(os.path.join('templates', cfg.lisflood_template), "r") as f:
            template_xml = f.read()
    
        template_xml = template_xml.replace('%gaugeloc', subcatch.gaugeloc) # Gauge location
        template_xml = template_xml.replace('%inflowflag', subcatch.inflowflag)
        template_xml = template_xml.replace('%ForcingStart', cfg.forcing_start.strftime('%d/%m/%Y %H:%M')) # Date of forcing start
        template_xml = template_xml.replace('%SubCatchmentPath', subcatch.path)

        self.template_xml = template_xml

    def settings_path(self, suffix, run_id):
        return self.outfix+suffix+run_id+'.xml'

    def write_template(self, run_id, cal_start_local, cal_end_local, param_ranges, parameters, write_states):

        out_xml = self.template_xml

        #out_xml = out_xml.replace('%run_rand_id', run_id)
        out_xml = out_xml.replace('%CalStart', cal_start_local) # Date of Cal starting
        out_xml = out_xml.replace('%CalEnd', cal_end_local)  # Time step of forcing at which to end simulation

        for ii in range(len(param_ranges)):
            ## DD Special Rule for the SAVA --> SAVA belongs to EFAS, these lines must be commented when running the GloFAS calibration
            #if self.obsid == '851' and (param_ranges.index[ii] == "adjust_Normal_Flood" or param_ranges.index[ii] == "ReservoirRnormqMult"):
            #    out_xml = out_xml.replace('%adjust_Normal_Flood',"0.8")
            #   out_xml = out_xml.replace('%ReservoirRnormqMult',"1.0")
            out_xml = out_xml.replace("%"+param_ranges.index[ii],str(parameters[ii]))

        out_xml_prerun = out_xml
        out_xml_prerun = out_xml_prerun.replace('%InitLisflood',"1")
        out_xml_prerun = out_xml_prerun.replace('%EndMaps', "1")
        # do not write tss files of the states during the calibration
        out_xml_prerun = out_xml_prerun.replace('%repStateGauges', "0")
        out_xml_prerun = out_xml_prerun.replace('%repRateGauges', "0")
        out_xml_prerun = out_xml_prerun.replace('%repMeteoGauges', "0")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%UZo_prerun%run_rand_id', "0")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%UZf_prerun%run_rand_id', "0")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%UZi_prerun%run_rand_id', "0")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%LZinit_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th1o_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th2o_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th3o_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th1f_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th2f_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th3f_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th1i_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th2i_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th3i_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%run_rand_id', run_id)
        out_xml_prerun = out_xml_prerun.replace('%initialize', '_prerun')                
        # use bogus values at the first time step
        
        with open(self.outfix+'-PreRun'+run_id+'.xml', "w") as f:
            f.write(out_xml_prerun)

        out_xml_run = out_xml
        out_xml_run = out_xml_run.replace('%InitLisflood',"0")
        out_xml_run = out_xml_run.replace('%EndMaps', "0")
              
        if (write_states=='yes'):
            out_xml_run = out_xml_run.replace('%repStateGauges', "1")
            out_xml_run = out_xml_run.replace('%repRateGauges', "1")
            out_xml_run = out_xml_run.replace('%repMeteoGauges', "1")
        else:     
            out_xml_run = out_xml_run.replace('%repStateGauges', "0")
            out_xml_run = out_xml_run.replace('%repRateGauges', "0")
            out_xml_run = out_xml_run.replace('%repMeteoGauges', "0")              
            
        #out_xml_run = out_xml_run.replace('%$(PathOut)/%UZo_prerun', "$(PathOut)/uzoend_prerun")
        #out_xml_run = out_xml_run.replace('%$(PathOut)/%UZf_prerun', "$(PathOut)/uzfend_prerun")
        #out_xml_run = out_xml_run.replace('%$(PathOut)/%UZi_prerun', "$(PathOut)/uziend_prerun")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%UZo_prerun%run_rand_id', "0")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%UZf_prerun%run_rand_id', "0")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%UZi_prerun%run_rand_id', "0")   
        out_xml_run = out_xml_run.replace('%$(PathOut)/%LZinit_prerun%run_rand_id',"-9999")     
        #out_xml_run = out_xml_run.replace('%$(PathOut)/%LZinit_prerun',"$(PathOut)/lzend_prerun")
        #out_xml_run = out_xml_run.replace('%$(PathOut)/%th1o_prerun',"$(PathOut)/th1oend_prerun")
        #out_xml_run = out_xml_run.replace('%$(PathOut)/%th2o_prerun',"$(PathOut)/th2oend_prerun")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th1o_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th2o_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th3o_prerun',"$(PathOut)/th3oend_prerun")
        #out_xml_run = out_xml_run.replace('%$(PathOut)/%th1f_prerun',"$(PathOut)/th1fend_prerun")
        #out_xml_run = out_xml_run.replace('%$(PathOut)/%th2f_prerun',"$(PathOut)/th2fend_prerun")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th1f_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th2f_prerun%run_rand_id',"-9999")        
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th3f_prerun',"$(PathOut)/th3fend_prerun")
        #out_xml_run = out_xml_run.replace('%$(PathOut)/%th1i_prerun',"$(PathOut)/th1iend_prerun")
        #out_xml_run = out_xml_run.replace('%$(PathOut)/%th2i_prerun',"$(PathOut)/th2iend_prerun")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th1i_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th2i_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th3i_prerun',"$(PathOut)/th3iend_prerun")
        out_xml_run = out_xml_run.replace('%run_rand_id', run_id)
        out_xml_run = out_xml_run.replace('%initialize', '_run')
        
        # read the endmaps of the prerun to initialize the soil layers and the groundwater zone
        
        with open(self.outfix+'-Run'+run_id+'.xml', "w") as f:
            f.write(out_xml_run)
            
            
    def write_init(self, run_id, prerun_start, prerun_end, run_start, run_end, param_ranges, parameters):

        prerun_file = self.settings_path('PreRun', run_id)
        run_file = self.settings_path('Run', run_id)
 
        out_xml = copy.deepcopy(self.template_xml)
        
 
        for ii in range(len(param_ranges)):
            ## DD Special Rule for the SAVA --> SAVA belongs to EFAS, these lines must be commented when running the GloFAS calibration
            #if self.obsid == '851' and (param_ranges.index[ii] == "adjust_Normal_Flood" or param_ranges.index[ii] == "ReservoirRnormqMult"):
            #    out_xml = out_xml.replace('%adjust_Normal_Flood',"0.8")
            #    out_xml = out_xml.replace('%ReservoirRnormqMult',"1.0")
            out_xml = out_xml.replace("%"+param_ranges.index[ii],str(parameters[ii]))
 
        out_xml_prerun = out_xml
        out_xml_prerun = out_xml_prerun.replace('%InitLisflood', "1")
        out_xml_prerun = out_xml_prerun.replace('%CalStart', prerun_start)
        out_xml_prerun = out_xml_prerun.replace('%CalEnd', prerun_end)
        out_xml_prerun = out_xml_prerun.replace('%EndMaps', "1")
        # do not write tss files of the states during the calibration
        out_xml_prerun = out_xml_prerun.replace('%repStateGauges', "0")
        out_xml_prerun = out_xml_prerun.replace('%repRateGauges', "0")
        out_xml_prerun = out_xml_prerun.replace('%repMeteoGauges', "0")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%UZo_prerun%run_rand_id', "0")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%UZf_prerun%run_rand_id', "0")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%UZi_prerun%run_rand_id', "0")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%LZinit_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th1o_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th2o_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th3o_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th1f_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th2f_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th3f_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th1i_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th2i_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%$(PathOut)/%th3i_prerun%run_rand_id',"-9999")
        out_xml_prerun = out_xml_prerun.replace('%run_rand_id', run_id)
        out_xml_prerun = out_xml_prerun.replace('%initialize', '_prerun')      
        
        with open(prerun_file, "w") as f:
            f.write(out_xml_prerun)
 
        out_xml_run = out_xml
        out_xml_run = out_xml_run.replace('%InitLisflood', "0")
        out_xml_run = out_xml_run.replace('%CalStart', run_start)
        out_xml_run = out_xml_run.replace('%CalEnd', run_end)
        out_xml_run = out_xml_run.replace('%EndMaps', "0")
        # do not write tss files of the states during the calibration
        out_xml_run = out_xml_run.replace('%repStateGauges', "0")
        out_xml_run = out_xml_run.replace('%repRateGauges', "0")
        out_xml_run = out_xml_run.replace('%repMeteoGauges', "0")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%UZo_prerun%run_rand_id', "0")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%UZf_prerun%run_rand_id', "0")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%UZi_prerun%run_rand_id', "0")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%LZinit_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th1o_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th2o_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th3o_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th1f_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th2f_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th3f_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th1i_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th2i_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%$(PathOut)/%th3i_prerun%run_rand_id',"-9999")
        out_xml_run = out_xml_run.replace('%run_rand_id', run_id)
        out_xml_run = out_xml_run.replace('%initialize', '_run')     
        with open(run_file, "w") as f:
            f.write(out_xml_run)
 
        return prerun_file, run_file            
            