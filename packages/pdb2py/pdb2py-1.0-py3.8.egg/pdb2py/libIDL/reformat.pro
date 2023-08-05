;=============================================;
;-reformat arrays in BASIS savefiles
; MVU, 30-jun-2005
;---------------------------------------------

function reformat2, arr2d
;
;

 n1=n_elements(arr2d(*,0))
 n2=n_elements(arr2d(0,*))
 arr1d=fltarr(n1*n2)

     for i=0,n1-1 do begin
      for j=0,n2-1 do begin
        ;
        arr1d[j+i*n2]=arr2d[i,j]
        ;
      endfor
     endfor

;
;
return, REFORM(arr1d,n1,n2)
end


function reformat3, arr3d
;
;

 n1=n_elements(arr3d(*,0,0))
 n2=n_elements(arr3d(0,*,0))
 n3=n_elements(arr3d(0,0,*))

 arr1d=fltarr(n1*n2*n3)

     for i=0,n1-1 do begin
      for j=0,n2-1 do begin
       for k=0,n3-1 do begin
        ;
;       # arr1d[k + j*n3 + i*n3*n2]=arr3d[i,j,k]
  arr1d[k + j*n3 + i*n2*n3]=arr3d[i,j,k]
        ;
       endfor
      endfor
     endfor

;
;
return, REFORM(arr1d,n1,n2,n3)
end


function Reformat_array, arr
;
 sz=SIZE(arr)
  if sz(0) le 1 then return, arr
  if sz(0) eq 2 then return, Reformat2(arr)
  if sz(0) eq 3 then return, Reformat3(arr)
;
end


function reformat_struc, d
;
;-reformat all fields in a structure
;-----------------------------------

 dnew=d
 dnames=TAG_NAMES(d)
 nn=n_elements(dnames)
  
  for i=0,nn-1 do begin
   dnew.(i)=Reformat_array(d.(i))
  endfor

;
return, dnew
end
;=============================================;
