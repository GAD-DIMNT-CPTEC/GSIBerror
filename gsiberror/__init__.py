#! /usr/bin/env python3

import numpy as np
import xarray as xr

from .plot_functions import var_name, global_minmax, plot_reg_coeffs, plot_amplitudes, plot_hscales, plot_vscales

class Berror(object):   
    """
    Berror
    ======
        
    Class with methods to read all the records of a GSI compatible background error covariance matrix (.gcv format).    

    """    
    
    def __init__(self, file_name):
        self.file_name = file_name
        #self._my_name = ''
    
    def read_records(self):
        """
        read_records
        ------------
        
        This method reads the first three records of the background error covariance matrix (nlat, nlon and nlev).
        These records are used to calculate the size of the remainder records from the matrix. All attributes read from
        the matrix are provided by this function. The plotting of the records are made through the use of the xarray's 'plot()'
        method; depending on the use, it can be necessary to to load the matplotlib and cartopy modules.
        
        Input parameters
        ----------------
            None.

        Result
        ------
            bfile: object created with the records and attributes from the background error covariance matrix (see the list below)
                   
        Available attributes
        --------------------
            file_name         : string with the name of the file
            nlat              : integer with the number of latitude points 
            nlon              : integer with the number of longitude points 
            nlev              : integer with the number of vertical levels
            lats              : nd-array with the latitude values (-90 to 90)
            lons              : nd-array with the longitude values (0 to 360)
            levs              : nd-array with the vertical levels (1 to nlev)
            amplitudes        : dicionary with the xarrays for the control variables amplitudes
            amplitudes_names  : names of the variables in the amplitudes dictionary
            balprojs          : dictionary with xarrays for the regression coefficients matrices for the temperature, 
                                surface pressure and velocity potential
            hscales           : dictionary with xarrays for the horizontal length scales
            hscales_var_names : names of the variables in the hscales dictionary
            vscales           : dictionary with xarrays for the vertical length scales
            vscales_var_names : names of the variables in the vscales dictionary
                    
        Use
        ---
            from GSIBerror import Berror
        
            bfile = Berror('arquivo_matriz_B.gcv')
        
            bfile.read_records()
            
            bfile.nlat, bfile.nlon, bfile.nlev
            
            bfile.amplitudes_names
            
            bfile.amplitudes['sf']
            
            bfile_amp_sf = bfile.amplitudes['sf']
            
            bfile_amp_sf.plot.contourf()    
        """
    
        # Reads the first three records to define the grid
        dt = np.dtype([ ('grid', '3>i4') ])

        with open(self.file_name, 'rb') as ftmp:
            fobj = np.fromfile(ftmp, dtype=dt, count=3, offset=4)  
        
        # Calculate the coordinates for lats, lons and levs dimensions
        nlev = fobj[0]['grid'][0]
        nlat = fobj[0]['grid'][1]
        nlon = fobj[0]['grid'][2]
       
        self.nlat = nlat
        self.nlon = nlon
        self.nlev = nlev
    
        self.lats = np.linspace(-90,90, self.nlat)
        self.lons = np.linspace(0,360, self.nlon)
        self.levs = np.arange(1, self.nlev+1)
        
        # Define the records sizes from within the file ('>f4' indicates 32 bits floats, big endian)
        tnlat = str(self.nlat) + '>f4'
        s2d = str(self.nlat*self.nlev) + '>f4'
        sst2d = str(self.nlat*self.nlon) + '>f4'
        s3d = str(self.nlat*self.nlev*self.nlev) + '>f4'

        # Define a structure for the records within the file ('padX' = 4 bytes; '>i4' indicates 32 bits integers, big endian)
        # Maybe this isn't the best way to read the records but it is explicity, at least
        dt =          [ ('grid', '3>i4'), 
                   
                        ('pad1', '>i4'), ('agvin',s3d), 
                        ('pad2', '>i4'), ('bgvin', s2d),
                        ('pad3', '>i4'), ('wgvin', s2d), 
                       
                        ('pad4', '>i4'), ('sf', '|a5'), ('sig_sf', '>i4'), ('pad5', '>i4'), 
                        ('pad6', '>i4'), ('corzin_sf', s2d), ('pad7', '>i4'), 
                        ('pad8', '>i4'), ('hscalesin_sf', s2d), ('pad9', '>i4'), 
                        ('pad10', '>i4'), ('vscalesin_sf', s2d), ('pad11', '>i4'), 
                   
                        ('pad12', '>i4'), ('vp', '|a5'), ('sig_vp', '>i4'), ('pad13', '>i4'),
                        ('pad14', '>i4'), ('corzin_vp', s2d), ('pad15', '>i4'), 
                        ('pad16', '>i4'), ('hscalesin_vp', s2d), ('pad17', '>i4'), 
                        ('pad18', '>i4'), ('vscalesin_vp', s2d), ('pad19', '>i4'), 
                   
                        ('pad20', '>i4'), ('t', '|a5'), ('sig_t', '>i4'), ('pad21', '>i4'),
                        ('pad22', '>i4'), ('corzin_t', s2d), ('pad23', '>i4'), 
                        ('pad24', '>i4'), ('hscalesin_t', s2d), ('pad25', '>i4'), 
                        ('pad26', '>i4'), ('vscalesin_t', s2d), ('pad27', '>i4'), 
                   
                        ('pad28', '>i4'), ('q', '|a5'), ('sig_q', '>i4'), ('pad29', '>i4'),
                        ('pad30', '>i4'), ('corzin_q', s2d), ('corqin_q', s2d), ('pad31', '>i4'), 
                        ('pad32', '>i4'), ('hscalesin_q', s2d), ('pad33', '>i4'), 
                        ('pad34', '>i4'), ('vscalesin_q', s2d), ('pad35', '>i4'), 
                   
                        ('pad36', '>i4'), ('oz', '|a5'), ('sig_oz', '>i4'), ('pad37', '>i4'),
                        ('pad38', '>i4'), ('corzin_oz', s2d), ('pad39', '>i4'), 
                        ('pad40', '>i4'), ('hscalesin_oz', s2d), ('pad41', '>i4'), 
                        ('pad42', '>i4'), ('vscalesin_oz', s2d), ('pad43', '>i4'), 
                                      
                        ('pad44', '>i4'), ('cw', '|a5'), ('sig_cw', '>i4'), ('pad45', '>i4'),
                        ('pad46', '>i4'), ('corzin_cw', s2d), ('pad47', '>i4'), 
                        ('pad48', '>i4'), ('hscalesin_cw', s2d), ('pad49', '>i4'), 
                        ('pad50', '>i4'), ('vscalesin_cw', s2d), ('pad51', '>i4'), 
                   
                        ('pad52', '>i4'), ('ps', '|a5'), ('sig_ps', '>i4'), ('pad53', '>i4'), 
                        ('pad54', '>i4'), ('corpin_ps', tnlat), ('pad55', '>i4'), 
                        ('pad56', '>i4'), ('hscalespin_ps', tnlat), ('pad57', '>i4'), 
                   
                        ('pad58', '>i4'), ('sst', '|a5'), ('sig_sst', '>i4'), ('pad59', '>i4'),
                        ('pad60', '>i4'), ('corsstin_sst', sst2d), ('pad61', '>i4'), 
                        ('pad62', '>i4'), ('hsstin_ps', sst2d), ('pad63', '>i4') ]   
    
        dt_obj = np.dtype(dt)#, align=True) # align=True should be automatic (?) 
                                            # accounts fo the 4 bytes padding (before and after the records)
    
        # Opens the file again to read all the records
        with open(self.file_name, 'rb') as ftmp:
            fobj = np.fromfile(ftmp, dtype=dt_obj, count=-1, offset=4) # count=-1 reads the whole file
    
        #
        # Records reading - Regression coefficients (balance projection matrices)  
        #
        
        balprojs = {} 
    
        self.balprojs = balprojs
    
        agvin = np.reshape(fobj[0]['agvin'], (self.nlat, self.nlev, self.nlev), order='F')
        da_agvin = xr.DataArray(agvin, dims=['latitude', 'level', 'level_2'], coords={'latitude':self.lats, 'level':self.levs, 'level_2':self.levs})
        da_agvin = da_agvin.transpose('level', 'latitude', 'level_2')
        da_agvin = da_agvin.rename('agvin')

        balprojs['agvin'] = da_agvin
    
        bgvin = np.reshape(fobj[0]['bgvin'], (self.nlat, self.nlev), order='F')
        da_bgvin = xr.DataArray(bgvin, dims=['latitude', 'level'], coords={'latitude':self.lats, 'level':self.levs})
        da_bgvin = da_bgvin.transpose('level', 'latitude')
        da_bgvin = da_bgvin.rename('bgvin')

        balprojs['bgvin'] = da_bgvin
    
        wgvin = np.reshape(fobj[0]['wgvin'], (self.nlat, self.nlev), order='F')
        da_wgvin = xr.DataArray(wgvin, dims=['latitude', 'level'], coords={'latitude':self.lats, 'level':self.levs})
        da_wgvin = da_wgvin.transpose('level', 'latitude')
        da_wgvin = da_wgvin.rename('wgvin')
    
        balprojs['wgvin'] = da_wgvin      
        
        #
        # Records reading - Amplitudes (standard deviations)
        #
        
        amplitudes = {}
        
        self.amplitudes = amplitudes
        
        amplitudes_names = {
            'sf':  'corzin_sf', 
            'vp':  'corzin_vp', 
            't':   'corzin_t', 
            'q':   'corzin_q', 
            'qin': 'corqin_q',
            'oz':  'corzin_oz', 
            'ps':  'corpin_ps', 
            'cw':  'corzin_cw', 
            'sst': 'corsstin_sst',
        }
        
        self.amplitudes_names = amplitudes_names
        
        # Loop over the variables to create a dictionary with xarrays for the amplitudes
        for var in amplitudes_names.items():
            if var[0] == 'ps':
                corzin_var = np.reshape(fobj[0][var[1]], (self.nlat), order='F')
                da_corzin_var = xr.DataArray(corzin_var, dims=['latitude'], coords={'latitude':self.lats})
            elif var[0] == 'sst':
                corzin_var = np.reshape(fobj[0][var[1]], (self.nlat, self.nlon), order='F')
                da_corzin_var = xr.DataArray(corzin_var, dims=['latitude', 'longitude'], coords={'latitude':self.lats, 'longitude':self.lons})
            else:
                corzin_var = np.reshape(fobj[0][var[1]], (self.nlat, self.nlev), order='F')
                da_corzin_var = xr.DataArray(corzin_var, dims=['latitude', 'level'], coords={'latitude':self.lats, 'level':self.levs})
                da_corzin_var = da_corzin_var.transpose('level', 'latitude')
            
            da_corzin_var = da_corzin_var.rename(var[1])
        
            amplitudes[var[0]] = da_corzin_var
        
        #
        # Records reading - Horizontal length scales (in meters) -> the in plot_functions.py script, the horizontal length scales
        #                                                           are divides by 1000
        #
        
        hscales = {}
        
        self.hscales = hscales
        
        hscales_var_names = {
            'sf':  'hscalesin_sf', 
            'vp':  'hscalesin_vp', 
            't':   'hscalesin_t', 
            'q':   'hscalesin_q', 
            'oz':  'hscalesin_oz', 
            'ps':  'hscalespin_ps', 
            'cw':  'hscalesin_cw', 
            'sst': 'hsstin_ps',
        }        
        
        self.hscales_var_names = hscales_var_names
        
        # Loop over the variables to create a dictionary with xarrays for the horizontal length scales
        for var in hscales_var_names.items():
            if var[0] == 'ps':
                hscalesin_var = np.reshape(fobj[0][var[1]], (self.nlat), order='F')
                da_hscalesin_var = xr.DataArray(hscalesin_var, dims=['latitude'], coords={'latitude':self.lats})
            elif var[0] == 'sst':
                hscalesin_var = np.reshape(fobj[0][var[1]], (self.nlat, self.nlon), order='F')
                da_hscalesin_var = xr.DataArray(hscalesin_var, dims=['latitude', 'longitude'], coords={'latitude':self.lats, 'longitude':self.lons})
            else:
                hscalesin_var = np.reshape(fobj[0][var[1]], (self.nlat, self.nlev), order='F')
                da_hscalesin_var = xr.DataArray(hscalesin_var, dims=['latitude', 'level'], coords={'latitude':self.lats, 'level':self.levs})
                da_hscalesin_var = da_hscalesin_var.transpose('level', 'latitude')
            
            da_hscalesin_var = da_hscalesin_var.rename(var[1])
        
            hscales[var[0]] = da_hscalesin_var           
        
        #
        # Records reading - Vertical length scales
        #
        
        vscales = {}
        
        self.vscales = vscales

        vscales_var_names = {
            'sf':  'vscalesin_sf', 
            'vp':  'vscalesin_vp', 
            't':   'vscalesin_t', 
            'q':   'vscalesin_q', 
            'oz':  'vscalesin_oz',  
            'cw':  'vscalesin_cw', 
        }         
        
        self.vscales_var_names = vscales_var_names
        
        # Loop over the variables to create a dictionary with xarrays for the vertical length scales
        for var in vscales_var_names.items():
            if var[0] == 'ps':
                vscalesin_var = np.reshape(fobj[0][var[1]], (self.nlat), order='F')
                da_vscalesin_var = xr.DataArray(vscalesin_var, dims=['latitude'], coords={'latitude':self.lats})
            elif var[0] == 'sst':
                vscalesin_var = np.reshape(fobj[0][var[1]], (self.nlat, self.nlon), order='F')
                da_vscalesin_var = xr.DataArray(vscalesin_var, dims=['latitude', 'longitude'], coords={'latitude':self.lats, 'longitude':self.lons})
            else:
                vscalesin_var = np.reshape(fobj[0][var[1]], (self.nlat, self.nlev), order='F')
                da_vscalesin_var = xr.DataArray(vscalesin_var, dims=['latitude', 'level'], coords={'latitude':self.lats, 'level':self.levs})
                da_vscalesin_var = da_vscalesin_var.transpose('level', 'latitude')
            
            da_vscalesin_var = da_vscalesin_var.rename(var[1])
        
            vscales[var[0]] = da_vscalesin_var

#    @property
    def my_name(self, name):
        #return self._my_name   
        self.my_name = str(name) 
#        return self.my_name 
            
#    @my_name.setter
#    def my_name(self, name):
#        self._my_name = str(name)    
        
#    @property
    def get_name(self):            
        return self.my_name        
