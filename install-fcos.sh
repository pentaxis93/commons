#!/bin/bash
# Install Fedora CoreOS on OVHcloud VPS from rescue mode.
#
# The rescue environment has very limited disk space (~2.9G), so we
# stream the FCOS image directly to disk rather than pulling container
# images. The Ignition config is injected manually into the boot
# partition after writing.
#
# Prerequisites:
#   1. Boot into rescue mode from OVHcloud console
#   2. SSH in with the temp credentials they email you
#   3. Copy this script and the host Ignition config to the rescue system
#   4. Run: bash install-fcos.sh <ignition-config>
#
# Based on: https://tim.siosm.fr/blog/2025/09/14/fedora-coreos-ovhcloud-vps/

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install-fcos.sh <ignition-config>

Install Fedora CoreOS on OVHcloud VPS from rescue mode.

Arguments:
  <ignition-config>  Path to the Ignition config file to inject.
EOF
}

error() {
  echo "ERROR: $*" >&2
  exit 1
}

if [ "$#" -eq 1 ] && { [ "$1" = "-h" ] || [ "$1" = "--help" ]; }; then
  usage
  exit 0
fi
if [ "$#" -eq 0 ]; then
  usage >&2
  error "ignition config path is required"
fi
if [ "$#" -ne 1 ]; then
  usage >&2
  error "expected exactly one ignition config path"
fi

IGNITION_CONFIG="$1"

required_tool_execution_status() {
  local status="$1"

  [ "$status" -eq 126 ] || [ "$status" -eq 127 ]
}

require_tool() {
  local tool="$1"
  local tool_path

  if ! tool_path="$(command -v "$tool")"; then
    error "required tool $tool was not found in PATH"
  fi
  if [ ! -x "$tool_path" ]; then
    error "required tool $tool is not executable: $tool_path"
  fi
}

capture_or_empty() {
  local tool="$1"
  shift

  local output
  local status
  if output="$("$tool" "$@")"; then
    printf '%s\n' "$output"
    return 0
  else
    status=$?
  fi

  if required_tool_execution_status "$status"; then
    echo "ERROR: required tool $tool could not execute" >&2
    return "$status"
  fi
  return 1
}

rescue_disk_parent_name() {
  lsblk -no PKNAME "$1" | awk 'NF { print $1; exit }'
}

rescue_source_type() {
  lsblk -no TYPE "$1" | awk 'NF { print $1; exit }'
}

persistent_disk_names() {
  lsblk -dnrpo NAME,TYPE |
    awk -v rescue="$1" '$2 == "disk" && $1 != rescue { print $1 }'
}

fcos_boot_partition() {
  partition_rows "$1" |
    awk '$2 == "3" { print $1; exit }'
}

kernel_partition_numbers() {
  partition_rows "$1" |
    awk '{ print $2 }'
}

partition_rows() {
  local disk="$1"

  lsblk -nrpo NAME,TYPE "$disk" |
    awk -v disk="$disk" '
      $2 != "part" { next }
      index($1, disk) != 1 { next }
      {
        suffix = substr($1, length(disk) + 1)
        if (suffix ~ /^[0-9]+$/) {
          print $1, suffix
          next
        }
        if (suffix ~ /^p[0-9]+$/) {
          print $1, substr(suffix, 2)
          next
        }
        print "could not parse partition number from " $1 > "/dev/stderr"
        exit 1
      }
    '
}

refresh_partition_table() {
  local disk="$1"
  local existing_partitions

  if ! existing_partitions="$(kernel_partition_numbers "$disk")"; then
    error "could not inspect kernel partition view for $disk"
  fi
  if [ -n "$existing_partitions" ]; then
    partx --delete "$disk"
  fi
  partx --add "$disk"
}

if [ ! -f "$IGNITION_CONFIG" ]; then
  error "$IGNITION_CONFIG is required in the current directory before writing the target disk."
fi

for tool in awk basename cp curl dd findmnt ls lsblk mkdir mount partx python3 sleep umount xzcat; do
  require_tool "$tool"
done

# Step 1: Identify the target disk
echo "Available disks:"
lsblk
echo

ROOT_SOURCE_STATUS=0
if ROOT_SOURCE="$(capture_or_empty findmnt -n -o SOURCE /)"; then
  :
