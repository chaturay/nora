# Author: Chatura Yapa 
# Last Updated : 04/06/2020
# This script will delete all files in the folder and subfolders specified under '$Path' older than '$Daysback'

$Path = "C:\temp"
$Daysback = "-30"
 
$CurrentDate = Get-Date
$DatetoDelete = $CurrentDate.AddDays($Daysback)
Get-ChildItem $Path -Recurse ( | Where-Object { $_.LastWriteTime -lt $DatetoDelete } | Remove-Item