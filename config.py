# Database name
databaseFile = "DE_flashcards.db"
##import os
##databaseFile = os.path.join(os.path.expanduser('~'), databaseFile)
# Number of backups. -1 will disbale this limitation (unlimited backups)
maxDBbackups = 5
# If the backup should be compress
backup_compress = True
# Address where the app listens. Note  listening 127.0.0.1 is diffrent than listening on the real NIC ip.
serverAddres = "127.0.0.1"
# Port of the web interface
serverPort = 8082

#Current version
ver = 3.7