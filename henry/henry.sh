#!/bin/bash

# Henry (Cleanup script)
#
# Removes temporary files (and optionally generated reports - in the future)
echo "Henry 0.0.1"

# Remove files generated during runs
echo "Removing run directory"
rm -rf run/

echo "Cleanup successful"
