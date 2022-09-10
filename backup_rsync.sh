#!/bin/bash 
out_path="../backup_etn1040/"
if [ ! -d "$out_path" ]; then
  # Tomar acción si el directorio no existe
    echo "Creando directorio ${out_path}..."
    mkdir $out_path
else
    echo ""
fi
source_path="../etn1040_1/"
foldername=$(basename $source_path)
backup_date=$(date +"%Y-%b-%d_%H:%M:%S")
output_nodate="${out_path}${foldername}-backup"
output_date="${output_nodate}_${backup_date}"

# rsync
rsync -av --exclude 'media/' --delete $source_path $output_nodate
echo "********** Sincronización hecha! *************"

# comprimir archivo
compress_file="${output_date}.tgz"
tar cfz $compress_file $output_nodate 
echo "********** Compresión hecha! *************"

# mantener la cantidad de archivos .tgz a un numero maximo
maxFiles=7
tarFiles=$(ls $out_path/$foldername*.tgz | wc -l)
if [[ $tarFiles -gt $maxFiles ]]
then
    # eliminar ultimo archivo 
    deleteFile=$(ls -t $out_path*.tgz | tail -1)
    rm $deleteFile
    echo "Se eliminó el último archivo"
    
else
    echo "La cantidad máxima son: <${maxFiles}> archivos"
fi
# encontrar el ultimo archivo ingresado