else
  ROOT_SOURCE_STATUS=$?
  ROOT_SOURCE=""
fi
if required_tool_execution_status "$ROOT_SOURCE_STATUS"; then
  exit 1
fi
if [ -z "$ROOT_SOURCE" ]; then
  error "could not identify the rescue disk mounted at /"
fi

if ! RESCUE_DISK_NAME="$(rescue_disk_parent_name "$ROOT_SOURCE")"; then
  RESCUE_DISK_NAME=""
fi
if [ -z "$RESCUE_DISK_NAME" ]; then
  if ! ROOT_SOURCE_TYPE="$(rescue_source_type "$ROOT_SOURCE")"; then
    ROOT_SOURCE_TYPE=""
  fi
  if [ "$ROOT_SOURCE_TYPE" = "disk" ]; then
    RESCUE_DISK_NAME="$(basename "$ROOT_SOURCE")"
  fi
fi
if [ -z "$RESCUE_DISK_NAME" ]; then
  error "could not identify the rescue disk mounted at / from $ROOT_SOURCE"
fi

case "$RESCUE_DISK_NAME" in
  /dev/*) RESCUE_DISK="$RESCUE_DISK_NAME" ;;
  *) RESCUE_DISK="/dev/$RESCUE_DISK_NAME" ;;
esac

if ! persistent_disks_output="$(persistent_disk_names "$RESCUE_DISK")"; then
  error "could not list persistent target disks with lsblk"
fi
PERSISTENT_DISKS=()
if [ -n "$persistent_disks_output" ]; then
  mapfile -t PERSISTENT_DISKS <<< "$persistent_disks_output"
fi

case "${#PERSISTENT_DISKS[@]}" in
  0)
    error "could not identify a persistent target disk distinct from rescue disk $RESCUE_DISK"
    ;;
  1)
    TARGET_DISK="${PERSISTENT_DISKS[0]}"
    ;;
  *)
    error "ambiguous persistent target disks: ${PERSISTENT_DISKS[*]}"
    ;;
esac

echo "Detected rescue disk: $RESCUE_DISK (mounted at / via $ROOT_SOURCE)"
echo "Target persistent disk: $TARGET_DISK"
echo
echo "This will destroy all data on $TARGET_DISK."
echo "Press Enter to continue or Ctrl-C to abort."
read -r

# Step 2: Stream the FCOS metal image directly to disk
# No temp storage needed — curl decompresses through xzcat into dd.
STREAM_URL="https://builds.coreos.fedoraproject.org/streams/stable.json"
echo "Fetching current stable FCOS version..."
IMAGE_URL=$(curl -sL "$STREAM_URL" | python3 -c "
import json,sys
data = json.load(sys.stdin)
print(data['architectures']['x86_64']['artifacts']['metal']['formats']['raw.xz']['disk']['location'])
")
echo "Image: $IMAGE_URL"
echo "Writing to $TARGET_DISK..."
curl -fsSL "$IMAGE_URL" | xzcat | dd of="$TARGET_DISK" bs=4M status=progress

# Step 3: Inject Ignition config into the boot partition
# FCOS partition layout after writing:
#   partition 1 — BIOS boot (1M)
#   partition 2 — EFI (127M)
#   partition 3 — /boot (384M) ← Ignition goes here
#   partition 4 — root
#
# This assumes the FCOS metal image keeps /boot at partition 3. If a future
# FCOS layout changes that, the mount below is the expected failure point.
echo
echo "Injecting Ignition config..."
refresh_partition_table "$TARGET_DISK"
sleep 1
if ! BOOT_PARTITION="$(fcos_boot_partition "$TARGET_DISK")"; then
  BOOT_PARTITION=""
fi
if [ -z "$BOOT_PARTITION" ]; then
  error "could not identify FCOS /boot partition 3 on $TARGET_DISK"
fi
mount "$BOOT_PARTITION" /mnt
mkdir -p /mnt/ignition
cp "$IGNITION_CONFIG" /mnt/ignition/config.ign
echo "Ignition config placed at /mnt/ignition/config.ign"
ls -la /mnt/ignition/
umount /mnt

echo
echo "Done. Reboot out of rescue mode from the OVHcloud console:"
echo "  Boot -> Reboot my VPS"
echo
echo "Then SSH in: ssh core@<your-vps-ip>"
