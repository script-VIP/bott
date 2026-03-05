#!/bin/bash
VARS_FILE="/root/bott/Botresseler/.vars.json"
DB_FOLDER="/root/bott/Botresseler"
BACKUP_DIR="/root/bott/Botresseler/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

BOT_TOKEN=$(jq -r '.BOT_TOKEN' $VARS_FILE)
BACKUP_CHAT_ID=$(jq -r '.BACKUP_CHAT_ID' $VARS_FILE)

if [ -z "$BOT_TOKEN" ] || [ -z "$BACKUP_CHAT_ID" ]; then
    echo "❌ BOT_TOKEN atau BACKUP_CHAT_ID kosong"
    exit 1
fi

DB_FILES=("botresseler.db" "trial.db" "ressel.db")

for DB_FILE in "${DB_FILES[@]}"; do
    if [ -f "$DB_FOLDER/$DB_FILE" ]; then
        cp "$DB_FOLDER/$DB_FILE" "$BACKUP_DIR/${DB_FILE%.*}_$DATE.db"
        curl -s -F chat_id="$BACKUP_CHAT_ID" \
             -F document=@"$DB_FOLDER/$DB_FILE" \
             -F caption="📦 Backup $DB_FILE - $DATE" \
             "https://api.telegram.org/bot$BOT_TOKEN/sendDocument" >/dev/null
        echo "✅ $DB_FILE terkirim"
    fi
done

find $BACKUP_DIR -type f -mtime +7 -delete
echo "✅ Backup selesai $DATE"
