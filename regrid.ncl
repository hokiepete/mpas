;======================================================================
; ESMF_regrid_10.ncl
;
; Concepts illustrated:
;   - Interpolating from one grid to another using ESMF_regrid
;   - Interpolating data from an MPAS grid to 0.25 degree grid
;======================================================================
; This example is identical to ESMF_all_10.ncl, except it does the
; regridding in one call to "ESMF_regrid".  See ESMF_wgts_10.ncl
; for a faster example of regridding using an existing weights file.
;======================================================================
; This example uses the ESMF application "ESMF_RegridWeightGen" to 
; generate the weights.
;
; For more information about ESMF:
;
;        http://www.earthsystemmodeling.org/
;
; This script uses built-in functions that will be in NCL version
; 6.1.0.
;======================================================================
;
; These files are loaded by default in NCL V6.2.0 and newer
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
;
; This file still has to be loaded manually
load "$NCARG_ROOT/lib/ncarg/nclscripts/esmf/ESMF_regridding.ncl"

begin
i = 0
n = 3
   ;do while(i.le.n)
    ; i=i+1
	; print(i)
   ;end do
;---Retrieve data
    srcFileName = "MPAS.nc"
    sfile = addfile(srcFileName,"r")
	;sp    = sfile->uReconstructZonal(0,:,40)
;    sp    = sfile->surface_pressure(0,:)
;    sp    = sp/1000.   ; Not sure what the pressure units are, there's
                       ; not much metadata info on this file

    lonCell = sfile->lonCell    ; Cell centers
    latCell = sfile->latCell

    r2d     = 180.0d/(atan(1)*4.0d)  ; Radian to Degree
    lonCell := lonCell*r2d
    latCell := latCell*r2d

    Opt                 = True                     ; Regridding optioins

    Opt@SrcFileName     = "MPAS_ESMF.nc"           ; output files
    Opt@DstFileName     = "World_0.25deg_SCRIP.nc"
    Opt@WgtFileName     = "MPAS_2_World.nc"
    Opt@ForceOverwrite  = True

    Opt@SrcGridLat      = latCell                  ; source grid
    Opt@SrcGridLon      = lonCell
    Opt@InputFileName   = srcFileName              ; optional

	
	
    Opt@DstGridType     = "0.25deg"                ; destination grid
    Opt@DstTitle        = "World Grid 0.25 degree resolution"
    Opt@DstLLCorner     = (/-89.75d, -180.00d /)
    Opt@DstURCorner     = (/ 89.75d,  179.75d /) 

    Opt@Debug           = True
    ;;Opt@PrintTimings  = True
	fili = systemfunc("ls diag*.nc")
	;print(fili) ; all file names
	nfili = dimsizes(fili)
	;print(nfili) 
	do nf=0,nfili-1
		dsrcFileName = fili(nf)
		outFileName = "outfile_"+nf+".nc"
		;f = addfile(diri+fili(nf), "r")
		;x = f->pr

		;dsrcFileName = "diag.2010-09-28_12.00.00.nc"
		dfile = addfile(dsrcFileName,"r")
		u    = dfile->uzonal_925hPa
		u_regrid = ESMF_regrid(u,Opt)
		printVarSummary(u_regrid)
		v    = dfile->umeridional_925hPa 
		v_regrid = ESMF_regrid(v,Opt)
		printVarSummary(v_regrid)
		system("/bin/rm -f "+outFileName)   ; remove any pre-existing file
		ncdf = addfile(outFileName ,"c")  ; open output netCDF file

		;===================================================================
		; create global attributes of the file (optional)
		;===================================================================
		fAtt               = True            ; assign file attributes
		fAtt@title         = "NCL Simple Approach to netCDF Creation"
		fAtt@source_file   =  "original-file.nc"
		fAtt@Conventions   = "None"
		fAtt@creation_date = systemfunc ("date")
		fileattdef( ncdf, fAtt )            ; copy file attributes

		;===================================================================
		; make time an UNLIMITED dimension; recommended  for most applications
		;===================================================================
		filedimdef(ncdf,"time",-1,True) 

		;===================================================================
		; output variables directly; NCL will call appropriate functions
		; to write the meta data associated with each variable
		;===================================================================
		;ncdf->T  = T                          ; 4D               
		;ncdf->PS = PS                         ; 3D 

		U = u_regrid							 ; say U(:,:)
		U!0    = "time"
		U!1    = "lat"                      ; assign named dimensions
		U!2    = "lon"


		U@long_name = "Eastward Velocity 925mb"           ; assign attributes 
		U@units     = "m/s"

		ncdf->U_925mb = U                ; name on file different from name in code

		
		V = v_regrid							 ; say U(:,:)
		V!0    = "time"
		V!1    = "lat"                      ; assign named dimensions
		V!2    = "lon"


		V@long_name = "Northward Velocity 925mb"           ; assign attributes 
		V@units     = "m/s"

		ncdf->V_925mb = V                ; name on file different from name in code
		delete([/U,u_regrid,u,V,v_regrid,v,ncdf,dfile,outFileName,dsrcFileName/])
	end do
end
