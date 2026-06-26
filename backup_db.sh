#!/bin/bash

DB_FILE="database.db"
BACKUP_DIR="backups"

#  verificar si existe la base de datos
if [ ! -f "$DB_FILE" ]; then
    echo "ERROR: No existe $DB_FILE"
    exit 1
fi

mkdir -p $BACKUP_DIR

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.db"

cp $DB_FILE $BACKUP_FILE

#  validar que el backup se hizo
if [ $? -eq 0 ]; then
    echo " Backup creado correctamente: $BACKUP_FILE"
else
    echo " Error al crear backup"
fi